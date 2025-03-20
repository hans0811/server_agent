pipeline {
    agent any

    environment {
        IMAGE_NAME = "chaimarket0811/serverflask"
        CONTAINER_NAME = "serverflask"
        DOCKER_REGISTRY_CREDENTIALS = "docker-hub-credentials"  // Set this in Jenkins credentials
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        stage('Print Branch & Generate Version') {
            steps {
                script {
                    def branch = sh(script: "git rev-parse --abbrev-ref HEAD", returnStdout: true).trim()
                    def commitHash = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    def buildNumber = env.BUILD_NUMBER  // Jenkins build number
                    
                    env.IMAGE_TAG = "${branch}-${buildNumber}-${commitHash}"  // Example: main-23-a1b2c3d
                    echo "Current Git Branch: ${branch}"
                    echo "Docker Image Tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Test Docker') {
            steps {
                sh 'docker images'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${env.IMAGE_TAG} -f server/Dockerfile server/"
                    sh "docker tag ${IMAGE_NAME}:${env.IMAGE_TAG} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh "docker run -d --name ${CONTAINER_NAME} ${IMAGE_NAME}:${env.IMAGE_TAG}"

                    sleep 5
                    def containerStatus = sh(script: "docker ps --filter 'name=${CONTAINER_NAME}' --format '{{.Names}}'", returnStdout: true).trim()
                    if (containerStatus != "${CONTAINER_NAME}") {
                        error "Container failed to start!"
                    }

                    echo "Container ${CONTAINER_NAME} is running successfully."
                }
            }
        }

        stage('Run Pytest') {
            steps {
                script {
                    def testResult = sh(script: "docker exec ${CONTAINER_NAME} pytest", returnStatus: true)
                    if (testResult != 0) {
                        error "Tests failed, stopping pipeline"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                        sh "docker push ${IMAGE_NAME}:${env.IMAGE_TAG}"
                        sh "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker rm ${CONTAINER_NAME} || true"
        }
    }
}