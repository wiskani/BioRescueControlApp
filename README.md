
# Aplicación para Base de Datos de los Planes de Rescate de Flora y Fauna

Este repositorio contiene los archivos de configuración de Docker para desplegar una aplicación web utilizando Next.js, FastAPI y PostgreSQL en un entorno de producción y desarrollo.

## Requisitos

- Docker
- Docker Compose

## Despliegue en producción

Para desplegar la aplicación en producción, sigue estos pasos:

1. Configura las variables de entorno necesarias en un archivo `.env` en la raíz del proyecto:

   ```
   POSTGRES_DB=nombre_de_tu_base_de_datos
   POSTGRES_USER=usuario_de_la_base_de_datos
   POSTGRES_PASSWORD=contraseña_de_la_base_de_datos
   ```
   En el /backend se deben configurar las siguientes variables de entorno:
   ```
   SECRET_KEY=your_secret_key
   APP_MAX=100
   FIRST_USER_MAIL=first_user_email
   FIRST_USER_PASSWORD=first_user_password
   POSTGRES_DB=database_name
   POSTGRES_USER=database_user
   POSTGRES_PASSWORD=database_password
   DATABASE_URL=postgresql://database_user:database_password@db:5432/database_name
   NEXTJS_URL= Direccion del servidor del frontend para los CORS
   ```

   En el /frontend se debe establecer las siguientes variables:
   ```
   NEXT_PUBLIC_MAPBOX_TOKEN= token de MAPBOX
   NEXT_PUBLIC_API_URL=Dirección del servicor
   NEXTAUTH_SECRET= codigo secreto para nextauth
   ```

3. Ejecuta el siguiente comando para iniciar los servicios:

   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. La aplicación estará disponible en:

   - Next.js (frontend): `http://localhost:3000`
   - FastAPI (backend): `http://localhost:8080`

## Desarrollo

Para trabajar en un entorno de desarrollo, sigue estos pasos:

1. Configura las mismas variables que producción, ademas se deben agregar las variables para el test backend:
    ```
   POSTGRES_DB_TEST=test_database_name
   POSTGRES_USER_TEST=test_database_user
   POSTGRES_PASSWORD_TEST=test_database_password
    DATABASE_URL_TEST=postgresql://test_database_user:test_database_password@db-test:5432/test_database_name
     ```

3. Ejecuta el siguiente comando para iniciar los servicios:

   ```bash
   docker-compose up -d
   ```

4. La aplicación y las herramientas estarán disponibles en:

   - Next.js (frontend): `http://localhost:3000`
   - FastAPI (backend): `http://localhost:8080`
   - PostgreSQL (base de datos): `localhost:5432`
   - PostgreSQL (base de datos de pruebas): `localhost:5433`
   - pgAdmin (herramienta de administración de PostgreSQL): `http://localhost:5050`

## Notas adicionales

- Asegúrate de personalizar las variables de entorno según tus necesidades.
- Para detener y eliminar los contenedores, redes y volúmenes creados, puedes usar el comando `docker-compose down -v`.
