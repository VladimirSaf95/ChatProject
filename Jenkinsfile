pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python:3.9.13-alpine3.16'
    }

    stages {
        stage('Cache Dependencies') {
            steps {
                script {
                    // Загрузка кеша зависимостей, если он есть
                    def cachedDeps = cache(steps: [
                        // Копирование кеша зависимостей в рабочую директорию
                        load('/path/to/cache/key')
                    ])
                    // Если кеш был найден, используем его, иначе устанавливаем зависимости заново
                    if (cachedDeps != null) {
                        echo 'Using cached dependencies'
                    } else {
                        echo 'Installing dependencies'
                        sh 'pip install -r requirements.txt'
                    }
                }
            }
        }

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
        always {
            // Сохранение кеша зависимостей для будущих сборок
            cache(save: '/path/to/cache/key', paths: ['~/.cache/pip'])
        }

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
