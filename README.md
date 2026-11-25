# pause: ReadyStack build kit

The offline build kit for the Docker image `readystack/pause:3.10.2-CE-scratch-r1`. It holds what the image is built from (upstream source, base images, toolchain, pinned dependencies) and the documents, so the image can be rebuilt with no network access (`docker build --network=none`).

- Release: [3.10.2-CE-scratch-r1](https://github.com/readystack-dev/pause/releases/tag/3.10.2-CE-scratch-r1)
- Image: [`docker.io/readystack/pause:3.10.2-CE-scratch-r1`](https://hub.docker.com/r/readystack/pause/tags), manifest digest `sha256:6b74cfa71db2c51e1a21e3342402d3993573ea02a0c85063897eda87958dca26`
- Product page: https://readystack.dev/products/pause
- Source and build recipe: https://readystack.dev/products/pause/recipe
- Build trail: https://readystack.dev/products/pause/trail/3.10.2-CE-scratch-r1
- Defects: this repository's Issues (defects recorded from 25 November 2026 on) and https://readystack.dev/defects.html?product=pause

## The image

Not started by hand: containerd's CRI plugin starts it for every Pod (sandbox_image in /etc/containerd/config.toml). In the Kubernetes VM Stack it is mirrored into the local registry as <LOCAL_REGISTRY>/pause:3.10.2, the name kubeadm v1.36.6 expects (kubeadm config images list).

## Who uses pause and why

Kubernetes cluster administrators. It is not normally run by hand: the container runtime starts it for every pod.

The pause container is the infrastructure container of a pod. It starts first and keeps the pod's namespaces alive, so the pod's other containers can crash or restart without losing the pod's network setup.

A typical use: When a web pod's application container crashes and restarts, the pod keeps its IP address and network configuration, because the pause container still holds them. Administrators meet it mostly in the container runtime's settings, where its image is named as the sandbox image.

From the upstream project's own description: https://github.com/kubernetes/kubernetes/blob/master/build/pause/linux/pause.c, https://kubernetes.io/docs/concepts/windows/intro/, https://kubernetes.io/docs/setup/production-environment/container-runtimes/.

## This release

- Docker Scout policy grade at release: **A** (100%), graded 2026-10-29 with `docker scout policy` (CLI 1.26.0, docker-default configuration).
- Signed with ReadyStack's release key (fingerprint `04daa92344a52dbc`): https://readystack.dev/keys/cosign.pub.
- Runs as a non-root user (`65535:65535`).
- Attestations on the image: an SPDX SBOM and SLSA provenance v1.
- Rebuilt from this kit with network egress blocked on 2026-10-29; the rebuilt image digest is the published one.
- Base: scratch.

The current grade, measured again every day, is on https://readystack.dev/products/pause.

pause is distributed under its upstream licence (Apache-2.0 AND LGPL-2.1-or-later); the kit contains upstream's source under that licence, and each vendored component under its own.

## Download

From the [3.10.2-CE-scratch-r1 release](https://github.com/readystack-dev/pause/releases/tag/3.10.2-CE-scratch-r1): `ReadyStack-pause-3.10.2-CE-scratch-r1.tar.gz` (426.5 MB), SHA-256 `021b80ad6deb979b0586e7b3577582f174f400206f5d2a83f82a1857a10706e5`.

```sh
sha256sum --check --ignore-missing SHA256SUMS
```

## Verify and rebuild

The rebuild statement is signed with the ReadyStack release key. Check the signature before you rely on it:

```sh
cosign verify-blob --key https://readystack.dev/keys/cosign.pub \
  --bundle ReadyStack-pause-3.10.2-CE-scratch-r1.rebuild.json.sigstore ReadyStack-pause-3.10.2-CE-scratch-r1.rebuild.json
```

Unpack with `-p` so file modes are kept, then follow the kit's own README.md and docs/REBUILD.md:

```sh
tar -xpzf ReadyStack-pause-3.10.2-CE-scratch-r1.tar.gz
cd 3.10.2-CE-scratch-r1
less README.md docs/REBUILD.md
```

The build trail (`ReadyStack-pause-3.10.2-CE-scratch-r1.trail.json`, signed the same way, and its Markdown copy) records how this release was built and checked.

## This repository

`recipe/` holds the kit's recipe files (Dockerfiles, build scripts, pins) as published at https://readystack.dev/products/pause/recipe. The complete kit is the release download. Each release is a tag here.

— ReadyStack · https://readystack.dev
