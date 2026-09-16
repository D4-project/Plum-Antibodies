#!/usr/bin/env python3
"""Add verified manufacturer homepages to rules with unambiguous vendors."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


REFERENCES = {
    "adobe": "https://www.adobe.com/",
    "amazon": "https://aws.amazon.com/",
    "apache": "https://httpd.apache.org/",
    "apple": "https://www.apple.com/",
    "aruba": "https://www.arubanetworks.com/",
    "asus": "https://www.asus.com/",
    "atlassian": "https://www.atlassian.com/",
    "baidu": "https://www.baidu.com/",
    "barracuda": "https://www.barracuda.com/",
    "checkpoint": "https://www.checkpoint.com/",
    "cisco": "https://www.cisco.com/",
    "citrix": "https://www.citrix.com/",
    "dell": "https://www.dell.com/",
    "docker": "https://www.docker.com/",
    "drupal": "https://www.drupal.org/",
    "f5": "https://www.f5.com/",
    "filezilla": "https://filezilla-project.org/",
    "fortinet": "https://www.fortinet.com/",
    "freebsd": "https://www.freebsd.org/",
    "gitlab": "https://about.gitlab.com/",
    "google": "https://www.google.com/",
    "hashicorp": "https://www.hashicorp.com/",
    "huawei": "https://www.huawei.com/",
    "ibm": "https://www.ibm.com/",
    "intelbras": "https://www.intelbras.com/",
    "ivanti": "https://www.ivanti.com/",
    "jenkins": "https://www.jenkins.io/",
    "juniper": "https://www.juniper.net/",
    "microsoft": "https://www.microsoft.com/",
    "mysql": "https://www.mysql.com/",
    "nagios": "https://www.nagios.org/",
    "netgear": "https://www.netgear.com/",
    "nginx": "https://nginx.org/",
    "nmap": "https://nmap.org/",
    "openvpn": "https://openvpn.net/",
    "palo-alto": "https://www.paloaltonetworks.com/",
    "php": "https://www.php.net/",
    "qnap": "https://www.qnap.com/",
    "redhat": "https://www.redhat.com/",
    "sap": "https://www.sap.com/",
    "siemens": "https://www.siemens.com/",
    "slack": "https://slack.com/",
    "sonicwall": "https://www.sonicwall.com/",
    "sophos": "https://www.sophos.com/",
    "synology": "https://www.synology.com/",
    "vmware": "https://www.vmware.com/",
    "wordpress": "https://wordpress.org/",
    "xerox": "https://www.xerox.com/",
    "zabbix": "https://www.zabbix.com/",
    "zyxel": "https://www.zyxel.com/",
}

VENDOR_RE = re.compile(r"^\s*- vendor:([^\s]+)\s*$", re.MULTILINE)
VERSION_RE = re.compile(r"^version:.*$", re.MULTILINE)


def add_reference(path: Path, stamp: str) -> str | None:
    """Add one reference when the rule has a mapped vendor and no references."""
    content = path.read_text(encoding="utf-8")
    if re.search(r"^references:", content, re.MULTILINE):
        return None
    match = VENDOR_RE.search(content)
    if not match or match.group(1) not in REFERENCES:
        return None
    url = REFERENCES[match.group(1)]
    content = content.replace("version:", f"references:\n- {url}\nversion:", 1)
    content = VERSION_RE.sub(f"version: {stamp}", content, count=1)
    path.write_text(content, encoding="utf-8")
    return match.group(1)


def main() -> None:
    """Populate references for the rules directory."""
    root = Path(__file__).resolve().parents[1] / "tags"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    changed = 0
    for path in sorted(root.glob("*.yaml")):
        if add_reference(path, stamp):
            changed += 1
    print(f"Added references to {changed} rules (version {stamp}).")


if __name__ == "__main__":
    main()
