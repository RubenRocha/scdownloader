import urllib.request
import json
import string
import sys
import argparse
import os

import traceback

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
sound_list = []

api_url = "http://api.soundcloud.com/"
base_url = "http://soundcloud.com/"
client_id = ""  # Your client id here.


def resolveTrack(url):
    link = api_url + "resolve.json?client_id=" + client_id + "&url=" + url
    f = urllib.request.urlopen(link)
    response = f.read()
    result_json = json.loads(str(response.decode("utf-8")))
    return {
        'title': result_json['title'],
        'streamURL': result_json['stream_url'],
        'user': result_json['user']['username'],
        'albumart': result_json['artwork_url'],
        'genre': result_json['genre'],
        'bpm': result_json['bpm']
    }


def getTracks(username):
    try:
        link = api_url + "users/" + username + \
            "/tracks/?client_id=" + client_id + "&format=json"
        f = urllib.request.urlopen(link)
        response = f.read()
        result_json = json.loads(str(response.decode("utf-8")))
        prepareTracks(result_json)
    except Exception as e:
        print("An unexpected error has occurred... [{}]".format(str(e)))


def prepareTracks(result):
    count = 0

    for x in result:
        res = resolveTrack(base_url + x['user']
                           ['permalink'] + "/" + x['permalink'])
        sound_list.append(res)
        print("[{}] Found: {} - {}".format(str(count), res['user'], res['title']))
        count = count + 1

    if not sound_list:
        print("No music found!")
    else:
        print("\nEnter the numbers to download, separated by commas (no spaces)")
        print("\"all\" if you want to download them all.")
        print("\"x\" if you want to exit.\n")
        download = input("Choice(s): ")

        if download.lower() == "x":
            raise SystemExit
        elif "all" in download.lower():
            for y in range(len(sound_list)):
                downloadTrack(y)
        else:
            for y in download.split(","):
                downloadTrack(y)


def getMetadata(data, filename):
    try:
        import eyed3
        import eyed3.id3
        eyed3.log.setLevel("ERROR")
        data = sound_list[int(data)]

        audiofile = eyed3.core.load(filename)
        audiofile.tag = eyed3.id3.Tag()
        if not data['user'] == None:
            audiofile.tag.artist = data['user']
        if not data['title'] == None:
            audiofile.tag.title = data['title']
        if not data['genre'] == None:
            audiofile.tag.genre = data['genre']
        if not data['bpm'] == None:
            audiofile.tag.bpm = data['bpm']
        if not data['albumart'] == None:
            img_filename = filename.split(".mp3")[0] + ".jpg"
            urllib.request.urlretrieve(data['albumart'], img_filename)
            img_data = open(img_filename, "rb").read()
            audiofile.tag.images.set(3, img_data, "image/jpeg", u"Cover")
            os.remove(img_filename)

        audiofile.tag.save(filename)

    except Exception as e:
        pass


lp = 0


def dlProgress(count, blockSize, totalSize):
    global lp
    percent = int(count * blockSize * 100 / totalSize)
    hs = percent / 10
    if percent % 10 == 0 and percent <= 100 and not lp == percent:
        lp = percent
        sys.stdout.write("\n\t[{}{}] {:.0f}%".format(
            "#" * int(hs), " " * int(10 - hs), percent))
        sys.stdout.flush()


def downloadTrack(info):
    name = sound_list[int(info)]['user'] + " - " + \
        sound_list[int(info)]['title']
    try:
        url = sound_list[int(info)]['streamURL'] + "?client_id=" + client_id
        sys.stdout.write("\nDownloading " + name + "... ")
        filename = ''.join(c for c in name if c in valid_chars) + ".mp3"
        urllib.request.urlretrieve(url, filename, reporthook=dlProgress)
        if args.m == True:
            getMetadata(info, filename)
    except Exception as e:
        print("\nError downloading file {} [{}]".format(name, str(e)))
        pass


def getPlaylist(url):
    try:
        link = api_url + "resolve.json?client_id=" + client_id + "&url=" + url
        f = urllib.request.urlopen(link)
        response = f.read()
        result_json = json.loads(str(response.decode("utf-8")))
        prepareTracks(result_json['tracks'])
    except Exception as e:
        print("An unexpected error has occurred... [{}]".format(str(e)))

parser = argparse.ArgumentParser(description='Soundcloud downloader')
parser.add_argument('-u', metavar='username', type=str,
                    help='A username to get the tracks of.')
parser.add_argument('-p', metavar='playlist', type=str,
                    help='A playlist URL to get the tracks of.')
parser.add_argument('-m', action='store_true',
                    help='Enables fetching metadata (requires eyed3 module)')
args = parser.parse_args()

if args.u:
    getTracks(args.u)
elif args.p:
    getPlaylist(args.p)
