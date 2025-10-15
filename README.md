# OpenSight — Passive OSINT Collection Framework

**Author:** White (© 2025)  
**Description:** Kali-friendly passive OSINT tool for lawful reconnaissance. Collects domain and person information via WHOIS, DNS, crt.sh, homepage, GitHub, social profiles, and email patterns. Outputs structured JSON for security research and analysis.

---

## Features
- Passive-first: no port scanning or brute-force.
- Supports domain and person investigation.
- Collects:
  - WHOIS & DNS records
  - Certificate transparency data (crt.sh)
  - Homepage links and metadata
  - GitHub code references
  - Social profile presence
  - Email pattern generation
- Saves results to JSON.

---

## Installation

```bash
git clone https://github.com/yourusername/opensight.git
cd opensight
pip3 install -r requirements.txt


Dependencies:

#Python 3.9+

#aiohttp, beautifulsoup4, dnspython, colorama, pyfiglet

Scan a domain with default modules:
python3 opensight.py --target example.com

Scan a domain with specific modules:
python3 opensight.py --target example.com --modules whois,dns,crtsh,homepage,github


Scan a person for social profiles:
python3 opensight.py --target "Firstname Lastname" --person

Save output to a JSON file:
python3 opensight.py --target example.com --out results/example_osint.json

Default modules:
whois, dns, crtsh, homepage, github, emailpatterns





