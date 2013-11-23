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
