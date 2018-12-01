#!/usr/bin/env python
# -*- coding: utf-8

import sys
import Queue
from bdt2s import T2S
from Player import Player

import time, sys, random
from danmu import DanMuClient
from utils import *

random.seed(None)
color = Colored()

if len(sys.argv) < 2 or sys.argv[1] == '-h':
    print('Usage: python %s <roomId>' % __file__)
    sys.exit(0)

dmc = DanMuClient('http://www.douyu.com/{}'.format(sys.argv[1]))
if not dmc.isValid(): print('Url not valid')

t2s = T2S("./config")
t2s.initT2S()

TASK_QUEUE = Queue.Queue(10)
player = Player(TASK_QUEUE)
player.daemon = True

def pp(msg):
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'black']
    color_name = random.choice(colors)
    color_render = getattr(color, color_name)
    msg = msg.encode(sys.stdin.encoding, 'ignore').decode(sys.stdin.encoding)
    print(color_render(msg))

@dmc.danmu
def danmu_fn(msg):
    text = '[%*s] >> %s' % (20-wide_chars(msg['NickName']), msg['NickName'], msg['Content'])
    pp(text)
    text = msg['NickName'] + u'说' + msg['Content']
    textVoice = t2s.getT2S(text.encode('utf-8'))
    if not TASK_QUEUE.full():
        if random.random() < 0.2:
            TASK_QUEUE.put(textVoice)

@dmc.gift
def gift_fn(msg):
    text = '[%*s] >> %s' % (20-wide_chars(msg['NickName']), msg['NickName'], u'送礼物了')
    pp(text)

#@dmc.other
#def other_fn(msg):
#    pp(u'收到其它消息')

player.start()
dmc.start(blockThread=True)
