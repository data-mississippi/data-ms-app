##backend
django with a json api

##frontend
react deploy as a static asset by django/whitenoise

##docker
both self-contained apps use docker, and the entire project uses docker

`docker-compose up` to run both at once
`docker run -it -v $PWD/frontend:/app -p 3000:3000 frontend:latest npm start` to run only frontend 
`docker run -v $PWD/backend:/app/backend -p 8000:8000 backend:latest` to run only backend
`docker-compose run --rm backend python3 manage.py startapp app_name` to create a new app module

rebuild image after changes to react package.json 
`docker-compose up --build`

for instance, to add axios, go
```
docker-compose run --rm frontend npm add axios
docker-compose run --rm frontend npm install tailwindcss npm-run-all chokidar-cli
docker-compose down
docker-compose up --build
```
Since we're changing project settings, we'll need to stop our Docker Compose processes (either ctl+c or `docker-compose stop` in a separate tab) and start it again with `docker-compose up`. 
`docker-compose down` works to stop too



access the backend at localhost:8000
access the frontend at localhost:3000
docker/create-react-app weirdness :(
- https://stackoverflow.com/questions/60790440/docker-container-exiting-immediately-after-starting-when-using-npm-init-react-ap
- https://github.com/facebook/create-react-app/issues/8688

$ docker ps # get the id of the running container
$ docker stop <container> # kill it (gracefully)


In the backend/hello_world, which is our project directory, create a settings folder (as usual, with a __init__.py inside to make it a module), move the existing settings.py into it, and rename it base.py. This will be the collection of base app settings that all environments will inherit. To make sure we don't accidentally deploy with unsafe settings, cut the following code from base.py, and paste it into a newly-created development.py:

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "<some long series of letters, numbers, and symbols that Django generates>"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["backend"]

Double check now: have those lines of code disappeared from base.py? Good. We are slightly less hackable. At the top of the file, add the line from hello_world.settings.base import *. What the * import from base does is make all of those settings that are already defined in our base available in development as well, where we're free to overwrite or extend them as necessary.

Since we're embedding our settings files a little deeper in the project by moving them into a settings subdirectory, we'll also need to update BASE_DIR in base.py to point to the correct directory, which is now one level higher (relatively speaking). You can wrap the value in one more os.path.dirname call, but I find the following a little easier to read:

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

Django determines which module to use when running the app with the environment variable DJANGO_SETTINGS_MODULE, which should be the module path to the settings that we want to use. To avoid errors, we update the default in backend/hello_world/wsgi.py to 'hello_world.settings.base', and add the following to our backend service in docker-compose.yml:

environment:
  - DJANGO_SETTINGS_MODULE=hello_world.settings.development


generate secret token
`python3 -c 'import secrets; print(secrets.token_urlsafe(32))'`

`heroku config:set PRODUCTION_HOST='secret-dusk-91150.herokuapp.com' SECRET_KEY=secret_hair_key DJANGO_SETTINGS_MODULE=app.settings.production --app=secret-dusk-91150`

We also need to run `heroku stack:set container` in the terminal to tell our Heroku app to use Docker rather than one of Heroku's language-specific build packs. Now, deploying is as easy as running git push heroku master (if you're on the master branch; otherwise, run git push heroku <your branch>:master).


--app=secret-dusk-91150
`heroku update`
`heroku logs --tail --app=secret-dusk-91150`

### postgres
`heroku addons:create heroku-postgresql:hobby-dev -a secret-dusk-91150`
`heroku run python backend/manage.py makemigrations -a secret-dusk-91150`
`heroku run python backend/manage.py migrate -a secret-dusk-91150`

check on it 
`heroku pg:psql -a secret-dusk-91150`

https://stackoverflow.com/questions/59719175/where-to-run-collectstatic-when-deploying-django-app-to-heroku-using-docker

https://www.reddit.com/r/django/comments/grdk7z/django_docker_heroku_and_a_staticfiles_hell/

https://stackoverflow.com/questions/62101834/django-static-files-are-not-loaded-when-deploying-on-heroku-using-docker-and-whi

https://devcenter.heroku.com/articles/django-assets#collectstatic-during-builds



`git push heroku master DEBUG=*`

https://devcenter.heroku.com/articles/django-assets

https://devcenter.heroku.com/articles/heroku-cli#troubleshooting

https://testdriven.io/blog/deploying-django-to-heroku-with-docker/#whitenoise


https://github.com/cfranklin11/docker-django-react/tree/production-heroku

https://dev.to/englishcraig/docker-django-react-building-assets-and-deploying-to-heroku-24jh?signin=true


tailwind
https://daveceddia.com/tailwind-create-react-app/


Build the image:

$ docker-compose build

Once the image is built, run the container:

$ docker-compose up -d

Navigate to http://localhost:8000/ to again view the welcome screen.

    Check for errors in the logs if this doesn't work via docker-compose logs -f.




  Build the new image and spin up the two containers:

$ docker-compose up -d --build



Run the migrations:

$ docker-compose exec web python manage.py migrate --noinput





    Get the following error?

    django.db.utils.OperationalError: FATAL:  database "hello_django_dev" does not exist

    Run docker-compose down -v to remove the volumes along with the containers. Then, re-build the images, run the containers, and apply the migrations.


goood things to do with docker
https://mherman.org/presentations/dockercon-2018


Ensure the default Django tables were created:

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
