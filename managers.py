# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:43:08 2017

@author: hsoest
"""

import cv2
import numpy as np
import time

class CpatureManager:
    
    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False):
        self.previewWindowManager = previewWindowManager
        self.souldMirrorPreview = shouldMirrorPreview
        
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None
        
        self._startTime = None
        self._frameElapsed = long(0)
        self._fpsEstimate = None
        
        @property
        def channel(self):
            return self._channel
        
        
        @channel.setter
        def channel(self, value):
            if self._channel != value:
                self._channel = value
                self._frame = None
        
        
        @property
        def frame(self):
            if self._enteredFrame and self._frame is None:
                _, self._frame = self._capture.retrive()
                return self._frame
            
            
        @property
        def isWritingImage(self):
            return self._imageFilename is not None
            
            
        @property
        def isWritingVideo(self):
            return self._videoFilename is not None
            
            
        def enterFrame(self):
            """Capture the next frame, is any"""
            #fist check, that any previous frame was exited.
            assert not self._enterdFrame, 'previous enterFrame() had no matching exitFrame()'
            
            if self._capture is not None:
                self._enteredFrame = self._capture.grap()
            
            
        def exitFrame(self):
            """Draw to the window. Write to the files. Release the frame"""
            
            # check whether any grapped frame is retievable.
            # the getter may retrieve and cache the frame.
            
            if self._frame is None:
                self._enteredFrame = False
                return
            
            #Update the FPS estimate and related variabels.
            if self._frameElapsed == 0:
                self._startTime = time.time()
            else:
                timeElapsed = time.time() - self._startTime
                self._fpsEstimate = self._framesElaped / timeElapsed
                self._frameElapsed += 1
                
            #Draw to the window, if any
            if self.previewWindowManager is not None:
                if self.shouldMirrorPreview:
                    mirroredFrame = np.fliplr(self._frame).copy()
                    self.previewWindowManager.show(mirroredFrame)
                else:
                    self.previewWindowManager.show(self._frame)
            
            #Write to image File, if any
            if self.isWritingImage:
                cv2.imwirite(self._imageFilename, self._frame)
                self._imageFilename = None
                
            #Write to the video file, if any
            self._writeVideoFrame()
            
            #Release the frame
            self._frame = None
            self._enteredFrame = False
            
            
        def writeImage(self, filename):
            """Write the next exited frame to an image file."""
            self._imageFilename = filename
            
            
        def startWritingVideo(self, filename, encoding = cv2.VideoWriter_fourcc('I', '4', '2', '0')):
            """Start writing exited frames to a video file."""
            self._videoFilename = filename
            self._videoEncoding = encoding
            
            
        def stopWritingVideo(self):
            """Stop writing exited frames to a video file."""
            self._videoFilename = None
            self._videoEncoding = None
            self._videoWriter = None
            
        def _writeVideoFrame(self):
            if not self.isWritingVideo:
                return
                
            if self._videoWriter is None:
                fps = self._capture.get(cv2.CAP_PROP_FPS)
                if fps == 0.0:
                    #The capture's FPS is unknown so use the estimate.
                    if self._frameElapsed < 20:
                        return
                    else:
                        fps = self._fpsEstime
                size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._capture.get(cv2.CAP_PROP_FRAME_HIGHT)))
                self._videoWriter = cv2.VideoWriter(self._videoFilename, self._videoEncoding, fps, size)
            
            self._videoWriter.write(self._frame)
            
            
            
                
            
            
            
            
            
            
            
            
            
            
            
            
        