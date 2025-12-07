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
                   credentialsId: 'docker-hub-creds',   // use the actual credentials ID in Jenkins
                   usernameVariable: 'DOCKER_USER',     // define a variable to hold the username
                   passwordVariable: 'DOCKER_PASS'      // define a variable to hold the password
        )]) {
                 sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
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
