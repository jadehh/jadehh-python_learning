ffmpeg -hwaccel cuvid -c:v h264_cuvid \
-rtsp_transport tcp -i "rtsp://admin:samples123@192.168.35.119:554/Streaming/tracks/201?starttime=20200116t105450z&endtime=20200117t170000z" \
-c:v h264_nvenc -b:v 2048k -vf scale_npp=1280:-1 -y /home/2.mp4