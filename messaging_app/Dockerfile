FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set working directory
WORKDIR /app

# copy requirements to /app
COPY requirements.txt /app/

# install Python requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy the full app
COPY . /app/

# Expose default django Default port

EXPOSE 8000

# Run Django developement server by default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]