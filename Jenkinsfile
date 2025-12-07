pipeline {
    agent any

    environment {
        IMAGE_NAME = "sheetalkadolkar/login-app"
        DOCKER_CREDS = "docker-hub-creds"
        KUBE_CONFIG = "C:/Users/Sheetal/.kube/config"
    }

    stages {

        stage("Clone Code") {
            steps {
                git branch: 'main',
                    url: 'https://github.com/SheetalKadolkar/login-devops.git'
            }
        }

        stage("Build Docker Image") {
            steps {
                sh "docker build -t $IMAGE_NAME:latest ."
            }
        }

        stage("Login to DockerHub") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "$DOCKER_CREDS",
                    usernameVariable: 'sheetalkadolkar',
                    passwordVariable: 'DeleteCopy@2'
                )]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                }
            }
        }

        stage("Push Image to DockerHub") {
            steps {
                sh "docker push $IMAGE_NAME:latest"
            }
        }

        stage("Deploy to Kubernetes") {
            steps {
                sh "kubectl apply -f k8s/"
                sh "kubectl rollout restart deployment login-app"
            }
        }
    }
}
