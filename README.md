# Data Mississippi core app
This **work in progress** application has two parts: a Django `/backend` with and a React `/frontend`. A Django backend serves JSON and a React frontend. The React frontend gets data from the JSON backend.

Deployment and development is managed by Docker. The Docker build process writes the React files to a static build so the backend can serve the React application. This approach is [based on this guide](https://dev.to/englishcraig/creating-an-app-with-docker-compose-django-and-create-react-app-31lf), with our own quirks to make it work. 

## Local Development Setup
System Requirements:
- Docker

### Load data
TODO: make this work...
```bash
docker-compose run --rm backend make
```

### Build app image
```bash
docker-compose build
```

### Run the app
```bash
docker-compose up
```

### Django and React
Access the Django admin section and JSON APIs at `localhost:8000`, and access the frontend at `localhost:3000`. (TODO: fix the bugs caused by this.)

docker/create-react-app weirdness :(
- https://stackoverflow.com/questions/60790440/docker-container-exiting-immediately-after-starting-when-using-npm-init-react-ap
- https://github.com/facebook/create-react-app/issues/8688


## ETL

create the county data:
```bash
docker-compose run --rm backend python3 manage.py load_county_data
```

## Heroku
The app is deployed on Heroku. They have a CLI tool to manage it.

Deploy:
```
$ git push heroku master --app=secret-dusk-91150
```

Sometimes you need some more logging:
```
git push heroku master DEBUG=*
```

Push different branch for deployment:
```
$ git push heroku <your branch>:master
```

Log stream:
```
$ heroku logs --tail --app=secret-dusk-91150
```

You can set config like this:
```
$ heroku config:set PRODUCTION_HOST='secret-dusk-91150.herokuapp.com' SECRET_KEY=secret_hair_key DJANGO_SETTINGS_MODULE=app.settings.production --app=secret-dusk-91150
```

### Note!
When setting up Docker, we needed to run `heroku stack:set container` in the terminal to tell our Heroku app to use Docker rather than one of Heroku's language-specific build packs.


## Postgres on Heroku
Load fixtures and make migrations:
```
heroku run python backend/manage.py loaddata backend/app/fixtures/db.json
heroku run python backend/manage.py makemigrations -a secret-dusk-91150
heroku run python backend/manage.py migrate -a secret-dusk-91150
```

Check on it!
```bash
heroku pg:psql -a secret-dusk-91150
```

Created postgres DB on heroku like this:
```bash
heroku addons:create heroku-postgresql:hobby-dev -a secret-dusk-91150
```

Create admin superuser:
```bash
heroku run python backend/manage.py createsuperuser
```

Ensure the default Django tables were created:
```bash
docker-compose exec db psql --username=postgres --dbname=postgres
postgres=# \c postgres
postgres=# \dt

docker volume inspect data-ms-app_postgres_data

debug docker
RUN echo "$PWD"

list containers
docker ps 
```

Test entire project's docker build
```
docker build -t web:latest .
docker run -d --name django-heroku -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```

## TailwindCSS
The React application uses TailwindCSS. It required a build script that was [inspired by this guide](https://daveceddia.com/tailwind-create-react-app/). Tailwind writes a generated CSS file based on whatever Tailwind classes the application uses. PurgeCSS removes any unused Tailwind classes before writing to the build folder. PostCSS finishes the build.


