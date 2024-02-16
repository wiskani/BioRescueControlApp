
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

2. Ejecuta el siguiente comando para iniciar los servicios:

   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. La aplicación estará disponible en:

   - Next.js (frontend): `http://localhost:3000`
   - FastAPI (backend): `http://localhost:8080`

## Desarrollo

Para trabajar en un entorno de desarrollo, sigue estos pasos:

1. Configura las variables de entorno necesarias en un archivo `.env` en la raíz del proyecto:

   ```
   POSTGRES_DB=nombre_de_tu_base_de_datos
   POSTGRES_USER=usuario_de_la_base_de_datos
   POSTGRES_PASSWORD=contraseña_de_la_base_de_datos
   POSTGRES_DB_TEST=nombre_de_tu_base_de_datos_de_pruebas
   POSTGRES_USER_TEST=usuario_de_la_base_de_datos_de_pruebas
   POSTGRES_PASSWORD_TEST=contraseña_de_la_base_de_datos_de_pruebas
   PGADMIN_DEFAULT_EMAIL=email_para_pgadmin
   PGADMIN_DEFAULT_PASSWORD=contraseña_para_pgadmin
   ```

2. Ejecuta el siguiente comando para iniciar los servicios:

   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. La aplicación y las herramientas estarán disponibles en:

   - Next.js (frontend): `http://localhost:3000`
   - FastAPI (backend): `http://localhost:8080`
   - PostgreSQL (base de datos): `localhost:5432`
   - PostgreSQL (base de datos de pruebas): `localhost:5433`
   - pgAdmin (herramienta de administración de PostgreSQL): `http://localhost:5050`

## Notas adicionales

- Asegúrate de personalizar las variables de entorno según tus necesidades.
- Para detener y eliminar los contenedores, redes y volúmenes creados, puedes usar el comando `docker-compose down -v`.
