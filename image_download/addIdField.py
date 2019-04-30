import os
import json
import requests

dataPath = os.path.join(os.sep, 'team', 'scratch', 'album-ai', 'data')
albumFile = 'albums.jl'
newAlbumFile = 'albumsId.jl'

numberAlbums = 5
albumsRead = 0

with open(os.path.join(dataPath, albumFile)) as fr:
    with open(os.path.join(dataPath, newAlbumFile), 'a') as fw:
        for album in fr:
            # if albumsRead >= numberAlbums:
            #     break

            albumJson = json.loads(album)
            albumId = albumJson['url'].split('/')[4].split('-')[0]

            albumJson['album_id'] = int(albumId)

            fw.write(json.dumps(albumJson) + '\n')
            albumsRead += 1

    fw.close()
fr.close()