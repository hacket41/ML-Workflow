# Linux ML Demo

A small end-to-end example for an interview demonstration: a Python ML model served through FastAPI, packaged with Docker, tested and deployed through a CI/CD pipeline, and managed on Linux.

## Project layout

```
linux-ml-demo/
  app/main.py              FastAPI service (health, predict, stats)
  train.py                 Trains an Iris classifier and saves model.joblib
  tests/test_api.py        Automated tests (pytest)
  Dockerfile               Container image definition
  docker-compose.yml       One-command run
  Jenkinsfile              Jenkins pipeline
  .github/workflows/ci.yml GitHub Actions pipeline
  deploy/ml-service.service systemd unit for start-on-boot
  scripts/demo.sh          Step-by-step live demo
```

## 1. Run locally without Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python train.py
pytest -q
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for the interactive API page.

## 2. Run with Docker

```bash
docker build -t ml-service .
docker run -d --name ml-service -p 8000:8000 ml-service
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

Or with Compose:

```bash
docker compose up -d --build
```

## 3. Pipeline

- Jenkins: create a Pipeline job pointing at this repository. The Jenkinsfile runs test, build, deploy and a smoke test. The Jenkins user must be in the `docker` group.
- GitHub Actions: push to GitHub. The workflow in `.github/workflows/ci.yml` runs automatically on push and pull request.

Flow: git push, run tests, build image, start container, smoke test the health endpoint.

## 4. Linux management

Start on boot with systemd:

```bash
sudo cp -r . /opt/linux-ml-demo
sudo cp deploy/ml-service.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ml-service
systemctl status ml-service
journalctl -u ml-service -f
```

Useful checks:

```bash
docker ps                      # running containers
docker logs -f ml-service      # live logs
docker stats --no-stream       # CPU and memory
ss -tulpn | grep 8000          # who is listening on port 8000
htop                           # system resources
df -h && free -h               # disk and memory
sudo ufw allow 8000/tcp        # open the port if a firewall is active
```

## 5. Live demo script

Run `./scripts/demo.sh` and press Enter between steps. It builds the image, runs the container, calls the API, shows logs and resource usage, then stops and restarts the service.

## 6. Talking points

- Why Linux: servers, cloud, containers and GPU tooling are Linux-first.
- Why Docker: the same image runs on any machine, so "works on my machine" problems disappear.
- Why tests in the pipeline: broken code never reaches deployment.
- Why a non-root user in the Dockerfile: least privilege.
- Why a health endpoint: pipelines and monitors can check the service automatically.
- Why a restart policy and systemd: the service recovers from crashes and reboots.
- How to extend: swap the Iris model for your own (for example the Artify EfficientNet classifier), add a reverse proxy such as Nginx, add monitoring with Prometheus.
