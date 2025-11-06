pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
        ALLURE_REPORT = "${WORKSPACE}\\allure-report"
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
                bat """
                call "${WORKSPACE_DIR}\\run_tests.bat"
                """
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
                         <p>Check Allure report here: ${BUILD_URL}allure-report/</p>""",
                to: "neethuelzageorge@gmail.com"
            )
        }
        failure {
            echo 'Pipeline failed!'
            emailext(
                subject: "❌ Build FAILURE: ${currentBuild.fullDisplayName}",
                body: """<p>Hi Neethu,</p>
                         <p>The Jenkins build <b>${currentBuild.fullDisplayName}</b> failed.</p>
                         <p>Check console output here: ${BUILD_URL}console</p>""",
                to: "neethuelzageorge@gmail.com"
            )
        }
    }
}
