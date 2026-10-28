<?php
/**
 * E-Suero — reached when a visitor backs out of Stripe Checkout before paying.
 *
 * If they had already typed an email/phone on Stripe's page before leaving,
 * this captures it and emails the shop so staff can follow up directly and
 * try to close the sale — even though no payment happened.
 */
require __DIR__ . '/config.php';

$configured = strpos(STRIPE_SECRET_KEY, 'REPLACE_WITH') === false;
$sessionId = isset($_GET['session_id']) ? preg_replace('/[^a-zA-Z0-9_]/', '', $_GET['session_id']) : '';
$lead = null;

if ($configured && $sessionId !== '') {
    $session = stripeGet("/checkout/sessions/{$sessionId}?expand[]=customer");
    if ($session && !isset($session['error'])) {
        // Stripe sometimes commits a typed phone/email to the Customer object
        // slightly before it shows up in customer_details (e.g. if the visitor
        // leaves right after typing, before the field fully syncs) — check both.
        $email = $session['customer_details']['email'] ?? ($session['customer']['email'] ?? '');
        $phone = $session['customer_details']['phone'] ?? ($session['customer']['phone'] ?? '');
        $name = $session['customer_details']['name'] ?? ($session['customer']['name'] ?? '');
        if ($email !== '' || $phone !== '') {
            $lead = [
                'session_id' => $sessionId,
                'name' => $session['metadata']['product_name'] ?? 'E-Suero Fahrzeug',
                'customer_name' => $name,
                'email' => $email,
                'phone' => $phone,
            ];
            logLead($lead);
            notifyAdminOfLead($lead);
        }
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

function logLead($lead) {
    // session_id is included so webhook.php can recognize this session was
    // already reported here (via Stripe's own "← Zurück" link) and skip its
    // own duplicate notification when the session later expires.
    $line = sprintf(
        "[%s] ABGEBROCHEN | %s | %s | %s <%s / %s>\n",
        date('Y-m-d H:i:s'),
        $lead['session_id'],
        $lead['name'],
        $lead['customer_name'] ?: '(kein Name)',
        $lead['email'] ?: '(keine E-Mail)',
        $lead['phone'] ?: '(kein Telefon)'
    );
    @file_put_contents(__DIR__ . '/orders.log', $line, FILE_APPEND | LOCK_EX);
}

function notifyAdminOfLead($lead) {
    $subject = "⚠️ Kauf abgebrochen, aber Kontaktdaten vorhanden: {$lead['name']}";
    $body = "Jemand hat den Kauf auf e-suero.ch abgebrochen, aber vorher folgende Daten eingegeben:\n\n" .
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
?>
<!doctype html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Kauf abgebrochen — E-Suero</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#050505">
<link rel="icon" href="../assets/icons/favicon.png" type="image/png">
<link rel="stylesheet" href="../assets/fonts/fonts.css?v=20260808">
<link rel="stylesheet" href="../styles.css?v=20260815">
</head>
<body>
<main id="main" style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem">
  <div class="container" style="max-width:640px;text-align:center">
    <span class="eyebrow">Kein Problem</span>
    <h1>Zahlung abgebrochen</h1>
    <p style="color:var(--c-mute);font-size:1.05rem;margin:1rem 0 2rem">
      Es wurde keine Zahlung durchgeführt. Bei Fragen zu Ihrer Bestellung oder wenn Sie lieber
      persönlich beraten werden möchten, sind wir gerne für Sie da:
      <a href="mailto:info@e-suero.ch" class="inline" style="color:var(--c-primary)">info@e-suero.ch</a>
      oder <a href="tel:+41796689088" class="inline" style="color:var(--c-primary)">+41 79 668 90 88</a>.
    </p>
    <a href="../index.html#products" class="btn btn-primary magnetic">Zurück zum Katalog</a>
  </div>
</main>
</body>
</html>
