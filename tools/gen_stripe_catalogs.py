# -*- coding: utf-8 -*-
"""Regenerates every stripe/catalog-*.php price whitelist from its
single-source-of-truth Python catalog module. Run this after any price
change so the server-side Stripe validation never drifts out of sync
with what the pages actually show (this drift caused a real dead
"Jetzt kaufen" button once already — see QUELLEN-PRODUKTDATEN.md)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "stripe")

HEADER = """<?php
/**
 * E-Suero — server-side price whitelist for {category} products.
 * Generated from the single source of truth ({source}) that also
 * drives the individual model pages. Never trust a price the browser
 * sends with a checkout request — look it up here instead.
 *
 * Structure: slug => ['name' => ..., 'prices' => [valid unit_amount values in Rappen]]
 * (a list, not a single value, because some models sell in more than
 * one battery/variant tier at different prices).
 */
return [
"""


def php_string(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def write_catalog(products, category_name, source_module, out_filename):
    lines = [HEADER.format(category=category_name, source=source_module)]
    for p in products:
        if not p.get("price_rappen"):
            continue  # "Preis auf Anfrage" products have nothing to whitelist
        prices = sorted({p["price_rappen"]} | {v["price_rappen"] for v in p.get("variants", [])})
        prices_php = ", ".join(str(v) for v in prices)
        lines.append(
            f"    {php_string(p['slug'])} => ['name' => {php_string(p['name'])}, 'prices' => [{prices_php}]],\n"
        )
    lines.append("];\n")
    out_path = os.path.join(OUT_DIR, out_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print("wrote", out_path)


if __name__ == "__main__":
    from eroller_catalog import PRODUCTS as ROLLER_PRODUCTS
    from minicar_catalog import PRODUCTS as MINICAR_PRODUCTS

    write_catalog(ROLLER_PRODUCTS, "E-Roller", "eroller_catalog.py", "catalog-eroller.php")
    write_catalog(MINICAR_PRODUCTS, "E-Minicar", "minicar_catalog.py", "catalog-minicar.php")
