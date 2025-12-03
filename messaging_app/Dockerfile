FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set working directory
WORKDIR /app

# Install system dependencies psycop2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

#mysql dependencies
RUN apt-get install -y default-libmysqlclient-dev build-essential

# copy requirements to /app
COPY requirements.txt /app/

# install Python requirements
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy the full app
COPY . /app/

# Expose default django Default port

EXPOSE 8000
# -p 8000:8000

# Run Django developement server by default
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# For production ready container:
# RUN pip install gunicorn

# CMD ["gunicorn", "your_project_name.wsgi:application", "--bind", "0.0.0.0:8000"]