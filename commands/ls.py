import io, subprocess, sqlite3, collections, datetime, re, sys, operator


def run(args, db):
 cmd = 'ls'
 table = 'ls'

 args.append('-i')
 args.append('-lU')
 args.append('-Q')
 args.extend(['--time-style', 'full-iso'])
 args.append('--indicator-style=classify')
 out_structure = """[index] permissions num [user] [group] size time_mod  filename refers_to type
                    int     text        int text   text    int  time_mod  text     text      text""".split('\n')

 class Column:
  def __init__(s, **kwargs):
   for k, v in kwargs.items():
    setattr(s, k, v)

 columns = []
 for field, type in zip(out_structure[0].split(), out_structure[1].split()):
  columns.append(Column(field=field, type=type))

 def time_mod_converter(bvalue):
  # 2013-11-24 04:05:05.498121677 +0200
  time_format = '%Y-%m-%d %H:%M:%S.%f %z'
  # only 6 digits supported by %f
  txt = re.sub(r'\.(\d{6})\d{3}\s', lambda m: '.{} '.format(m.group(1)), bvalue.decode())
  t = datetime.datetime.strptime(txt, time_format)
  return t

 sqlite3.register_converter('time_mod', time_mod_converter)

 bout = subprocess.check_output([cmd] + args)
 out_lines = bout.decode(errors='surrogate').split('\n')
 out_lines.pop(0)
 out_lines.pop()

 sql = 'CREATE TABLE {table} ({columns})'.format(table=table, columns=','.join(['{} {}'.format(col.field, col.type) for col in columns]))
 db.execute(sql)
 for line in out_lines:
  m = re.match(r'^\s*(?P<ix>\d+)\s(?P<perm>.*)\s+(?P<num>\d+)\s(?P<user>\S+)\s(?P<group>\S+)\s+(?P<size>\d+)\s(?P<mod_time>.{35})\s"(?P<filename>.*)"(?P<type>[*/=>@|]?)$', line)

  val_keys = 'ix perm num user group size mod_time filename type'.split()
  vals = list(m.groups())

  # split filename and refers_to
  ix = val_keys.index('filename')
  arr = vals[ix].split('" -> "', 1)+['']
  vals[ix] = arr[0]
  vals.insert(ix + 1, arr[1])

  assert len(vals) == len(columns), 'parsed line has {} matches instead of {}'.format(len(vals), len(columns)-1)

  q_marks = ','.join('?' * len(vals))
  db.execute('INSERT INTO {table} VALUES ({q})'.format(table=table, q=q_marks), tuple(vals))

