REBUILD_SQL="drop database rocket; \
			create database rocket;"
rebuild_db:
	echo $(REBUILD_SQL) | mysql -u root -p && ./manage.py syncdb --traceback

HOST:=0.0.0.0
PORT:=8000

debug:
	./manage.py runserver $(HOST):$(PORT)

start-uwsgi:
	uwsgi --ini uwsgi.ini

stop-uwsgi: 
	uwsgi --stop app.pid

.PHONY: rebuild_db debug start-uwsgi stop-uswgi

