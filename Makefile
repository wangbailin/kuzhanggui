REBUILD_SQL="drop database rocket; \
			create database rocket;"
rebuild-db:
	echo $(REBUILD_SQL) | mysql -u root -p && ./manage.py syncdb --traceback

HOST:=0.0.0.0
PORT:=8000

debug:
	./manage.py runserver $(HOST):$(PORT)

start-uwsgi:
	uwsgi --ini uwsgi.ini

stop-uwsgi: 
	uwsgi --stop app.pid

console_polyfill=assets/js/console-polyfill.js
$(console_polyfill): bower_components/console-polyfill/index.js
	cp $? $(console_polyfill)

assets: $(console_polyfill)

.PHONY: rebuild-db debug start-uwsgi stop-uswgi 