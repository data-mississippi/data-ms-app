FROM python:3.8.3-alpine

# Install curl, node, & yarn
RUN apk add --update nodejs \
    && apk add yarn \
    && apk add npm
# RUN apt-get update \
#   && apt-get -y install curl \
#   && curl -sL https://deb.nodesource.com/setup_12.x | bash \
#   && apt-get install nodejs \
#   && curl -o- -L https://yarnpkg.com/install.sh | bash

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /app/backend

# Install Python dependencies
COPY ./backend/requirements.txt /app/backend/
RUN pip install --upgrade -r requirements.txt

# Install JS dependencies
WORKDIR /app/frontend

COPY ./frontend/package.json ./frontend/yarn.lock /app/frontend/
RUN npm install

# Add the rest of the code
COPY . /app/

# Build static files
RUN npm run-script build

# Have to move all static files other than index.html to root/
# for whitenoise middleware
WORKDIR /app/frontend/build

RUN mkdir root && mv *.ico *.js *.json root

# Collect static files
RUN mkdir /app/backend/staticfiles

WORKDIR /app

RUN DJANGO_SETTINGS_MODULE=app.settings.production \
  SECRET_KEY=SECRET_KEY \
  python3 backend/manage.py collectstatic --noinput

EXPOSE $PORT

# add and run as non-root user
RUN adduser -D sam
USER sam

#CMD python3 backend/manage.py runserver 0.0.0.0:$PORT

#gonna get postgres working before i bother with gunicorn

# CMD gunicorn backend.app.wsgi --bind 0.0.0.0:$PORT
CMD gunicorn backend.app.wsgi --bind 0.0.0.0:$PORT

#this command returns the error but also reaches wsgi.py
#CMD gunicorn backend.app.wsgi --bind 0.0.0.0:$PORT
