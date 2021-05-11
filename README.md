# Modelo predictivo de consumo de cerveza

![Cervecero](https://raw.githubusercontent.com/orcilatam/cervecero/master/cervecero/static/img/cervecero.png)

Proyecto de prueba para curso práctico de DevOps de la UDD. Conversión de dinámica 2 de clase 4 (notebook de Jupyter con regresión lineal para predicción de consumo de cerveza) a una aplicación Python 3 independiente, sobre un pipeline de Jenkins.

## Paso 1 — Ejecución del notebook de Jupyter

Se incluye el notebook de Jupyter original de la clase 4. En la dinámica 2 de este notebook se encuentra el modelo de predicción de consumo de cerveza basado en una regresión lineal.

Como el entorno de la máquina virtual ya tiene Jupyter instalado vía Anaconda, el notebook se puede ejecutar localmente de la siguiente forma:

```sh
conda activate
jupyter notebook
```

Lo anterior debería ejecutar una instancia de Jupyter y abrir automáticamente Firefox. Navegue a `curso/cervecero/notebooks` y haga clic en `Clase-4-Dinámicas.ipynb` para abrir el notebook.

Para cerrar Jupyter, vaya al terminal, pulse Ctrl+C y desactive Anaconda:

```sh
conda deactivate
```

## Paso 2 — Ejecución de la aplicación independiente

El código de la predicción de consumo de cerveza basado en la regresión lineal se extrajo de `Clase-4-Dinámicas.ipyinb` y se llevó a `cervecero/modelos/clase4.py`. Nótese que se comentaron las líneas que emitían información del dataset y se encapsuló la lógica en una función `resultado`. Luego, este modelo se incorporó a una aplicación web simple de Python 3 basada en Flask.

Para ejecutar esta aplicación:

```sh
cd ~/curso/cervecero
python3 -m venv venv
./venv/bin/pip3 install -r requirements.txt
./venv/bin/python3 cervecero/server.py
```

Abra Firefox y navegue a http://localhost:9090/ para ver la aplicación.


## Paso 3 — Jenkins y un pipeline mínimo

Asumiendo que tenemos Jenkins instalado y correctamente configurado, podemos usarlo como infraestructura mínima para un pipeline.

Jenkins está preinstalado en la VM, puede acceder a él en http://localhost:8080/

Para ver el código de este paso:

```sh
git checkout master
git reset --hard paso-3
```

Se agrega una shared library en Jenkins para uso de los pipelines. Ésta consta de una serie de funciones utilitarias en Groovy para uso de los pipelines. Para nuestro ejemplo usaremos https://github.com/orcilatam/sharedlib.

Se agrega un pipeline básico en un nuevo archivo archivo `Jenkinsfile`; éste usa la shared library anterior. Aquí se observan las llamadas a los stages de compilación y ejecución de tests unitarios.

Se agrega en Jenkins un job del tipo Multibranch pipeline que apunte al repositorio de Cervecero.

Se modifica `clase4.py` para agregar tests unitarios.

Finalmente, hacer clic en _Build Now_ en Jenkins.


## Paso 4 — Revisión de calidad de código con SonarQube

Asumiendo que tenemos **SonarQube** instalado y correctamente configurado, podemos usarlo para revisar la calidad del código fuente de la aplicación.

SonarQube está preinstalado en la nube, acceda a él en http://sonarqube:9000/

Para ver el código de este paso:

```sh
git checkout master
git reset --hard paso-4
```

Se agrega una llamada a `runSonarQubePython` en el `Jenkinsfile`y se agrega el archivo `sonar-project.properties` con parámetros para SonarQube. Nótese que el Sonar Scanner está preinstalado en la VM en `/opt/sonar-scanner`.

Hacer clic en *Build Now* en Jenkins para ejecutar el pipeline. Una vez finalizado el pipeline, el reporte de calidad se puede observar en http://sonarqube:9000/


## Paso 5 — Creación de artefacto y construcción de imagen Docker

En términos generales, un _artefacto_ es un objeto binario que representa una aplicación, biblioteca u otro recurso de una aplicación. Un artefacto consiste generalmente de un único archivo binario comprimido. Por ejemplo, para Java los packages `.jar`, `.ear` y `.war` se consideran artefactos. Para el caso de Python, como es un lenguaje dinámico e interpretado, no genera artefactos binarios (a menos que se use un compilador especializado, pero esto no es usual).

Un artefacto tiene, además de un nombre, una *etiqueta* generalmente asociada con su número de versión. De esta manera es posible tener el mismo artefacto con distintas versiones.

Una imagen de Docker es simplemente un artefacto que representa una máquina virtual muy ligera. Para este curso, construiremos una imagen de Docker simple que contendrá:

- Un sistema operativo Debian mínimo (“slim”)
- Python 3.9
- El código de Flask y el código modelo de predicción

Para ver estos cambios:

```sh
git checkout master
git reset --hard paso-5
```

Se agrega una llamada a `buildDockerImage` en el `Jenkinsfile`.  Hacer clic en *Build Now* en Jenkins para ejecutar el pipeline.


## Paso 6 — Subida a Artifactory

Artifactory, como lo sugiere su nombre, es un repositorio central de artefactos. En este paso se tomará la imagen Docker creada localmente y se subirá a una instancia de Artifactory en la nube.

Para ver el nuevo stage:

```sh
git checkout master
git reset --hard paso-6
```

Se agrega una llamada a `pushImageToArtifactory` en el `Jenkinsfile`.  Hacer clic en *Build Now* en Jenkins para ejecutar el pipeline.

El servidor de artifactory está en la nube, se puede acceder a él en http://artifactory:8082/artifactory. Use el usuario `estudiante`.


## Paso 7 — Despliegue a Kubernetes

Kubernetes es un sistema de orquestación de contenedores para automatizar el despliegue, el escalado y la gestión de aplicaciones que actúan en conjunto en un *cluster*.

Para este curso, desplegaremos a un *cluster* predefinido en Digital Ocean. El despliegue a Kubernetes requiere agregar al menos dos archivos YAML con la descripción del cluster: `service.yaml` y `deployment.yaml`.

Para ver los archivos en el nuevo stage:

```sh
git checkout master
git reset --hard paso-7
```

Se agregan (entre otras cosas) llamadas a  `deployToKubernetes` en el `Jenkinsfile`.  Hacer clic en *Build Now* en Jenkins para ejecutar el pipeline.

El resultado del despliegue puede observarse ejecutando:

```sh
kubectl get services
kubectl get deployments
kubectl get pods
POD=$( kubectl get pods | grep cervecero | cut -d ' ' -f 1 )
kubectl get pod $POD
kubectl describe pod $POD
kubectl logs -f pod $POD
kubectl logs -f $POD
```

## Paso 8 — Configuración de Ingress

Los despliegues del paso anterior no son visibles fuera del cluster de Kubernetes. Para exponer el cluster al mundo, lo usual es proveerle un punto de entrada controlado denominado **Ingress**.

Este consiste de un *web front* (también llamado *reverse proxy*) que acepta las peticiones HTTP de internet y las encamina hacia un Servicio Kubernetes en el proxy. Ingress es una definición genérica; la implementación concreta se basa en un **Ingress Controller**.

El Ingress Controller para nuestro ejemplo se basa en un servidor **Nginx** con balanceo de carga. Para instalar el Ingress Controller, se usará **Helm**.

Helm es un gestor de paquetes para Kubernetes. Este permite instalar y pre-configurar un grupo relacionado de servicios, deployments, configuraciones y recursos de Kubernetes como una unidad en lugar de tener que aplicar manifiestos de Kubernetes uno por uno.

Para ver los archivos en el nuevo stage:

```sh
git checkout master
git reset --hard paso-8
```

Hacer clic en *Build Now* en Jenkins para ejecutar el pipeline.

Nótese que incluso después de instalar el Ingress Controller la aplicación continúa inaccesible desde internet. Es necesario completar dos pasos adicionales con los DNS que generalmente se ejecutan manualmente:

- Registrar un dominio público y apuntar los DNS a DigitalOcean. Para nuestro ejemplo usaremos el dominio `parroquiano.info`, que ya apunta a `ns{1,2}.digitalocean.com`
- Crear un subdominio DNS `cervecero.parroquiano.info` que apunte al Ingress Controller creado con Helm (usar TTL 300)


## Paso 9 — Prometheus y Grafana

**Prometheus** es una base de datos para series de tiempo. Esto quiere decir que está optimizada para guardar eficientemente series de datos con *timestamps* y produce resultados rápidos para consultas basadas en intervalos de tiempo. Esto la hace ideal para guardar métricas de hardware, como uso de disco, CPU y red.

Se suele usar en conjunción con **Grafana**, un producto para construir *dashboards* de visualización de métricas en tiempo real. Ambos constituyen una alternativa muy usada para monitorear clusters de Kubernetes.

Prometheus y Grafana se pueden instalar directamente en el marketplace del cluster de Kubernetes de Digital Ocean.  Para acceder a los dashboards de Grafana, avance hasta el paso 9.

```sh
git checkout master
git reset --hard paso-9
```

Y luego ejecute un utilitario para levantar un acceso local vía port forwarding:

```sh
cd ~/curso/cervecero
./grafana 8084
```

Puede acceder a los dashboards en el navegador Firefox de la VM abra [http://locahost:8084/](http://locahost:8084/). Puede ingresar con el usuario `admin`.


## Paso adicional 10 — Infraestructura como código

En los pasos anteriores la infraestructura ya se asumía instalada. La instalación de ésta generalmente se gestiona a través de **Terraform**.

```sh
git checkout master
git reset --hard paso-10
```

La ejecución de este paso requiere su propio pipeline. Por favor, [continúe aquí](https://github.com/orcilatam/iac/) para completar el ejercicio.


## Paso adicional 11 — Verificación de vulnerabilidades

OWASP (Open Web Application Security Project) es una fundación sin fines de lucro que publica herramientas y manuales para difundir buenas prácticas de seguridad. **Dependency Check** es un utilitario open source creado por OWASP para detectar vulnerabilidades conocidas en las *dependencias* de un proyecto. Por *dependencias* se entienden todas las bibliotecas, utilitarios y otros proyectos de base encima de las cuales se construye una aplicación. Dependency Check puede analizar una aplicación para determinar si alguna de sus dependencias contiene vulnerabilidades documentadas (conocidas como **CVE** o Common Vulnerabilities and Exposures en la jerga de seguridad) y cuáles son las posibles soluciones (conocidas como **mitigaciones** en la jerga). Dependency Check se conecta a una base de datos de OWASP en internet para mantenerse constantemente actualizado con las nuevas CVEs que se descubren y publican casi a diario. En internet es posible consultar las CVEs, si se conoce su número identificador, en [https://cve.mitre.org/](https://cve.mitre.org/)

La verificación de dependencias es sólo uno de los muchos aspectos de seguridad que pueden aparecer en DevOps. De hecho, muchas organizaciones ya hablan de  *DevSecOps* (Development, Security and Operations). Entre estos aspectos tenemos, además de las verificaciones de dependencias, el análisis estático del código de la aplicación para detectar prácticas inseguras (nótese que SonarQube ya emite un reporte de este aspecto), el análisis de comportamiento dinámico de una aplicación en producción, los tests de penetración (pentests) ejecutados por hackers éticos, el establecimiento y revisión de perímetros de seguridad web usando WAFs (Web Application Firewalls), etc.

Una exploración de todos estos aspectos está fuera del alcance de este curso introductorio. Sin embargo, la combinación de SonarQube y Dependency Check asegura una base mínima suficiente para la verificación de vulnerabilidades más comunes.

Para ver cómo incorporar Dependency Check a un nuevo stage:

```sh
git checkout master
git reset --hard paso-11
```

Hacer clic en *Build Now* en Jenkins para ejecutar el pipeline.

Una vez concluido el pipeline haga clic en el número de Build. Al lado izquierdo aparece un link al reporte de Dependency Check.


## Paso adicional 12 — Notificaciones a Slack

Una característica útil de Jenkins es la capacidad de enviar notificaciones en vivo (vía un plugin) a un canal de Slack. Esto permite que otras personas observen y monitoreen la ejecución de un pipeline sin necesidad de ingresar a Jenkins.

Para ver cómo incorporar notificaciones a Slack:

```sh
git checkout master
git reset --hard paso-12
```

Hacer clic en *Build Now* en Jenkins para ejecutar el pipeline.

Las notificaciones se envían al canal de Slack configurado en Jenkins.

---

Copyright &copy; 2021 Marco Bravo, con licencia [GPL v3](LICENSE)
