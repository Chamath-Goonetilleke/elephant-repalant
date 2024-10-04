import cv2


def video_generator(func):
    yolo_output = func
    for detection_ in yolo_output:
        ret, buffer = cv2.imencode('.jpg', detection_)
        if not ret:
            continue  # Skip frames that fail to encode
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
