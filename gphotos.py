import json
import requests
from datetime import datetime

class GooglePhotos():
    def __init__(self):
        with open('gphoto.json', 'r') as file:
            json_file = json.load(file)
            self.refresh_token = json_file['refresh_token']
            self.access_token = None
            self.album_id = json_file['album_id']
            self.client_id = json_file['client_id']
            self.client_secret = json_file['client_secret']
    
    def add_photo(self, photo):
        refresh_token = requests.post('https://oauth2.googleapis.com/token', params=
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token"
            }
        )

        self.access_token = refresh_token.json()['access_token']

        sent_photo = requests.post(
            'https://photoslibrary.googleapis.com/v1/uploads', 
            headers={"X-Goog-Upload-Protocol": "raw", "Content-Type": "application/octet-stream", "Authorization": "Bearer {}".format(self.access_token)},
            data=photo
        )
        sent_photo.raise_for_status()

        now = datetime.now()
        datestring = now.strftime("%m/%d/%Y")

        media_item_req = requests.post(
            'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate',
            headers={"Authorization": "Bearer {}".format(self.access_token)},
            json={
                "albumId": self.album_id,
                "newMediaItems": [
                    {
                        "description": "From {}".format(datestring),
                        "simpleMediaItem": {
                            "fileName": "{}".format(datestring),
                            "uploadToken": sent_photo.text
                        }
                    }
                ]
            }
        )
        media_item_req.raise_for_status()
