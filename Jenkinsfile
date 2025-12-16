pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        KUBECONFIG = '/var/lib/jenkins/.kube/config'  // استخدم kubeconfig الخاص بالـ Jenkins
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo 'Checking out source code...'
                checkout scm
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
                script {
                    // تعريف الخدمات اللي هنعمل لها save و import
                    def services = ['auth-service', 'todo-service', 'alarm-service', 'todo-frontend']

                    for (svc in services) {
                        def image = "todo-k3s-pipeline-${svc}:latest"
                        def tarFile = "${svc}.tar"

                        echo "Saving Docker image: ${image} -> ${tarFile}"
                        sh "docker save ${image} -o ${tarFile}"

                        echo "Importing ${tarFile} into k3s containerd..."
                        sh "sudo k3s ctr -n k8s.io images import ${tarFile}"
                    }
                }
            }
        }

        stage('Deploy to k3s') {
            steps {
                echo 'Applying Kubernetes manifests...'
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/secret.yaml
                    kubectl apply -f k8s/configmap.yaml
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
