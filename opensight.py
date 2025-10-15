#!/usr/bin/env python3
"""
OpenSight — Passive OSINT Collection Framework (Kali-friendly)
Author: White (© 2025)
"""

import argparse
import asyncio
import aiohttp
import subprocess
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import dns.resolver
import urllib.parse as urlparse
import re
from colorama import Fore, Style, init
from pyfiglet import Figlet

# Initialize colorama
init(autoreset=True)

# Banner function
def banner():
    fig = Figlet(font="slant")
    print(Fore.RED + fig.renderText("OpenSight"))
    print(Fore.LIGHTCYAN_EX + "   Passive OSINT Collection Framework (Kali Friendly)")
    print(Fore.LIGHTWHITE_EX + "   Developed by: " + Fore.LIGHTRED_EX + "White\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "-" * 80 + "\n")

# Basic settings
USER_AGENT = "OpenSight/1.0 (+passive osint collector)"
RATE_LIMIT = 1.0  # seconds between HTTP requests
OUT_DIR = Path("results")
OUT_DIR.mkdir(exist_ok=True)

def save_json(data, path: Path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Example dummy modules (placeholders)
def module_whois(target):
    return {"domain": target, "info": "Sample WHOIS data"}

def module_dns(target):
    return {"A": "1.2.3.4", "MX": "mail." + target}

async def module_crtsh(target, session):
    await asyncio.sleep(0.5)
    return [{"issuer": "Let's Encrypt", "cn": target}]

async def module_http_passive(target, session):
    await asyncio.sleep(0.5)
    return {"title": "Example Domain", "tech": ["nginx", "cloudflare"]}

async def module_github(target, session):
    await asyncio.sleep(0.5)
    return {"repos": ["https://github.com/example/repo"]}

async def module_social_guess(target, session):
    await asyncio.sleep(0.5)
    return {"twitter": f"https://twitter.com/{target}", "linkedin": f"https://linkedin.com/in/{target}"}

def module_email_patterns(target):
    return [f"admin@{target}", f"security@{target}"]

# ---- Main orchestration ---- #
async def run_all(target: str, modules: List[str], person_mode: bool=False) -> Dict[str, Any]:
    output = {"target": target, "collected": {}, "timestamp": time.time()}
    async with aiohttp.ClientSession() as session:
        for mod in modules:
            print(Fore.CYAN + f"[>] Running module: {mod}..." + Style.RESET_ALL)
            try:
                if mod == "whois" and not person_mode:
                    output["collected"]["whois"] = module_whois(target)
                elif mod == "dns" and not person_mode:
                    output["collected"]["dns"] = module_dns(target)
                elif mod == "crtsh" and not person_mode:
                    output["collected"]["crtsh"] = await module_crtsh(target, session)
                elif mod in ("http", "homepage"):
                    output["collected"]["http_passive"] = await module_http_passive(target, session)
                elif mod == "github":
                    output["collected"]["github"] = await module_github(target, session)
                elif mod in ("social",) or person_mode:
                    output["collected"]["social" if person_mode else "social_guesses"] = await module_social_guess(target, session)
                elif mod == "emailpatterns" and not person_mode:
                    output["collected"]["email_patterns"] = module_email_patterns(target)
                print(Fore.GREEN + f"    [+] {mod} completed successfully.\n")
            except Exception as e:
                print(Fore.RED + f"    [x] Error in {mod}: {e}\n")
    return output

# ---- CLI Parsing ---- #
def parse_args():
    p = argparse.ArgumentParser(description="OpenSight — Passive OSINT collector (Kali-friendly)")
    p.add_argument("--target", "-t", required=True, help="Domain or person name to investigate")
    p.add_argument("--modules", "-m", default="whois,dns,crtsh,homepage,github,emailpatterns", help="Comma list of modules")
    p.add_argument("--out", "-o", help="Output JSON path (default: results/<target>_osint.json)")
    p.add_argument("--person", action="store_true", help="Treat target as a person name (social handle discovery)")
    return p.parse_args()

def safe_filename(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9_.-]', '_', s)[:200]

def main():
    banner()
    args = parse_args()
    modules = [m.strip() for m in args.modules.split(",") if m.strip()]
    target = args.target.strip()
    print(Fore.LIGHTYELLOW_EX + f"[*] Target: {target}")
    print(Fore.LIGHTYELLOW_EX + f"[*] Modules: {', '.join(modules)}")
    print(Fore.LIGHTYELLOW_EX + "[*] Starting passive reconnaissance...\n")

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(run_all(target, modules, person_mode=args.person))

    outpath = Path(args.out) if args.out else OUT_DIR / f"{safe_filename(target)}_osint.json"
    save_json(result, outpath)
    print(Fore.LIGHTGREEN_EX + f"\n[+] Results saved to {outpath}")
    print(Fore.LIGHTCYAN_EX + "Review the JSON file for full module outputs.")
    print(Fore.YELLOW + "\n--- Scan Complete ---" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
