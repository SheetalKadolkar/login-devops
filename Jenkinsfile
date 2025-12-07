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

        stage('Login to DockerHub') {
                  withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', 
                  usernameVariable: 'DOCKER_USER', 
                  passwordVariable: 'DOCKER_PASS')]) {
                 sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
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
