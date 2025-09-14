import io
import logging
import traceback
from PIL import Image
import numpy as np
from rembg import new_session, remove





class Remove_Bkgrd_Crop():
        

        ''' Class to Remove background using rembg '''

        def __init__(self):

                ## Load model 
                self.session = new_session(model_name="u2netp")  


        def remove_background(self, pil_image):

            try:
                

                if pil_image is None:
                    print(f" Failed to load image at path")
                    return None  
                
                ## Check if image is in RGBA format
                if pil_image.mode != "RGBA":
                    pil_image = pil_image.convert("RGBA")

                ## Convert PIL image to bytes
                input_bytes = io.BytesIO()
                pil_image.save(input_bytes, format="PNG")
                input_bytes.seek(0)

                ## Remove background of image using rembg 
                output_bytes = remove(input_bytes.read(), session=self.session)
                output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

                return output_image
            
            except Exception as e:
                 
                 print("Error occured:",e)
                 traceback.print_exc()
                 logging.error("Error:",e)
                 logging.error("Traceback:", traceback.print_exc)


        

        def test(self, input_path, output_path = "./temp/corrected_output.png"):
                
            try:


                # Load the input image
                original = Image.open(input_path)
                #print(f"Loaded image: {input_path} ")

                # Remove background
                result = self.remove_background(original)

                # Save result
                result.save(output_path)
                #print(f"Saved image: {output_path}")

                return result,output_path
        
            except Exception as e:
                    
                    print("Error occured:",e)
                    traceback.print_exc()
                    logging.error("Error:",e)
                    logging.error("Traceback:", traceback.print_exc)


           