pipeline {
    agent any

    environment {
        IMAGE_NAME = "sheetalkadolkar/login-app"
        DOCKER_CREDS = "docker-hub-creds"
        KUBE_NAMESPACE = "default"
        TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Clean Workspace") {
            steps {
                sh "rm -rf * || true"
                checkout scm
            }
        }

        stage("Build Docker Image") {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${TAG} ."
                sh "docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_NAME}:latest"
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
                        docker push ${IMAGE_NAME}:${TAG}
                        docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage("Deploy to Kubernetes") {
            steps {
               sh '''
                 aws eks update-kubeconfig --region us-east-1 --name my-eks-cluster

                 kubectl get nodes
                 kubectl apply -f k8s/

                 kubectl rollout status deployment/mysql
                 kubectl rollout status deployment/login-app
        '''
    }
}

    }

    post {
        always {
            echo "Build Completed"
        }
        success {
            echo "Deployment Successful"
        }
        failure {
            echo "Build Failed — Check Logs"
        }
    }
}
