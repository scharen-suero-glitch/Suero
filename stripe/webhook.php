<?php
/**
 * E-Suero — Stripe webhook endpoint.
 *
 * Stripe calls this URL directly from its own servers whenever something
 * happens to a Checkout Session — this is what catches an abandoned checkout
 * even when the visitor just closes the tab or hits the browser's own back
 * button (cancel.php only catches it if they use Stripe's own "← Zurück"
 * link on the payment page; this endpoint catches everything else too).
 *
 * SETUP: see the "WEBHOOK SETUP" comment block in config.php. Until
 * STRIPE_WEBHOOK_SECRET is filled in there, this endpoint safely no-ops
 * (returns 200 without processing anything) so Stripe doesn't see failures.
 */
require __DIR__ . '/config.php';

http_response_code(200); // Acknowledge fast; Stripe retries on non-2xx.
header('Content-Type: application/json; charset=utf-8');

$configured = strpos(STRIPE_SECRET_KEY, 'REPLACE_WITH') === false;
$webhookConfigured = strpos(STRIPE_WEBHOOK_SECRET, 'REPLACE_WITH') === false;

if (!$configured || !$webhookConfigured) {
    echo json_encode(['received' => true, 'note' => 'webhook not configured yet']);
    exit;
}

$payload = file_get_contents('php://input');
$sigHeader = $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '';

$event = verifyAndParseEvent($payload, $sigHeader, STRIPE_WEBHOOK_SECRET);
if ($event === null) {
    // Invalid signature or malformed payload — do not process, but still
    // answer 200 so a spoofed/broken request doesn't trigger Stripe retries.
    logWebhookError('signature verification failed');
    echo json_encode(['received' => false]);
    exit;
}

$type = $event['type'] ?? '';
$session = $event['data']['object'] ?? [];

if ($type === 'checkout.session.expired') {
    handleExpiredSession($session);
} elseif ($type === 'checkout.session.completed') {
    handleCompletedSession($session);
}

echo json_encode(['received' => true]);
exit;

/**
 * A Checkout Session hit its expiry (see the shortened 2h expires_at in
 * create-checkout-session.php) without ever being paid — this is the
 * "gave up somewhere, no matter how" signal. If they'd typed contact info
 * on Stripe's page before leaving, it's already attached to the session.
 */
function handleExpiredSession($session) {
    $sessionId = $session['id'] ?? '';
    if ($sessionId === '' || sessionAlreadyLogged($sessionId)) {
        return; // Already reported by cancel.php (Stripe's own back link) — skip duplicate.
    }

    $email = $session['customer_details']['email'] ?? '';
    $phone = $session['customer_details']['phone'] ?? '';
    $name = $session['customer_details']['name'] ?? '';
    if ($email === '' && $phone === '') {
        return; // No contact info was ever entered — nothing actionable to report.
    }

    $lead = [
        'session_id' => $sessionId,
        'name' => $session['metadata']['product_name'] ?? 'E-Suero Fahrzeug',
        'customer_name' => $name,
        'email' => $email,
        'phone' => $phone,
    ];

    $line = sprintf(
        "[%s] ABGEBROCHEN (Webhook) | %s | %s | %s <%s / %s>\n",
        date('Y-m-d H:i:s'),
        $lead['session_id'],
        $lead['name'],
        $lead['customer_name'] ?: '(kein Name)',
        $lead['email'] ?: '(keine E-Mail)',
        $lead['phone'] ?: '(kein Telefon)'
    );
    @file_put_contents(__DIR__ . '/orders.log', $line, FILE_APPEND | LOCK_EX);

    $subject = "⚠️ Kauf abgebrochen, aber Kontaktdaten vorhanden: {$lead['name']}";
    $body = "Jemand hat den Kauf auf e-suero.ch abgebrochen (Tab geschlossen oder zurücknavigiert),\n" .
        "aber vorher folgende Daten eingegeben:\n\n" .
        "Produkt: {$lead['name']}\n" .
        "Name: " . ($lead['customer_name'] ?: '(kein Name)') . "\n" .
        "E-Mail: " . ($lead['email'] ?: '(keine E-Mail)') . "\n" .
        "Telefon: " . ($lead['phone'] ?: '(kein Telefon)') . "\n\n" .
        "Empfehlung: Direkt kontaktieren, um den Verkauf zu sichern.";
    $headers = "From: " . ADMIN_EMAIL . "\r\nContent-Type: text/plain; charset=UTF-8";
    if ($lead['email']) {
        $headers .= "\r\nReply-To: " . $lead['email'];
    }
    @mail(ADMIN_EMAIL, $subject, $body, $headers);
}

