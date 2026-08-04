<?php
/**
 * E-Suero — Stripe Embedded Checkout session endpoint.
 *
 * SETUP (do this once, directly on the server — never via chat/AI):
 * 1. Log in to https://dashboard.stripe.com/apikeys
 * 2. Copy your SECRET key (starts with sk_live_... or sk_test_...)
 * 3. Replace the placeholder below with that key.
 * 4. Never commit the real secret key to git or share it anywhere else.
 */
define('STRIPE_SECRET_KEY', 'sk_live_REPLACE_WITH_YOUR_STRIPE_SECRET_KEY');

define('STRIPE_API_BASE', 'https://api.stripe.com/v1');
define('SITE_URL', 'https://e-suero.ch');

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

if (strpos(STRIPE_SECRET_KEY, 'REPLACE_WITH') !== false) {
    http_response_code(500);
    echo json_encode(['error' => 'Stripe ist noch nicht konfiguriert. Bitte kontaktieren Sie uns direkt.']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid request body']);
    exit;
}

$name = isset($input['name']) ? trim((string) $input['name']) : '';
$priceRappen = isset($input['price']) ? (int) $input['price'] : 0;
$image = isset($input['image']) ? trim((string) $input['image']) : '';
$slug = isset($input['slug']) ? preg_replace('/[^a-z0-9\-]/', '', strtolower((string) $input['slug'])) : '';

if ($name === '' || $priceRappen <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing or invalid product name/price']);
    exit;
}

// Basic sanity cap to avoid abuse via a tampered client request (order-on-demand catalog, no live cart total exceeds this).
if ($priceRappen > 5000000) {
    http_response_code(400);
    echo json_encode(['error' => 'Price out of allowed range']);
    exit;
}

$productData = ['name' => $name];
if ($image !== '' && strpos($image, SITE_URL) === 0) {
    $productData['images'] = [$image];
}

$params = [
    'mode' => 'payment',
    'ui_mode' => 'embedded',
    // No payment_method_types set on purpose: Stripe automatically offers every
    // method enabled in the Dashboard (card today; TWINT, Apple Pay, Google Pay,
    // Klarna, PayPal tomorrow) with zero code changes here.
    'line_items' => [[
        'quantity' => 1,
        'price_data' => [
            'currency' => 'chf',
            'unit_amount' => $priceRappen,
            'product_data' => $productData,
        ],
    ]],
    'return_url' => SITE_URL . '/stripe/success.html?session_id={CHECKOUT_SESSION_ID}' . ($slug ? '&product=' . $slug : ''),
];

$response = stripeRequest('/checkout/sessions', $params);

if (isset($response['error'])) {
    http_response_code(502);
    echo json_encode(['error' => 'Zahlung konnte nicht gestartet werden. Bitte versuchen Sie es erneut.']);
    exit;
}

echo json_encode(['clientSecret' => $response['client_secret']]);
exit;

/**
 * Minimal dependency-free Stripe REST call (no Composer/SDK required on shared hosting).
 */
function stripeRequest($path, $params) {
    $ch = curl_init(STRIPE_API_BASE . $path);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, httpBuildQueryDeep($params));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . STRIPE_SECRET_KEY,
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);
    $body = curl_exec($ch);
    $err = curl_error($ch);
    curl_close($ch);

    if ($body === false) {
        return ['error' => $err ?: 'cURL request failed'];
    }
    $decoded = json_decode($body, true);
    return is_array($decoded) ? $decoded : ['error' => 'Invalid Stripe response'];
}

/**
 * Stripe's API expects PHP-style bracket-encoded form params for nested arrays,
 * with explicit numeric indices for list items (e.g. line_items[0][price_data][currency]).
 */
function httpBuildQueryDeep($params, $prefix = '') {
    $pairs = [];
    foreach ($params as $key => $value) {
        $formKey = $prefix === '' ? $key : "{$prefix}[{$key}]";
        if (is_array($value)) {
            $pairs[] = httpBuildQueryDeep($value, $formKey);
        } else {
            $pairs[] = rawurlencode($formKey) . '=' . rawurlencode((string) $value);
        }
    }
    return implode('&', $pairs);
}
