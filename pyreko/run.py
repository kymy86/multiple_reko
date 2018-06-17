import cv2
from time import sleep
import boto3
from threading import Thread

_IMAGE_PATH = '../images/frame.jpg'


def get_response(response_handlers, helper_function, image_path):
    """
    Send the frame to Rekognition service by using a Thread
    """
    
    if 'on_success' not in response_handlers:
        raise KeyError('You have to specify the success handler with key "on_success"')
    if 'on_failure' not in response_handlers:
        raise KeyError('You have to specify the failure handler with key "on_failure"')

    thread = Thread(
        target=helper_function,
        args=(image_path, response_handlers)
    )
    thread.daemon = False
    thread.start()
    return thread

def helper_function(image_path, response_handlers):
    try:
        client = boto3.client('rekognition')
        with open(image_path, 'rb') as image_bytes:
            res = client.detect_labels(
                Image={
                    'Bytes':bytearray(image_bytes.read())
                }
            )
    except Exception as exception:
        response_handlers['on_failure'](exception)
        return
    response_handlers['on_success'](res)


if __name__ == '__main__':
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        exit()

    def on_success(res):
       for label in res['Labels']:
           print(label['Name']+ ": "+str(label['Confidence']))

    def on_failure(res):
        print(res)

    HANDLERS = {'on_success':on_success, 'on_failure':on_failure}

    try:
        while True:
            sleep(3)
            print('I\'m watching....')
            ret, frame = webcam.read()
            cv2.imwrite(_IMAGE_PATH, frame)
            get_response(HANDLERS, helper_function, _IMAGE_PATH)
        webcam.release()
    except KeyboardInterrupt:
        exit(0)