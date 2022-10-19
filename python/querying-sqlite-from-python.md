# Querying SQLite from Python

As capable as SQL is, sometimes it's easier to get something done with
a python script. It's super easy to connect to an SQLite database from
python with the [sqlite3 module](https://docs.python.org/3/library/sqlite3.html)
in the standard library and do whatever you need.

```python
import sqlite3
con = sqlite3.connect("cc.db")
cur = con.cursor()
res = cur.execute("<query>")
rows = res.fetchall()
...
```
