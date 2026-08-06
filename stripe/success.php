<?php
/**
 * E-Suero — post-payment confirmation page.
 *
 * Uses the SAME secret key already configured in config.php — no separate
 * webhook signing secret needed. On load it asks Stripe directly "is this
 * session actually paid?" instead of trusting the redirect alone, then logs
 * the order locally and best-effort emails the shop.
 */
require __DIR__ . '/config.php';

$configured = strpos(STRIPE_SECRET_KEY, 'REPLACE_WITH') === false;
$sessionId = isset($_GET['session_id']) ? preg_replace('/[^a-zA-Z0-9_]/', '', $_GET['session_id']) : '';

$status = 'error';
$order = null;

if ($configured && $sessionId !== '') {
    $session = stripeGet("/checkout/sessions/{$sessionId}?expand[]=payment_intent&expand[]=customer");
    if ($session && !isset($session['error']) && ($session['payment_status'] ?? '') === 'paid') {
        $status = 'paid';
        $order = [
            'id' => $session['id'],
            'name' => $session['metadata']['product_name'] ?? 'E-Suero Fahrzeug',
            'slug' => $session['metadata']['product_slug'] ?? '',
            'amount' => isset($session['amount_total']) ? number_format($session['amount_total'] / 100, 2, '.', "'") : '',
            'currency' => strtoupper($session['currency'] ?? 'CHF'),
            'email' => $session['customer_details']['email'] ?? ($session['customer']['email'] ?? ''),
            'customer_name' => $session['customer_details']['name'] ?? '',
        ];
        logOrder($order);
        notifyAdmin($order);
    } elseif ($session && ($session['payment_status'] ?? '') === 'unpaid') {
        $status = 'unpaid';
    }
}

function stripeGet($path) {
    $ch = curl_init(STRIPE_API_BASE . $path);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Authorization: Bearer ' . STRIPE_SECRET_KEY]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);
    $body = curl_exec($ch);
    curl_close($ch);
    if ($body === false) return null;
    $decoded = json_decode($body, true);
    return is_array($decoded) ? $decoded : null;
}

function logOrder($order) {
    $line = sprintf(
        "[%s] %s | %s %s | %s | %s <%s>\n",
        date('Y-m-d H:i:s'),
        $order['id'],
        $order['amount'], $order['currency'],
        $order['name'],
        $order['customer_name'] ?: '(kein Name)',
        $order['email'] ?: '(keine E-Mail)'
    );
    @file_put_contents(__DIR__ . '/orders.log', $line, FILE_APPEND | LOCK_EX);
}

function notifyAdmin($order) {
    // Best-effort via PHP's built-in mail() — works out of the box on most shared
    // hosting (incl. Hostinger) without SMTP credentials. If the host blocks it,
    // the order is still safely recorded in orders.log above.
    // The From: address must be a real mailbox on the sending domain (ADMIN_EMAIL
    // itself is the safest choice) — an invented address is a common reason these
    // land in spam or get silently dropped by the mail server.
    $subject = "✅ Neue Bestellung: {$order['name']}";
    $body = "Neue Bestellung über e-suero.ch\n\n" .
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
?>
<!doctype html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Bestellung erhalten — E-Suero</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#050505">
<link rel="icon" href="../assets/icons/favicon.png" type="image/png">
<link rel="stylesheet" href="../assets/fonts/fonts.css?v=20260808">
<link rel="stylesheet" href="../styles.css?v=20260815">
</head>
<body>
<main id="main" style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem">
  <div class="container" style="max-width:640px;text-align:center">
<?php if ($status === 'paid'): ?>
    <span class="eyebrow">Bestellung bestätigt</span>
    <h1>Vielen Dank für Ihre Bestellung!</h1>
    <p style="color:var(--c-mute);font-size:1.05rem;margin:1rem 0 1.6rem">
      Ihre Zahlung für <strong style="color:var(--c-white)"><?= htmlspecialchars($order['name']) ?></strong>
      (<?= htmlspecialchars($order['amount']) ?> <?= htmlspecialchars($order['currency']) ?>) wurde erfolgreich verarbeitet.
      Wir haben Ihre Bestellung erhalten und melden uns in Kürze bei Ihnen, um die Lieferung bzw. Abholung
      in Freienbach SZ zu besprechen.
    </p>
    <p style="color:var(--c-mute-2);font-size:.85rem;margin-bottom:2rem">Bestellreferenz: <?= htmlspecialchars($order['id']) ?></p>
<?php elseif ($status === 'unpaid'): ?>
    <span class="eyebrow">Zahlung offen</span>
    <h1>Ihre Zahlung ist noch nicht abgeschlossen</h1>
    <p style="color:var(--c-mute);font-size:1.05rem;margin:1rem 0 2rem">
      Falls Sie den Bezahlvorgang abgebrochen haben, ist keine Zahlung erfolgt. Sie können es jederzeit erneut versuchen.
    </p>
<?php else: ?>
    <span class="eyebrow">Bestellung</span>
    <h1>Wir konnten Ihre Bestellung nicht bestätigen</h1>
    <p style="color:var(--c-mute);font-size:1.05rem;margin:1rem 0 2rem">
      Falls eine Zahlung erfolgt ist, wurde diese von Stripe verarbeitet. Bitte kontaktieren Sie uns direkt,
      damit wir Ihre Bestellung überprüfen können: <a href="mailto:info@e-suero.ch" class="inline" style="color:var(--c-primary)">info@e-suero.ch</a>
      oder <a href="tel:+41796689088" class="inline" style="color:var(--c-primary)">+41 79 668 90 88</a>.
    </p>
<?php endif; ?>
    <a href="../index.html" class="btn btn-primary magnetic">Zurück zur Startseite</a>
  </div>
</main>
</body>
</html>
