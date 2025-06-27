# financialwork

## Local setup with Nginx and HTTPS

1. Generate a self‑signed certificate:

```bash
./nginx/generate-self-signed.sh
```

2. Start the services:

```bash
docker compose up --build
```

Nginx will expose HTTPS on port 443 and proxy requests to the frontend and backend containers. You can use tools like `ngrok` on port 443 to expose the application publicly.

The Telegram login widget requires HTTPS, so using this setup allows it to work correctly with a self-signed certificate during development.
