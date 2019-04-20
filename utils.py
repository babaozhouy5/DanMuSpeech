# -*- coding: utf-8

from __future__ import print_function
import os
import md5
import json
import random
import unicodedata

ZH_PUNCT = [u'？', u'！', u'。', u'，', u'、', u'：', u"“", u"”", u"（", u"）", u"；", u"《", u"》"]

def wide_chars(s):
    return sum(unicodedata.east_asian_width(x)=='W' or x in ZH_PUNCT for x in s)

def width(s):
    return len(s) + wide_chars(s)

def assertUTF8(text):
    flag = True
    try:
        text.decode('utf-8')
    except UnicodeError as error:
        flag = False
    return flag

def uniqueString(size=30):
    secretSrc = 'babaozhouy5'
    salt = random.randint(32768, 65536)
    sign = secretSrc + str(salt)
    m1 = md5.new()
    m1.update(sign)
    return m1.hexdigest()[:size]

def loadConf(conf_path):
    with open(conf_path) as fp:
        return json.loads(fp.read())

def writeConf(conf, conf_path="./config"):
    with open(conf_path, "w") as fw:
        conf = json.dumps(conf, indent=4, sort_keys=True)
        fw.write(conf)

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


from colorama import  init, Fore, Back, Style
init(autoreset=True)
class Colored(object):

    def red(self, s):
        return Fore.RED + s + Fore.RESET

    def green(self, s):
        return Fore.GREEN + s + Fore.RESET

    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET

    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET

    def magenta(self, s):
        return Fore.MAGENTA + s + Fore.RESET

    def cyan(self, s):
        return Fore.CYAN + s + Fore.RESET

    def white(self, s):
        return Fore.WHITE + s + Fore.RESET

    def black(self, s):
        return Fore.BLACK

    def white_green(self, s):
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET


if __name__ == "__main__":
    # ----------使用示例如下:-------------
    print(uniqueString(100))

    writeConf({'a':1, 'b':2, 'c':{'d':3, 'e':5}}, 'test.conf')

    if not which("ffmpeg.exe"):
        print("ffmpeg: Executable not found on machine.")
        raise Exception("Dependency not found: ffmpeg.exe")

    color = Colored()
    print(color.red('I am red!'))
