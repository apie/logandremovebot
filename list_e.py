#!/usr/bin/env python3
from datetime import datetime
from tinydb import TinyDB

# TODO better timedelta display
db = TinyDB('db.json')

def list_entries(table_name, m=5, f=None):
    table = db.table(table_name)
    if m:
        print(f'Showing the {m} most recent entries..', file=f)

    old_date = {}
    old_date_all = None
    # Fetch last 100 for stats calculation
    entries = table.all()[-100:]
    num_entries = len(entries)
    for i, entry in enumerate(entries):
        timestamp, text = entry.values()
        text = text.lower()
        date = datetime.fromtimestamp(int(timestamp))
        difference = date - old_date.get(text) if text in old_date else None
        difference_all = date - old_date_all if old_date_all else None
        old_date[text] = date
        old_date_all = date
        if i >= num_entries - m:
            print(f"{date} ({difference_all} since any, {difference} since last {text}): {text}", file=f)


if __name__ == '__main__':
    for table_name in db.tables():
        print(table_name)
        list_entries(table_name)

