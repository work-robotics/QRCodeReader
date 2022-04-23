# Copyright 2022 Work Robotics Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
from pyzbar.pyzbar import decode, ZBarSymbol
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
import cv2

class QRCodeReader(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.pastData = None
        print("==================================================")
        print(" QRCode Reader")
        print("==================================================")
    
    def run(self):
        while True:
            self.frame, self.image = self.capture.read()
            data = decode(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), symbols=[ZBarSymbol.QRCODE])
            if data:
                x, y, w, h = data[0].rect
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                decode_data = data[0].data.decode('utf-8')
                if self.pastData != decode_data:
                    print("URL:", decode_data)
                    self.pastData = decode_data

            cv2.imshow("QRCodeReader", self.image)
            if cv2.waitKey(1) == ord('q'):
                break
        
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    QRCodeReader().run()