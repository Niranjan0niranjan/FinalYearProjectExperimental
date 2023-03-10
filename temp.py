import json
import cv2
import numpy as np
# Load an image
img = cv2.imread("carParkImg.jpg")

# Define a global list of lists to store polygon points
polygons = [[]] # Initialize polygons list with an empty sublist

# Define a callback function for mouse events
def draw_polygon(event, x, y, flags, param):
    global polygons

    # If left button is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the point to the last sublist of polygons
        polygons[-1].append([x,y])
        # Draw a small circle on the image
        cv2.circle(img,(x,y),3,(0 ,0 ,255),-1)
        # Show updated image
        cv2.imshow("Image", img)

    # If right button is clicked
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Reshape points of last sublist to fit cv2.polylines()
        pts = np.array(polygons[-1], np.int32).reshape((-1 ,1 ,2))
        # Draw polygon on image
        cv2.polylines(img , [pts], True ,(255, 0, 255) ,2)
        # Show updated image
        cv2.imshow("Image", img)
        
        # Create a new empty sublist for next polygon
        polygons.append([])

    # If middle button is clicked (added by Bing)
    elif event == cv2.EVENT_MBUTTONDOWN:
        # Check if there are any polygons drawn on the image 
        if len(polygons) > 1:
            # Remove the last drawn polygon from the list 
            removed_polygon = polygons.pop()
            # Reshape points of removed polygon to fit cv2.fillPoly()
            pts = np.array(removed_polygon, np.int32).reshape((-1 ,1 ,2))
            # Fill polygon with white color on image 
            cv2.fillPoly(img, [pts], (255, 0, 255))
            # Show updated image 
            cv2.imshow("Image", img)

# Create a window and set mouse callback function
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_polygon)

# Load polygons list from a json file if exists
try:
    with open("polygons.json", "r") as f:
        polygons = json.load(f)
except FileNotFoundError:
    pass

# Show original image or image with polygons if points exist
if polygons:
    for p in polygons:
        p = np.array(p,np.int32).reshape((-1 ,1 ,2))
        cv2.polylines(img,[p],True,(255, 0, 255) , 2)
cv2.imshow("Image", img)
cv2.waitKey(0)

# Save polygons list to a json file before exiting 
with open("polygons.json", "w") as f:
    json.dump(polygons,f)

cv2.destroyAllWindows()