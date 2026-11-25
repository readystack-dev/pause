# =====================================================================
# pause 3.10.2 L-009 HERMETIC OFFLINE BUILD — the canonical, attestation-producing build. build_kit runs
#   docker buildx build --builder readystack-builder-max --network=none
#     --attest type=provenance,mode=max --attest type=sbom --push <context>
# Pinned-public-base + vendored model: golang 1.26.10-bookworm (its gcc 12.2, Debian bookworm) pinned BY DIGEST
# (BASE_IMAGE_DIGESTS.lock) compiles; vendored/pause-src is build/pause/ of kubernetes v1.36.6. The image is FROM scratch.
# Dockerfile and Dockerfile.offline are byte copies of this file (the repo-wide convention).
#
# SHAPE (upstream build/pause/Dockerfile + Makefile at v1.36.6): FROM scratch, the static /pause, compiled from
# linux/pause.c with the Makefile's CFLAGS (-Os -Wall -Werror -static -DVERSION=v$(TAG)-$(REV), TAG ?= 3.10.2) and
# stripped as the Makefile strips it; USER 65535:65535 and ENTRYPOINT ["/pause"] as upstream. REV is empty, as in
# upstream's published build: registry.k8s.io/pause:3.10.2 (sha256:f548e0e8e3dc1896ca956272154dde3314e8cc4fde0a57577ee9fa1c63f5baf4)
# answers `/pause -v` with "pause.c v3.10.2-" (measured 2026-10-28), and so does this one.
# =====================================================================
FROM golang:1.26.10-bookworm@sha256:632dff7351799a5a9954a48dc06670ade72ee44e8c351cdc0e5a57af2fea21af AS build
ARG SOURCE_DATE_EPOCH=1793102572
WORKDIR /src
COPY vendored/pause-src/ .
COPY static-sbom.py /usr/local/bin/static-sbom.py
# TAG is read from build/pause/Makefile and must be 3.10.2 (the pin manifest's pause, kubeadm v1.36.6's PauseVersion);
# the binary must then report exactly pause.c v$(TAG)-. gcc -static copies glibc (libc6-dev's libc.a) and libgcc
# (libgcc-12-dev) into it, which no scanner can see in a binary: static-sbom.py declares both, at the builder's exact
# package versions, in an SPDX document the image ships under /usr/local/share/readystack/sbom/ (owner rule 2026-10-28:
# make linked code visible; chain 781 found the image read as 0 packages).
RUN T=$(sed -n 's/^TAG ?= //p' build/pause/Makefile) && [ "$T" = 3.10.2 ] && \
    gcc --version | head -n1 && mkdir -p /out && \
    gcc -Os -Wall -Werror -static "-DVERSION=v$T-" -o /out/pause build/pause/linux/pause.c && \
    strip /out/pause && [ "$(/out/pause -v)" = "pause.c v$T-" ] && \
    python3 /usr/local/bin/static-sbom.py /out/sbom/pause.spdx.json "pause-$T-static-links" /pause \
      deb:libc6-dev deb:libgcc-12-dev

FROM scratch
# Reproducibility: the build reads SOURCE_DATE_EPOCH (BuildKit's rewrite-timestamp clamps the layer's mtimes to it).
# ARG, never ENV: an ENV would persist into the image config and change the digest. No dpkg or apt runs in this image
# and no user is created (65535 is upstream's numeric user, with no passwd entry), so there are no package logs, no
# /var/cache/ldconfig/aux-cache and no /etc/shadow to freeze: the files are /pause and the SPDX document that declares
# what it links statically.
ARG SOURCE_DATE_EPOCH=1793102572
COPY --from=build /out/pause /pause
COPY --from=build /out/sbom/ /usr/local/share/readystack/sbom/
USER 65535:65535
ENTRYPOINT ["/pause"]
# >>> readystack OCI labels: strategies/pause.json image_labels plus the standard OCI labels,
# the set a generated kit carries (gen_dockerfile.label_lines). Written by scripts/kit_migrations.py;
# scripts/retarget.py re-renders it with every retarget. Never edit it by hand.
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.title="pause"
LABEL org.opencontainers.image.description="pause 3.10.2 built from Kubernetes v1.36.6's pause.c: the static sandbox (infra) container every Pod starts first, user 65535:65535 as upstream."
LABEL org.opencontainers.image.source="https://github.com/kubernetes/kubernetes"
LABEL org.opencontainers.image.version="3.10.2-CE-scratch-r1"
LABEL org.opencontainers.image.revision="1b2171b110bb2a2542e1322035c6583ec86eb976"
# <<< readystack OCI labels
