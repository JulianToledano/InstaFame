import os
from .utils import *


class FaceFinder:
    def __init__(self,
                 model_cfg,
                 model_weights,
                 save_photo_predicted=False,
                 output_path=None):
        self._output_dir = output_path
        self._save_photo = save_photo_predicted
        self._net = cv2.dnn.readNetFromDarknet(str(model_cfg),
                                               str(model_weights))
        self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def results(self, image_path):
        image = image_path
        output_file = ''

        if image:
            if not os.path.isfile(image):
                print(
                    "[!] ==> Input image file {} doesn't exist".format(image))
                return None
            cap = cv2.VideoCapture(str(image))
            output_file = image[:-4].rsplit('/')[-1] + '_yoloface.jpg'

        has_frame, frame = cap.read()

        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(frame,
                                     1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                     [0, 0, 0],
                                     1,
                                     crop=False)

        # Sets the input to the network
        self._net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = self._net.forward(get_outputs_names(self._net))

        # Remove the bounding boxes with low confidence
        faces, scores = post_process(frame, outs, CONF_THRESHOLD,
                                     NMS_THRESHOLD)

        if not self._save_photo:
            cv2.imwrite(os.path.join(self._output_dir, output_file),
                        frame.astype(np.uint8))
        return frame, scores
