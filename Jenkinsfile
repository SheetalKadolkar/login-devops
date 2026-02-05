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

        stage("Docker Check") {
            steps {
                sh 'docker --version'
            }
        }

        stage("Build Docker Image") {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
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
                        docker push ${IMAGE_NAME}
                    '''
                }
            }
        }

        stage("Deploy to Kubernetes") {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                        
                        kubectl get nodes

                        kubectl apply -f k8s/mysql-deployment.yaml -n ${KUBE_NAMESPACE}
                        kubectl apply -f k8s/mysql-service.yaml -n ${KUBE_NAMESPACE}

                        kubectl apply -f k8s/app-deployment.yaml -n ${KUBE_NAMESPACE}
                        kubectl apply -f k8s/app-service.yaml -n ${KUBE_NAMESPACE}

                        kubectl rollout status deployment/mysql -n ${KUBE_NAMESPACE}
                        kubectl rollout status deployment/login-app -n ${KUBE_NAMESPACE}
                    '''
                }
            }
        }

    }

   }
