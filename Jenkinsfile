environment {
    AWS_REGION = 'eu-north-1'
    EC2_HOST   = '51.21.180.76'
    AWS_CREDS  = credentials('aws-flask-cred')
}

stage('Terraform Init & Apply') {
    steps {
        dir('infra') {
            withEnv([
                "AWS_ACCESS_KEY_ID=${AWS_CREDS_USR}",
                "AWS_SECRET_ACCESS_KEY=${AWS_CREDS_PSW}",
                "AWS_DEFAULT_REGION=${AWS_REGION}"
            ]) {
                sh """
                  terraform init
                  terraform apply -auto-approve -var="aws_region=${AWS_REGION}"
                """
            }
        }
    }
}
