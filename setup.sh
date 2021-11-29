## Copyright 2021 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.
rm env 

DEFAULT_EMAIL="user@pgadmin4.web"

COOKIE_SECRET=$(pwgen -1s 32)
SECRET_KEY=$(pwgen -1s 32)
REDASH_ADMIN_PASSWORD=$(pwgen -1s 32)
POSTGRES_PASSWORD=$(pwgen -1s 32)
REDASH_DATABASE_URL="postgresql://postgres:${POSTGRES_PASSWORD}@postgres/postgres"
DATABASE_CONNECTION="postgresql://postgres:${POSTGRES_PASSWORD}@localhost:5432/postgres"
PGADMIN4_PASSWORD=$(pwgen -1s 32)
HOST_IP_ADDRESS=$(ip -o route get to 8.8.8.8 | sed -n 's/.*src \([0-9.]\+\).*/\1/p')

## Settings for the postgres data database
POSTGRES_DB_NAME="postgres"
POSTGRES_DB_USER="postgres"

echo "PYTHONUNBUFFERED=0" >> env
echo "REDASH_LOG_LEVEL=INFO" >> env
echo "REDASH_REDIS_URL=redis://redis:6379/0" >> env
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> env
echo "REDASH_COOKIE_SECRET=$COOKIE_SECRET" >> env
echo "REDASH_SECRET_KEY=$SECRET_KEY" >> env
echo "REDASH_ADMIN_EMAIL=$DEFAULT_EMAIL" >> env
echo "REDASH_ADMIN_PASSWORD=$REDASH_ADMIN_PASSWORD" >> env
echo "REDASH_DATABASE_URL=$REDASH_DATABASE_URL" >> env
echo "DATABASE_CONNECTION=$DATABASE_CONNECTION" >> env
echo "PGADMIN_DEFAULT_EMAIL=$DEFAULT_EMAIL" >> env
echo "PGADMIN_DEFAULT_PASSWORD=$PGADMIN4_PASSWORD" >> env

## Run server create_db entrypoint. This runs
## /app/manage.py database create_tables
sudo docker-compose run --rm server create_db

## Run server manage entrypoint. This runs
## /app/manage.py users create_root [admin_email] admin --password [admin_email]
## This command is to create a base line admin user. 
sudo docker-compose run --rm server manage users create_root --password ${REDASH_ADMIN_PASSWORD} ${DEFAULT_EMAIL} admin 

## Retrieve the API Key from the first user we created
ADMIN_API_KEY=$(docker-compose run --rm postgres psql -d $REDASH_DATABASE_URL -c "SELECT api_key FROM public.users" | sed -n '3 p' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

## Run server manage entrypoint. This runs
## /app/manage.py manage ds new --type pg --options 
## This will create the first datasource that will be hold the cell data

### Data source options JSON format to populate the database
DATASOURCE_OPTIONS_JSON_FMT='{"dbname":"%s","host":"%s","port":5432,"password":"%s","user":"%s"}'
DATASOURCE_OPTIONS_JSON_STRING=$(printf "$DATASOURCE_OPTIONS_JSON_FMT" $POSTGRES_DB_NAME $HOST_IP_ADDRESS $POSTGRES_PASSWORD $POSTGRES_DB_USER)

## Add the first datasource
sudo docker-compose run --rm server manage ds new --type pg --options ${DATASOURCE_OPTIONS_JSON_STRING} "battery_archive"

## Run the composed stack
sudo docker-compose up -d 

## Add all of the pre-built queries now
## This needs to be done after bringing up the docker-compose stack. Reliant on nginx being ready
##sudo python3 scripts/redash_queries/query_import.py --api-key=$ADMIN_API_KEY --redash-url=$HOST_IP_ADDRESS
(cd scripts/redash_queries; sudo python3 query_import.py --api-key=$ADMIN_API_KEY --redash-url=http://$HOST_IP_ADDRESS)

