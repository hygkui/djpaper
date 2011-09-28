#!/bin/sh
./manage.py dbshell < droptables
./manage.py syncdb
./manage.py runserver
