<?php
/**
 * E-Suero — server-side price whitelist for E-Minicar products.
 * Generated from the single source of truth (minicar_catalog.py) that also
 * drives the individual model pages. Never trust a price the browser
 * sends with a checkout request — look it up here instead.
 *
 * Structure: slug => ['name' => ..., 'prices' => [valid unit_amount values in Rappen]]
 * (a list, not a single value, because some models sell in more than
 * one battery/variant tier at different prices).
 */
return [
    'next-one-tsc-e-minicar' => ['name' => 'NEXT ONE TSC e-Minicar 25 km/h Lithium Edition', 'prices' => [999000]],
    'next-one-tsc-e-minicar-10-20' => ['name' => 'NEXT ONE TSC e-Minicar 10/20 km/h Lithium Edition', 'prices' => [999000]],
];
