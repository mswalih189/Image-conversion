node {
    def AWS_REGION = 'eu-north-1'
    def EC2_HOST   = '51.21.162.125'

    stage('Checkout') {
        checkout scm
    }

    stage('Terraform Init & Apply') {
        dir('infra') {
            withCredentials([usernamePassword(credentialsId: 'aws-flask-cred',
                                              usernameVariable: 'AWS_ACCESS_KEY_ID',
                                              passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                withEnv(["AWS_DEFAULT_REGION=${AWS_REGION}"]) {
                    sh '''
                        terraform init
                        terraform apply -auto-approve -var="aws_region=${AWS_REGION}"
                        echo "✅ Terraform Outputs:"
                        terraform output
                    '''
                }
            }
        }
    }

    stage('Deploy to EC2') {
        sh """
            ssh -i /var/lib/jenkins/.ssh/proj.pem -o StrictHostKeyChecking=no ec2-user@${EC2_HOST} '
              set -eux
              sudo yum install -y git python3-pip
              sudo mkdir -p /opt/image_s3_app
              cd /opt/image_s3_app
              
              # FORCE reset to latest code - NO CONFLICTS!
              sudo git fetch origin
              sudo git reset --hard origin/main
              sudo git clean -fd
              
              # Install/upgrade dependencies
              sudo pip3 install -r requirements.txt --upgrade --no-cache-dir
              
              # Restart Flask service
              sudo systemctl daemon-reload
              sudo systemctl restart flask-app
              sleep 5
              sudo systemctl status flask-app --no-pager -l
            '
        """
    }

    stage('Health Check') {
        sh """
            echo "🔍 Checking http://51.21.162.125:5000..."
            curl -s -o /dev/null -w "HTTP Status: %%{http_code}\\n" http://51.21.162.125:5000 || echo "⚠️ Site may take 30s to fully start"
        """
    }
}
