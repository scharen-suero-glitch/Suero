# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from eroller_catalog import PRODUCTS
import model_page_lib as lib

CATEGORY = {"name": "E-Roller", "dir": "e-roller", "landing": "fahrzeuge/e-roller.html"}
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "fahrzeuge", "e-roller")

if __name__ == "__main__":
    lib.generate(PRODUCTS, CATEGORY, OUT_DIR)
