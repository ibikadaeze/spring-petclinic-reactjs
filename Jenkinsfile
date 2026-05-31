pipeline {
    agent any

    tools {
        nodejs 'NodeJS 20'
    }

    environment {
        FRONTEND_HOST = '192.168.56.11'
        FRONTEND_USER = 'vagrant'
        FRONTEND_URL = 'http://192.168.56.11/'
        BACKEND_HEALTH_URL = 'http://192.168.56.12:9966/petclinic/actuator/health'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'scripts/build_frontend.sh'
            }
        }

        stage('Archive Frontend') {
            steps {
                archiveArtifacts artifacts: 'client/build/**', fingerprint: true, allowEmptyArchive: true
            }
        }

        stage('Deploy Frontend') {
            steps {
                sh 'scripts/deploy_frontend.sh'
            }
        }

        stage('Smoke Test Frontend') {
            steps {
                sh 'scripts/smoke_frontend.sh'
            }
        }

        stage('Selenium E2E Test') {
            steps {
                sh 'scripts/selenium_frontend.sh'
            }
        }
    }
}
