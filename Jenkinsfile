pipeline {
    agent any
    environment {
        REPO_URL = 'https://github.com/MohanadHesham98/ToDo.git'
        BRANCH = 'k3s'
        KUBECONFIG = '/home/test/.kube/config' // path for your kubeconfig
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: "${BRANCH}", url: "${REPO_URL}", credentialsId: 'GITHUB_PAT'
            }
        }
        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images using docker-compose...'
                sh 'docker compose build'
            }
        }
        stage('Save & Load Images into k3s') {
            steps {
                echo 'Saving Docker images and loading into k3s...'
                sh '''
                #!/bin/sh
                for SERVICE in auth-service todo-service alarm-service todo-frontend; do
                    IMAGE="todo-k3s-pipeline-${SERVICE}:latest"
                    TAR_FILE="${SERVICE}.tar"
                    echo "Saving $IMAGE to $TAR_FILE..."
                    docker save $IMAGE -o $TAR_FILE
                    echo "Importing $TAR_FILE into k3s..."
                    sudo ctr -n k8s.io images import $TAR_FILE
                done
                '''
            }
        }
        stage('Deploy to k3s') {
            steps {
                echo 'Applying Kubernetes manifests...'
                sh '''
                kubectl apply -f k8s/namespace.yaml
                kubectl apply -f k8s/configmap.yaml
                kubectl apply -f k8s/secret.yaml

                kubectl apply -f k8s/auth-service/
                kubectl apply -f k8s/todo-service/
                kubectl apply -f k8s/alarm-service/
                kubectl apply -f k8s/frontend/
                '''
            }
        }
    }
    post {
        always {
            echo 'Cleaning up tar files...'
            sh 'rm -f *.tar'
        }
    }
}
