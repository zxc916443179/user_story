# requirements
python==3.6.8 django==3.1.7 channels=3.0.3 pymysql ffmpeg-python

# run
python manage.py runserver

# apis
- log_up params: username:用户名 password: 密码 ret: user
- log_in params: username:用户名 password: 密码 ret: user
- log_out params: None ret: ''
- trim params: url: 视频链接 start_time: 开始时间（单位：s）end_time: 结束时间（单位：s）
- file_download: params: None ret: 返回用户裁剪完成url