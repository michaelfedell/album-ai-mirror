import os
import json
import requests

dataPath = os.path.join(os.sep, 'team', 'scratch', 'album-ai', 'data')
albumFile = 'albums.jl'
albumCoverFolder = 'albumArt'

numberAlbums = 5
albumsRead = 0

if not os.path.isfile(os.path.join(dataPath, albumFile)):
    raise FileNotFoundError('The albums.jl file could no be found')

with open(os.path.join(dataPath, albumFile)) as f:
    for album in f:
        # if albumsRead >= numberAlbums:
        #     break

        albumJson = json.loads(album)
        albumId = albumJson['url'].split('/')[4].split('-')[0]
        albumName = albumJson['album']
        artistName = albumJson['artist']
        imageLink = albumJson['image_link']
        
        """ Need to decide how to do genre """
        # Taking first genre for now
        genres = albumJson['genres']
        if len(genres) == 0:
            genre = 'None'
        else:
            genre = genres[0]

        """ Need to check to see if albumId will work """
        # Including artistName, albumName, and genre can result in invalid file names
        # imageName = albumId + '~' + artistName + '~' + albumName + '~' + genre
        imageName = albumId
        imageName += '.jpg'

        with open(os.path.join(dataPath, albumCoverFolder, imageName), 'wb') as image:
            response = requests.get(imageLink)
            if not response.ok:
                raise Exception(response.content)
            image.write(response.content)
        image.close()

        albumsRead += 1
f.close()
