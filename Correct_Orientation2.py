import logging
import traceback
import cv2
import numpy as np
from PIL import Image




class Edge_detect_opencv():

    ''' Class to Correct orientation using OpenCV HoughLines '''


    def predict(self, input_image):

        ## METHOD 1

        try:
            image = input_image

            if image is None:
                print(f"[ERROR] Failed to load image")
                return None  

            orig = image.copy()

            ## Preprocessing
            image1 = cv2.resize(image, (900, 600))
            gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 50, 150)

            cv2.imwrite("./temp/corrected_output.png", edged)

            #cv2.imshow("Edges", edged)
            #cv2.waitKey(0)

            ## Detect lines in the image
            lines = cv2.HoughLines(edged, 1, np.pi / 180, 100)
            angles = []

            ## Get angles of detected lines
            if lines is not None:
                for line in lines:
                    rho, theta = line[0]
                    angle = (theta * 180 / np.pi) - 90  

                    # Focus on near-horizontal lines only
                    if -45 < angle < 45:
                        angles.append(angle)
                
                if len(angles) > 0:
                    ## get median rotation angle
                    rotation_angle = np.median(angles)
                    #print(f" Detected rotation angle : {rotation_angle:.2f}°")
                else:
                    #print("No  horizontal lines detected.")
                    rotation_angle = 0
            else:
                #print(" No lines detected.")
                rotation_angle = 0

            ## Rotate the image
            if rotation_angle != 0:
                ## get image dimensions
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)

                ## Get rotation matrix for rotating image - counter clockwise
                matrix = cv2.getRotationMatrix2D(center,- rotation_angle, 1.0)

                ## Get sin and cosine of rotation angle
                cos = np.abs(matrix[0, 0])
                sin = np.abs(matrix[0, 1])
                
                ## Calculate new width and height
                new_w = int((h * sin) + (w * cos))
                new_h = int((h * cos) + (w * sin))

                ## Adjust rotation matrix
                matrix[0, 2] += (new_w / 2) - center[0]
                matrix[1, 2] += (new_h / 2) - center[1]

                ## Rotate the image
                rotated = cv2.warpAffine(
                    image, matrix, (new_w, new_h),
                    flags=cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_CONSTANT,
                    borderValue=(255, 255, 255)  
                )
            else:
                rotated = image

            # cv2.imwrite("./temp/corrected_output.png", rotated)
            # print(f"Saved corrected image to: ./temp/corrected_output.png")

            #result_path = "./temp/corrected_output.png"

            return rotated

        except Exception as e:
         
                print("Error:",e)
                traceback.print_exc()
                logging.error("Error:",e)
                logging.error("Traceback:", traceback.print_exc)
       
        

    def predict1(self, path):

        ## METHOD 2

        try:
            image = cv2.imread(path)

            if image is None:
                print(f" Failed to load image")
                return None  # or raise an exception

            orig = image.copy()

            image1 = cv2.resize(image, (900, 600))
            gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 100, 300)  ## 50 150

            cv2.imwrite("./temp/corrected_output.png", edged)

            #cv2.imshow("Edges", edged)
            #cv2.waitKey(0)

            #  Hough Line Transform to find rotation angle
            lines = cv2.HoughLines(edged, 1, np.pi / 180, 100)
            angles = []

            if lines is not None:
                for line in lines:
                    rho, theta = line[0]
                    angle = (theta * 180 / np.pi) - 90  # Convert from radians to degrees and shift
                    # Focus on near-horizontal lines only
                    if -45 < angle < 45:
                        angles.append(angle)
                
                if len(angles) > 0:
                    rotation_angle = np.median(angles)
                    #print(f" Detected rotation angle : {rotation_angle:.2f}°")
                else:
                    #print("No  horizontal lines detected. ")
                    rotation_angle = 0
            else:
                
                rotation_angle = 0

            # Rotate image to deskew 
            if rotation_angle != 0:
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)

                matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)

                cos = np.abs(matrix[0, 0])
                sin = np.abs(matrix[0, 1])

                new_w = int((h * sin) + (w * cos))
                new_h = int((h * cos) + (w * sin))

                matrix[0, 2] += (new_w / 2) - center[0]
                matrix[1, 2] += (new_h / 2) - center[1]

                rotated = cv2.warpAffine(
                    image, matrix, (new_w, new_h),
                    flags=cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_CONSTANT,
                    borderValue=(255, 255, 255)  # white background
                )
            else:
                rotated = image

            # cv2.imwrite("./temp/corrected_output.png", rotated)
            # print(f"Saved corrected image to: ./temp/corrected_output.png")

            # result_path = "./temp/corrected_output.png"

            return rotated
        
        except Exception as e:
         
                print("Error:",e)
                traceback.print_exc()
                logging.error("Error:",e)
                logging.error("Traceback:", traceback.print_exc)

       

   