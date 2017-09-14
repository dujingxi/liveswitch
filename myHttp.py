#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
from flask import abort, Flask, request, Response, jsonify
from config import JSON_DB
import json
from time import sleep

app = Flask(__name__)

with open(JSON_DB) as fp:
    STREAMS = json.load(fp)

@app.route('/')
def index():
    return "hello world"

@app.route('/new/', methods=['GET', 'POST'])
def add_json():
    if request.method == 'POST':
        if not request.get_json():
            return jsonify({'returnCode':400, 'errMsg':'Not json.'})
            abort(400)
        elif request.json['out'] == '':
            return jsonify({'returnCode':400, 'errMsg':'Out can not be empty.'})
        else:
            num = len(STREAMS)
            stream_info = request.json
            stream_info['stream_id'] = num
            STREAMS.append(stream_info)
            with open(JSON_DB, 'w') as fp:
                json.dump(STREAMS, fp)
            return jsonify({'returnCode':200, 'errMsg':'Added successfully.'})
    else:
        abort(405)

@app.route('/delete/', methods=['POST'])
def del_json():
    if request.method == 'POST':
        if not 'stream_id' in request.json or request.json['stream_id'] == '':
            return jsonify({'returnCode':400, 'errMsg':'Failed to delete.'})
        else:
            for stream in STREAMS:
                if stream['stream_id'] == request.json['stream_id']:
                    del STREAMS[STREAMS.index(stream)]
                    with open(JSON_DB, 'w') as fp:
                        json.dump(STREAMS, fp)
                    return jsonify({'returnCode':200, 'errMsg':'Deleted successfully.'})
            else:
                return jsonify({'returnCode':400, 'errMsg':'Can\'t find stream id.'})
    else:
        abort(405)

@app.route('/put/<int:stream_id>', methods=['PUT'])
def update_json(stream_id):
    sid = [x['stream_id'] for x in STREAMS if x['stream_id'] == stream_id]
    if len(sid) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'out' in request.json:
        STREAMS[stream_id]['out'] = request.json['out']
    if 'bgMusic' in request.json:
        STREAMS[stream_id]['bgMusic'] = request.json['bgMusic']
    if 'description' in request.json:
        STREAMS[stream_id]['description'] = request.json['description']
    if 'ins' in request.json:
       STREAMS[stream_id]['ins'] = request.json['ins']
    with open(JSON_DB, 'w') as fp:
        json.dump(STREAMS, fp)
    return jsonify({'returnCode':200, 'errMsg':'Updated.'})

@app.route('/get/', methods=['GET'])
def get_query():
    return jsonify({'streams': STREAMS})

@app.route('/get/<int:stream_id>', methods=['GET'])
def get_id_json(stream_id):
    sid = [x['stream_id'] for x in STREAMS if x['stream_id'] == stream_id]
    if len(sid) == 0:
        abort(404)
    return jsonify({'stream': STREAMS[stream_id]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
