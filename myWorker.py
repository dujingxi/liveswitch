#!/usr/bin/python
# -*- coding: utf-8 -*-

# Title: myWorker.py
# Description: Receive data via web service and send it to target

# Author: dujingxi
# Email: dujingxi@streamocean.com
# Date: 2017/08/29

from gevent import monkey
import gevent
from myHttp import app, STREAMS
from config import *
import copy
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
monkey.patch_all()
from myDef import *

weather_info = {}
def weather_work(stream_id=0):
    def def_wea(ll):
        for s in ll:
            weather_info[s['url']] = get_he_weather(s['cityid'])
    url_list = []
    num = 1
    while True:
        if url_list == STREAMS[stream_id]['ins']:
            if num % 7200 == 0:
                def_wea(url_list)
                num = 1
            num += 1
            gevent.sleep(1)
            continue
        else:
            def_wea(url_list)
            url_list = STREAMS[stream_id]['ins']
            num = 1
            gevent.sleep(1)
    
def get_work(stream_id=0):
    setlog()
    while True:
        if len(STREAMS) == 0:
            logging.warning("STREAMS empty.")
            gevent.sleep(5)
            continue
        else: break
    current_stream = STREAMS[stream_id]
    dest_url = STREAMS[stream_id]['out']
    bgMusic = []
    for music in STREAMS[stream_id]['bgMusic']:
        a_s, a_f = get_file(music, "mp3")
        if a_s != 0:
            logging.error("Load mp3 file $s failed."%music)
            bgMusic.append("%s/%s" % (MP3_DIR, DEFAULT_MP3))
        else:
            bgMusic.append("%s/%s" % (MP3_DIR, a_f))
    one_json = {
        'cmdName': 'init',
        'out': dest_url,
        'bgMusic': bgMusic,
    }
    gevent.sleep(5)
    try:
        res = post_data(DES_URL, one_json)
        logging.info("post one_json: %s"%one_json)
    except Exception, e:
        logging.error(e)
        return e
    gevent.sleep(5)

    while True:
        for s in STREAMS[stream_id]['ins']:
            now_time = time.time()
            cmd = "%s %s" % (CHECK_CMD, s['url'])
            cmd_dict = sys_command_outstatuserr(cmd)
            _code = cmd_dict['code']
            _time = cmd_dict['time']
            if _code != 0:
                logging.error('url: %s invalid.'%s['url'])
                continue
            pic_tmp = copy.deepcopy(s['pic'])
            caption_tmp = copy.deepcopy(s['caption'])
            g1 = gen_case()
            filter_cmd = ''
            pre_map = ''
            n = 1
            for pic in pic_tmp:
                c, f = get_file(pic['address'], "pic")
                if c != 0:
                    logging.error('Load %s failed'%pic['address'])
                    continue
                cur_map = g1.next()
                next_map = g1.next()
                if n == 1:
                    filter_cmd += 'movie=%s/%s[%s];[in][%s] overlay=%s:%s [%s]; ' % (PIC_DIR, f, cur_map, cur_map, pic['positionX'], pic['positionY'], next_map)
                else:
                    filter_cmd += 'movie=%s/%s[%s];[%s][%s] overlay=%s:%s [%s]; ' % (PIC_DIR, f, cur_map, pre_map, cur_map, pic['positionX'], pic['positionY'], next_map)
                pre_map = next_map
                n += 1


            cur_map = g1.next()
            next_map = g1.next()
            try:
                code_num = weather_info[s['url']]['code']
            except:
                code_num = "100"
            filter_cmd += 'movie=%s/%s.png [%s]; [%s][%s] overlay=%s [%s]; '%(WEATHER_DIR,code_num, cur_map , pre_map, cur_map, "W-w-50:H-h-52", next_map) 

            pre_map = next_map
            for cap  in caption_tmp:
                fontfile = cap['fontFile']
                cur_map = g1.next()
                if cap['direction'] == '0':
                    filter_cmd += '[%s] drawtext=text=%s: fontfile=%s/%s: fontsize=%s: fontcolor=%s: shadowx=%s: shadowy=%s: shadowcolor=%s: borderw=%s: bordercolor=%s: x=%s: y=%s [%s]; ' % (pre_map, cap['content'], FONT_DIR, fontfile, cap['fontSize'], cap['fontColor'], cap['shadowX'], cap['shadowY'], cap['shadowColor'], cap['borderW'], cap['borderColor'], cap['positionX'], cap['positionY'], cur_map)
                elif cap['direction'] == '1':
                    filter_cmd += '[%s] drawtext=text=%s: fontfile=%s/%s: fontsize=%s: fontcolor=%s: shadowx=%s: shadowy=%s: shadowcolor=%s: borderw=%s: bordercolor=%s: x=&if(gte(t,1),(main_w-mod(t*%s,main_w+text_w)),NAN)&: y=%s [%s]; ' % (pre_map, cap['content'], FONT_DIR, fontfile, cap['fontSize'], cap['fontColor'], cap['shadowX'], cap['shadowY'], cap['shadowColor'], cap['borderW'], cap['borderColor'], cap['step'], cap['positionY'], cur_map)
                else:
                    filter_cmd += '[%s] drawtext=text=%s: fontfile=%s/%s: fontsize=%s: fontcolor=%s: shadowx=%s: shadowy=%s: shadowcolor=%s: borderw=%s: bordercolor=%s: x=%s: y=%s [%s]; ' % (pre_map, cap['content'], FONT_DIR, fontfile, cap['fontSize'], cap['fontColor'], cap['shadowX'], cap['shadowY'], cap['shadowColor'], cap['borderW'], cap['borderColor'], cap['positionX'], cap['positionY'], cur_map)
                pre_map = cur_map
                

            # weather text
            try:
                content = '%s' % weather_info[s['url']]['text']
            except:
                content = ' '
            # cur_map = g1.next()
            filter_cmd += '[%s] drawtext=text=%s: fontfile=%s/%s: fontsize=22: fontcolor=white@0.8: shadowx=0: shadowy=0: shadowcolor=black:x=(w-text_w-20): y=(main_h-line_h-67)[out] ' % (pre_map, content, FONT_DIR, fontfile )
            # stream name
            # content = s['name']
            # filter_cmd += '[%s] drawtext=text="%s": fontfile=%s/%s: fontsize=22: fontcolor=black: shadowx=1: shadowy=1: shadowcolor=black:x=10: y=20 [out]; ' % (cur_map, content, FONT_DIR, fontfile)

            # for content in ['%s %s %s'%(wea_res['city'], wea_res['text'], wea_res['temp']), s['name']]:
                # caption_tmp.insert(0, {'fontFile':'fontdir/cukai', 'borderColor':'#fff', 'direction':'1', 'shadowX':'1', 'shadowY':'23', 'content':content, 'step':'10', 'width':'30', 'shadowColor':'#fff', 'fontSize':'22' , 'positionX':'2', 'positionY':'3', 'fontColor':'#fff', 'borderW':'3'})
            switch_json = {
                'cmdName': 'switch',
                # 'name': s['name'],
                'url': s['url'],
                'filter_content': filter_cmd,
                # 'cityid': s['cityid'],
                # 'pic': pic_tmp,
                # 'caption': caption_tmp
            }
            try:
                res = post_data(DES_URL, switch_json)
                logging.info("post switch_json: %s" % switch_json)
            except Exception, e:
                logging.error("send switch cmd error: %s"%e)
                # return e
                continue
            sleep_time = now_time+int(s['duration'])-time.time()
            gevent.sleep(sleep_time)
        else:
            while True:
                if len(STREAMS) == 0:
                    logging.warning("STREAMS empty.")
                    gevent.sleep(10)
                    continue
                else: break

if __name__ == '__main__':
    g1 = gevent.spawn(app.run, host=LISTEN_IP, port=LISTEN_PORT)
    g2 = gevent.spawn(get_work)
    g3 = gevent.spawn(weather_work)
    g1.join()
    g2.join()
    g3.join()
