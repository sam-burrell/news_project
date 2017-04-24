#!/usr/bin/python3
from flask import Flask, jsonify
import redis
import json
from collections import Counter
from datetime import datetime


app = Flask(__name__)
redisServer = redis.Redis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

@app.route("/")
def hello():
    return "Hello World !"

@app.route('/tags',methods=['GET'])
def getAllTags():
    # Most likely use this in the API
    # remove all items older than 60 seconds
    redisServer.zremrangebyscore('tags', 0, int(datetime.utcnow().timestamp()-60))
    tagCounter = Counter()
    for element in redisServer.zrange('tags', 0, -1):
        element = element.split('---')
        tagCounter[element[1]] += 1
    return jsonify({'tags':tagCounter.most_common()})

@app.route('/tags/<tag>',methods=['GET'])
def getTag(tag):
    # Most likely use this in the API
    # remove all items older than 60 seconds
    redisServer.zremrangebyscore('tags', 0, int(datetime.utcnow().timestamp()-60))
    urlWithTag = {}
    for element in redisServer.zrange('tags', 0, -1):
        element = element.split('---')
        urlWithTag.setdefault(element[1], []).append(element[0])
    return jsonify({tag:urlWithTag[tag]})

if __name__ == "__main__":
    app.run()
