
import requests
from io import BytesIO
import cv2
import numpy as np
import time
import csv
from datetime import datetime

#Change this ------------------------------------------------
ip_addr = '192.168.0.245'
#------------------------------------------------------------
stream_url = 'http://' + ip_addr + ':81/stream'


print_username = True

while print_username == True:



    res = requests.get(stream_url, stream=True)

    for chunk in res.iter_content(chunk_size=100000):

        if len(chunk) > 100:
            try:
                start_time = time.time()
                img_data = BytesIO(chunk)
                cv_img = cv2.imdecode(np.frombuffer(img_data.read(), np.uint8), 1)
                height_image, width_image, channels_image = cv_img.shape
                print(f'image dimensions (pixels):, height =  {height_image}, width = {width_image}')
                #cv_img = cv2.flip(cv_img, 0)
                #cv_img = cv2.flip(cv_img, 1)
                Thermometer_image = cv_img
                for_save = cv_img

                cv2.imshow("OpenCV", Thermometer_image)

                #I added a delay because I was having problems with the 1200 x 1600 images

                cv2.waitKey(500)








                Save_name = "/Users/damianwilliams/Desktop/thermometer_test.jpg"
                cv2.imwrite(Save_name, Thermometer_image)

                print_username = False

                break

            except Exception as e:
                print(e)

            continue
