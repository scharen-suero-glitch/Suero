# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from minicar_catalog import PRODUCTS
import model_page_lib as lib

CATEGORY = {"name": "E-Minicar", "dir": "e-minicar", "landing": "fahrzeuge/e-minicar.html"}
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "fahrzeuge", "e-minicar")

if __name__ == "__main__":
    lib.generate(PRODUCTS, CATEGORY, OUT_DIR)
