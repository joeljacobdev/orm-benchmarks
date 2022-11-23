#!/bin/sh

PGPASSWORD=joeljacob psql -h 0.0.0.0 -p 9500 -U joel fastapi-sqlalchemy -w -c 'drop database tbench';
PGPASSWORD=joeljacob psql -h 0.0.0.0 -p 9500 -U joel fastapi-sqlalchemy -w -c 'create database tbench';
