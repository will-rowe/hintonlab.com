The Hinton Lab Website
======
This is the repo for the current version of the **Hinton Lab Website**.
The website is built using Django (Version 1.9) and is designed to run in Docker containers.
The website is currently hosted on a DigitalOcean server and uses an AWS S3 bucket to host static content.

#### Screenshot
![Screenshot software](https://s3-eu-west-1.amazonaws.com/hinton-lab/static/img/misc/hintonlab-screenshot.png "screenshot")

## Visit
* [Version 0.0.1](http://www.hintonlab.com)

## Contributors

### Contributors on GitLab
* [Will Rowe](https://gitlab.com/u/will_rowe)

### Third party libraries and apps
* see [REQUIREMENTS](https://gitlab.com/will_rowe/hintonlab.com/blob/de7a2508ce09f39fb548a326dfe803f51fe66fdc/website/web/requirements.txt) for list of libraries and apps
* credit to [RealPython](https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/) for tutorial on using Docker with Django

## Version
* Version 0.0.1

## Docker set up (development)
Build containers on the virtual machine:
* Build images - `docker-compose build`
* Start services - `docker-compose up -d`
* Create migrations - `docker-compose run web /usr/local/bin/python manage.py migrate`
* Create DB table for cache - `docker-compose run web python manage.py createcachetable HintonLab-website-cache`
* Collect static files - `docker-compose run web /usr/local/bin/python manage.py collectstatic`
* Build Watson index - `docker-compose run web /usr/local/bin/python manage.py buildwatson`

## Docker set up (production)
* Create virtual server to host website - `docker-machine create -d digitalocean --digitalocean-access-token=ADD_YOUR_TOKEN_HERE --digitalocean-region lon1 HintonLab-website`
* Build images - `docker-compose build`
* Start services - `docker-compose -f production.yml up -d`
* Create migrations - `docker-compose -f production.yml run web python -u manage.py migrate --noinput`
* Create DB table for cache - `docker-compose -f production.yml run web python manage.py createcachetable HintonLab-website-cache`
* Collect static files - `docker-compose -f production.yml run web python -u manage.py collectstatic`
* Build Watson index - `docker-compose -f production.yml run web python -u manage.py buildwatson`

## Site set up
Once containers are launched and site is live, the following set up steps must be followed in order to allow users to register:
* Create a superuser (complete with names and email)
* Create groups (lab, collaborators, admin etc.)
* Create sign on account (must be 'hinton.admin')
* Assign existing users to groups
* Create profiles for existing users
* Allow new users to be created by giving out the details for hinton.admin

## Contact
#### Will Rowe
* Homepage: [hintonlab.com](http://www.hintonlab.com)
* e-mail: [Will Rowe @ Liverpool](will.rowe@liverpool.ac.uk)
* Twitter: [@will__rowe](https://twitter.com/will__rowe)

## Notes
* Remember to buildwatson in order to index site for searching
* Make sure the production server's IP is whitelisted for SendGrid!

## ToDo List
* Additional email notifications (add notifications for new posts etc.)
* Clean up and minify site CSS
* Create automated docker builds?
