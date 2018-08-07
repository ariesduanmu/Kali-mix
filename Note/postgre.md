##start postgresql
* service postgresql restart

##set password
* sudo -u postgres psql postgres
* \password postgres
* \q

##create new user
* CREATE USER dbuser WITH PASSWORD ';password';;

##create database
* CREATE DATABASE question OWNER dbuser;

##grant privileges
 GRANT ALL PRIVILEGES ON DATABASE question to dbuser;

psql -U dbuser -d question
