import io, subprocess, sqlite3, collections, datetime, re, sys, operator


def run(args, db):
 cmd = 'mount'
 table = 'mount'

 out_structure = 'device mountpoint type options'.split()

 class Column:
  def __init__(s, **kwargs):
   for k, v in kwargs.items():
    setattr(s, k, v)

 columns = []
 for field in out_structure:
  columns.append(Column(field=field, type='text'))

 bout = subprocess.check_output([cmd] + args)
 out_lines = bout.decode(errors='surrogate').split('\n')
 out_lines.pop()

 sql = 'CREATE TABLE {table} ({columns})'.format(table=table, columns=','.join(['{} {}'.format(col.field, col.type) for col in columns]))
 db.execute(sql)
 for line in out_lines:
  m = re.match(r'^(.*)\son\s(.*)\stype\s(.*)\s\((.*)\)$', line)
  vals = m.groups()
  assert len(vals) == len(columns), 'parsed line has {} matches instead of {}'.format(len(vals), len(columns))

  q_marks = ','.join('?' * len(vals))
  db.execute('INSERT INTO {table} VALUES ({q})'.format(table=table, q=q_marks), tuple(vals))

