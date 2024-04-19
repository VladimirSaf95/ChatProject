pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python:3.9.13-alpine3.16'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Сборка Docker-образа
                    docker.build DOCKER_IMAGE, '--file Dockerfile .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Запуск тестов внутри Docker-контейнера
                    docker.withRegistry('', '') {
                        docker.image(DOCKER_IMAGE).inside('-v $PWD:/usr/workspace') {
                            sh 'ls -la'
                            sh 'pytest -sv --alluredir=allure-results'
                        }
                    }
                }
            }
        }

        // Другие этапы пайплайна, если есть
    }

    post {
        success {
            // Публикация отчетов Allure в случае успешного завершения сборки
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
    }
}
