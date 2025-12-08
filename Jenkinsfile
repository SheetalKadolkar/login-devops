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

    stage("Deploy to Kubernetes") {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig-id', variable: 'KUBECONFIG_FILE')]) {
          sh '''
            export KUBECONFIG=$KUBECONFIG_FILE
            kubectl apply -f k8s/mysql-deployment.yaml
            kubectl apply -f k8s/my-sqlservice.yaml
            kubectl apply -f k8s/app-deploymeny.yaml
            kubectl apply -f k8s/app-service.yaml
            kubectl get pods
            kubectl get svc
          '''
        }
      }
    }

  }
}
