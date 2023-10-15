web: gunicorn bigdatave.wsgi --log-file -
worker: celery worker --app=bigdatave --loglevel=info
beat: celery beat --app=bigdatave --loglevel=info




# Uncomment this `release` process if you are using a database, so that Django's model
# migrations are run as part of app deployment, using Heroku's Release Phase feature:
# https://docs.djangoproject.com/en/4.2/topics/migrations/
# https://devcenter.heroku.com/articles/release-phase
#release: ./manage.py migrate --no-input
