# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
import ffmpeg
import subprocess, re, time
from LogModel.controller import LogController
def get_seconds(time):
    h = int(time[0:2])
    m = int(time[3:5])
    s = int(time[6:8])
    ms = int(time[9:12])
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts
class TrimConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        params = text_data_json
        params['username'] = 'root'
        input_vid = ffmpeg.input(params['url'])
        vid = input_vid.trim(start=params['start_time'], end=params['end_time']).setpts('PTS-STARTPTS')
        aud = input_vid.filter_('atrim', start=params['start_time'], end=params['end_time']).filter_('asetpts', 'PTS-STARTPTS')
        joined = ffmpeg.concat(vid, aud, v=1, a=1).node
        stream = ffmpeg.output(joined[0], joined[1], f"out_t_{params['username']}.mp4")
        stream = stream.overwrite_output()
        log = LogController.add_log(params['username'], params['start_time'], params['end_time'], params['url'])
        cmd = ffmpeg.compile(stream)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
        for line in process.stdout:
            duration_res = re.search(r'\sDuration: (?P<duration>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)
                
            result = re.search(r'\stime=(?P<time>\S+)', line)
            if result is not None:
                elapsed_time = result.groupdict()['time']
                progress = (get_seconds(elapsed_time) / get_seconds(duration)) * 100
                print("进度:%3.2f" % progress + "%")
                # time.sleep(1)
                self.send(text_data=json.dumps({'progress': progress}))
        process.wait()
        if process.poll() == 0:
            self.send(text_data=json.dumps({'progress': 100.00}))
            self.send(text_data=json.dumps({'msg': 'success'}))