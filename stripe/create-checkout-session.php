<?php
/**
 * E-Suero — Stripe Embedded Checkout session endpoint.
 * Configuration (incl. the secret key placeholder) lives in config.php —
 * that is the only file you need to edit.
 */
require __DIR__ . '/config.php';

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

$orderMetadata = [
    'product_slug' => $slug !== '' ? $slug : 'unknown',
    'product_name' => $name,
    'source' => 'e-suero.ch',
];

$params = [
    'mode' => 'payment',
    // Hosted Stripe Checkout (no ui_mode set): the visitor is redirected to
    // Stripe's own polished, mobile-optimized payment page and returns to
    // success.php afterwards. Chosen over an embedded/iframe checkout after
    // that mode's ui_mode value changed server-side (Stripe API update) and
    // proved unreliable to size correctly inside a modal — this is Stripe's
    // most battle-tested integration path.
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
    // Order-on-demand business model: capture who bought what directly on the
    // Checkout Session and the PaymentIntent, so it's visible in the Stripe
    // Dashboard and in stripe/success.php without needing a webhook/database.
    'metadata' => $orderMetadata,
    'payment_intent_data' => [
        'metadata' => $orderMetadata,
        'description' => "E-Suero Bestellung: {$name}",
    ],
    // Collects the customer's email as part of Checkout and attaches a Customer
    // record to the payment, so an order always has contact info to follow up on.
    'customer_creation' => 'always',
    // Also ask for a phone number during Checkout — this business follows up by
    // phone/WhatsApp, so a second contact channel beyond email is valuable even
    // for orders that don't complete.
    'phone_number_collection' => ['enabled' => true],
    'success_url' => SITE_URL . '/stripe/success.php?session_id={CHECKOUT_SESSION_ID}',
    // Sent back to cancel.php (not straight to the homepage) so an abandoned
    // checkout where the visitor already typed their email/phone still gets
    // captured and reported — see cancel.php.
    'cancel_url' => SITE_URL . '/stripe/cancel.php?session_id={CHECKOUT_SESSION_ID}',
];

$response = stripeRequest('/checkout/sessions', $params);

if (isset($response['error'])) {
    logStripeError('create-checkout-session', $response['error'], ['name' => $name, 'price' => $priceRappen, 'slug' => $slug]);
    http_response_code(502);
    echo json_encode(['error' => 'Zahlung konnte nicht gestartet werden. Bitte versuchen Sie es erneut oder kontaktieren Sie uns direkt.']);
    exit;
}

// Real-time purchase-intent signal: fire the moment someone reaches Stripe's
// payment page, whether or not they go on to actually pay. Lets staff follow
// up proactively on serious interest, not just completed orders.
notifyIntent($name, $priceRappen);

echo json_encode(['url' => $response['url']]);
exit;

/**
 * Best-effort admin notification the instant a checkout is started. No
 * customer contact info exists yet at this point (that's collected on
 * Stripe's own page) — this is purely a "someone is looking at buying X"
 * signal, sent via the same real ADMIN_EMAIL mailbox as every other notice.
 */
function notifyIntent($name, $priceRappen) {
    $amount = number_format($priceRappen / 100, 2, '.', "'");
    $subject = "👀 Kaufversuch gestartet: {$name}";
    $body = "Jemand hat gerade \"Jetzt kaufen\" angeklickt auf e-suero.ch\n\n" .
        "Produkt: {$name}\n" .
        "Preis: CHF {$amount}\n" .
        "Zeit: " . date('Y-m-d H:i:s') . "\n\n" .
        "Dies bestätigt nicht, dass die Zahlung abgeschlossen wurde — nur, dass jemand zur Stripe-Zahlungsseite weitergeleitet wurde.\n" .
        "Eine Bestätigung mit Kundendaten folgt separat, sobald die Zahlung abgeschlossen ist (oder falls die Person ihre Kontaktdaten eingegeben, aber abgebrochen hat).";
    $headers = "From: " . ADMIN_EMAIL . "\r\nContent-Type: text/plain; charset=UTF-8";
    @mail(ADMIN_EMAIL, $subject, $body, $headers);
}

/**
 * Best-effort local error log (never exposed to the client). Silently no-ops
 * if the directory isn't writable — logging must never break checkout.
 */
function logStripeError($context, $error, $extra = []) {
    $line = sprintf(
        "[%s] %s: %s | %s\n",
        date('Y-m-d H:i:s'),
        $context,
        is_string($error) ? $error : json_encode($error),
        json_encode($extra)
    );
    @file_put_contents(__DIR__ . '/error.log', $line, FILE_APPEND | LOCK_EX);
}

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
            // PHP casts true/false to "1"/"" — Stripe's API requires the literal
            // strings "true"/"false" for boolean params (e.g. phone_number_collection[enabled]).
            if (is_bool($value)) {
                $value = $value ? 'true' : 'false';
            }
            $pairs[] = rawurlencode($formKey) . '=' . rawurlencode((string) $value);
        }
    }
    return implode('&', $pairs);
}
