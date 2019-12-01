import cv2
import numpy as np
from threading import Thread
import time


img = 0

class HSV_MASK (Thread):
    
   
    def __init__ (self, img_hsv, low, high, median, dilate, erode, mask, paint):
        Thread.__init__(self)
        self.img_hsv = img_hsv
        self.low = low
        self.high = high
        self.median = median
        self.dilate = dilate
        self.erode = erode
        self.mask = mask
        self.paint = paint
        self.tt = 0


    def run(self):
        kernel = np.ones((3,3), np.uint8)
        
        if (self.mask is 0):
            self.mask = cv2.inRange(self.img_hsv, self.low, self.high)

        
        self.mask = cv2.medianBlur(self.mask, self.median)
        self.mask = cv2.dilate(self.mask, kernel, iterations=self.dilate)
        self.mask = cv2.erode(self.mask, kernel, iterations=self.erode)
        
        contours, h = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        med = 0
        ctr = 0
        for obj in contours:
            area = cv2.contourArea(obj)
            
            if (area > 2000):
                ctr = ctr + 1
                med = med + area
        
        if (ctr > 0):
            med = med/ctr
            
            for obj in contours:
                area = cv2.contourArea(obj)
                
                if (area > med*0.6):
                    self.tt = self.tt + 1
                    x, y, w, h = cv2.boundingRect(obj)
                    global img
                    img = cv2.rectangle(img, (x,y), (x+w, y+h), self.paint, 3)


for p2 in range(0, 4):
    for p1 in range(1, 11):
        st = "misc/m" + str(p1) + "_" + str(p2) + ".jpg"
        print(st)
        img = cv2.imread(st)
            
        #Open & Filter
        #img = cv2.resize(img, (1920, 1080))
        img = cv2.medianBlur(img, 3)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


        
        #Color detectors THREAD
        mask1 = cv2.inRange(img_hsv, (0, 100, 150), (5, 255, 255))
        mask2 = cv2.inRange(img_hsv, (170, 100, 150), (180, 255, 255))
        r_mask = cv2.bitwise_or(mask1, mask2)
        

        r = HSV_MASK(img_hsv, (0, 0, 0), (180, 255, 50), 3, 1, 6, r_mask, (0, 0, 255))
        g = HSV_MASK(img_hsv, (30, 50, 50), (80, 255, 255), 3, 1, 6, 0, (0, 255, 0))
        b = HSV_MASK(img_hsv, (85, 50, 50), (105, 255, 255), 3, 1, 6, 0, (255, 0, 0))
        o = HSV_MASK(img_hsv, (10, 150, 170), (20, 255, 255), 3, 1, 6, 0, (80, 127, 255))
        y = HSV_MASK(img_hsv, (20 , 100, 170), (30, 255, 255), 3, 1, 12, 0, (0, 255, 255))
        p = HSV_MASK(img_hsv, (130, 50, 50), (150, 255, 255), 3, 1, 6, 0, (255, 0, 255))
        k = HSV_MASK(img_hsv, (155, 60, 170), (170, 255, 255), 3, 1, 6, 0, (193, 182, 255))


        tsk_lt = [r, g, b, o, y, p, k]
        for obj in tsk_lt:
            obj.start()
            
        for obj in tsk_lt:
            obj.join()


        img = cv2.resize(img, (1024, 720))
        img = cv2.medianBlur(img, 3)


        tt = 0
        y_pos = 0
        for obj in tsk_lt:
            if obj.tt == 0:
                continue
            
            tt = tt + obj.tt
            y_pos = y_pos + 70
            cv2.putText(img, str(obj.tt), (10,  y_pos), cv2.FONT_HERSHEY_SIMPLEX, 2, obj.paint, 3, cv2.LINE_AA)

        cv2.putText(img, str(tt), (10,  y_pos+70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)



        cv2.imshow("Org", img)
        cv2.waitKey(60000)
        cv2.destroyAllWindows()


        if r.tt != 12 and r.tt > 0:
            print("R: " + str(r.tt))
        if g.tt != 15 and g.tt > 0:
            print("G: " + str(g.tt))
        if b.tt != 31 and b.tt > 0:
            print("B: " + str(b.tt))
        if o.tt != 29 and o.tt > 0:
            print("O: " + str(o.tt))
        if y.tt != 27 and y.tt > 0:
            print("Y: " + str(y.tt))
        if p.tt != 38 and p.tt > 0:
            print("P: " + str(p.tt))
        if k.tt != 14 and k.tt > 0:
            print("K: " + str(k.tt))







