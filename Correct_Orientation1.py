import base64
import logging
import traceback
import cv2
import numpy as np
from PIL import Image
import pytesseract

class Edge_detect_tesseract():

    
    
    def ndarray_to_base64(self,ndarray):
            
            ''' Convert image to Base64 string'''
            try:
                _, buffer = cv2.imencode('.png', ndarray)
                encoded = base64.b64encode(buffer).decode('utf-8')
                return encoded
            
            except Exception as e:
         
                print("Error:",e)
                traceback.print_exc()
                logging.error("Error:",e)
                logging.error("Traceback:", traceback.print_exc)


    def predict(self, path):
        
           
        ''' Function to Correct text orientation of document using Pytesseract '''

        ## NOT USED
        ## Pytesseract not used to correct orientation as accuracy was low

       

        try:
            image = cv2.imread(path)

            if image is None:
                print(f"[ERROR] Failed to load image at path: {path}")
                return None  
        
            orig = image.copy()

            ## Preprocessing 
            image1 = cv2.resize(image, (900, 600))
            gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 10, 200)
            

            cv2.imwrite("./temp/corrected_output.png",edged)

        
            try:
                ## Pytesseract - Orientation and script detection
                osd = pytesseract.image_to_osd('./temp/corrected_output.png', output_type='dict')


                print(osd)
                rotation_angle = osd.get("rotate", 0)

                #print(f"Detected rotation angle: {rotation_angle}°")
                
            except pytesseract.TesseractError as e:
                print(f"[WARN] Orientation detection failed: {e}")
                rotation_angle = 0  

            

            if rotation_angle != 0:

                ## Get image dimensions
                (h, w) = image.shape[:2]
                ## Get center
                center = (w // 2, h // 2)

                ## Get rotation matrix for rotating image - counter clockwise
                matrix = cv2.getRotationMatrix2D(center, -rotation_angle, 1.0)

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
                
                ## if rotation angle = 0
                rotated = image


            cv2.imwrite("./temp/corrected_output.png", rotated)

            

            return rotated
        
        except Exception as e:
         
                print("Error:",e)
                traceback.print_exc()
                logging.error("Error:",e)
                logging.error("Traceback:", traceback.print_exc)

            


