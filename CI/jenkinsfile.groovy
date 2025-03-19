pipeline {
    agent any

    stages {
        stage('Git Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Print Branch') {
            steps {
                script {
                    echo "Branch: ${env.GIT_BRANCH}"
                }
            }
        }
        stage('Build') {
            steps {
                echo 'Build ...'
            }
        }
        stage('Upload to S3') {
            steps {
                echo 'Upload ...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploy ...'
            }
        }
    }
}
