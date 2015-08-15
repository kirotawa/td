### What is it?
	- td is an acronym for TODO that aims to provide a way using just
	  command line for keep a track of activities/todo things.

### Usage:
	usage: td [-h] [-a] [-d DESC] [-S {started,finished,canceled}] [-s START]
          [-e END] [-D] [-i ID] [-p {normal,medium,high}] [--debug] [-v]
          [--list | -ls | -le | -lp | -lS]

	optional arguments:
  	-h, --help            show this help message and exit
  	-a, --add             adds a todo into list
  	-d DESC, --desc DESC  sets a description
  	-S {started,finished,canceled}, --status {started,finished,canceled}
                        sets todo status
  	-s START, --start START
                        sets a start date
  	-e END, --end END     sets a end date=d/m/y format
  	-D, --delete          delete a give todo by id
  	-i ID, --id ID        pass a id to other options
  	-p {normal,medium,high}, --priority {normal,medium,high}
                        sets a priority
  	--debug               provides debug info
  	-v, --version         provies current version
  	--list                list everything todo by id
  	-ls, --lstart         list by start date
  	-le, --lend           list by end date
  	-lp, --lprio          list by priority
  	-lS, --lstatus        list by status

### Dependencies:
	- sqlite3

### INSTALL
	- make prepare
	- sudo make install

