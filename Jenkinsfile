pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
        VENV_PATH = "C:\\Users\\neeth\\PycharmProjects\\SAMPLEFRAMEWORK\\.venv\\Scripts\\activate.bat"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'master', url: 'https://github.com/neethuelza/PythonProject3.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat """
                    cd /d ${WORKSPACE_DIR}
                    call ${VENV_PATH}
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
                        call ${VENV_PATH}
                        pytest -v --alluredir=reports/allure-results --browser chrome
                    """
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                echo 'Generating Allure report (even if tests fail)...'
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        results: [[path: 'reports/allure-results']],
                        reportBuildPolicy: 'ALWAYS',
                        installation: 'Allure'  // Make sure this matches the Allure installation name in Jenkins
                    ])
                }
            }
        }
    }

    post {
        always {
            script {
                def buildStatus = currentBuild.currentResult
                def emailSubject = buildStatus == 'SUCCESS' ? "\u2705 Build SUCCESS: ${currentBuild.fullDisplayName}" :
                                                               "\u274C Build FAILURE: ${currentBuild.fullDisplayName}"

                def emailBody = buildStatus == 'SUCCESS' ?
                    """<p>Hi Neethu,</p>
                       <p>The Jenkins build <b>${currentBuild.fullDisplayName}</b> succeeded.</p>
                       <p>View the Allure report online: <a href='${BUILD_URL}allure'>Allure Report</a></p>""" :
                    """<p>Hi Neethu,</p>
                       <p>The Jenkins build <b>${currentBuild.fullDisplayName}</b> failed.</p>
                       <p>Check console output here: <a href='${BUILD_URL}console'>Console Output</a></p>
                       <p>View Allure report (if any): <a href='${BUILD_URL}allure'>Allure Report</a></p>"""

                emailext(
                    subject: emailSubject,
                    body: emailBody,
                    to: "neethuelzageorge@gmail.com",
                    mimeType: 'text/html'
                )
            }

            cleanWs() // Clean workspace after all actions
        }
    }
}
