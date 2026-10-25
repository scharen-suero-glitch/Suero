# E-Roller content generator

`eroller_catalog.py` is the single source of truth for every E-Roller
product (name, price, variants, full spec table) — the same data that
appears on `fahrzeuge/e-roller.html`'s cards, on each individual model
page, and in the Stripe server-side price whitelist. When a price,
spec, or model changes, edit it there first.

After editing `eroller_catalog.py`, regenerate everything it drives:

```bash
cd tools
python3 gen_eroller_pages.py        # rewrites fahrzeuge/e-roller/*.html

python3 - << 'EOF'
import sys; sys.path.insert(0, '.')
from eroller_catalog import PRODUCTS
catalog = {}
for p in PRODUCTS:
    prices = sorted({p["price_rappen"], *[v["price_rappen"] for v in p["variants"]]})
    catalog[p["slug"]] = {"name": p["name"], "prices": prices}
lines = ["<?php", "return ["]
for slug, d in catalog.items():
    prices = ", ".join(map(str, d["prices"]))
    lines.append(f"    '{slug}' => ['name' => '{d['name']}', 'prices' => [{prices}]],")
lines.append("];")
open("../stripe/catalog-eroller.php", "w", encoding="utf-8").write("\n".join(lines) + "\n")
EOF
```

Then still by hand: update the matching product cards on
`fahrzeuge/e-roller.html` itself (names/prices/specs there are not
auto-generated from this file — only the individual pages and the
Stripe whitelist are) and bump the `styles.css`/`main.js` `?v=` cache
query string on any page you touched.
