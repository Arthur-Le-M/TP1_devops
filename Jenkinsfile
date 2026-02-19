pipeline {
    agent any
    environment {
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Python') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt
                pyinstaller --onefile main.py
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') { 
                    sh "${SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=MonProjetPython \
                    -Dsonar.sources=. \
                    -Dsonar.language=py \
                    -Dsonar.exclusions=**/.venv/**,**/dist/**,**/build/**"
                }
            }
        }
    }
}
