# Data Mississippi core app
This **work in progress** application has two parts: a Django `/backend` with and a React `/frontend`. Django serves json and acts as the CDN for the React app. 

Deployment and development is managed by Docker. The Docker build process writes the React files to a static build so the backend can serve the React application. 

# docker
### to run both at once:
```
$ docker-compose up
``` 
### to run only frontend:
```
$ docker run -it -v $PWD/frontend:/app -p 3000:3000 frontend:latest npm start
``` 
### to run only backend:
```
$ docker run -v $PWD/backend:/app/backend -p 8000:8000 backend:latest
``` 
### to create a new app module:
```
$ docker-compose run --rm backend python3 manage.py startapp app_name
```
### rebuild image after changes to react package.json or django requirements.txt, environment variables, etc:
```
$ docker-compose up --build
```

for example, to add axios, go:
```
$ docker-compose run --rm frontend npm add axios
$ docker-compose down
$ docker-compose up --build
```
Or something like this:
```
$ docker-compose up -d --build
```
Run migrations for Django in dev:
```
$ docker-compose exec web python manage.py migrate --noinput
```
If you're ever doing anything with docker-compose volumes and it don't work:
```
docker-compose down -v # removes volumes
```
```
$docker-compose logs -f
```
```
docker-compose run --rm backend python3 manage.py shell
```
```
docker-compose run --rm backend python manage.py dumpdata --exclude=sessions --exclude=messages --exclude=contenttypes --exclude=auth.permission --indent 2 > backend/app/fixtures/db.json
```
```
docker-compose run --rm backend python manage.py loaddata app/fixtures/db.json
```
Since we're changing project settings, we'll need to stop our Docker Compose processes (either ctl+c or `docker-compose stop` in a separate tab) and start it again with `docker-compose up`. 
`docker-compose down` works to stop too

Access the backend at `localhost:8000` and the frontend at `localhost:3000`

docker/create-react-app weirdness :(
- https://stackoverflow.com/questions/60790440/docker-container-exiting-immediately-after-starting-when-using-npm-init-react-ap
- https://github.com/facebook/create-react-app/issues/8688
```
$ docker ps # get the id of the running container
$ docker stop <container> # kill it (gracefully)
```

# Heroku
The app is deployed on Heroku. They have a CLI tool to manage it.

Deploy:
```
$ git push heroku master
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

Update heroku
```
$ heroku update
```


When setting up Docker, we needed to run `heroku stack:set container` in the terminal to tell our Heroku app to use Docker rather than one of Heroku's language-specific build packs.

# Postgress
Make migrations in production:
```
$ heroku run python backend/manage.py makemigrations -a secret-dusk-91150
$ heroku run python backend/manage.py migrate -a secret-dusk-91150
```
Check on it!
```
$ heroku pg:psql -a secret-dusk-91150
```
Created postgres DB on heroku like this:
```
$ heroku addons:create heroku-postgresql:hobby-dev -a secret-dusk-91150
```
Create admin superuser:
```
$heroku run python backend/manage.py createsuperuser
```

# TailwindCSS
The React application uses TailwindCSS. It required a build script that was [inspired by this guide](https://daveceddia.com/tailwind-create-react-app/). He's edited since then, but basically Tailwind must write a generated CSS file based on whatever Tailwind classes the application is using. PurgeCSS removes any unused classes before writing to the build folder. PostCSS finishes the build.


# ETC
## just some links for reference
good things to do with docker
https://mherman.org/presentations/dockercon-2018

https://stackoverflow.com/questions/59719175/where-to-run-collectstatic-when-deploying-django-app-to-heroku-using-docker

https://www.reddit.com/r/django/comments/grdk7z/django_docker_heroku_and_a_staticfiles_hell/

https://stackoverflow.com/questions/62101834/django-static-files-are-not-loaded-when-deploying-on-heroku-using-docker-and-whi

https://devcenter.heroku.com/articles/django-assets#collectstatic-during-builds

https://devcenter.heroku.com/articles/django-assets

https://devcenter.heroku.com/articles/heroku-cli#troubleshooting

https://testdriven.io/blog/deploying-django-to-heroku-with-docker/#whitenoise

https://github.com/cfranklin11/docker-django-react/tree/production-heroku

https://dev.to/englishcraig/docker-django-react-building-assets-and-deploying-to-heroku-24jh?signin=true



Ensure the default Django tables were created:
```
docker-compose exec db psql --username=postgres --dbname=postgres
postgres=# \c postgres
postgres=# \dt

docker volume inspect data-ms-app_postgres_data

debug docker
RUN echo "$PWD"

list containers
docker ps 

test entire project's docker build
$ docker build -t web:latest .
$ docker run -d --name django-heroku -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```