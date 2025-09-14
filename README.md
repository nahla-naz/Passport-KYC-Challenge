# Passport-Crop-Orientation-Challenge
Detect Passport from image, crop it and correct its orientation.


PASSPORT DOCUMENT CROP AND ORIENTATION CHALLENGE WITH FASTAPI

Tools used :  OpenCV, Rembg, Mediapipe

Pre-requisites:
1. Python version : 3.11
2. Install all dependencies in requirements.txt

Instructions:

1. Run App_main.py to run the Fast API application

2. To test :

Go to the Swagger URL to test with different Passport document images : " http://127.0.0.1:8000/docs " (Change IP and PORT in CONFIG.ini file if needed)


3. Result image saved as "BASE64_OUTPUT.png" in working directory.

4. Change configuration in CONFIG.ini file - adjust area_threshold based on image quality. (can be decided after testing)



Detailed description: 


    Pipeline for Passport Document crop and Orientation includes:-


    1. Checking Document size using OpenCV contours (Check size.py): The Area of image and Area of document are compared to determine whether the document image is already cropped.

    2. Rembg model for Background removal (Document_Crop1.py): If Document is not cropped, image is sent to Rembg model to turn the background into black colour.

    3. Cropping document using OpenCV contours(Document_Crop2.py):  After removing the background, document is cropped using OpenCV contours.

    4. Correct orientation of Document using OpenCV (Correct_Orientation2.py): After cropping the document, orientation is corrected using cv2.HoughLines

    NOTE: This method was used instead of pytesseract Orientation and Script detection (pytesseract.image_to_osd - in Correct_Orientation1.py ) as accuracy was low.

    5. Face orientation using Mediapipe (Detect_face.py): For further correction of document image, image is rotated until Face is detected.

    6. Padding using OpenCV

    7. Convert image to Base64 string and save the image as BASE64_OUTPUT.png


    Note: Mostly OpenCV methods were used in this challenge because of limited time and dataset availability.

    














