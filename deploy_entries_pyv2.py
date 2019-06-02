import sqlite3
import os
import json
from os.path import expanduser
home = expanduser("~")
print(str(home))

entries_dirs = os.listdir("entries")
entries = []
categories = []

for entry in entries_dirs:
    body = open('entries/' + entry + '/body.md', 'r').read()
    metadata = json.load(open('entries/' + entry + '/metadata.json', 'r'))
    print(metadata['title'])

    entries.append((metadata['id'], metadata['title'], metadata['snippet'], body, metadata['date'], metadata['category'], ''))
    categories.append((metadata['category'], metadata['category'].title(), metadata['colour']))

conn = sqlite3.connect(str(home) + '/.picoblog/picoblog.db')

c = conn.cursor()

create = open('create.sql', 'r').read()

c.executescript(create)
conn.commit()

c.executemany('INSERT OR REPLACE INTO Entry VALUES (?, ?, ?, ?, ?, ?, ?)', entries)
conn.commit()

c.executemany('INSERT OR REPLACE INTO Category VALUES (?, ?, ?)', categories)
c.close()
conn.commit()
conn.close()