/**
 * Redundant safety net for a completed payment, in case the visitor closed
 * the tab right after paying and never actually reached success.php. Skips
 * itself if success.php already logged this session, so a normal successful
 * checkout never gets emailed twice.
 */
function handleCompletedSession($session) {
    $sessionId = $session['id'] ?? '';
    if ($sessionId === '' || ($session['payment_status'] ?? '') !== 'paid') {
        return;
    }
    if (sessionAlreadyLogged($sessionId)) {
        return; // success.php already handled this one.
    }

    $order = [
        'id' => $sessionId,
        'name' => $session['metadata']['product_name'] ?? 'E-Suero Fahrzeug',
        'amount' => isset($session['amount_total']) ? number_format($session['amount_total'] / 100, 2, '.', "'") : '',
        'currency' => strtoupper($session['currency'] ?? 'CHF'),
        'email' => $session['customer_details']['email'] ?? '',
        'customer_name' => $session['customer_details']['name'] ?? '',
    ];

    $line = sprintf(
        "[%s] %s (Webhook) | %s %s | %s | %s <%s>\n",
        date('Y-m-d H:i:s'),
        $order['id'],
        $order['amount'], $order['currency'],
        $order['name'],
        $order['customer_name'] ?: '(kein Name)',
        $order['email'] ?: '(keine E-Mail)'
    );
    @file_put_contents(__DIR__ . '/orders.log', $line, FILE_APPEND | LOCK_EX);

    $subject = "✅ Neue Bestellung: {$order['name']}";
    $body = "Neue Bestellung über e-suero.ch (per Webhook bestätigt)\n\n" .
        "Produkt: {$order['name']}\n" .
        "Betrag: {$order['amount']} {$order['currency']}\n" .
        "Kunde: " . ($order['customer_name'] ?: '(kein Name)') . "\n" .
        "E-Mail: " . ($order['email'] ?: '(keine E-Mail)') . "\n" .
        "Stripe Session: {$order['id']}\n";
    $headers = "From: " . ADMIN_EMAIL . "\r\nContent-Type: text/plain; charset=UTF-8";
    if ($order['email']) {
        $headers .= "\r\nReply-To: " . $order['email'];
    }
    @mail(ADMIN_EMAIL, $subject, $body, $headers);
}

/**
 * True if this Stripe session ID already appears anywhere in orders.log —
 * i.e. success.php or cancel.php already reported it, so the webhook must
 * not send a second, duplicate notification for the same session.
 */
function sessionAlreadyLogged($sessionId) {
    $path = __DIR__ . '/orders.log';
    if (!is_file($path)) {
        return false;
    }
    $contents = @file_get_contents($path);
    if ($contents === false) {
        return false;
    }
    return strpos($contents, $sessionId) !== false;
}

/**
 * Verifies Stripe's webhook signature by hand (no SDK/Composer available on
 * shared hosting) and returns the decoded event array, or null if the
 * signature is missing/invalid/too old. Follows Stripe's documented scheme:
 * https://stripe.com/docs/webhooks#verify-manually
 */
function verifyAndParseEvent($payload, $sigHeader, $secret) {
    if ($payload === '' || $sigHeader === '') {
        return null;
    }

    $timestamp = null;
    $signatures = [];
    foreach (explode(',', $sigHeader) as $part) {
        $pair = explode('=', $part, 2);
        if (count($pair) !== 2) continue;
        [$key, $value] = $pair;
        if ($key === 't') {
            $timestamp = $value;
        } elseif ($key === 'v1') {
            $signatures[] = $value;
        }
    }

    if ($timestamp === null || empty($signatures)) {
        return null;
    }

    // Reject anything older than 5 minutes to guard against replay attacks.
    if (abs(time() - (int) $timestamp) > 300) {
        return null;
    }

    $expected = hash_hmac('sha256', $timestamp . '.' . $payload, $secret);

    $valid = false;
    foreach ($signatures as $sig) {
        if (hash_equals($expected, $sig)) {
            $valid = true;
            break;
        }
    }
    if (!$valid) {
        return null;
    }

    $decoded = json_decode($payload, true);
    return is_array($decoded) ? $decoded : null;
}

function logWebhookError($message) {
    $line = sprintf("[%s] webhook: %s\n", date('Y-m-d H:i:s'), $message);
    @file_put_contents(__DIR__ . '/error.log', $line, FILE_APPEND | LOCK_EX);
}
