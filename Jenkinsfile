pipeline {
    agent any

    environment {
        IMAGE_NAME = "sheetalkadolkar/login-app"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/SheetalKadolkar/login-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub', url: '']) {
                    sh 'docker push $IMAGE_NAME:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}
