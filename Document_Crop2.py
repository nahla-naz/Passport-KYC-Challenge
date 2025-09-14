import logging
import traceback
import cv2
import numpy as np
import imutils




class Edge_detect_Crop():

    ''' Class to Crop document using Edge detection '''

    def predict(self, path):

        try:

            image = cv2.imread(path)

            if image is None:
                print(f"Failed to load image at path: ")
                return None  # or raise an exception

            orig = image.copy()

            ## Preprocessing
            image = cv2.resize(image, (900, 600))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 10, 100)
            edged = cv2.dilate(edged, np.ones((5, 5), np.uint8))

            #cv2.imshow("Edges", edged)
            #cv2.waitKey(0)

            ## Get contours
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            if len(cnts) == 0:
                print("No contours found.")
                return

            # Collect all areas > 1000
            area_contours = [(cv2.contourArea(c), c) for c in cnts if cv2.contourArea(c) > 1000]

            if not area_contours:
                print("No contours with area > 1000")
                return

            ## Get mean of areas of all contours
            areas = [a for a, _ in area_contours]
            mean_area = np.mean(areas)

            #print(f"Mean area: {mean_area}, Max area: {max_area}")

            # Select the first contour between mean and max area
            selected_cnt = None
            for area, cnt in area_contours:
                #print(f"Checking contour area: {area}")
                if  area > mean_area or area == mean_area:
                    selected_cnt = cnt
                    #print(f"Selected contour area: {area}")
                    break

            if selected_cnt is None:
                print("No contour found between given values")
                return

            
            display_image = image.copy()

            ## Draw contours for testing
            cv2.drawContours(display_image, [selected_cnt], -1, (0, 255, 0), 2)
            #cv2.imshow("Detected Passport Contour", display_image)
            #cv2.waitKey(0)

            # Scale points back to original image size
            scale_x = orig.shape[1] / 900
            scale_y = orig.shape[0] / 600
            scaled_cnt = selected_cnt.reshape(-1, 2).astype("float32")
            scaled_cnt[:, 0] *= scale_x
            scaled_cnt[:, 1] *= scale_y

            # Crop the image using perspective transform
            cropped_image = self.four_point_transform(orig, scaled_cnt)

            #cv2.imshow("Cropped Document", cropped_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            save_path = "./temp/corrected_output.png"
            # cv2.imwrite(save_path, cropped_image)
            # print(f"Cropped document saved to: {save_path}")

            return cropped_image,save_path
        
        except Exception as e:
                 
                 print("Error occured:",e)
                 traceback.print_exc()
                 logging.error("Error:",e)
                 logging.error("Traceback:", traceback.print_exc)



    def order_points(self, pts):

        try:

            ''' Function to correct the order of the four points '''
            
            rect = np.zeros((4, 2), dtype="float32")

            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            return rect
        
        except Exception as e:
                 
                 print("Error occured:",e)
                 traceback.print_exc()
                 logging.error("Error:",e)
                 logging.error("Traceback:", traceback.print_exc)



    def four_point_transform(self, image, pts):

        try:        
                ''' Function to crop the image using Perspective transform'''
                
                ## If contour has more than 4 points, approximate
                if len(pts) > 4:
                    peri = cv2.arcLength(pts, True)

                    ## Approximate contour to a polygon
                    approx = cv2.approxPolyDP(pts, 0.02 * peri, True)

                    ## if we get 4 points
                    if len(approx) == 4:
                        pts = approx.reshape(4, 2)
                    else:
                        ## Else draw a rectangle with 4 points
                        x, y, w, h = cv2.boundingRect(pts.astype(int))
                        return image[y:y+h, x:x+w]

                ## Make the points in order - top-left, top-right, bottom-right, bottom-left
                rect = self.order_points(pts)
                (tl, tr, br, bl) = rect

                ## Calculate width of new image
                widthA = np.linalg.norm(br - bl)
                widthB = np.linalg.norm(tr - tl)
                maxWidth = max(int(widthA), int(widthB))

                ## Calculate height of new image
                heightA = np.linalg.norm(tr - br)
                heightB = np.linalg.norm(tl - bl)
                maxHeight = max(int(heightA), int(heightB))

                dst = np.array([
                    [0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]
                ], dtype="float32")
                
                ## Get perspective transform matrix
                M = cv2.getPerspectiveTransform(rect, dst)

                ## Get transformed image
                warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

                return warped
        
        except Exception as e:
                 
                 print("Error occured:",e)
                 traceback.print_exc()
                 logging.error("Error:",e)
                 logging.error("Traceback:", traceback.print_exc)

