REBUILD_SQL="drop database rocket; \
			create database rocket;"
rebuild_db:
	echo $(REBUILD_SQL) | mysql -u root -p
	./manage.py syncdb

HOST:=0.0.0.0
PORT:=8000

debug:
	./manage.py runserver $(HOST):$(PORT)

start-uwsgi:
	uwsgi --ini uwsgi.ini

restart-uwsgi: 
	-uwsgi --stop app.pid
	uwsgi --ini uwsgi.ini

.PHONY: rebuild_db debug start-uwsgi restart-uwsgi

