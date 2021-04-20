@Library('sharedlib')
import static com.orcilatam.devops.Const.*
import static com.orcilatam.devops.Stage.*

def sonarqube = 'sonarqube:9000'
def registry = 'artifactory:8082/docker-local'
def registryId = 'registry-push-user'
def containerPort = '9090'
def kubeConfig = 'kubeconfig-multivac'
def kubeNamespace = 'default'
def ingressName = 'cervecero'

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

    stage('Despliegue a Kubernetes') {
      steps {
        script {
          replacePlaceholder(this, 'deployment.yaml', 'registry', registry)
          replacePlaceholder(this, 'deployment.yaml', 'project.port', containerPort)
          replacePlaceholder(this, 'service.yaml', 'project.port', containerPort)

          deployToKubernetes(this, kubeConfig, kubeNamespace, 'deployment.yaml')
          deployToKubernetes(this, kubeConfig, kubeNamespace, 'service.yaml')
        }
      }
    }

    stage('Instalación de LoadBalancer e Ingress Controller') {
      steps {
        script {
          updateHelmRepositories(this)
          installNginxIngressController(this, kubeConfig, kubeNamespace, ingressName)
        }
      }
    }

    stage('Configuración de Ingress') {
      steps {
        script {
          deployToKubernetes(this, kubeConfig, kubeNamespace, 'ingress.yaml')
        }
      }
    }

  }
}
