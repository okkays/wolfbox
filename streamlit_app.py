import cv2
import streamlit as st
import datetime
import stream_helper
import cam_helper
import cgi_helper
import files_helper

rtsp_address = f'rtsp://{cam_helper.CAM_ADDRESS}/livestream/1'


def get_and_display_vars(varname, container=st):
    display = container.expander(varname)
    details = cgi_helper.run_cgi(varname)
    for k, v in details.items():
        display.write(f"**{k}**: {v}")


def setup_files(container=st):
    files_helper.enter_read_mode()
    dirnames = files_helper.get_dirnames()
    counts = dict(files_helper.count_files(dirnames))
    lists = files_helper.list_files(counts.items())

    if not counts:
        container.write("No directories found.")
        return

    for dirname, filelist in lists:
        dir_expander = container.expander(f"Directory: {dirname}")
        if 'Files' not in filelist:
            dir_expander.write("Error retrieving file list.")
            dir_expander.write(filelist)
            continue
        if 'Error' in filelist:
            dir_expander.write("Error retrieving file count.")
            dir_expander.write(filelist['Error'])
            continue
        if not filelist.get('Files'):
            dir_expander.write("No files found.")
            continue
        for filename in filelist.get('Files', []):
            display_name = filename[len('sd//'):]
            file_url = f'http://{cam_helper.CAM_ADDRESS}/{filename}'
            thumb_url = file_url.replace('.MP4', '.THM')

            image_row = dir_expander.container()
            image_row.html(f'<a target="_blank" href={file_url}>'
                           f'<img height="50" src="{thumb_url}"/>'
                           f'{display_name}</a>')


def setup_time(container=st):
    config = container.expander("Camera time")
    current_time = cgi_helper.run_cgi('getsystime')['time']
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
    return int(cgi_helper.run_cgi('getcamchnl', camid=channel)['camchnl'])


def setup_cam_channel():
    channel_labels = {
        0: 'Front',
        1: 'Under',
        2: 'Rear',
    }
    number_of_cameras = int(cgi_helper.run_cgi('getcamnum')['camnum'])
    channel = st.selectbox('Camera channel',
                           list(range(0, number_of_cameras)),
                           format_func=lambda x: channel_labels[x],
                           index=0)
    set_channel(channel)


print(cgi_helper.run_cgi('client', operation='register',
                         ip=cgi_helper.CLIENT_ADDRESS))
st.title("Wolfbox web interface")
viewer = st.empty()
viewer.write("Starting camera...")
setup_cam_channel()
# files = st.expander("Recorded files")
config = st.expander("Camera configuration")
# setup_files(container=files)
setup_time(container=config)
# for varname in ['getdeviceattr', 'getworkstate']:
#     get_and_display_vars(varname, container=config)
with stream_helper.capture(rtsp_address) as streamer:
    setup_stream(streamer, viewer)
