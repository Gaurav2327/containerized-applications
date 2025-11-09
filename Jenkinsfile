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
        stage('checkout'){
            steps {
                echo "checking out source code"
                checkout scm
            }
        }
    }
}