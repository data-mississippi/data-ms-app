## Notes
This application has been a place for me to learn Docker, Django, mapping, and ETL. The following are some notes from that.

## helpful docker commands
### run django manage commands
```bash
docker-compose run --rm backend python3 manage.py shell
```

### rebuild image after changes to react package.json or django requirements.txt, environment variables, etc:
```
$ docker-compose up --build
```

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

for example, to add axios, go:
```
$ docker-compose run --rm frontend npm add axios
$ docker-compose down
$ docker-compose up --build
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
```
run tests
docker-compose run --rm backend python3 manage.py test
```

debug a container or stop it
```
$ docker ps # get the id of the running container
$ docker stop <container> # kill it (gracefully)
```

Since we're changing project settings, we'll need to stop our Docker Compose processes (either ctl+c or `docker-compose stop` in a separate tab) and start it again with `docker-compose up`. 
`docker-compose down` works to stop too



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

