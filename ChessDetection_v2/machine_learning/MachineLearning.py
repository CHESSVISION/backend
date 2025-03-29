from inference import get_model
import supervision as sv


class MachineLearning:
    def __init__(self, model_id):
        self.__detections = None
        self.__image = None
        self.__model = get_model(model_id=model_id)

    def detect(self):
        results = self.__model.infer(self.__image)[0]
        self.__detections = sv.Detections.from_inference(results)

    def get_detections(self):
        return self.__detections

    def set_image(self, image):
        self.__image = image
        self.detect()

    def get_image(self):
        return self.__image

    def display_image(self):

        # display the images
        sv.plot_image(self.get_annotated_image())

    def get_annotated_image(self):

        bounding_box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        # annotate the images with our inference results
        annotated_image = bounding_box_annotator.annotate(
            scene=self.__image, detections=self.get_detections())
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=self.get_detections())

        return annotated_image
