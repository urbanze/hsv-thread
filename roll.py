import cv2
import numpy as np


for i in range(1, 13):
	path = "original/m" + str(i) + ".jpg"
	img = cv2.imread(path)

	
	path = "misc/m" + str(i) + "_0" + ".jpg"
	cv2.imwrite(path, img)
	
	for j in range(0, 3):
		img = cv2.rotate(img, 2)
		
		path = "misc/m" + str(i) + "_" + str(j+1) + ".jpg"
		cv2.imwrite(path, img)
	


cv2.destroyAllWindows()
print("OK")
