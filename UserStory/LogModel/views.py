from django.shortcuts import render
from .controller import LogController
from dwebsocket.decorators import accept_websocket
import json
import subprocess
import re, time
# Create your views here.


from UserStory.api import APIFunction, APIError
from .controller import UserController
import ffmpeg

def get_seconds(time):
    h = int(time[0:2])
    m = int(time[3:5])
    s = int(time[6:8])
    ms = int(time[9:12])
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts
@accept_websocket
def trim(request):
    params = {}
    for message in request.websocket:
        params.update(json.loads(message))
    input_vid = ffmpeg.input(params['url'])
    vid = input_vid.trim(start=params['startTime'], end=params['endTime']).setpts('PTS-STARTPTS')
    aud = input_vid.filter_('atrim', start=params['startTime'], end=params['endTime']).filter_('asetpts', 'PTS-STARTPTS')
    joined = ffmpeg.concat(vid, aud, v=1, a=1).node
    stream = ffmpeg.output(joined[0], joined[1], f"out_t_{params['username']}.mp4")
    ffmpeg.run(stream)
    log = LogController.add_log(params['username'], params['startTime'], params['endTime'], params['url'])
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
            # 此处可能会出现进度超过100%，未对数值进行纠正
            progress = (get_seconds(elapsed_time) / get_seconds(duration)) * 100
            print("进度:%3.2f" % progress + "%")
            time.sleep(1)
            request.websocket.send(json.dumps({'progress': progress}))
    process.wait()
    if process.poll() == 0:
        print('success', process)
        request.websocket.send(json.dumps({'progress': 100.00}))
    return log 
