#!/usr/bin/env bash
# Step-by-step demo. Press Enter between steps.
set -e

step() { echo; echo "=== $1 ==="; read -r -p "Press Enter to run..."; }

step "1. Build the image"
docker build -t ml-service:latest .

step "2. Run the container"
docker rm -f ml-service 2>/dev/null || true
docker run -d --name ml-service --restart unless-stopped -p 8000:8000 ml-service:latest

step "3. Check it is running"
docker ps --filter name=ml-service
sleep 4
curl -s http://localhost:8000/health; echo

step "4. Make a prediction"
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
echo

step "5. Read the logs"
docker logs --tail 10 ml-service

step "6. Check resource usage"
docker stats --no-stream ml-service

step "7. Stop the service and bring it back"
docker stop ml-service
docker ps -a --filter name=ml-service
docker start ml-service
sleep 3
curl -s http://localhost:8000/health; echo
