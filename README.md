# MoMonitor-Heroku

Please see the following links to understand how Momonitor works.

* [Momonitor Main Project](https://github.com/mopub/momonitor)
* [Momonitor Guide](http://mopub.github.io/momonitor/)

This is a fork from [Momonitor](https://github.com/mopub/momonitor) to deploy Momonitor in Heroku.

Why Heroku
-------------

Deployment is fast and easy. Momonitor consists of the web app, the scheduler and also the service checks. 
Using heroku, we can easily seperate these 3 components scale up accordingly. 

You can add user:password for graphite's url authentication under environment config GRAPHITE_USER and GRAPHITE_API.
If there's no authentication, you can leave it as it is. We use aws for serving static files.


    heroku create
    heroku addons:add mandrill:starter
    heroku addons:add memcachier:dev
    heroku addons:add redistogo:nano
    
    heroku config:add AWS_ACCESS_KEY_ID='YOUR_AWS_ACESS_KEY_ID'
    heroku config:add AWS_SECRET_ACCESS_KEY='YOUR_AWS_SECRET_ACCESS_KEY'
    heroku config:add AWS_STORAGE_BUCKET_NAME='YOUR_AWS_STORAGE_BUCKET_NAME'
    
    heroku config:add SECRET_KEY='RANDOM_KEY'
    heroku config:add UMPIRE_ENDPOINT='UMPIRE_ENDPOINT'
    heroku config:add UMPIRE_USER='UMPIRE_USER'
    heroku config:add UMPIRE_API='UMPIRE_API'
    
    heroku config:add GRAPHITE_ENDPOINT='GRAPHITE_ENDPOINT'
    heroku config:add GRAPHITE_USER='GRAPHITE_USER'
    heroku config:add GRAPHITE_API='GRAPHITE_API'
    
    heroku config:add DOMAIN='DOMAIN'
    heroku config:add GOOGLE_WHITE_LISTED_DOMAINS='GOOGLE_WHITE_LISTED_DOMAINS'
    
    git push heroku master
    heroku ps:scale web=1 clock=1 worker=1
    heroku run python manage.py syncdb
    heroku run python manage.py migrate



