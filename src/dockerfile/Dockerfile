FROM python:3

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Descargar y configurar Microsoft EdgeDriver
ARG EDGE_VERSION=92.0.902.62
ENV EDGE_DRIVER_VERSION=${EDGE_VERSION}
RUN wget -q https://msedgedriver.azureedge.net/${EDGE_DRIVER_VERSION}/edgedriver_linux64.zip \
    && unzip -q edgedriver_linux64.zip \
    && rm edgedriver_linux64.zip \
    && chmod +x edgedriver \
    && mv edgedriver /usr/bin/edgedriver

# Copiar los archivos de la aplicación
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Configurar variables de entorno para EdgeDriver
ENV PATH="/usr/bin:${PATH}"
ENV EDGEWEBDRIVER=edgedriver

# Ejecutar el comando para iniciar la aplicación
CMD [ "python", "app.py" ]
