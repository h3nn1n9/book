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
        blurredSrc = cv2.medianBlur(src, blurKsize)
        graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    else:
        graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize=edgeKsize)
    normalizedInverseAlpha = (1.0/255) * (255-graySrc)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha
    cv2.merge(channels, dst)

class VConvolutionFilter:
    """A filter, that appies a convolution to V """

    def __init__(self, kernel):
        self._kernel = kernel

    def apply(self, src, dst):
        """Apply the filter with BGR or gray source/destination."""
        cv2.filter2D(src, -1, self._kernel, dst)


class SharpenFilter(VConvolutionFilter):
    """A sharpen filter with a 1-pixel radius"""

    def __init__(self):
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        VConvolutionFilter.__init__(self, kernel)


class FindEdgesFilter(VConvolutionFilter):
    """AN edges-fining filter with a 1-pixel radius"""

    def __init__(self):
        kernel = np.array([[-1, -1, -1],
                           [-1, 8, -1],
                           [-1, -1, -1]])
        VConvolutionFilter.__init__(self, kernel)


class BlurFilter(VConvolutionFilter):
    """A blur filter with a 2-pixel radius"""

    def __init__(self):
        kernel = np.array([[0.4, 0.4, 0.4, 0.4, 0.4],
                           [0.4, 0.4, 0.4, 0.4, 0.4],
                           [0.4, 0.4, 0.4, 0.4, 0.4],
                           [0.4, 0.4, 0.4, 0.4, 0.4],
                           [0.4, 0.4, 0.4, 0.4, 0.4]])
        VConvolutionFilter.__init__(self, kernel)


class EmbossFilter(VConvolutionFilter):
    """AN embos filter with a 1-pixel radius"""

    def __init__(self):
        kernel = np.array([[-2, -1, 0],
                           [-1, 1, 1],
                           [0, 1, 2]])
        VConvolutionFilter.__init__(self, kernel)

