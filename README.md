# pause: ReadyStack build kit

The offline build kit for the Docker image `readystack/pause:3.10.2-CE-scratch-r1`. It holds what the image is built from (upstream source, base images, toolchain, pinned dependencies) and the documents, so the image can be rebuilt with no network access (`docker build --network=none`).

- Release: [3.10.2-CE-scratch-r1](https://github.com/readystack-dev/pause/releases/tag/3.10.2-CE-scratch-r1)
- Image: [`docker.io/readystack/pause:3.10.2-CE-scratch-r1`](https://hub.docker.com/r/readystack/pause/tags), manifest digest `sha256:6b74cfa71db2c51e1a21e3342402d3993573ea02a0c85063897eda87958dca26`
- Product page: https://readystack.dev/products/pause
- Defects: this repository's Issues (defects recorded from 25 November 2026 on) and https://readystack.dev/defects.html?product=pause

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
