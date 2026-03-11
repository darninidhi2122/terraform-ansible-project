pipeline {

    agent any

    environment {
        AWS_DEFAULT_REGION = "us-east-1"
        ANSIBLE_HOST_KEY_CHECKING = "False"
        DOCKER_IMAGE = "YOUR_DOCKERHUB_USERNAME/nginx-devops"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/darninidhi2122/terraform-ansible-project.git'
            }
        }

        stage('Terraform Init') {
            steps {
                dir('infra') {
                    sh 'terraform init'
                }
            }
        }

        stage('Terraform Validate') {
            steps {
                dir('infra') {
                    sh 'terraform validate'
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir('infra') {
                    sh 'terraform plan'
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('infra') {
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Configure Minikube with Ansible') {
            steps {
                sshagent(credentials: ['ec2-key']) {
                    sh '''
                    cd ansible-1
                    export ANSIBLE_CONFIG=ansible.cfg
                    ansible-playbook -i aws_ec2.yml -u ubuntu playbook.yml
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:latest", "./app")
                }
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }

        stage('Deploy Application with Helm') {
            steps {
                sshagent(credentials: ['ec2-key']) {
                    sh '''
                    ssh ubuntu@$(terraform -chdir=infra output -raw minikube_public_ip) << EOF
                    cd terraform-ansible-project
                    helm upgrade --install nginx-app helm/nginx-chart
                    kubectl get pods
                    kubectl get svc
                    EOF
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution finished"
        }
        success {
            echo "Infrastructure, Docker build, and Helm deployment completed successfully."
        }
        failure {
            echo "Pipeline failed. Check logs."
        }
    }
}
