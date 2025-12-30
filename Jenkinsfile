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
                withCredentials([string(credentialsId: 'kube-token', variable: 'KUBE_TOKEN')]) {
                    sh '''
                      kubectl config set-credentials jenkins --token=$KUBE_TOKEN
                      kubectl config set-context jenkins --cluster=minikube --user=jenkins
                      kubectl config use-context jenkins

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
