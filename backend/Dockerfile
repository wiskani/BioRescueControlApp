#Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /fastapi

# Install dependencies
COPY requirements.txt /fastapi
RUN pip install -r requirements.txt

# Copy project
COPY . /fastapi
RUN ls -la /fastapi

# start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
