# FROM python:3.10
# EXPOSE 5000
# WORKDIR /app
# COPY ./requirements.txt requirements.txt
# RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY . .
# CMD ["flask", "run", "--host", "0.0.0.0"]



# FROM python:3.8-slim-buster

# RUN apt update -y && apt install awscli -y
# WORKDIR /app

# COPY . /app
# RUN pip install -r requirements.txt
# RUN pip install --upgrade pip
# RUN pip install --upgrade dill

# CMD ["python3", "app.py"]



# FROM python:3.10
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# EXPOSE 5000
# # COPY . .
# CMD gunicorn --workers=4 --bind 0.0.0.0:5000 app:app




FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]