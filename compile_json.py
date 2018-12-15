import os
import json
from titlecase import titlecase

print('Running entry compiler...')
path = './entries_in'


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, text):
    with open(file_path, 'w') as file:
        return file.write(text)

def get_entry(entry_path):
    return (json.loads(read_file(entry_path + '/metadata.json')), read_file(entry_path + '/entry.md'))

entries = []
categories = [c['slug'] for c in json.loads(read_file('./categories.json'))['categories']]

files = os.listdir(path)
for name in files:
    if os.path.isdir(path + '/' + name):
        print('Processing: ' + name)
        metadata, entry_markdown = get_entry(path + '/' + name)
        metadata['id'] = len(entries)
        metadata['slug'] = name
        entries.append(metadata)

        entry = dict(metadata)
        entry['body'] = entry_markdown

        write_file('./entries/' + entry['slug'] + '.json', json.dumps({"entry": entry}))

        if metadata['category'] not in categories:
            print('WARNING: found unrecognised category - ' + metadata['category'])

write_file('./entries.json', json.dumps({"entries": entries}))

print('Processed: ' + str(len(entries)) + ' entries')