import os
import json
import requests

def tryCastInt(val):
    try: 
        int(val)
        return True
    except ValueError:
        return False

def checkDups(lst):
    seen = set()
    for x in lst:
        if x in seen: return True
        seen.add(x)
    return False

dataPath = os.path.join(os.sep, 'team', 'scratch', 'album-ai', 'data')
albumFile = 'albums.jl'
albumCoverFolder = 'albumArt'

albumIds = []
with open(os.path.join(dataPath, albumFile)) as f:
    for album in f:

        albumJson = json.loads(album)
        albumId = albumJson['url'].split('/')[4].split('-')[0]
        if not tryCastInt(albumId):
            raise ValueError('albumId not cost to int')
        albumIds.append(albumId)
f.close()

if checkDups(albumIds):
    raise Exception('Duplicates found')
else:
    print('No duplicate ID\'s found')