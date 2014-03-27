
REBUILD_SQL="drop database rocket; \
			create database rocket;"
rebuild_db:
	echo $(REBUILD_SQL) | mysql -u root -p
	./manage.py syncdb

.PHONY: rebuild_db 
