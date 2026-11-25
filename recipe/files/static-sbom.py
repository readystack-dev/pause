#!/usr/bin/env python3
"""static-sbom.py OUT DOC_NAME BINARY ITEM [ITEM ...] -- declare the C libraries linked statically into BINARY.

A static C link copies library code into the binary, and no scanner can see it there: Docker Scout read pause 3.10.2
(gcc -static, chain 781, 2026-10-29) as an image with 0 packages, and the OSV cross-check could not run. Owner rule
(2026-10-28): a grade blind to linked code is not a grade we publish; make the packages visible, disclose what is left.
This writes an SPDX 2.3 document, at build time inside the builder that linked BINARY, naming every linked library at
its exact version. The image ships it under /usr/local/share/readystack/sbom/, where
  - syft's sbom-cataloger reads it (ReadyStack's own scan, scripts/scan-inventory.py, counts only documents under
    /usr/local/share/readystack/; BuildKit's SBOM attestation, which Docker Scout and the OSV cross-check read, too);
  - a Debian package carries its distribution in the purl twice: distro=debian-12 (syft and grype; grype is given
    --distro from it when the image has no OS of its own) and os_name/os_version/os_distro (Docker Scout's own
    qualifiers; without them Scout lists the package and matches nothing, measured 2026-10-29);
  - an upstream tarball (no distribution) carries its CPE: grype matches it against NVD; Scout and OSV have no data
    for it, which the strategy's security notes say.

ITEM is
  deb:<package>                                     a package of the builder's own distribution: its version, source
                                                    package and architecture come from dpkg, its distribution from
                                                    /etc/os-release (no image has to carry either)
  src:<name>|<version>|<purl>|<cpe>|<url>|<licence> a library built from an upstream release tarball
No timestamps but SOURCE_DATE_EPOCH (required) and sorted output: two builds write the same bytes.
"""
import json
import os
import subprocess
import sys
import time
from urllib.parse import quote


def os_release(path="/etc/os-release"):
    out = {}
    for line in open(path):
        k, _, v = line.strip().partition("=")
        if k:
            out[k] = v.strip('"')
    return out


def deb(pkg, rel):
    fmt = "${Version}\t${source:Package}\t${source:Version}\t${Architecture}"
    r = subprocess.run(["dpkg-query", "-W", "-f", fmt, pkg], capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit(f"static-sbom: {pkg} is not installed in the builder ({r.stderr.strip()})")
    ver, src, srcver, arch = r.stdout.split("\t")
    dist, dver, code = rel["ID"], rel["VERSION_ID"], rel.get("VERSION_CODENAME") or ""
    upstream = src if srcver == ver else f"{src}@{srcver}"
    purl = (f"pkg:deb/{dist}/{pkg}@{quote(ver, safe='')}?arch={arch}&upstream={quote(upstream, safe='@')}"
            f"&distro={dist}-{dver}" + (f"&os_distro={code}" if code else "") + f"&os_name={dist}&os_version={dver}")
    return {"name": pkg, "versionInfo": ver, "supplier": f"Organization: {rel.get('NAME') or dist}",
            "downloadLocation": "NOASSERTION", "licenseDeclared": "NOASSERTION",
            "comment": f"from the builder's {dist} {dver} package {pkg} (source {src} {srcver})",
            "externalRefs": [{"referenceCategory": "PACKAGE-MANAGER", "referenceType": "purl", "referenceLocator": purl}]}


def src(spec):
    name, ver, purl, cpe, url, lic = (spec.split("|") + [""] * 6)[:6]
    if not (name and ver and (purl or cpe)):
        sys.exit(f"static-sbom: src item needs name|version|purl|cpe|url|licence, got {spec!r}")
    refs = ([{"referenceCategory": "SECURITY", "referenceType": "cpe23Type", "referenceLocator": cpe}] if cpe else []) + \
           ([{"referenceCategory": "PACKAGE-MANAGER", "referenceType": "purl", "referenceLocator": purl}] if purl else [])
    return {"name": name, "versionInfo": ver, "supplier": "NOASSERTION", "downloadLocation": url or "NOASSERTION",
            "licenseDeclared": lic or "NOASSERTION", "comment": "built from the upstream release tarball",
            "externalRefs": refs}


def main(argv):
    if len(argv) < 5:
        sys.exit(__doc__.split("\n\n")[0])
    out, doc, binary, items = argv[1], argv[2], argv[3], argv[4:]
    sde = os.environ.get("SOURCE_DATE_EPOCH")
    if not (sde or "").isdigit():
        sys.exit("static-sbom: SOURCE_DATE_EPOCH must be set (the document's only timestamp)")
    rel = os_release()
    pkgs = []
    for it in items:
        kind, _, rest = it.partition(":")
        p = deb(rest, rel) if kind == "deb" else src(rest) if kind == "src" else sys.exit(f"static-sbom: bad item {it!r}")
        p.update({"SPDXID": "SPDXRef-Package-" + "".join(c if c.isalnum() or c in ".-" else "-" for c in p["name"]),
                  "filesAnalyzed": False, "licenseConcluded": "NOASSERTION", "copyrightText": "NOASSERTION",
                  "sourceInfo": f"linked statically into {binary}"})
        pkgs.append(p)
    pkgs.sort(key=lambda p: p["name"])
    d = {"spdxVersion": "SPDX-2.3", "dataLicense": "CC0-1.0", "SPDXID": "SPDXRef-DOCUMENT", "name": doc,
         "documentNamespace": f"https://readystack.dev/spdx/{doc}",
         "creationInfo": {"created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(sde))),
                          "creators": ["Tool: readystack static-sbom.py"],
                          "comment": f"The libraries linked statically into {binary}, which no scanner can see in it."},
         "packages": pkgs,
         "relationships": [{"spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES",
                            "relatedSpdxElement": p["SPDXID"]} for p in pkgs]}
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as f:
        json.dump(d, f, indent=1, sort_keys=True)
        f.write("\n")
    os.utime(out, (int(sde), int(sde)))
    print(f"static-sbom: {out}: " + ", ".join(f"{p['name']} {p['versionInfo']}" for p in pkgs))


if __name__ == "__main__":
    main(sys.argv)
