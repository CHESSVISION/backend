from ChessDetection_v2.machine_learning.MachineLearning import MachineLearning


class HandDetector(MachineLearning):

    def __init__(self, image=None, model_id="hand-detection-2r6df/1"):
        super().__init__(image, model_id)

    def found_hand_detected(self, image=None):
        if image is not None:
            self.set_image(image)
        return self.get_detections().xyxy.size != 0
