pipeline {
    agent any

    environment {
        DOCKER_USER = 'sheetalkadolkar'
        DOCKER_PASS = credentials('docker-hub-creds') // Jenkins credential ID
        IMAGE_NAME = "sheetalkadolkar/login-app:latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/SheetalKadolkar/login-devops.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $IMAGE_NAME'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Use Minikube context
                    sh 'kubectl config use-context minikube'

                    // Apply all Kubernetes manifests
                    sh 'kubectl apply -f k8s/mysql-deployment.yaml'
                    sh 'kubectl apply -f k8s/login-app-deployment.yaml'
                    sh 'kubectl apply -f k8s/login-app-service.yaml'
                }
            }
        }

    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}
