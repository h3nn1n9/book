# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:34:54 2017

@author: hsoest
"""

import cv2
import numpy as np
import utils

def stokeEdges(src, dst, blurKsize = 7, edgeKsize = 5):
    if blurKsize >= 3:
        blurredSrc = cv2.medianBlur(src, blurKzise)
        graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    else:
        graySrc = cv2.cvtColor(src, cv2.COLOR_BRG2GRAY)
    cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize=edeKsize)
    normalizedInverseAlpha = (1.0/255) * (255-graySRC)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha
    cv2.merge(channels, dst)
    
    
    
