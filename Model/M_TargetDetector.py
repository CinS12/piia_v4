"""Pressure injury image class
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>
algorithm author:: Pau Nonell Isach <pau.nonell@students.salle.url.edu>
Class to detect the target in the image.
"""
import cv2
import numpy as np
from pubsub import pub
from PIL import Image
import scipy
import math
from scipy.spatial import distance
import matplotlib.pyplot as plt


class TargetDetector:

    def __init__(self, img):
        self.img_bgr = img.copy()
        self.img_gray = None
        self.px_dist = np.float64(0)
        self.cut_bgr = None
        self.roi = None
        self.image_setup()
        return

    def image_setup(self):
        cimg = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2GRAY)
        self.img_gray = cimg
        self.find_marker()

    def find_marker(self):
        # self.img = cv2.medianBlur(self.img, 5)
        # circles = cv2.HoughCircles(self.img, cv2.HOUGH_GRADIENT, 1, 100,
        #                           param1=100, param2=50, minRadius=10, maxRadius=50)
        circles = cv2.HoughCircles(self.img_gray, cv2.HOUGH_GRADIENT, 1, 100,
                                   param1=500, param2=30, minRadius=1, maxRadius=50)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            if len(circles) == 1:
                for i in circles[0, :]:
                    # draw the outer circle
                    # cv2.circle(self.img_gray, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    # draw the center of the circle
                    # cv2.circle(self.img_gray, (i[0], i[1]), 2, (0, 0, 255), 3)
                    radius = i[2]
                    print("Radi: "+str(radius))
                    center = (i[0], i[1])
                    self.createTargetMask(radius, center)
                """
                kernel = np.ones((3, 3), np.uint8)
                print(type(self.img_gray))
                print(type(self.img_gray[2]))
                image = cv2.erode(self.img_gray, kernel)
                cv2.imshow('detected circles', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                """
            else:
                print("NOT ONE TARGET")
                # Controlar ERROR
                pass
        else:
            # Controlar ERROR
            print("NO TARGET")
            pub.sendMessage("TARGET_NOT_FOUND")
            pass

    def createTargetMask(self, radius, center):
        # Crear una màscara del marcador per fer la comprovació
        # zeros = np.zeros((radius*4, radius*4))
        targetMask = np.full((radius * 4, radius * 4), 255, np.uint8)
        targetMask[int(round(radius / 2)):int(round(radius * 3.5)), int(round(radius / 2)):int(round(radius * 3.5))] = 0
        self.angleTarget(targetMask, center, radius)

    def angleTarget(self, targetMask, center, radius):
        im = Image.fromarray(targetMask)
        # Inicialitzar array d'angles de 0 a 89
        sums = np.zeros(90)
        for i in range(90):
            i = i + 1
            J = im.rotate(i - 1, expand=True)
            width, height = J.size
            # Obtenim part de la imatge a comparar
            cut = self.img_gray[int(round(center[1] - (width / 2))): int(round(center[1] + (width / 2))),
                  int(round(center[0] - (width / 2))): int(round(center[0] + (width / 2)))]
            # resized = cv2.resize(cut, (width, height), interpolation = cv2.INTER_AREA)
            np.resize(cut, (width, height))
            J = np.array(J, np.float64)
            cut = np.array(cut, np.float64)
            # Fem la resta i emmascarem amb el marcador
            dif = J - cut
            dif[J == 0] = 0
            #np.savetxt('dif.txt', dif, fmt='%.2f')
            # Sumem i guardem els valors
            pixelSum = np.sum(dif[:])
            sums[i - 1] = pixelSum
        # El maxim correspon a l'angle de rotació de la foto
        angle = np.argmax(sums)
        #print("Angle: "+str(angle))
        self.matchMarker(im, angle, center, targetMask, radius)

    def matchMarker(self, im, angle, center, targetMask, radius):
        # Obtenir la part de la imatge del marcador amb l'angle correcte
        J = im.rotate(angle, expand=True)
        width, height = J.size
        cut = self.img_gray[int(round(center[1] - (width / 2))): int(round(center[1] + (width / 2))),
              int(round(center[0] - (width / 2))): int(round(center[0] + (width / 2)))]
        cut_bgr = self.img_bgr[int(round(center[1] - (width / 2))): int(round(center[1] + (width / 2))),
                  int(round(center[0] - (width / 2))): int(round(center[0] + (width / 2)))]
        np.resize(cut_bgr, (width, height))
        self.createRoi(im, targetMask, radius, cut_bgr, angle)

    def createRoi(self, im, targetMask, radius, cut_bgr, angle):
        # Creem la roi de la part blanca del marcador, amb una erosió per deixar-hi marge
        targetMask = 255 - targetMask
        width, height = im.size
        cv2.circle(targetMask, (int(width / 2), int(height / 2)), radius, 0, -1)
        im = Image.fromarray(targetMask)
        J = im.rotate(angle, expand=True)
        # Erosion
        kernel = np.ones((3, 3), np.uint8)
        J = np.array(J)
        J = J.astype('uint8')
        roi = cv2.erode(J, kernel)

        """
        f = plt.figure()
        f.add_subplot(1, 2, 1)
        plt.imshow(np.rot90(targetMask, 2))
        f.add_subplot(1, 2, 2)
        plt.imshow(np.rot90(roi, 2))
        plt.show(block=True)
        """
        self.cut_bgr = cut_bgr
        self.roi = roi
        #self.whiteBalance(cut_bgr, roi)
        self.measureDistance(radius)

    def whiteBalance(self):
        #roi[roi != 0] = 1
        roi = self.roi.astype('bool')
        cutB = self.cut_bgr[:, :, 0]
        cutG = self.cut_bgr[:, :, 1]
        cutR = self.cut_bgr[:, :, 2]

        bp = cutB[roi]
        gp = cutG[roi]
        rp = cutR[roi]

        whiteB = np.mean(cutB[roi])
        whiteG = np.mean(cutG[roi])
        whiteR = np.mean(cutR[roi])
        lum = (whiteR + whiteG + whiteB) / 3
        print("lum: ", lum)
        I = self.img_bgr
        I[:, :, 0] = self.img_bgr[:, :, 0] * (lum / whiteB)
        I[:, :, 1] = self.img_bgr[:, :, 1] * (lum / whiteG)
        I[:, :, 2] = self.img_bgr[:, :, 2] * (lum / whiteR)
        bgr = I
        return bgr
        cv2.imshow('White Balanced', bgr)
        cv2.waitKey(0)

    def measureDistance(self, radius):
        # img_to_array = np.array(self.img_gray)
        pxmeasure = 0.5 / radius
        self.px_dist = pxmeasure
        print("Valor px_cm: ",self.px_dist)