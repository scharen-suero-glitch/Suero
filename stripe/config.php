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
 */
define('STRIPE_SECRET_KEY', 'sk_live_REPLACE_WITH_YOUR_STRIPE_SECRET_KEY');

define('STRIPE_API_BASE', 'https://api.stripe.com/v1');
define('SITE_URL', 'https://e-suero.ch');
define('ADMIN_EMAIL', 'info@e-suero.ch');
