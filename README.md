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
