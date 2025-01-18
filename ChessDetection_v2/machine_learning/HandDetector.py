from ChessDetection_v2.machine_learning.MachineLearning import MachineLearning
from config import settings


class HandDetector(MachineLearning):

    def __init__(self):
        super().__init__(settings.hand_detector_model)

    def found_hand_detected(self, image):
        self.set_image(image)
        return self.get_detections().xyxy.size != 0


hand_detector = HandDetector()
