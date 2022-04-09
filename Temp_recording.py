
import requests
from io import BytesIO
import cv2
import numpy as np
import time
import csv
from datetime import datetime

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,600)
fontScale = 1
fontColor = (0,0,0)
thickness = 2
lineType = 2


# IP address ------------change this------------------------
ip_addr = '192.168.0.245'
#-----------------------------------------------------------

stream_url = 'http://' + ip_addr + ':81/stream'

#Calibration------------change this-------------------------
#temperature value 1
t1_F1 = 80
#pixel location of temperature in y axis 1
t1_P1 = 446
#temperature value 2
t1_F2 = 60
#pixel location of temperature in y axis 2
t1_P2 = 918
#------------------------------------------------------------

# range of blue colors that will be detected based on blue image acquired before
blue_img = cv2.imread("/Users/damianwilliams/Desktop/new_blue.jpg")
hsv = cv2.cvtColor(blue_img, cv2.COLOR_BGR2HSV)
mu, sig = cv2.meanStdDev(hsv)

#Range of blue_values-----Change this -----------
a = 5
#------------------------------------------------

# threshold for rectangle size defined as liquid column size (ignores small areas)________change this______
minArea = 500
#------------------------------------------------


def CalculateTemp(temp1, temp2, pixel1, pixel2, yval):
    pix_per_deg = (pixel2 - pixel1) / (temp2 - temp1)
    pixels_diff = yval - pixel2
    delta_fah = pixels_diff / pix_per_deg
    fahrenheit = temp2 + delta_fah
    celcius = ((fahrenheit - 32) * (5 / 9))
    temps = [celcius,fahrenheit]
    return temps


idx = 0

while True:

    with open("/Users/damianwilliams/Desktop/test_data.csv", "a") as f:
        writer = csv.writer(f, delimiter=",")

    res = requests.get(stream_url, stream=True)

    for chunk in res.iter_content(chunk_size=100000):

        if len(chunk) > 100:
            try:
                start_time = time.time()
                img_data = BytesIO(chunk)
                cv_img = cv2.imdecode(np.frombuffer(img_data.read(), np.uint8), 1)
                height_image, width_image, channels_image = cv_img.shape
                print(f'image dimensions (pixels):, height =  {height_image}, width = {width_image}')
                Thermometer_image = cv_img
                for_save = cv_img

                #I added a delay because I was having problems with the 1200 x 1600 images
                cv2.waitKey(500)

                #Uncomment to see original image
                #cv2.imshow("Original Image", cv_img)

                #Mask for blue color
                therm_hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
                therm_hsv = cv2.inRange(therm_hsv, mu - a * sig, mu + a * sig)

                #Uncomment to check mask
                #cv2.imshow("Check mask", therm_hsv)

                #Smooth and fill masks
                kernel = np.ones((2, 2), np.uint8)
                dilated_image = cv2.dilate(therm_hsv, kernel, iterations=5)

                mask_image = cv2.cvtColor(dilated_image, cv2.COLOR_GRAY2RGB)
                contours, hierarchy = cv2.findContours(image=dilated_image, mode=cv2.RETR_TREE,method=cv2.CHAIN_APPROX_NONE)

                number_regions_found = 0

                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    area = cv2.contourArea(cnt)

                    if area > minArea:
                        Thermometer_image = cv2.rectangle(Thermometer_image, (x, y), (x + w, y + h), (0, 255, 0), 1)
                        mask_image = cv2.rectangle(mask_image, (x, y), (x + w, y + h), (0, 255, 0), 1)


                        #Uncomment to see mask and image with rectangle used to calculate temperature
                        #vis = np.concatenate((mask_image, Thermometer_image), axis=1)
                        #cv2.imshow("Image used for detection", vis)

                        therm_reading_1 = CalculateTemp(t1_F1, t1_F2, t1_P1, t1_P2, y)
                        therm_1_stringC = "%.1f" % round(therm_reading_1[0], 1)
                        print("Therm 1 Calculated_value: " + therm_1_stringC)
                        therm_1_stringF = "%.1f" % round(therm_reading_1[1], 1)
                        print("Therm 1 Calculated_value: " + therm_1_stringF)
                        number_regions_found = 1
                        now = datetime.now()
                        print(now)

                        now = datetime.now()
                        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                        current_time = time.time()
                        for_log = [current_time, dt_string, therm_1_stringC,therm_1_stringF]

                        #Uncomment to save measurements
                        #with open("/Users/damianwilliams/Desktop/test_data.csv", "a") as f:
                        #   writer = csv.writer(f, delimiter=",")
                        #   writer.writerow(for_log)

                        # Create image with annotation
                        place = (f"{dt_string} \n"
                                 f"{therm_1_stringF} F, {therm_1_stringC} C\n")


                        position = (40, 50)
                        text = place
                        font_scale = 1.5
                        color = (255, 0, 0)
                        thickness = 2
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        line_type = cv2.LINE_AA
                        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
                        line_height = text_size[1] + 5
                        x, y0 = position
                        for i, line in enumerate(text.split("\n")):
                            y = y0 + i * line_height
                            Save_image = cv2.putText(for_save,
                                              line,
                                              (x, y),
                                              font,
                                              font_scale,
                                              color,
                                              thickness,
                                              line_type)



                        #Uncomment to see final image
                        #cv2.imshow("Finished Image", Save_image)


                        #Uncomment to save measurements
                        #Save_name = "/Users/damianwilliams/Desktop/Image_set/thermometer_" + str(idx) + ".jpg"
                        #cv2.imwrite(Save_name, Save_image)



                        print(idx)
                        idx = idx + 1





            except Exception as e:
                print(e)
            continue
