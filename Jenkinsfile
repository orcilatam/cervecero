@Library('sharedlib')
import static com.orcilatam.devops.Const.*
import static com.orcilatam.devops.Stage.*

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

  }
}
