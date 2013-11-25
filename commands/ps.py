import io, subprocess, sqlite3, collections, datetime, re, sys


def run(args, db):
 cmd = 'ps'
 table = 'ps'

 out_structure = \
 """pid  tname    time      etime        %cpu      sgi_p     uname     comm    args
    10   10       20        20           10        10        100       20      100500
    pid  tty_name cpu_time  elapsed_time cpu_ratio processor user_name command command_line
    int  text     cpu_time  elapsed_time float     text      text      text    text          """.split('\n')

 ps_out        = out_structure[0].split()
 ps_sizes      = out_structure[1].split()
 ps_names      = out_structure[2].split()
 ps_types      = out_structure[3].split()

 class Column:
  def __init__(s, **kwargs):
   for k, v in kwargs.items():
    setattr(s, k, v)

 columns = [Column(out=out, size=int(size), name=name, type=type) for out, size, name, type in zip(ps_out, ps_sizes, ps_names, ps_types)]

 class elapsed_time:
   # [DD-]hh:mm:ss
  def __init__(s, text):
   s.text = text

  @staticmethod
  def adapter(s):
   digits = list(map(int, list(re.findall('\d+', s.text))))
   ss = digits.pop()
   mm = digits.pop()
   hh = digits.pop() if digits else 0
   dd = digits.pop() if digits else 0
   t = datetime.timedelta(days=dd, hours=hh, minutes=mm, seconds=ss)
   return int(t.total_seconds())

  @staticmethod
  def converter(value):
   return datetime.timedelta(seconds=int(value))

 class cpu_time(elapsed_time):
  pass

 type_map = dict(int=int, float=float, text=str, bytes=bytes)
 for c in [elapsed_time, cpu_time]:
  type_map[c.__name__] = c
  sqlite3.register_adapter(c, c.adapter)
  sqlite3.register_converter(c.__name__, c.converter)

 args.extend(['-o', ','.join(['{}:{}'.format(col.out, col.size) for col in columns])])
 bout = subprocess.check_output([cmd] + args)
 out = io.StringIO(bout.decode(errors='surrogate'))
 out.readline()

 sql = 'CREATE TABLE {table} ({columns})'.format(table=table, columns=','.join(['{} {}'.format(col.name, col.type) for col in columns]))
 db.execute(sql)

 left = 0
 header = []
 for size in ps_sizes:
  right = left + int(size) + 1
  header.append([left, right])
  left = right

 for line in out:
  vals = [line[start:end].strip() for start, end in header]
  vals = [type_map[t](v) for t, v in zip(ps_types, vals)]
  db.execute('INSERT INTO {table} VALUES ({q})'.format(table=table,q=','.join('?'*len(ps_names))), tuple(vals))