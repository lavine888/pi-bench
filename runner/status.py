import json
from pathlib import Path
from .config import ROOT

def main():
    path = ROOT / "results" / "latest.json"
    print(path.read_text(encoding="utf-8") if path.exists() else json.dumps({"status": "no completed runs"}))

if __name__ == "__main__": main()
