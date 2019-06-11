#!/usr/bin/env bash
MYSQL_USER='highmood_user'
MYSQL_PASS='Vulinm7jGQN@$@#$@#BnW'

mysql --user=$MYSQL_USER --password=$MYSQL_PASS --init-command='use highmood; show tables;'
