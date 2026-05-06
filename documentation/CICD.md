# CI/CD Procedure

This project uses GitHub Actions and Docker Compose to deploy the stack automatically.

The CI/CD setup has two main parts:

1. GitHub Actions builds and publishes the custom Docker image.
2. A self-hosted runner on the VM pulls the newest version and redeploys the Docker Compose stack.

## GitHub Actions Workflow

The workflow is stored in:

```text
.github/workflows/docker-publish.yml
```

The workflow runs automatically when changes are pushed to the `main` branch.

The first job, `build-and-push`, runs on a GitHub-hosted Ubuntu runner. It checks out the repository, logs in to GitHub Container Registry, builds the custom `sensors` Docker image, and pushes it to GHCR.

The image is published as:

```text
ghcr.io/jschacht06/opdracht-switching-routing-sensors:latest
```

A second tag is also created with the commit SHA. This makes it possible to identify exactly which commit created a specific image.

## Deployment Runner

The second job, `deploy`, runs on a self-hosted runner.

The self-hosted runner is installed on the deployment VM. This means the VM connects to GitHub and waits for deployment jobs. GitHub does not need to SSH into the VM.

The deploy job performs these steps:

1. Go to the project folder on the VM.
2. Update the local repository from GitHub.
3. Run `deploy.sh`.

The VM must have:

- Docker installed
- Docker Compose installed
- the GitHub self-hosted runner running
- permission for the runner user to use Docker
- the project cloned locally
- a local `.env` file with the required secrets

The `.env` file stays on the VM and should not be committed to GitHub.

## Docker Compose

The `sensors` service uses the image built by GitHub Actions:

```yaml
sensors:
  image: ghcr.io/jschacht06/opdracht-switching-routing-sensors:latest
```

This means the VM does not build the `sensors` image itself. Instead, it pulls the already-built image from GitHub Container Registry.

The other services use public Docker images, such as Mosquitto, Node-RED, InfluxDB, and Portainer.

## Deployment Script

The deployment script is:

```text
deploy.sh
```

The script stops the current stack, removes the local InfluxDB data and config folders, pulls the newest Docker images, and starts the stack again.

The InfluxDB folders are deleted on every deployment:

```text
./influxdb/data
./influxdb/config
```

This makes sure InfluxDB starts from a clean state after deployment.

The script then runs:

```bash
docker compose pull
docker compose up -d --remove-orphans
docker image prune -f
docker compose ps
```

## Deployment Flow

The complete deployment flow is:

1. Code is pushed to the `main` branch.
2. GitHub Actions starts the workflow.
3. The `sensors` Docker image is built.
4. The image is pushed to GitHub Container Registry.
5. The self-hosted runner on the VM starts the deploy job.
6. The VM updates its local repository.
7. The VM runs `deploy.sh`.
8. Docker Compose pulls the newest images and restarts the containers.

## Manual Redeploy

A manual redeploy can still be done on the VM with:

```bash
cd ~/opdracht-switching-routing
bash deploy.sh
```

If the repository path is different on the VM, use the correct local project path.

## Notes

If the GitHub Actions deploy job stays on `Waiting for a runner to pick up this job`, the self-hosted runner is not online.

If Docker gives a permission error, the runner user probably does not have permission to access Docker. The runner user should be added to the Docker group.

If the GHCR image is private, the VM must be logged in to GitHub Container Registry. For this project, making the package public is the simplest option.
