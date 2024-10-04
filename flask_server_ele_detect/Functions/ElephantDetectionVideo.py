import cv2
from collections import deque
from ultralytics import YOLO

# Define the path to the video file
video = "/Users/chamathkavindya/Projects/Pending/elephant-detection/Elephant/yolov8custom5/weights/ali3.mp4"

# Load the YOLO model for emergency vehicle detection
ev_model = YOLO(
    "/Users/chamathkavindya/Projects/Pending/elephant-detection/flask_server_ele_detect/Model/best_n.pt")


def check_elephant_presence(predictions_buffer):
    ele_count = 0
    no_detection_count = 0

    out_put = {
        "pred_class": "Not Elephant",
        "is_elephant_present": False,
    }

    for predictions in predictions_buffer:
        if len(predictions) > 0:
            elephant_count = sum(1 for pred in predictions if pred == "Elephant")
            if elephant_count >= 1:
                ele_count += 1
        else:
            no_detection_count += 1

    frames_without_no_predictions = len(predictions_buffer) - no_detection_count

    if frames_without_no_predictions > 0:
        if ele_count / frames_without_no_predictions >= 0.7:
            out_put["pred_class"] = "Elephant"
            out_put["is_elephant_present"] = True
            return out_put

    return out_put


# Function for emergency vehicle detection
def elephant_detect(video_path=video, model=ev_model):
    cap = cv2.VideoCapture(video_path)

    frame_interval = 0.2
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total_time = frame_count / frame_rate

    current_time = 0
    current_frame = 0

    buffer_size = 25
    predictions_buffer = deque(maxlen=buffer_size)

    class_labels = ['Racoon', 'Southern Boo-book', 'Bear', 'Buffalo', 'Bicycle', 'Car', 'Clock', 'Cow', 'Deer', 'Dog',
                    'Eagle', 'Elephant', 'Elk', 'Gaur', 'OtherEntities', 'Person', 'Tiger', 'Umbrella', 'Wolf']
    # class_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0)]

    # Dictionary to store output frames and results
    frames_with_output = {
        "out_frames": "",
        "out_res": {
            "pred_class": "Not Elephant",
            "is_elephant_present": False,
        }
    }

    while current_time <= total_time:
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = cap.read()

        if not ret:
            break

        results = model.predict(frame, conf=0.1)
        bboxes = results[0].boxes
        predictions = [class_labels[int(bbox.cls)] for bbox in bboxes]
        predictions_buffer.append(predictions)

        if len(predictions_buffer) == 25:
            res = check_elephant_presence(predictions_buffer)
            predictions_buffer.clear()
            frames_with_output["out_res"] = res

        for bbox in bboxes:
            x1, y1, x2, y2 = bbox.xyxy[0]
            confidence = float(bbox.conf)
            class_id = int(bbox.cls)

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            cv2.putText(frame, f"{class_labels[class_id]}: {confidence:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        frames_with_output["out_frames"] = frame
        yield frames_with_output

        current_time += frame_interval
        current_frame = int(current_time * frame_rate)

    cap.release()
    cv2.destroyAllWindows()

