import sys
import os

from flask import Response, jsonify, stream_with_context

# Add the parent directory to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Functions.MainFuntion import main
from Functions.Video_Generator import video_generator


def get_frames():
    result = main()
    print(result)
    for res in result:
        yield res["frames"]


def elephant_route(app):
    def video():
        return Response(video_generator(get_frames()), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/video')
    def video_feed():
        return Response(
            stream_with_context(video_generator(get_frames())),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
