pipeline {
    agent any
    environment {
        SCANNER_HOME = tool 'SonarScanner'
        NEXUS_URL = "http://host.docker.internal:8081/repository/python-release/"
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

        stage('Unit Tests') {
            steps {
                sh '''
                . .venv/bin/activate
                export SDL_VIDEODRIVER=dummy
                python -m unittest test_main.py
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
                withCredentials([usernamePassword(credentialsId: '23b9c147-5544-460a-ae4a-600d80b8d23d', 
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
