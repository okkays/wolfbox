WOLFBOX=192.168.1.1

# echo 'register:'
# curl "$WOLFBOX/cgi-bin/hisnet/client.cgi?&-operation=register&-ip=192.168.1.21"

# echo
# echo 'getworkstate:'
# curl "$WOLFBOX/cgi-bin/hisnet/getworkstate.cgi"

echo
echo 'setsystime:'
current_date="$(date +%Y%m%d%H%M%S)"
curl "$WOLFBOX/cgi-bin/hisnet/setsystime.cgi?&-time=$current_date"

# echo
# echo 'experiment:'
# curl "$WOLFBOX/cgi-bin/hisnet/getfilecount.cgi"

# cam_num=0
# while true; do
#     if [ "$cam_num" -gt 2 ]; then
#         cam_num=0
#     fi
#     echo
#     echo "Camera $cam_num"
#     curl "$WOLFBOX/cgi-bin/hisnet/getcamchnl.cgi?&-camid=$cam_num"
#     cam_num="$(( cam_num + 1 ))"
#     sleep 1
# done

# curl "$WOLFBOX/cgi-bin/hisnet/getcamchnl.cgi?&-camid=0"
echo
echo 'getdeviceattr:'
curl "$WOLFBOX/cgi-bin/hisnet/getdeviceattr.cgi"

echo
echo 'getcamnum:'
curl "$WOLFBOX/cgi-bin/hisnet/getcamnum.cgi"

echo
echo 'getcamparamcapability:'
curl "$WOLFBOX/cgi-bin/hisnet/getcamparamcapability.cgi?&-workmode=NORM_REC&-type=MEDIAMODE"

echo
echo 'getworkmodeparam:'
curl "$WOLFBOX/cgi-bin/hisnet/getvideoverbosefileinfo.cgi"

# echo
# echo 'getsdstatus:'
# curl "$WOLFBOX/cgi-bin/hisnet/getsdstatus.cgi"

# echo
# echo 'getcamchnl:'
# curl "$WOLFBOX/cgi-bin/hisnet/getcamchnl.cgi?&-camid=2"

# echo
# echo 'getcommparamcapability:'
# curl "$WOLFBOX/cgi-bin/hisnet/getcommparamcapability.cgi?&-type=ENC_PAYLOAD_TYPE"
# curl "$WOLFBOX/cgi-bin/hisnet/getcommparamcapability.cgi?&-type=GSR_SENSITIVITY"
# curl "$WOLFBOX/cgi-bin/hisnet/getcommparamcapability.cgi?&-type=GSR_PARKING"
# curl "$WOLFBOX/cgi-bin/hisnet/getcommparamcapability.cgi?&-type=LOW_FPS_REC_TIME"
# curl "$WOLFBOX/cgi-bin/hisnet/getcommparamcapability.cgi?&-type=LOW_FPS_REC_INTERVAL"

# echo
# echo 'commparamcapability:'
# curl "$WOLFBOX/cgi-bin/hisnet/commparamcapability.cgi?&-type=VOLUME"

