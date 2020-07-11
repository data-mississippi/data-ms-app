FROM node:lts as build-deps
# WORKDIR /frontend
# RUN echo "$PWD"
# RUN ls
# COPY ./frontend/package.json ./frontend/yarn.lock ./
# RUN yarn
# COPY ./frontend /frontend
# RUN yarn build

FROM python:3.7

# Install curl, node, & yarn
# CMD apt-get -y install curl \
#   && curl -sL https://deb.nodesource.com/setup_12.x | bash \
#   && apt-get install nodejs \
#   && curl -o- -L https://yarnpkg.com/install.sh | bash

WORKDIR /app/backend
RUN echo "$PWD"
RUN ls

# Install Python dependencies
COPY ./backend/requirements.txt /app/backend/
RUN pip3 install --upgrade pip -r requirements.txt

# Install JS dependencies
WORKDIR /app/frontend

COPY ./frontend/package.json ./frontend/yarn.lock /app/frontend/
CMD $HOME/.yarn/bin/yarn install

# Add the rest of the code
COPY . /app/

# Build static files
CMD $HOME/.yarn/bin/yarn build

# Have to move all static files other than index.html to root/
# for whitenoise middleware
WORKDIR /app/frontend/build

CMD mkdir root && mv *.ico *.js *.json root

# Collect static files
CMD mkdir /app/backend/staticfiles

WORKDIR /app
RUN echo "$PWD"
RUN ls

# COPY . .
# COPY --from=build-deps /frontend/build /app/frontend/build

# WORKDIR /app/frontend/build

# RUN echo "$PWD"
# RUN ls
# RUN mkdir root && mv *.ico *.js *.json root
# RUN mkdir /app/staticfiles

# WORKDIR /app

RUN echo "$PWD"
RUN ls

EXPOSE $PORT
# SECRET_KEY is only included here to avoid raising an error when generating static files.
CMD DJANGO_SETTINGS_MODULE=app.settings.production \
  SECRET_KEY=SECRET_KEY \
  python3 backend/manage.py collectstatic --noinput

WORKDIR /app/backend

RUN echo "$PWD"
RUN ls

CMD python3 backend/manage.py runserver 0.0.0.0:$PORT