import urllib, json, string, sys, argparse, cStringIO

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
sound_list = []

api_url = "http://api.soundcloud.com/"
base_url = "http://soundcloud.com/"
client_id= "" #Your client id here.

def resolveTrack(url):
	link = api_url + "resolve.json?client_id=" + client_id + "&url=" + url
	f = urllib.urlopen(link)
	response = f.read()
	result_json = json.loads(response)
	return {
	'title': result_json['title'].encode(sys.stdout.encoding, errors='replace'), 
	'streamURL': result_json['stream_url'], 
	'user': result_json['user']['username'].encode(sys.stdout.encoding, errors='replace'), 
	'albumart': result_json['artwork_url'], 
	'genre': result_json['genre'], 
	'bpm': result_json['bpm']
	}
	
def getTracks(username):
	try:
		link = api_url + "users/" + username + "/tracks/?client_id=" + client_id + "&format=json"
		f = urllib.urlopen(link)
		response = f.read()
		result_json = json.loads(response)
		prepareTracks(result_json)
	except Exception as e:
		print "An unexpected error has occurred... [" + str(e) + "]"
	
def prepareTracks(result):
	print "\n"	
	count = 0
	
	for x in result:
		res = resolveTrack(base_url + x['user']['permalink'] + "/" + x['permalink'])
		sound_list.append(res)
		print "[" + str(count) + "] Found: " + res['user'] + " - " + res['title']
		count = count + 1
		
	if not sound_list:
		print "No music found!"
	else:
		print "\nEnter the numbers to download, separated by commas (no spaces)"
		print "\"all\" if you want to download them all.\n"
		print "\"x\" if you want to exit.\n"
		download = raw_input("Choice(s): ")
		
		if download.lower() == "x":
			raise SystemExit
		elif download.lower() == "all":
			for y in range(len(sound_list)):
				downloadTrack(y)
		else:
			for y in download.split(","):
				downloadTrack(y)

				

def getMetadata(data, filename):
	try:
		import eyed3
		import eyed3.id3
		data = sound_list[int(data)]

		audiofile = eyed3.core.load(filename)
		audiofile.tag = eyed3.id3.Tag()
		audiofile.tag.artist = unicode(data['user'])
		audiofile.tag.title = unicode(data['title'])
		audiofile.tag.genre = unicode(data['genre'])
		if not data['bpm'] == None: 
			audiofile.tag.bpm = unicode(data['bpm'])
		if not data['albumart'] == None:
			img_filename = filename.split(".mp3")[0] + ".jpg"
			urllib.urlretrieve (data['albumart'], img_filename)
			img_data = open(img_filename,"rb").read()
			audiofile.tag.images.set(3,img_data,"image/jpeg",u"Cover")
		audiofile.tag.save(filename)
		
	except Exception as e:
		pass
	


def dlProgress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("[" + "#"*(percent/10) + " "*(10 - (percent/10)) + "] %2d%%" % percent)
      sys.stdout.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
      sys.stdout.flush()
	  
def downloadTrack(info):
	print "\n"	
	name = sound_list[int(info)]['user'] + " - " + sound_list[int(info)]['title']
	try:
		url = sound_list[int(info)]['streamURL'] + "?client_id=" + client_id
		sys.stdout.write("Downloading " + name + "... ")    
		filename = ''.join(c for c in name if c in valid_chars) + ".mp3"
		urllib.urlretrieve (url, filename, reporthook=dlProgress)
		if args.m == True:
			getMetadata(info, filename)
	except Exception, e:
		print "\nError downloading file [" + name + "]!" + str(e)
		pass


def getPlaylist(url):
	try:
		print "\n"
		link = api_url + "resolve.json?client_id=" + client_id + "&url=" + url
		f = urllib.urlopen(link)
		response = f.read()
		result_json = json.loads(response)
		prepareTracks(result_json['tracks'])
	except Exception as e:
		print "An unexpected error has occurred... [" + str(e) + "]"

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
