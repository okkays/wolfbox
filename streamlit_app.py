import cv2
import streamlit as st
import datetime
import stream_helper
import cam_helper
import cgi_helper

rtsp_address = st.empty()


def get_and_display_vars(varname):
    display = st.expander(f"{varname}.cgi")
    details = cgi_helper.get_vars(varname)
    for k, v in details.items():
        display.write(f"**{k}**: {v}")


def setup_time():
    config = st.expander("Camera time")
    current_time = cgi_helper.get_vars('getsystime')['time']
    readable_time = datetime.datetime.strptime(
        current_time, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    config.write(f"**Current camera time:** {readable_time}")
    config.button("Sync camera time", on_click=cgi_helper.set_time)


def setup_stream(streamer, viewer):
    while True:
        frame = stream_helper.read_frame(streamer)
        frame_jpg = cv2.imencode('.jpg', frame)[1].tobytes()
        viewer.image(frame_jpg, channels="BGR", width="stretch")


def set_channel(channel):
    return int(cgi_helper.get_vars('getcamchnl', camid=channel)['camchnl'])


def setup_cam_channel():
    channel_labels = {
        0: 'Front',
        1: 'Under',
        2: 'Rear',
    }
    number_of_cameras = int(cgi_helper.get_vars('getcamnum')['camnum'])
    channel = st.selectbox('Camera channel',
                           list(range(0, number_of_cameras)),
                           format_func=lambda x: channel_labels[x],
                           index=0)
    set_channel(channel)


st.title("Wolfbox web interface")
viewer = st.empty()
viewer.write("Starting camera...")
setup_cam_channel()
rtsp_address = f'rtsp://{cam_helper.CAM_ADDRESS}/livestream/1'
setup_time()
for varname in ['getdeviceattr']:
    get_and_display_vars(varname)

with stream_helper.capture(rtsp_address) as streamer:
    setup_stream(streamer, viewer)
