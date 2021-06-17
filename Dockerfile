# This Dockerfile builds the app when it's pushed to Heroku

FROM python:3.8.3-alpine

# Install curl, node, & yarn
RUN apk add --update nodejs \
    && apk add yarn \
    && apk add npm \
    && apk add bash


# install psycopg2 dependencies
RUN apk update \
    && apk add curl build-base gdal gdal-tools postgresql-dev gcc python3-dev musl-dev

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

CMD gunicorn --pythonpath backend app.wsgi --bind 0.0.0.0:$PORT
