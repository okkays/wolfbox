import cv2
import streamlit as st
import requests
import datetime
import stream_helper

CAM_ADDRESS = "192.168.1.1"
HTTP_ADDRESS_BASE = f'http://{CAM_ADDRESS}/cgi-bin/hisnet'
rtsp_address = st.empty()


def clean_var_result(var_result):
    lines = var_result.splitlines()
    return {
        # Remove the var prefix as well as quoted values:
        line.split('=')[0][4:]: line.split('=')[1][1:-2]
        for line in lines if '=' in line
    }


def set_time():
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    requests.get(f'{HTTP_ADDRESS_BASE}/setsystime.cgi'
                 f'?&-time={current_time}')


def get_vars(varname):
    deviceattr_raw = requests.get(f'{HTTP_ADDRESS_BASE}/{varname}.cgi').text
    deviceattr = clean_var_result(deviceattr_raw)
    return {
        **deviceattr,
    }


def get_and_display_vars(varname):
    display = st.expander(f"{varname}.cgi")
    details = get_vars(varname)
    for k, v in details.items():
        display.write(f"**{k}**: {v}")


def setup_time():
    config = st.expander("Camera time")
    current_time = get_vars('getsystime')['time']
    readable_time = datetime.datetime.strptime(
        current_time, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    config.write(f"**Current camera time:** {readable_time}")
    config.button("Sync camera time", on_click=set_time)


def setup_stream(streamer, viewer):
    while True:
        frame = stream_helper.read_frame(streamer)
        frame_jpg = cv2.imencode('.jpg', frame)[1].tobytes()
        viewer.image(frame_jpg, channels="BGR", width="stretch")


st.title("Wolfbox web interface")
viewer = st.empty()
rtsp_address = st.text_input('rtsp_address',
                             value=f'rtsp://{CAM_ADDRESS}/livestream/1')
setup_time()
for varname in ['getdeviceattr']:
    get_and_display_vars(varname)

with stream_helper.stream(rtsp_address) as streamer:
    setup_stream(streamer, viewer)
