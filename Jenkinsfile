pipeline {
    agent any
    environment {
        SCANNER_HOME = tool 'SonarScanner'
        NEXUS_URL = "http://localhost:8081/repository/python-releases"
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

        stage('Upload to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: '80bfa4bb-b200-4511-9309-c0589d1db30e', 
                                                usernameVariable: 'NEXUS_USER', 
                                                passwordVariable: 'NEXUS_PASSWORD')]) {
                    sh """
                    curl -v -u ${NEXUS_USER}:${NEXUS_PASSWORD} \
                        --upload-file dist/main \
                        ${NEXUS_URL}/main-v${env.BUILD_ID}
                    """
                }
            }
        }
    }
}
