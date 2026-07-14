
**Date:** July 14, 2026  
**Original Reports Path:** `docs/scanners-reports/`  

---

## Top Priority (Critical & High with Available Fixes)
These packages carry high risk/severity, but **fixed versions are already available**. They must be updated first.

### Python Utilities & Libraries (python-pkg)
*   **starlette (0.37.2 -> High/Medium)**
    *   *Issue:* DoS via multipart/form-data (CVE-2024-47874), SSRF, and credential leakage (CVE-2026-48818).
    *   *Remediation:* Upgrade to version **1.3.1** (this will resolve all vulnerabilities spanning from 0.40.0 to 1.3.1).
*   **wheel (0.45.1 -> High)**
    *   *Issue:* Remote Code Execution (RCE) / Privilege Escalation via malicious wheel files (CVE-2026-24049).
    *   *Remediation:* Upgrade to **0.46.2**.
*   **pip (24.0 -> Medium/Low)**
    *   *Issue:* Code execution and path traversal during package installation (CVE-2025-8869, CVE-2026-8643).
    *   *Remediation:* Upgrade to **26.1.2**.
*   **openssl (3.5.6 -> High/Critical)** *(System Binary)*
    *   *Issue:* Multiple 2026 CVEs (including CVE-2026-45447 and the Critical CVE-2026-34182).
    *   *Remediation:* Upgrade to **3.5.7** or higher.
*   **python (3.11.15 -> High)** *(System Binary)*
    *   *Issue:* Recent vulnerabilities such as CVE-2026-7210, CVE-2026-11940, etc.
    *   *Remediation:* Update to patch versions **3.13.14 / 3.14.6** (or update the base image if using Docker).

---

## OS System Packages (Fix Available)
Certain Debian system utilities have patches available and should be updated via the OS package manager:

*   **util-linux (2.41-5 -> Medium/High)** — Upgrade to `2.42-1` (fixes CVE-2026-3184).
*   **liblzma5 (5.8.1-1 -> Medium)** — Upgrade to `5.8.1-1+deb13u1` (fixes CVE-2026-34743).

---

## Risk Acceptance / Exceptions (Won't Fix)
These vulnerabilities are explicitly marked by the distribution maintainers as **(won't fix)**. Standard OS package manager updates will not resolve them. They should be added to the scanner's ignore list or accepted as operational risks:

*   **systemd (257.13-1~deb13u1)** — Contains a large number of CVEs (including High: CVE-2023-50387 with 100% EPSS score, and CVE-2023-50868). *Note: If this runs inside a minimal Docker container, systemd is typically inactive, making the actual exploit risk minimal.*
*   **shadow (1:4.17.4-2)** — Legacy vulnerabilities (e.g., Critical CVE-2017-12424) that Debian does not plan to patch.
*   **libc6 / libc-bin (2.41-12+deb13u3)** — Critical CVE-2026-5450. Await a status change from Debian or consider migrating to a different base image.
*   **perl-base, coreutils, tar** — Multiple vulnerabilities designated as `won't fix`.

---

##  Action Items Checklist
- [ ] 1. Update dependencies in `requirements.txt` / `pyproject.toml` (Starlette, Wheel, Pip).
- [ ] 2. Rebuild the Docker image using the `--no-cache` flag, ensuring `apt-get update && apt-get upgrade -y` is executed to catch updates for OpenSSL, `util-linux`, and `gzip`.
- [ ] 3. Configure the scanner's ignore file (e.g., `trivy.yaml` or `.grype.yaml`) to suppress `won't fix` alerts for `systemd` and `shadow` to reduce CI/CD build noise.