# Usar como base la imagen oficial de Python 3.9
FROM python:3.9

# El puerto de EXPOSE es meramente informativo
# (no expone realmente)
EXPOSE 9090

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar requerimientos al contenedor e instalarlos
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copiar proyecto al contenedor, incluendo los datasets
COPY datasets/ datasets/
COPY cervecero/ cervecero/

# Ejectutar al inicio
CMD [ "python3", "./cervecero/server.py" ] 
