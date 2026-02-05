pipeline {
    agent any

    environment {
        IMAGE_NAME = "sheetalkadolkar/login-app"
        DOCKER_CREDS = "docker-hub-creds"
        KUBE_NAMESPACE = "default"
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
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage("Docker Login & Push") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage("Deploy to Kubernetes") {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                      export KUBECONFIG=$KUBECONFIG
                      kubectl get nodes

                      kubectl apply -f k8s/mysql-deployment.yaml
                      kubectl apply -f k8s/mysql-service.yaml
                      kubectl apply -f k8s/app-deployment.yaml
                      kubectl apply -f k8s/app-service.yaml

                      kubectl rollout status deployment/mysql
                      kubectl rollout status deployment/login-app
                    '''
                }
            }
        }
    }
    
}
