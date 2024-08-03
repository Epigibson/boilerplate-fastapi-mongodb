Este proyecto es una aplicación web API RESTful que utiliza el framework FastAPI para Python y la base de datos NoSQL MongoDB. Está diseñado para ser ejecutado en un entorno de Docker y se incluye un archivo docker-compose.yml para facilitar la configuración.

Requerimientos:
Docker
Docker Compose

Configuración:
Clona este repositorio: git clone https://github.com/tu_usuario/tu_proyecto.git
Entra en el directorio del proyecto: cd tu_proyecto
Crea un archivo .env con las variables de entorno necesarias (ver sample.env para un ejemplo)
Ejecuta el comando docker-compose up -d para construir y ejecutar los contenedores de Docker.

Uso:
Para acceder a la interfaz de la API, abre tu navegador y entra en http://localhost:8000/. Desde aquí, podrás probar los endpoints de la API utilizando una herramienta como Postman o cURL.

API:
La API expone los siguientes endpoints:
/items: CRUD para items en la base de datos MongoDB. Incluye endpoints para obtener un item por ID, crear un nuevo item, actualizar un item existente y eliminar un item existente.
Contribución

¡Agradecemos cualquier contribución a este proyecto! Si deseas informar de un problema o sugerir una nueva función, utiliza la sección "Issues" en este repositorio. Si deseas contribuir al código fuente, realiza una solicitud de extracción (PR) y haremos lo posible por revisarla lo antes posible.

UTILIZACION DE KUBERNETES
Crear la imagen de Docker:
docker build -t beplus-app:latest . 

Crear un tag personalizado a la imagen creada:
docker tag beplus-app:latest localhost:5000/beplus-app:latest

Iniciar un registro local de Docker:
docker run -d -p 5000:5000 --restart=always --name registry registry:2

Empujar la imagen creada al regitro local de Docker:
docker push localhost:5000/beplus-app:latest

Eliminar configuraciones de Deploy:
kubectl delete deployment fastapi-deployment

Eliminar configuraciones de Servicios:
kubectl delete service fastapi-service

Aplicar la confguracion nueva de Deploy:
kubectl apply -f deployment.yaml

Aplicar la configuracion nueva de Servicios:
kubectl apply -f service.yaml

Obtener los PODS para verificar que esten ejecutandose:
kubectl get pods

Verificar que los servivcios estan corriendo y ver si esta el que se configuro:
kubectl get services

Ver la descripcion del POD:
kubectl describe pod <nombre-del-pod>

Verificar los logs del POD:
kubectl logs <nombre-del-pod>


Licencia:
Este proyecto se encuentra bajo la Licencia MIT. Consulta el archivo LICENSE para más información.
