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
                  withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', 
                  usernameVariable: 'DOCKER_USER', 
                  passwordVariable: 'DOCKER_PASS')]) {
                  sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                  sh 'docker push sheetalkadolkar/login-app:latest'
}
    }
}


        stage("Push Image to DockerHub") {
            steps {
                sh "docker push $IMAGE_NAME:latest"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                kubernetesDeploy(configs: 'k8s/deployment.yaml', kubeconfigId: 'kube-config-id')

    }
}

}

}
