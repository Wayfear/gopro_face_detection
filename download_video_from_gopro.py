from goprocam import GoProCamera
import os
from os.path import join
import json
from datetime import datetime, timedelta
import subprocess
import re

project_dir = os.getcwd()
video_path = join(project_dir, 'video')

gpCam = GoProCamera.GoPro()
data = json.loads(gpCam.listMedia())

file_list = []

for folder in data['media']:
    dic = folder['d']
    for file in folder['fs']:
        file_list.append({'dictionary': dic, 'name': file['n'], 'time': file['mod']})

# get the wireless SSID
tmp = subprocess.check_output('iwconfig', stderr=subprocess.STDOUT)
tmp_ls = tmp.decode("ascii").replace("\r", "").split("\n")
wifi_info = tmp_ls[4]
start_symbol = '"'
end_symbol = '" '
wifi = re.search('%s(.*)%s' % (start_symbol, end_symbol), wifi_info).group(1)
print('connected wifi is {}'.format(wifi))

# format time
for file in reversed(file_list):
    gpCam.downloadMedia(file['dictionary'], file['name'])
    name = datetime.fromtimestamp(int(file['time']))
    # name = name - timedelta(hours=1)
    os.rename(file['name'], join(video_path, '%s_%s.MP4' %(name.strftime('%m-%d-%H-%M-%S'), wifi)))
    gpCam.deleteFile(file['dictionary'], file['name'])


