# CI/CD Procedure

This project uses a simple deployment script to demonstrate CI/CD principles with Docker Compose.

The script builds the local Docker images, stops the old containers, and starts the updated Docker Compose stack again.

Run this command from the root of the repository:

```bash
./deploy.sh
```

If the script is not executable yet on Linux, run this once:

```bash
chmod +x deploy.sh
```

The script performs these steps:

1. `docker compose build`
2. `docker compose down`
3. `docker compose up -d --remove-orphans`
4. `docker compose ps`

This keeps the deployment process repeatable. Instead of manually remembering multiple Docker Compose commands, the stack can be updated with one command after code or configuration changes.

## Real CI/CD Pipeline

In a real CI/CD pipeline, this script could be executed automatically after changes are pushed to the Git repository.

For example, a GitHub Actions workflow could:

1. Run checks or tests for the repository.
2. Connect to the deployment VM through SSH.
3. Pull the latest version of the repository.
4. Run `./deploy.sh` on the VM.

Secrets such as InfluxDB credentials should stay in the `.env` file on the server and should not be committed to Git.
