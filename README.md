# The Human Canon

A personal reading checklist for anyone curious about the ideas and stories that shaped human history. Explore 47 influential works spanning ancient epics, literature, philosophy, political thought and science.

The suggested reading order starts with approachable works and gradually introduces more demanding texts. It is an editorial starting point, not a universal ranking or endorsement of the books' ideas. The initial selection is predominantly Western, with some ancient Near Eastern and Chinese works.

## Features

- Responsive English interface with search, category and reading-status filters.
- Unread, reading and completed states, with an overall progress indicator.
- Short book descriptions, approximate publication dates and selected translation recommendations.
- Links to edition searches in Open Library and Project Gutenberg, and author biographies on Wikipedia.
- Server-side SQLite persistence. Use the same checklist across your devices.
- No external database, API keys, JavaScript framework or build dependencies.

## Self-hosting

Requires Docker with the Compose plugin.

```sh
git clone https://github.com/drian/The-human-canon.git
cd The-human-canon
docker compose up -d --build
```

Open http://localhost:8080 on the Docker host. The default Compose port is bound to loopback for safety. For access from another computer on a trusted LAN, change the host mapping to "8080:8080" and configure your firewall appropriately.

### Reverse proxy (optional)

Any HTTP reverse proxy can route to the application on container port 8080. For a proxy on the host, use http://127.0.0.1:8080. For a containerized proxy, connect both services to a shared Docker network.

For example, with an existing external Docker network named traefik, create a compose.override.yaml:

```yaml
services:
  canon:
    networks:
      - traefik
    labels:
      traefik.enable: "true"
      traefik.docker.network: traefik
      traefik.http.routers.canon.rule: "Host(\`canon.example.com\`)"
      traefik.http.services.canon.loadbalancer.server.port: "8080"
networks:
  traefik:
    external: true
```

Replace the hostname and network name with your own. Configure your TLS entrypoint, certificate resolver and authentication middleware according to your proxy setup. No proxy is included or required.

### Updating

```sh
git pull
docker compose up -d --build
```

The named data volume survives rebuilds.

## Data and security

The app is designed for a single person or trusted household. Everyone with access shares the same reading progress. There are no accounts or built-in authentication. Protect remote access with VPN or reverse proxy authentication; do not expose an unprotected instance publicly.

Progress is stored in SQLite at /data/canon.db in the canon-data Docker volume. Back up the volume with the container stopped for a consistent snapshot. Running docker compose down -v deletes that volume and your progress.

The catalog lives in books.json. Keep existing numeric IDs stable when editing it; IDs identify saved progress and currently also determine the displayed recommended rank. Append new entries with unique IDs. Rebuild the container after changes.

External links are searches, not guarantees that a particular edition is available or free in your jurisdiction. No book text is redistributed by this project.

## License

MIT. See LICENSE.
