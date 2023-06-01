# applifting-test-docker

## Prerequisites

### Required

It is assumed you have Docker installed and it can run commands as root.

---

## What's Included

* Flask core application and dependencies
* Postgres database
* Redis - caching/queues
* Adminer - database management
  * Nginx
  * PHP 7.4

---

## Installation

The first time you clone the repo.

```bash
git clone https://github.com/alex-kalanis/applifting-test-docker.git
cd applifting-test-docker                                # into project
docker-compose build                                     # build from sources
docker-compose up -d                                     # start this docker
```

Now install system with simple commands. This also bring the box up.
That may take several minutes. If it doesn't explicitly
fail/quit, then it is still working.

```bash
./install.sh
```

Once the Docker finishes and is ready, you can verify PHP is working at
[http://localhost:23450/](http://localhost:23450/) for python/Flask,
[http://localhost:23450/v1/documentation/](http://localhost:23450/v1/documentation) for swagger documentation
[http://localhost:23459/](http://localhost:23459/) for php/Adminer.

## Default settings

Everything is in docker-compose.yml.

Postgres
* user: applifting-test
* pass: donotremindmeanythingsafeforsicknamingwhenisearchforthat

## Manage

For working with products to offers, you must set some users with their  
tokens first. Then you can add, change or remove existing products. There  
is delayed deletion - you must call delete twice to really remove the  
product. Calling once only disables it.

For user management you have set a master token which allows you to work  
with users. Beware that this token does not allow you to work with products  
and offers. That works only with each user's token. The master token is  
set during installation and can be defined via environment variable in  
docker-compose.

For accessing offers on the remote service you need another master token.  
Ït is also set during installation and it could be defined in docker-compose.

The rest of the work is via REST-api as seen in swagger.
