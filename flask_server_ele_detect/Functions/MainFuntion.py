from Functions.ElephantDetectionCamera import elephant_detect_from_camera
from Functions.ElephantDetectionVideo import elephant_detect

ele_detection_status = {
    "is_elephant_detect": False,
    "pred_class": "Not Elephant",
    "frames": ""
}


def main():
    result = elephant_detect()
    for res in result:
        # print( res['out_res']['is_elephant_present'])
        is_elephant_detect = res['out_res']['is_elephant_present']
        if is_elephant_detect:
            ele_detection_status["is_elephant_detect"] = True
            ele_detection_status["pred_class"] = res["out_res"]["pred_class"]
            ele_detection_status["frames"] = res["out_frames"]
            yield ele_detection_status
        else:
            ele_detection_status["is_elephant_detect"] = False
            ele_detection_status["pred_class"] = res["out_res"]["pred_class"]
            ele_detection_status["frames"] = res["out_frames"]
            yield ele_detection_status

