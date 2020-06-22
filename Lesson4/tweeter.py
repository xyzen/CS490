import sys
from twython import Twython
from picamera import PiCamera
from time import sleep

apiKey = "sQQEszZ8Gwy8SVnZeeuLMF40C"
apiSecret = "GWdTgpS7p9t6P7ZCC3QdRFTMBl75NyTVQwodz20sOIV85n7ooo"
accessToken = "1271178365219766272-R5eAnVIeIRDFdlYpp7namiweyFk3Zp"
accessTokenSecret = "1XxHeiD9vL851hbbuuXoJHMuCTvPEqymbdtYCopQ1UxdG"

api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

camera = PiCamera()

for i in range(5):
    camera.start_preview()
    sleep(5)
    camera.capture('./image{}.jpg'.format(i))
    camera.stop_preview()
    sleep(5)
    photo = open('./image{}.jpg'.format(i), 'rb')
    response = api.upload_media(media=photo)
    api.update_status(status="Image{} from Raspberry Pi Camera".format(i), media_ids=[response['media_id']])
    
