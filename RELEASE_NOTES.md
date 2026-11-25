# pause 3.10.2 — ReadyStack release `3.10.2-CE-scratch-r1`

Generated 2026-10-29 from this release's build records and strategy. Statements that come from a single record name it in brackets; the others come from this release's strategy and build log.

## Release

- **Image:** `readystack/pause:3.10.2-CE-scratch-r1` (linux/amd64). Index digest `sha256:205b1d99aed2a00e741d04e7a9dede1ee8eca72e392088e3e2c0d1d0cf649253` [`docs/provenance/LOCKED_DIGEST.txt`].
- **Image manifest digest:** `sha256:6b74cfa71db2c51e1a21e3342402d3993573ea02a0c85063897eda87958dca26` [`TARGET_DIGEST.txt`].
- **Upstream:** pause 3.10.2 built from source at `v1.36.6` of https://github.com/kubernetes/kubernetes — upstream notes: https://github.com/kubernetes/kubernetes/releases/tag/v1.36.6 [`docs/provenance/BUILD_RECIPE.json`].
- **Base image:** `scratch`; runtime user `65535:65535`.
- **Build:** `source-rebuild-c`, compiled offline with `--network=none`.

## What changed in this release

- First ReadyStack release of pause 3.10.2.
- First release of pause 3.10.2 (Kubernetes VM Stack Kits).

## Security status at release (measured 2026-10-29)

- **Docker Scout:** 0 fixable critical/high vulnerabilities; runs as `65535:65535` (non-root); SBOM + provenance attestations present (SPDX SBOM + SLSA v1) [`docs/provenance/SCOUT_VERDICT.json`].
- **OSV cross-check:** no fixable critical/high vulnerability beyond Docker Scout's findings.
- **Signature:** cosign signature verified by ReadyStack's release gate before publishing; check it yourself with `cosign verify --key https://readystack.dev/keys/cosign.pub readystack/pause:3.10.2-CE-scratch-r1` (signatures are recorded in the public Sigstore transparency log).
- **ReadyStack release check at release:** passed (ReadyStack's own test, not a Docker Scout grade). Vulnerabilities are disclosed every day and the image never changes, so it is re-checked daily, beside Docker Scout's own dated grade, at https://readystack.dev/queue.
- **Before exposing this service:** The image's default user is 65535 and pause opens nothing; the Pod spec can set another user for the sandbox (the stack's four control-plane static pods run theirs as uid 0).
- **Before exposing this service:** /pause is linked statically: it carries code from GNU libc and libgcc, from the builder's Debian 12 packages libc6-dev and libgcc-12-dev. No scanner can see code inside a binary, so the image declares both, at their exact versions, in /usr/local/share/readystack/sbom/pause.spdx.json, where Docker Scout, grype and the OSV cross-check match them. A fix in either reaches this image only through a rebuild on a builder that carries it.

## Reproducibility

Rebuilds offline from this archive to the identical image digest `sha256:6b74cfa71db2c51e1a21e3342402d3993573ea02a0c85063897eda87958dca26`: run `./BUILD_OFFLINE.sh`, then `./VERIFY_OFFLINE.sh` (add `--online` to confirm the Docker Hub tag holds the same digest). Before publishing, ReadyStack rebuilt the kit with `./BUILD_OFFLINE.sh` and compared the result with the published digest [`docs/provenance/REPRO_VERIFICATION.json`], then ran `./BUILD_OFFLINE.sh` and `./VERIFY_OFFLINE.sh` from this archive (without `--online`).

## Validation

- 4 of 4 runbook checks passed (4 authored) on the stack's 3-node integration cluster, recorded 2026-10-29T02:34:55Z [`docs/validation/test-results.json`, from the run's record `docs/stack/RUNBOOK_EVIDENCE.json`]. They are the checks of the stack's operator runbook that name this component; no container of this image was started on its own for them. The record does not show this release's image (`sha256:6b74cfa71db2c51e1a21e3342402d3993573ea02a0c85063897eda87958dca26`) in that run: it lists the component's images as they were then, an earlier build or a tag, so the checks describe the component, not this digest.
- Failed cases are listed in `docs/validation/FAILED_TESTS.md`.

## Known issues

- **medium** (ReadyStack package): The image's licences label omits LGPL-2.1-or-later: /pause links the GNU C Library statically [`RSD-pause-2b72da4dde`]
- **low** (ReadyStack package): REBUILD.md: The sentence says pause runs only inside a cluster. [`RSD-pause-f3910b3db4`]

## Defects fixed

- 1 problem found before release and fixed before it shipped (1 by review); each is listed in `docs/defects/defects.json`.

## Verify this archive

```
sha256sum -c CHECKSUMS.sha256
./BUILD_OFFLINE.sh && ./VERIFY_OFFLINE.sh --online
cosign verify --key https://readystack.dev/keys/cosign.pub readystack/pause:3.10.2-CE-scratch-r1
```

ReadyStack records every signature in the public Sigstore transparency log (Rekor), so the command needs no extra flags.

