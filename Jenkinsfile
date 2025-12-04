pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out the repository...'
                git branch: 'master', url: 'https://github.com/neethuelza/PythonProject3.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                bat """
                cd /d ${WORKSPACE_DIR}
                python -m venv .venv
                call .venv\\Scripts\\activate.bat
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Selenium-Pytest tests with Allure results...'
                timeout(time: 30, unit: 'MINUTES') {
                    bat """
                    cd /d ${WORKSPACE_DIR}
                    call .venv\\Scripts\\activate.bat
                    pytest -v --alluredir=reports/allure-results --browser chrome
                    """
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports/allure-results']],
                    reportBuildPolicy: 'ALWAYS',
                    properties: []
                ])
            }
        }
    }

    post {
        always {
            script {
                // Compose email
                def buildStatus = currentBuild.currentResult
                def emailSubject = buildStatus == 'SUCCESS' ? "\u2705 Build SUCCESS: ${currentBuild.fullDisplayName}" :
                                                               "\u274C Build FAILURE: ${currentBuild.fullDisplayName}"

                def emailBody = buildStatus == 'SUCCESS' ?
                    """<p>Hi Neethu,</p>
                       <p>The Jenkins build <b>${currentBuild.fullDisplayName}</b> succeeded.</p>
                       <p>View the Allure report online: <a href='${BUILD_URL}allure'>Allure Report</a></p>""" :
                    """<p>Hi Neethu,</p>
                       <p>The Jenkins build <b>${currentBuild.fullDisplayName}</b> failed.</p>
                       <p>Check console output here: <a href='${BUILD_URL}console'>Console Output</a></p>"""

                // Email sending
                emailext(
                    subject: emailSubject,
                    body: emailBody,
                    to: "neethuelzageorge@gmail.com",
                    mimeType: 'text/html'
                )
            }

            // Clean workspace
            cleanWs()
        }
    }
}
