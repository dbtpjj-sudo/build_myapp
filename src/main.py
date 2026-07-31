# src/main.py
import json
from utils import resource_path
from playwright.sync_api import sync_playwright

def main():
    cfg = resource_path("data/config.json")
    # BOM を自動で取り除く utf-8-sig を指定
    with open(cfg, "r", encoding="utf-8-sig") as f:
        config = json.load(f)
    print("config loaded:", config)

if __name__ == "__main__":
    main()
