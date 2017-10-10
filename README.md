Single page app talking to API talking to postgres DB, in one container each so we can work on local machines and deploy on AWS/GCP.

Don't worry about sign in yet, eventually use Google

Database of members, groups (eg CLPs or wards), events (eg calling about an election) and contacts, where a contact records a call to a person about an event. An event has a target group of people to call (eg everyone in Cotham ward).

Going to site/event (eg momentum.com/election provides first uncalled person. Submitting the outcome (spoken to or didn't answer) gets the next person until there's no-one left in the group to call.

Minimal data about people, groups, events and contacts to start with.

Some random dev notes:

Create the dockerized postgres DB:
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

Run the postgress CLI against the containerized DB:
docker run -it --rm --link some-postgres:postgres postgres psql -h postgres -U postgres

Currently it seems you have to go into psql and "create database redux;" whereas I'm pretty sure I read somewhere that connecting would create the DB if it doesn't already exist.

Run the create_DB script. Then run the import people and import events python scripts if you need test data.

Then start the web server and api:
gunicorn redux_API:api

If using the static index page, also need to start ngnix:
sudo nginx
