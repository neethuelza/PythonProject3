pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
        ALLURE_REPORT = "${WORKSPACE_DIR}\\allure-report"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'master', url: 'https://github.com/neethuelza/PythonProject3.git'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Selenium-Pytest tests directly...'
                timeout(time: 30, unit: 'MINUTES') {
                    bat """
                    cd /d ${WORKSPACE_DIR}
                    echo ================================
                    echo Starting test execution...
                    echo ================================

                    REM Activate virtual environment
                    call C:\\Users\\abyja\\PycharmProjects\\PythonProject3\\.venv\\Scripts\\activate.bat

                    REM Run pytest with Allure results and Chrome browser
                    pytest -v --alluredir=reports/allure-results --browser chrome

                    echo ================================
                    echo Test execution completed.
                    echo ================================
                    """
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report...'
                bat """
                allure generate "${WORKSPACE_DIR}\\reports\\allure-results" -o "${ALLURE_REPORT}" --clean
                """
            }
        }

        stage('Archive Allure Report') {
            steps {
                echo 'Archiving Allure report...'
                archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Sending email and cleaning workspace...'
            script {
                def attachmentPattern = fileExists("${ALLURE_REPORT}") ? 'allure-report/**' : ''

                if (currentBuild.currentResult == 'SUCCESS') {
                    emailext(
                        subject: "✅ Build SUCCESS: ${currentBuild.fullDisplayName}",
                        body: """<p>Hi Neethu,</p>
                                 <p>The Jenkins build <b>${currentBuild.fullDisplayName}</b> succeeded.</p>
                                 <p>View Allure report online: <a href='${BUILD_URL}allure-report/index.html'>Allure Report</a></p>
                                 <p>Allure report folder is attached to this email.</p>""",
                        to: "neethuelzageorge@gmail.com",
                        attachmentsPattern: attachmentPattern,
                        mimeType: 'text/html'
                    )
                } else {
                    emailext(
                        subject: "❌ Build FAILURE: ${currentBuild.fullDisplayName}",
                        body: """<p>Hi Neethu,</p>
                                 <p>The Jenkins build <b>${currentBuild.fullDisplayName}</b> failed.</p>
                                 <p>Check console output here: <a href='${BUILD_URL}console'>Console Output</a></p>""",
                        to: "neethuelzageorge@gmail.com",
                        mimeType: 'text/html'
                    )
                }
            }

            echo 'Cleaning workspace...'
            cleanWs()
        }
    }
}
