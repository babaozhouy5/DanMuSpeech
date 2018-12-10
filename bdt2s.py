# -*- coding: utf-8

from __future__ import print_function
import requests

import time
import datetime

from utils import assertUTF8, uniqueString, loadConf, writeConf

class T2S(object):

    def __init__(self, conf_path):
        self.conf_path = conf_path
        self.conf = loadConf(conf_path)

        self.appKey = self.conf["appKey"]
        self.appSecret = self.conf["appSecret"]
        self.tokenInfos = self.conf["token"]
        self.vtsInfos= self.conf["vts"]


    def reqThing(self, url, data, method):
        reqMethod = getattr(requests, method)
        if not reqMethod:
            print("Method [{}] doesn't support!".format(method))
            return None
        req = reqMethod(url, data=data, params=data, timeout=5)
        if req.status_code != 200:
            return None
        return req

    def getToken(self):
        if self.tokenInfos["accessToken"] != "" and time.time() <= int(self.tokenInfos["expire"]):
            print("Load AccessToken OK!")
            self.accessToken = self.tokenInfos["accessToken"]
        else:
            print("AccessToken useless, need to re-get!")

            url = self.tokenInfos["url"]
            sendData = {"grant_type": self.tokenInfos["grant_type"],
                        "client_id": self.appKey,
                        "client_secret": self.appSecret}
            method = self.tokenInfos["method"]
            ret = self.reqThing(url, sendData, method)
            if ret:
                print("Get new AccessToken OK!")
                content = ret.json()
                self.accessToken = content["access_token"]
                expire = content["expires_in"]

                self.conf["token"]["expire"] = int(time.time() + expire)
                self.conf["token"]["accessToken"] = self.accessToken
                writeConf(self.conf, conf_path=self.conf_path)

    def initT2S(self):
        self.getToken()

    def getT2S(self, text):
        assert assertUTF8(text) == True, "Input text must be encode with UTF-8!"

        url = self.vtsInfos["url"]
        sendData = {"tex": text,
                    "tok": self.accessToken,
                    "cuid": uniqueString(size=30),
                    "ctp": 1,
                    "lan": "zh",
                    }
        method = self.vtsInfos["method"]

        ret = self.reqThing(url, sendData, method)

        if ret:
            if ret.headers["content-type"] == "application/json":
                 content = ret.json()
                 print("Get VTS ERROR, code [{}], msg [{}]!".format(content["err_no"], content["err_msg"]))
            else:
                return ret.content
