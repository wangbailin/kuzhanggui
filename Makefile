
REBUILD_SQL="drop database rocket; \
			create database rocket;"
rebuild_db:
	echo $(REBUILD_SQL) | mysql -u root -p
	./manage.py syncdb

PORT:=9999
start-uwsgi:
	uwsgi --socket 127.0.0.1:$(PORT) \
		--chdir $(shell pwd) \
		--wsgi-file $(shell pwd)/rocket/wsgi.py \
		--python-path .. \
		--process 1 \
		--daemonize $(shell pwd)/logs/uwsgi.log \
		--pidfile $(shell pwd)/uwsgi.pid \
		--master

reload-uwsgi:
	uwsgi --reload uwsgi.pid

stop-uwsgi:
	uwsgi --stop uwsgi.pid

.PHONY: rebuild_db  start-uwsgi reload-uwsgi stop-uwsgi
