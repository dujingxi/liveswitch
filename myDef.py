#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import ssl
import json
import string
import urllib
import urllib2
import hashlib
import logging
from config import CHECK_URL_TIMEOUT, PIC_DIR, LOG_LEVEL, LOG_FILE, MP3_DIR, CAPTION_DIR
from subprocess import Popen , PIPE
import time

def sys_command_outstatuserr(cmd):
    p1 = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        if p1.poll() is not None:
            res = p1.communicate()
            exitcode = p1.poll() if p1.poll() else 0
            return {'code':exitcode, 'msg':'', 'time':seconds_passed}
        seconds_passed = time.time() - t_beginning
        if seconds_passed > CHECK_URL_TIMEOUT:
            p1.terminate()
            exitcode, err = 128, 'Execute timeout.'
            return {'code':exitcode, 'msg':err, 'time': seconds_passed}
        time.sleep(0.5)

def post_data(url, data):
    url = url
    header = {
        'Content-Type': 'application/json',
        'charset': 'utf-8'
    }
    data = json.dumps(data)
    req = urllib2.Request(url=url, headers=header, data=data)
    response = urllib2.urlopen(req)
    res = response.read()
    return res

def setlog():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    fh = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

def gen_case():
    gen1 = (x for x in string.lowercase)
    return gen1


def get_file(url, t):
    #if url != '':
    if url.startswith('http'):
        filename = url.split('/')[-1]
        if t == 'pic':
            filepath = "%s/%s" % (PIC_DIR, filename)
        else:
            filepath = "%s/%s" % (MP3_DIR, filename)
        if not os.path.exists(filepath):
            try:
                urllib.urlretrieve(url, filepath)
                return 0,filename
            except Exception, e:
                logging.error(e)
                return -1, 
        else: return 0, filename
    else: return -100, 

def get_caption(text):
    content = ' ' if not text else text
    md5 = hashlib.md5()
    md5.update(content)
    content_txt = md5.hexdigest()
    if not os.path.exists(content_txt):
        fp = open("%s/%s"%(CAPTION_DIR, content_txt), 'w')
        fp.write(content)
        fp.close()
    return "%s/%s" % (CAPTION_DIR, content_txt)



# weather function
def get_weather(city="beijing"):
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    url = 'https://api.seniverse.com/v3/weather/now.json'
    location = city
    params = {
        'key': 'aqbscwqmeczjh8yv',
        'location': location,
        'language': 'zh-Hans',
        'unit': 'c'
    }                                                                                                                                          
    try:
        data = urllib.urlencode(params)
        req = urllib2.Request("{url}?{data}".format(url=url, data=data))
        res = urllib2.urlopen(req, context=gcontext)
        result = eval(res.read())
        rest = result['results'][0]
        name = rest['location']['name']
        text = rest['now']['text']
        code = rest['now']['code']
        temp = rest['now']['temperature']                                          
    except Exception, e:
        name = '未知'
        text = '晴'
        code = '0'
        temp = '20'
    return {'city':name, 'text':text, 'code':str(code), 'temp':temp+'℃'}                            

def get_he_weather(city="beijing"):
    url = "https://free-api.heweather.com/v5/now"
    key = "90ecbe59600e4d768f89d36a395ffd2f"
    lang = "zh"
    params = {
            "city":city,
            "key":key,
            "lang":lang
            }
    p = urllib.urlencode(params)
    try:
        res = urllib.urlopen("%s?%s"%(url,p))
        response = json.loads(res.read(),encoding='utf-8')
        stats = response['HeWeather5'][0]['status']
        now = response['HeWeather5'][0]['now']
        code = now['cond']['code']
        text = "%s %s℃  %s %s级" % (now['cond']['txt'], now['tmp'], now['wind']['dir'], now['wind']['sc'])
    except:
        stats = '400'
        code = '100'
        text = "晴 20℃  东风 微风级"

    return {"code":code, "status":stats, "text":text}


if __name__ == '__main__':
#    url = "http://172.16.1.122:8888/post"
#    data = {
#        "description": "",
#        "bgMusic": "test.mp3",
#        "cmdName":"init",
#        "destURl": "/live/out"
#        }
#    print post_data(url, data)
    res = get_weather("jiaxing")
    print res['text']
