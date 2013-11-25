import io, subprocess, sqlite3, collections, datetime, re, sys, operator


def run(args, db):
 cmd = 'lsof'
 table = 'lsof'

 out_structure = \
 """COMMAND   command          text
    PID       pid              int
    TID       tid              int
    USER      user             text
    FD        file_descriptor  text
    TYPE      type             text
    DEVICE    device           text
    SIZE/OFF  size             int
    NODE      node             text
    NAME      name             text""".split('\n')

 class Column:
  def __init__(s, **kwargs):
   for k, v in kwargs.items():
    setattr(s, k, v)

 columns = []
 for out, field, type in map(lambda s: s.split(), out_structure):
  columns.append(Column(out=out, field=field, type=type))

 args.append('-b')
 args.append('-w')

 bout = subprocess.check_output([cmd] + args)
 out_lines = bout.decode(errors='surrogate').split('\n')
 out_lines.pop()

 header = out_lines.pop(0)
 # finding all columns that consist of spaces:
 spaces = [ix for ix, c in enumerate(header) if c == ' ']
 for line in out_lines:
  spaces = [ix for ix in spaces if line[ix] == ' ']
 # integrating found columns as stars in header line
 header = ''.join('*' if ix in spaces and ((ix-1) not in spaces) else c for ix, c in enumerate(header))
 # appending enough spaces to header
 header += ' ' * (max(map(len, out_lines)) - len(header))
 # removing irrelevant stars
 header = re.sub('\*(\s+\*)', lambda mo: ' ' + mo.group(1), header)
 headers = header.split('*')

 # -i attribute removes TID column
 if header.find('TID') == -1:
  columns.remove(next(filter(lambda col: col.out == 'TID', columns)))

 assert len(headers) == len(columns), 'parsed header has {} columns instead of {}'.format(len(headers),len(columns))

 # print('lsblk ' + ' '.join(args))
 # print(header)
 # print('\n'.join(out_lines))

 sql = 'CREATE TABLE {table} ({columns})'.format(table=table, columns=','.join(['{} {}'.format(col.field, col.type) for col in columns]))
 db.execute(sql)
 for line in out_lines:
  h_start = 0
  h_end = 0
  vals = []
  for h in headers:
   h_end += len(h)
   val = line[h_start:h_end].strip()
   vals.append(val)
   h_start = h_end + 1
   h_end = h_start
  q_marks = ','.join('?' * len(vals))
  db.execute('INSERT INTO {table} VALUES ({q})'.format(table=table, q=q_marks), tuple(vals))

