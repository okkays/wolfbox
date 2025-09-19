import ffmpeg
import cv2
import numpy as np
import contextlib


def _open_stream(source):
    args = {"rtsp_transport": "tcp"}  # Use TCP for the RTSP stream
    probe = ffmpeg.probe(source)
    print(probe)
    cap_info = next(x for x in probe['streams'] if x['codec_type'] == 'video')

    return cap_info, (
        ffmpeg
        .input(source, **args)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .overwrite_output()
        .run_async(pipe_stdout=True)
    )


def read_frame(streamer):
    cap_info, stream = streamer
    width = cap_info['width']
    height = cap_info['height']
    up, down = str(cap_info['r_frame_rate']).split('/')

    in_bytes = stream.stdout.read(width * height * 3)
    if not in_bytes:
        return
    in_frame = np.frombuffer(
        in_bytes, np.uint8).reshape([height, width, 3])
    frame = cv2.resize(in_frame, (1280, 720))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame


@contextlib.contextmanager
def capture(source):
    try:
        cap_info, stream = _open_stream(source)
        yield (cap_info, stream)
    finally:
        stream.kill()
