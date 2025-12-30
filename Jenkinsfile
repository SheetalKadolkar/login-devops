pipeline {
    agent any

    environment {
        IMAGE_NAME = "sheetalkadolkar/login-app"
        DOCKER_CREDS = "docker-hub-creds"
    }

    stages {

        stage("Clone Code") {
            steps {
                git branch: 'main',
                    url: 'https://github.com/SheetalKadolkar/login-devops.git'
            }
        }

        stage("Docker Check") {
            steps {
                sh 'docker --version'
            }
        }

        stage("Build Docker Image") {
            steps {
                sh 'docker build -t sheetalkadolkar/login-app:latest .'
            }
        }

        stage("Login & Push to DockerHub") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                      echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                      docker push sheetalkadolkar/login-app:latest
                    '''
                }
            }
        }

        stage("Deploy to Kubernetes") {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                      kubectl get nodes
                      kubectl apply -f k8s/mysql-deployment.yaml
                      kubectl apply -f k8s/mysql-service.yaml
                      kubectl apply -f k8s/app-deployment.yaml
                      kubectl apply -f k8s/app-service.yaml
                     '''
        }
    }
}

    }
}
