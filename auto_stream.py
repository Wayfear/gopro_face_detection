import schedule
import time
import datetime
import sys
import math
from os.path import join
import os
import yaml
from func import live_stream_func

project_dir = os.getcwd()
with open(join(project_dir, 'config.yaml'), 'r') as f:
    cfg = yaml.load(f)

def start_shoot():
    shoot_seconds = math.ceil(cfg['auto_stream']['shoot_hours'] * 3600)
    live_stream_func(shoot_seconds)
    # download
    import download_video_from_gopro

start_time = cfg['auto_stream']['start_time']
schedule.every().day.at(start_time).do(start_shoot)
# schedule.every(1).minutes.do(start_shoot)

while True:
    schedule.run_pending()
    time.sleep(1)