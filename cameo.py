# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:48:51 2017

@author: hsoest
"""

import cv2
from managers import WindowManager, CaptureManager

class Cameo(object):
    
    def __init__(self):
        self._windowManager = WindowManager('Cameo', self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, True)
        
        
    def run(self):
        """Run the main loop"""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
            #TODO: Filter the frame
            
            self._captureManager.exitFrame
            self._windowManager.processEvents()
            
            
    def onKeypress(self, keycode):
        """Handle a keypress
        
        space -> Take a screenshot
        tab   -> Start/Stop recording a screencast
        esc   -> Quit.

        """
        if keycode == 32:  # space
            self._captureManager.writeImage('screenshot.png')
        elif keycode == 9:  # Tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screencarst.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27:  # ESC
            self._windowManager.destroyWindow()
            
    
if __name__  == "__main__":
    Cameo().run()