#!/bin/sh
# run things inside the python container
# run migrations
echo "Migrate tables and data"
flask db upgrade
echo "Tables migrated"
# then get token from server
echo "Initial tokens"
flask tasks init $MASTER_KEY $MASTER_TOKEN
echo "Got initial token"
# and now add cron to init queuing
echo "Initial queues"
echo '*  *  *  *  *    flask tasks ping' >> /etc/crontabs/root
echo "Set initial queues"
