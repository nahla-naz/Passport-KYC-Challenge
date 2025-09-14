import logging
import time
import traceback

import cv2
import mediapipe as mp

import cv2

mp_face_detection = mp.solutions.face_detection



def detect_face_mediapipe(image):

    try:

        ''' Function to detect and crop face'''
    
        if image is None:
            raise ValueError("Image not found")

        ## Convert to grayscale
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        ## Detect face using mediapipe
        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
            results = detector.process(rgb)

            if results.detections:
                
                ## Crop face 
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    h, w = image.shape[:2]
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    width = int(bbox.width * w)
                    height = int(bbox.height * h)

                    face_crop = image[y:y+height, x:x+width]
                    #cv2.imwrite("face_crop_mediapipe.png", face_crop)
                    return face_crop
            else:
                print("No face detected")
                return None
            
    except Exception as e:
         
                print("Error:",e)
                traceback.print_exc()
                logging.error("Error:",e)
                logging.error("Traceback:", traceback.print_exc)



def correct_face_orientation(input_image):

    try:
            '''  Function to correct document orientation based on face detection'''

            frame0 = input_image

            org = frame0.copy()

            i = 0

            while True:

                ## Check if face can be detected
                cropped_frame = detect_face_mediapipe(frame0)

                if(cropped_frame is None):
                    

                    i += 1

                    ## If face not detected, then rotate image

                    frame0 = cv2.rotate(frame0, cv2.ROTATE_90_CLOCKWISE)
                    


                    ## If face not detected after 5 rotations , return original frame
                    if(i>5):
                        
                        angle = 0

                        frame0 = org

                        break
                    

                else:

                    ## If face detected, return rotated frame

                    angle = i*90

                    
                    break

            return frame0
    
    except Exception as e:
         
                print("Error:",e)
                traceback.print_exc()
                logging.error("Error:",e)
                logging.error("Traceback:", traceback.print_exc)





    


               
                
                
                
                  
       