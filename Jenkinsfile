pipeline {
    agent any

    environment {
        IMAGE = "ml-service"
        TAG   = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install and Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    pytest -q
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE:$TAG -t $IMAGE:latest .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f ml-service || true
                    docker run -d --name ml-service \
                      --restart unless-stopped \
                      -p 8000:8000 $IMAGE:latest
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    sleep 5
                    curl --fail http://localhost:8000/health
                '''
            }
        }
    }

    post {
        failure { echo 'Pipeline failed. Check the stage logs above.' }
        success { echo "Deployed ${IMAGE}:${TAG}" }
    }
}
