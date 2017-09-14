# -*- coding:  utf-8 -*-

# DURATION = 15
CHECK_URL_TIMEOUT = 10
LOG_LEVEL = 20  # { 'DEBUG':10, 'INFO':20, 'WARNING':30, 'ERROR':40, 'CRITICAL':50 }
LOG_FILE = "worker.log"
PIC_DIR = "picdir"
FONT_DIR = "fontdir"
MP3_DIR = "mp3dir"
DEFAULT_MP3 = "qrsy.mp2"
# WEATHER_DIR = "weatherpng"
WEATHER_DIR = "weapng"
JSON_DB = "db.json"
LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 8000
DES_URL = 'http://127.0.0.1:8888/post'
CHECK_CMD = '/SO/bin/ad_config-6.0.0-17914/ffmpeg/bin/ffprobe'
THREAD_NUM = 16

'''
# streams example
STREAMS = [
    {
        'stream_id': 0,
        'out': '/live/livechina',
        'bgmusic': 'http://127.0.0.1/music.mp3',
        'description': '北京',
        'ins': [
            {
                'url': 'http://127.0.0.1/live/example',
                'pic': [
                    {
                        'address': 'http://127.0.0.1/imgs/1.png',
                        'sizeHeight': '200',
                        'sizeWidth': '320',
                        'positionX': '20',
                        'positionY': '0',
                        'loop': '0',      # 0 => not loop, 1 => loop
                        'transparent': '80',
                    }
                ],
                'caption': [
                    {
                        'text': 'welcome',
                        'fontfile': '/dir/kaiti.tff',
                        'fontsize': '25',
                        'fontcolor': 'white',
                        'borderw': '2',
                        'bordercolor': 'green',
                        'shadowx': '1',
                        'shadowy': '1',
                        'shadowcolor': '#fff',
                        'direction': '0',
                        'positionX': '0',
                        'positionY': '100',
                        'width': '1000',
                        'step': '50'
                    }
                ],
            },
        ],
    },
]
'''
