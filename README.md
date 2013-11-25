sysql
=====

sysql - use sql queries against output of linux commands

Usage
--------

Display help and list of available commands:

    sysql
    
Display output of ps command:

    sysql ps
    
Query output of lsblk command:

    sysql -q "SELECT device,uuid,filesystem FROM lsblk" lsblk 
    
Query output of several commands:

    sysql -q "SELECT ps.pid, ps.command, ps.elapsed_time, lsof.name FROM ps JOIN lsof ON ps.pid = lsof.pid WHERE name LIKE '%LISTEN%'" ps -e --- lsof -Pni4


Here is why I wrote it:
--------

* No need to remember command syntax to format command output - just select necessary fields in SQL query

* No need to know sed, awk, head, join and other linux commands to manipulate with output - it's all SQLite

* Table data is stored with meaningful column name and type (int, text, float, datetime etc)

* All power of SQL can be used to query output (JOIN, WHERE, GROUP BY etc.)

* To support new command, output parser must be developed only once and then can be shared with community to make life easier

* All supported commands are kept in one place as set of python files, so it is easy to find out how to customize existing parsers or create new ones