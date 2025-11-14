pipeline {
    agent any
    parameters {
        choice (name: 'ENVIRONMENT', choices: ['dev','staging','pre-prod','prod'],description:'Deployment Environment')
        choice (name: 'ACTION', choices: ['PLAN','APPLY'],description: 'Terraform Action')
    }
    environment {
        AWS_DEFAULT_REGION= 'us-east-2'
        TF_VAR_region="${AWS_DEFAULT_REGION}"
    }

    stages {
        stage('Checkout'){
            steps {
                echo "Checking out source code"
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo "Setting up Python environment"
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "Running unit tests with coverage"
                sh '''
                    . venv/bin/activate
                    cd python
                    pytest -v --cov=. --cov-report=xml:coverage.xml --cov-report=html --cov-report=term-missing --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'python/test-results.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'python/htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Coverage Check') {
            steps {
                echo "Checking coverage threshold"
                sh '''
                    . venv/bin/activate
                    cd python
                    coverage report --fail-under=90
                '''
            }
        }
        
        stage('SonarQube Analysis') {
            when {
                branch 'main'
            }
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=containerized-applications \
                            -Dsonar.sources=python/app.py \
                            -Dsonar.tests=python/test_app.py \
                            -Dsonar.python.coverage.reportPaths=python/coverage.xml \
                            -Dsonar.python.version=3.9
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            when {
                branch 'main'
            }
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image"
                sh '''
                    docker build -t containerized-app:${BUILD_NUMBER} .
                    docker tag containerized-app:${BUILD_NUMBER} containerized-app:latest
                '''
            }
        }
        
        stage('Terraform ${ACTION}') {
            when {
                expression { params.ACTION == 'PLAN' || params.ACTION == 'APPLY' }
            }
            steps {
                dir('terraform') {
                    script {
                        if (params.ACTION == 'PLAN') {
                            sh 'terraform init'
                            sh 'terraform plan -var="environment=${ENVIRONMENT}"'
                        } else if (params.ACTION == 'APPLY') {
                            sh 'terraform init'
                            sh 'terraform apply -var="environment=${ENVIRONMENT}" -auto-approve'
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace'
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
