<?php
/**
 * E-Suero — commercial (sales) and workshop inquiry endpoint.
 *
 * Handles two request types via the `type` field, kept deliberately
 * separate in validation and email formatting so neither can leak
 * into the other's rules:
 *   - "sales" (default, backward-compatible): verkauf/* pages via
 *     assets/js/sales-form.js. Subject "Verkaufsanfrage – <Modell>".
 *   - "workshop": index.html's #contact-form (main.js). Subject
 *     "Werkstattanfrage – <Service>". Previously this form only
 *     opened a mailto: link client-side; it now submits here like
 *     every other form on the site.
 *
 * Still separate from everything under stripe/ (payments). This is a
 * real server-side endpoint: it validates, actually sends mail via
 * PHP's mail() (the same mechanism already proven to work for every
 * Stripe notification on this hosting), and only ever reports success
 * once that has actually happened — never simulated.
 */
require __DIR__ . '/../stripe/config.php'; // only reads ADMIN_EMAIL — never touches the Stripe secret

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Invalid request body']);
    exit;
}

// Honeypot: a field real visitors never see or fill in (hidden via CSS in
// the form). Any bot that fills every field in the DOM trips this.
if (!empty($input['website'])) {
    // Pretend success so the bot doesn't learn anything; nothing is sent.
    echo json_encode(['ok' => true]);
    exit;
}

$type = isset($input['type']) && $input['type'] === 'workshop' ? 'workshop' : 'sales';
$name = isset($input['name']) ? trim((string) $input['name']) : '';
$phone = isset($input['phone']) ? trim((string) $input['phone']) : '';
$email = isset($input['email']) ? trim((string) $input['email']) : '';
$model = isset($input['model']) ? trim((string) $input['model']) : '';
$service = isset($input['service']) ? trim((string) $input['service']) : '';
$reasonRaw = isset($input['reason']) ? (string) $input['reason'] : '';
$message = isset($input['message']) ? trim((string) $input['message']) : '';
$preferredDate = isset($input['preferred_date']) ? trim((string) $input['preferred_date']) : '';
$pageUrl = isset($input['page_url']) ? trim((string) $input['page_url']) : '';

$reasons = [
    'beratung' => 'Beratung',
    'probefahrt' => 'Probefahrt',
    'angebot' => 'Angebot',
];
$reasonLabel = isset($reasons[$reasonRaw]) ? $reasons[$reasonRaw] : 'Allgemeine Anfrage';

$emailValid = $email !== '' && filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
// A Swiss/international phone number: digits, spaces, +, -, (), at least 7 digits total.
$phoneDigits = preg_replace('/[^0-9]/', '', $phone);
$phoneValid = $phone !== '' && strlen($phoneDigits) >= 7 && strlen($phoneDigits) <= 15;

$errors = [];
if ($name === '' || mb_strlen($name) > 120) {
    $errors[] = 'name';
}
if ($type === 'workshop') {
    // The workshop form requires a real email (no phone-only option), matching its HTML.
    if (!$emailValid) {
        $errors[] = 'email';
    }
    if ($message === '' || mb_strlen($message) > 2000) {
        $errors[] = 'message';
    }
} else {
    // Brief requirement: exactly one contact channel is mandatory (phone OR email), not both.
    if (!$emailValid && !$phoneValid) {
        $errors[] = 'contact';
    }
    if ($message !== '' && mb_strlen($message) > 2000) {
        $errors[] = 'message';
    }
}

if (!empty($errors)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Bitte Pflichtfelder prüfen.', 'fields' => $errors]);
    exit;
}

if ($type === 'workshop') {
    $subject = 'Werkstattanfrage' . ($service !== '' ? " – {$service}" : '');
    $bodyLines = [
        "Neue Werkstattanfrage über e-suero.ch",
        "",
        "Gewünschter Service: " . ($service !== '' ? $service : '(nicht angegeben)'),
        "Name: {$name}",
        "Telefon: " . ($phone !== '' ? $phone : '(nicht angegeben)'),
        "E-Mail: {$email}",
    ];
} else {
    $subjectModel = $model !== '' ? $model : 'Allgemein';
    $subject = "Verkaufsanfrage – {$subjectModel}";

    $bodyLines = [
        "Neue Verkaufsanfrage über e-suero.ch",
        "",
        "Grund: {$reasonLabel}",
        "Modell: " . ($model !== '' ? $model : '(kein Modell ausgewählt)'),
        "Name: {$name}",
        "Telefon: " . ($phone !== '' ? $phone : '(nicht angegeben)'),
        "E-Mail: " . ($email !== '' ? $email : '(nicht angegeben)'),
    ];
    if ($reasonRaw === 'probefahrt') {
        $bodyLines[] = "Wunschtermin: " . ($preferredDate !== '' ? $preferredDate : '(kein Wunschtermin angegeben)');
    }
}
if ($message !== '') {
    $bodyLines[] = "";
    $bodyLines[] = "Nachricht:";
    $bodyLines[] = $message;
}
if ($pageUrl !== '') {
    $bodyLines[] = "";
    $bodyLines[] = "Angefragt von: {$pageUrl}";
}
$bodyLines[] = "";
$bodyLines[] = "Zeit: " . date('Y-m-d H:i:s');
$body = implode("\n", $bodyLines);

$headers = "From: " . ADMIN_EMAIL . "\r\nContent-Type: text/plain; charset=UTF-8";
if ($emailValid) {
    $headers .= "\r\nReply-To: " . $email;
}

$sent = @mail(ADMIN_EMAIL, $subject, $body, $headers);

if (!$sent) {
    logInquiryError('mail() returned false', ['subject' => $subject]);
    http_response_code(502);
    echo json_encode([
        'ok' => false,
        'error' => 'Anfrage konnte nicht gesendet werden. Bitte rufen Sie uns direkt an oder schreiben Sie uns auf WhatsApp.',
    ]);
    exit;
}

logInquiry([
    'type' => $type,
    'reason' => $type === 'workshop' ? $service : $reasonRaw,
    'model' => $model,
    'name' => $name,
    'phone' => $phone,
    'email' => $email,
]);

$response = ['ok' => true];
if ($reasonRaw === 'probefahrt') {
    // Honesty requirement: there is no real booking calendar behind this —
    // a human confirms the actual date/time afterwards.
    $response['note'] = 'pending_confirmation';
}
echo json_encode($response);
exit;

function logInquiry($data) {
    $line = sprintf(
        "[%s] %s | %s | Modell: %s | %s <%s / %s>\n",
        date('Y-m-d H:i:s'),
        strtoupper($data['type']),
        $data['reason'] ?: 'unbekannt',
        $data['model'] !== '' ? $data['model'] : '(keines)',
        $data['name'],
        $data['email'] ?: '(keine E-Mail)',
        $data['phone'] ?: '(kein Telefon)'
    );
    @file_put_contents(__DIR__ . '/inquiries.log', $line, FILE_APPEND | LOCK_EX);
}

function logInquiryError($message, $extra = []) {
    $line = sprintf("[%s] %s | %s\n", date('Y-m-d H:i:s'), $message, json_encode($extra));
    @file_put_contents(__DIR__ . '/inquiries-error.log', $line, FILE_APPEND | LOCK_EX);
}
