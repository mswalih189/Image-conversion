node {
    // Global env
    def AWS_REGION = 'eu-north-1'
    def EC2_HOST   = '51.21.180.76'   // your proj4 EC2 IP

    stage('Checkout') {
        checkout scm
    }

    stage('Terraform Init & Apply') {
        dir('infra') {
            // AWS creds come from aws configure on Jenkins, or env vars if you set them
            sh '''
              terraform init
              terraform apply -auto-approve -var="aws_region=''' + AWS_REGION + '''"
            '''
        }
    }

    stage('Deploy to proj4 EC2') {
        // 'ec2-ssh-key' is Jenkins SSH credential ID with your proj private key
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
