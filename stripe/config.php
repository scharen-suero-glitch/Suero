<?php
/**
 * E-Suero — Stripe configuration. Shared by every file in stripe/.
 *
 * SETUP (do this once, directly on the server — never via chat/AI):
 * 1. Log in to https://dashboard.stripe.com/apikeys
 * 2. Copy your SECRET key (starts with sk_live_... or sk_test_...)
 * 3. Replace the placeholder below with that key.
 * 4. Save this file. That's it — every other Stripe file reads from here.
 * 5. Never commit the real secret key to git or share it anywhere else.
 *
 * WEBHOOK SETUP (optional, do this once you're ready for it):
 * 1. Log in to https://dashboard.stripe.com/webhooks
 * 2. Click "Add endpoint". URL: https://e-suero.ch/stripe/webhook.php
 * 3. Select events: checkout.session.expired and checkout.session.completed
 * 4. After creating it, click "Reveal" next to "Signing secret" (starts with whsec_...)
 * 5. Replace the STRIPE_WEBHOOK_SECRET placeholder below with that value.
 *    This is a DIFFERENT secret from your API key above — never share it either.
 */
define('STRIPE_SECRET_KEY', 'sk_live_REPLACE_WITH_YOUR_STRIPE_SECRET_KEY');
define('STRIPE_WEBHOOK_SECRET', 'whsec_REPLACE_WITH_YOUR_WEBHOOK_SIGNING_SECRET');

define('STRIPE_API_BASE', 'https://api.stripe.com/v1');
define('SITE_URL', 'https://e-suero.ch');
define('ADMIN_EMAIL', 'info@e-suero.ch');
