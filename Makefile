SQLITE3 := $(shell sqlite3 --version 2>/dev/null)
CREATE := "CREATE TABLE todo(id INTEGER PRIMARY KEY, description TEXT, start DATETIME, end DATETIME,  status varchar(10), priority varchar(6));"
INSTALL := /usr/bin/install -c
BINDIR := /usr/local/bin/td

prepare:
ifdef SQLITE3
	@echo Installing...
	$(shell echo $(CREATE) | sqlite3 $$HOME/.tdl.db)
else
	@echo Need to install sqlite3
endif

install:
	$(INSTALL) td.py	$(BINDIR)
