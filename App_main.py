


''' Run this file to run the FastAPI application for cropping Passport documents and correcting its orientation'''



## Import libraries

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from PIL import Image
import pytesseract  

import shutil  
import os      
import uuid    
import uvicorn

import time

from Correct_Orientation1 import Edge_detect_tesseract
from Correct_Orientation2 import Edge_detect_opencv
from Document_Crop1 import Remove_Bkgrd_Crop
from Document_Crop2 import Edge_detect_Crop
from Check_Size import Check_document_size
from Detect_face import correct_face_orientation

from Save_base64 import save_base64_image

import cv2

import base64
import traceback
import configparser
import logging




# Create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Capture all levels

# Error file handler
error_handler = logging.FileHandler('error_log.log')
error_handler.setLevel(logging.ERROR)
error_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_format)

# Info file handler
info_handler = logging.FileHandler('activity_log.log')
info_handler.setLevel(logging.INFO)
info_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(info_format)

# Add both handlers
logger.addHandler(error_handler)
logger.addHandler(info_handler)



## Reading config file
config = configparser.ConfigParser()
config.read('CONFIG.ini')
ip = config.get('settings', 'ip')
port = config.get('settings', 'port')
port = int(port)


## Folder to store uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Running API...")
logging.info("Running API...")


## SWAGGER UI - URL - To test API
print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Swagger UI available at: http://{ip}:{port}/docs")


## Iinitialising classes
edge_tess_orient = Edge_detect_tesseract()
edge_cv_orient = Edge_detect_opencv()
rem_crop = Remove_Bkgrd_Crop()
edge_crop = Edge_detect_Crop()




app = FastAPI()


@app.post("/upload-image/")


async def upload_image(file: UploadFile = File(...)):

    try:

          
            if not file.content_type.startswith("image/"):
                return JSONResponse(status_code=400, content={"error": "File is not an image."})
            
            print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Image received")
            logging.info("Image received")
            
            ## Generate a unique filename  for uploaded file
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            ## Save the uploaded file 
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

           
            try:
                    
                if(file_path):


                    ###################    PASSPORT DOCUMENT CROP AND ORIENTATION - PIPELINE    ########################


                    ## Check if document is already cropped or not
                    logging.info("Checking whether image needs cropping...")
                    print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Checking whether image needs cropping... " )
                    RET = Check_document_size(file_path)

                    if(RET):

                        ## If image not cropped
                        
                        ## Remove background
                        logging.info("Image not cropped...")
                        logging.info("Removing background of image...")
                        print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} |Removing background of image... " )
                        cropped_, path2 = rem_crop.test(file_path)
                        
                        ## Detect passport and crop
                        logging.info("Cropping Passport from image")
                        print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} |Cropping Passport from image " )
                        cropped2_,path3 = edge_crop.predict(path2)

                        ## Correct orientation of document
                        logging.info("Correcting Passport Orientation...")
                        print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Correcting Passport Orientation... " )
                        oriented = edge_cv_orient.predict(cropped2_)


                    else:
                         
                        ## If image already cropped - correct orientation
                        logging.info("Image already cropped...")
                        logging.info("Correcting orientation...")
                        print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Correcting orientation..." )
                        oriented = edge_cv_orient.predict1(file_path)


                    ## Correct using face orientation
                    logging.info("Correcting Face orientation...")
                    print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Correcting Face orientation..." )
                    corrected = correct_face_orientation(oriented)

                    
                    ## Add padding
                    logging.info("Adding padding...")
                    print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} |Adding padding... " )
                    padded_image = cv2.copyMakeBorder(
                                                          corrected,
                                                            20,
                                                            20,
                                                            20,
                                                            20,
                                                            cv2.BORDER_CONSTANT,
                                                            value=(255,255,255)
                                                        )


                    ## Convert image to base64
                    logging.info("Converting image to Base64 string...")
                    print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Converting image to Base64 string... " )
                    cropped_base64 = edge_tess_orient.ndarray_to_base64(padded_image)

                    
                

            except Exception as e:

                logging.error("Error:",e)
                logging.error("Traceback:", traceback.print_exc)

                return JSONResponse(status_code=400, content={"error": f"Invalid image file. {str(e)} ; {traceback.print_exc()}"})
                
            
            ## Convert Base64 string back to image 
            logging.info("Saving output image...")
            print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Saving output image... " )
            save_base64_image(cropped_base64)


            ## Returning response with Base64 string of image
            
            return {
                "filename": filename,
                "message": "Image uploaded and processed successfully.",
                "image_base64": cropped_base64
                
            }
    

    
    except Exception as e:
         
         print("Error:",e)
         traceback.print_exc()
         logging.error("Error:",e)
         logging.error("Traceback:", traceback.print_exc)


if __name__ == "__main__":


    try:
   
        uvicorn.run("App_main:app", host=ip, port=port , reload=True)

    except Exception as e:
         
         print("Error:",e)
         traceback.print_exc()
         logging.error("Error:",e)
         logging.error("Traceback:", traceback.print_exc)