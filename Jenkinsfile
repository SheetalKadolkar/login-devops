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

    stage("Build Docker Image") {
      steps {
        sh "docker build -t $IMAGE_NAME:latest ."
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

    stage('Deploy to Kubernetes') {
        steps {
        withCredentials([string(credentialsId: 'kube-token', variable: 'K8S_TOKEN')]) {
            sh """
            kubectl config set-cluster minikube --server=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}') --insecure-skip-tls-verify=true
            kubectl config set-credentials jenkins --token=$K8S_TOKEN
            kubectl config set-context jenkins --cluster=minikube --user=jenkins
            kubectl config use-context jenkins

            kubectl apply -f k8s/mysql-deployment.yaml
            kubectl apply -f k8s/app-deployment.yaml
            """
        }
    }
}

  }
}
