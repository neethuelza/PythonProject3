pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
        ALLURE_REPORT = "${WORKSPACE}/allure-report" // forward slashes for Windows
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'master', url: 'https://github.com/neethuelza/PythonProject3.git'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Selenium-Pytest tests via batch file...'
                timeout(time: 30, unit: 'MINUTES') {  // prevents hanging builds
                    bat """call "${WORKSPACE_DIR}/run_tests.bat" """
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report...'
                bat """allure generate "${WORKSPACE_DIR}/reports/allure-results" -o "${ALLURE_REPORT}" --clean"""
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
            emailext(
                subject: "✅ Build SUCCESS: ${currentBuild.fullDisplayName}",
                body: """<p>Hi Neethu,</p>
                         <p>The Jenkins build <b>${currentBuild.fullDisplayName}</b> succeeded.</p>
                         <p>View Allure report online: <a href='${BUILD_URL}allure-report/index.html'>Allure Report</a></p>
                         <p>Allure report folder is attached to this email.</p>""",
                to: "neethuelzageorge@gmail.com",
                attachmentsPattern: "allure-report/**",
                mimeType: 'text/html'
            )
        }

        failure {
            echo 'Pipeline failed!'
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
}
