<?php
/**
 * E-Suero — server-side price whitelist for E-Roller products.
 * Generated from the single source of truth (eroller_catalog.py) that
 * also drives the individual model pages. Never trust a price the
 * browser sends with a checkout request — look it up here instead.
 *
 * Structure: slug => ['name' => ..., 'prices' => [valid unit_amount values in Rappen]]
 * (a list, not a single value, because some models sell in more than
 * one battery/variant tier at different prices).
 */
return [
    'tsc-next-one-nx1-7i' => ['name' => 'TSC Next One NX1 7i', 'prices' => [299900]],
    'tsc-next-one-nx1-7i-45' => ['name' => 'TSC Next One NX1 7i 45 km/h', 'prices' => [299900]],
    'next-nx1' => ['name' => 'Next NX1', 'prices' => [299900]],
    'cityflizzer-tsc' => ['name' => 'CityFlizzer TSC', 'prices' => [219000, 299000]],
    'next-nx-plus' => ['name' => 'Next NX Plus', 'prices' => [325000, 395000]],
    'chopper-6-0-pro' => ['name' => 'Chopper 6.0 Pro', 'prices' => [359000]],
    'fatbob-pro' => ['name' => 'Fatbob Pro', 'prices' => [349000]],
    'next-nx-plus-45' => ['name' => 'Next NX Plus 45 km/h', 'prices' => [325000]],
    'next-nx1-45' => ['name' => 'Next NX1 45 km/h', 'prices' => [299000]],
    'fantic-issimo-city-escooter-l1' => ['name' => 'Fantic Issimo City E-Scooter L1', 'prices' => [489000]],
    'chopper-6-0-pro-45' => ['name' => 'Chopper 6.0 Pro 45 km/h', 'prices' => [399000]],
];
