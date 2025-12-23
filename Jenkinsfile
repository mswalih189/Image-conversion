node {
    def AWS_REGION = 'eu-north-1'
    def EC2_HOST   = '51.21.162.125'  // NEW EC2 from Terraform output!

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
                    '''
                }
            }
        }
    }

    stage('Deploy to EC2') {
        sh """
            ssh -i /var/lib/jenkins/.ssh/proj.pem -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} '
              set -eux
              cd /opt/image_s3_app || exit 1
              sudo git pull origin main
              source venv/bin/activate || pip install -r requirements.txt
              sudo systemctl restart flask-app || sudo systemctl start flask-app
            '
        """
    }
}
