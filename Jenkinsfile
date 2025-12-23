pipeline {
    agent any

    environment {
        // AWS region where Terraform creates proj4 EC2 and S3
        AWS_REGION = 'eu-north-1'
        // Your proj4 EC2 public IP
        EC2_HOST   = '51.21.180.76'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull latest code from your GitHub repo (where Jenkinsfile lives)
                checkout scm
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                dir('infra') {
                    // Terraform uses AWS credentials from AWS CLI config on Jenkins (~/.aws/credentials)
                    sh """
                      terraform init
                      terraform apply -auto-approve -var="aws_region=${AWS_REGION}"
                    """
                }
            }
        }

        stage('Deploy to proj4 EC2') {
            steps {
                // 'ec2-ssh-key' is a Jenkins SSH credential with your 'proj' private key
                sshagent (credentials: ['ec2-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} '
                      set -eux
                      cd /opt/image_s3_app || exit 1
                      sudo git pull origin main
                      source venv/bin/activate
                      pip install -r requirements.txt
                      sudo systemctl restart flask-app
                    '
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed – check console output for the failing stage."
        }
    }
}
