import base64
import logging
import time
import traceback



def save_base64_image(base64_str, output_path = "BASE64_OUTPUT.png"):
   
    try:
        ''' Function to convert base64 string back to image file '''

        
        if base64_str.startswith("data:image"):
            base64_str = base64_str.split(",", 1)[1]

        image_data = base64.b64decode(base64_str)

        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"{time.strftime('%d-%m-%y %H:%M:%Y')} | Corrected image saved as ./BASE64_OUTPUT.png successfully.")

        return True

    except Exception as e:
        print(f" Failed to save base64 image: {e}")

        logging.error("Error:",e)
        logging.error("Traceback:", traceback.print_exc)
        
        return False
