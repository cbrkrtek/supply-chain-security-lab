import os
import json
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(BASE_DIR, "docs", "scanners-reports", "grype-report.json")

with open(REPORT_PATH) as f:
    report = json.load(f)

matches = report.get("matches", [])
cve_ids = list({m["vulnerability"]["id"] for m in matches if m["vulnerability"]["id"].startswith("CVE-")})

epss_map = {}
for i in range(0, len(cve_ids), 100):
    batch = cve_ids[i:i+100]
    r = requests.get(f"https://api.first.org/data/v1/epss?cve={','.join(batch)}")
    for entry in r.json().get("data", []):
        epss_map[entry["cve"]] = float(entry["epss"])

findings = []
for m in matches:
    cve = m["vulnerability"]["id"]
    sev = m["vulnerability"]["severity"]
    epss = epss_map.get(cve, 0.0)
    findings.append((cve, sev, epss))

findings.sort(key=lambda x: x[2], reverse=True)
for cve, sev, epss in findings[:5]:
    print(f"{cve} | severity={sev} | epss={epss}")