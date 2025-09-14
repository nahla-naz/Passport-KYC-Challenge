





import logging
import traceback
import cv2
import imutils
import numpy as np
import configparser


## Access values from Config file
config = configparser.ConfigParser()
config.read('CONFIG.ini')
area_threshold = config.get('settings', 'Area_threshold')






def Check_document_size(image_path):
        
    try:    

        
        ''' Function to check if the document needs cropping '''

        ## Read image
        image = cv2.imread(image_path)

        if image is None:
            print(f" Failed to load image at path: {image_path}")
            return None  

        orig = image.copy()
        
        ## Get dimensions of image
        height, width = image.shape[:2]
        area_img = height * width

        ## Preprocessing
        image = cv2.resize(image, (900, 600))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 10, 100)
        edged = cv2.dilate(edged, np.ones((5, 5), np.uint8))

        #cv2.imshow("Edges", edged)
        #cv2.waitKey(0)

        ## Get all contours from image
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) == 0:
            print("No contours found.")
            return

        ## Check for contour with area >1000
        area_contours = [(cv2.contourArea(c), c) for c in cnts if cv2.contourArea(c) > 1000]

        if not area_contours:
            print("No contours with area > 1000 found.")
            return

        ## Get mean of contour areas
        areas = [a for a, _ in area_contours]
        mean_area = np.mean(areas)

        #print(f"Mean area: {mean_area}, Max area: {max_area}")

        
        selected_cnt = None
        
        for area, cnt in area_contours:
            #print(f"Checking contour area: {area}")

            ## Selecting first contour greater than mean area
            if  area > mean_area or area == mean_area:
                selected_cnt = cnt
                #print(f"Selected contour area: {area}")
                break

        ## Find difference between area of image and area of contour
        difference = area_img - area

        print("Difference in area:",difference)

        print("AREA THRESHOLD:",area_threshold)

        ## If difference is greater than threshold, Document is not cropped
        ## Default threshold : 800000
        if( difference > int(area_threshold)):  

            print("Document needs cropping...")
            return True
        
        else: 
             
             print("Document already cropped!")
             return False

    except Exception as e:
         
         print("Error:",e)
         traceback.print_exc()
         logging.error("Error:",e)
         logging.error("Traceback:", traceback.print_exc)
