HOST:=0.0.0.0
PORT:=8000
REBUILD_SQL="drop database rocket; \
			create database rocket;"
rebuild_db:
	echo $(REBUILD_SQL) | mysql -u root -p
	./manage.py syncdb

debug:
	./manage.py runserver $(HOST):$(PORT)

.PHONY: rebuild_db debug
