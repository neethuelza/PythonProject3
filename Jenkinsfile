pipeline {
    agent {
        docker {
            image 'selenium/standalone-chrome:latest'
            args '-v ${WORKSPACE}:/workspace'
        }
    }

    environment {
        VENV = "${WORKSPACE}/venv"
        ALLURE_RESULTS = "${WORKSPACE}/allure-results"
        ALLURE_REPORT = "${WORKSPACE}/allure-report"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from Git...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh 'python -m venv ${VENV}'
                sh '${VENV}/bin/pip install --upgrade pip'
                sh '${VENV}/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Selenium tests with Pytest inside Docker...'
                sh '${VENV}/bin/pytest tests/TEST.py --alluredir=${ALLURE_RESULTS} --browser=chrome'
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report...'
                sh 'allure generate ${ALLURE_RESULTS} -o ${ALLURE_REPORT} --clean'
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }

        stage('Archive Screenshots') {
            steps {
                echo 'Archiving failure screenshots...'
                archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
            }
        }

        stage('Notifications') {
            steps {
                echo 'Sending notifications...'
                // Slack or email notifications can be added here
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace...'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
