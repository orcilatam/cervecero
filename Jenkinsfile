@Library('sharedlib')
import static com.orcilatam.devops.Const.*
import static com.orcilatam.devops.Stage.*

def sonarqube = 'sonarqube:9000'
def registry = 'artifactory:8082/docker-local'
def registryId = 'registry-push-user'

pipeline {
  agent any

  stages {
    stage('Compilación') {
      steps {
        script {
          buildPython(this, 'cervecero', '1.0')
        }
      }
    }

    stage('Tests unitarios') {
      steps {
        script {
          testPython(this)
        }
      }
    }

    stage('Calidad de código') {
      steps {
        script {
          runSonarQubePython(this, sonarqube)
        }
      }
    }

    stage('Construcción de imagen Docker') {
      steps {
        script {
          buildDockerImage(this, registry)
        }
      }
    }

    stage('Subida a Artifactory') {
      steps {
        script {
          pushImageToArtifactory(this, registry, registryId)
        }
      }
    }
        
  }
}
