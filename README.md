# The Human Canon

A dependency-free, self-hosted reading checklist of 47 influential works. Norwegian descriptions, English titles, suggested reading order and persistent shared progress.

## Quick start

```sh
git clone https://github.com/drian/The-human-canon.git
cd The-human-canon
docker compose up -d --build
```

Open http://localhost:8080. The default published port is loopback-only. For Docker-based Traefik, connect the service to your existing proxy network and route to container port 8080; remove the ports mapping if unnecessary. For Coolify, deploy the Dockerfile with port 8080 and mount a persistent volume at /data.

## Storage and security

Progress is stored in SQLite at /data/canon.db. Back up the named volume with the container stopped. Do not run docker compose down -v unless you intend to delete progress.

This is a single shared checklist with no built-in login. Keep it on a trusted network or protect it with reverse proxy authentication. Do not expose it to the public internet without access control.

## Reading list

Book links search Open Library and Project Gutenberg; author links search Wikipedia. Availability varies. Reading order is editorial, not a definitive ranking. Keep IDs stable when editing books.json.

MIT licensed.
