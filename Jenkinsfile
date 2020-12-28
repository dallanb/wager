pipeline {

    environment {
        githubCredential = 'github'
        registry = "dallanbhatti/wager"
        registryCredential = 'dockerhub'
        dockerImage = ''
        dockerImageName = ''
    }
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    dockerImageName = registry + ":$BRANCH_NAME"
                    if (env.BRANCH_NAME == 'qaw' || env.BRANCH_NAME == 'prod') {
                        dockerImage = docker.build(dockerImageName, "-f build/Dockerfile.$BRANCH_NAME .")
                    }
                    else {
                        dockerImage = docker.build(dockerImageName, "-f build/Dockerfile .")
                    }

                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Clean') {
            steps {
                sh "docker rmi $dockerImageName"
            }
        }
    }
}