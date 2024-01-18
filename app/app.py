import sys
import bleach
from flask import Flask, request, redirect
from ytmusicapi import YTMusic

ytmplaylists = []
playlistmeta = {
	"id": "",
	"name": "",
	"tracks": []
}

app = Flask(__name__)
#ytm = YTMusic("oauth.json")
ytm = YTMusic("oauth.json")

def dtd(html):
	return "<!DOCTYPE html>\r\n" + html

def html(head, body):
	return "<html>\r\n" + head + "\r\n" + body + "\r\n" + "</html>\r\n"

def head():
	return "<head>\r\n" + "<meta charset='utf-8'>\r\n" + "<title>\r\n" + "Current Playlist\r\n" + "</title>\r\n" + "</head>\r\n"

def body():
	return "<body>\r\n" + title() + hr() + content() + "</body>\r\n"

def title():
	content = ""
	content = content + "<h1>\r\n" + playlistmeta["name"] + "\r\n" + "</h1>\r\n"
	content = content + form()

	return content

def form():
	content = ""
	content = content + "<form action='/refresh' method='POST'>\r\n"
	content = content + "<select name='playlist'>\r\n"
	for pl in ytmplaylists:
		pl["title"] = pl["title"].replace("'", "")
		content = content + "<option value='"+pl["title"]+"/"+pl["playlistId"]+"'"
		if pl["title"] == playlistmeta["name"]:
			content = content + " selected"
		content = content + ">"
		content = content + pl["title"]+"\r\n"
		content = content + "</option>\r\n"
	content = content + "</select>\r\n"
	content = content + "<input type='submit' value='submit'>\r\n"
	content = content + "</form>\r\n"

	return content

def hr():
	return "<hr>\r\n"

def content():
	content = ""
	content = content + "<table>\r\n"
	for tr in playlistmeta["tracks"]:
		content = content + "<tr>\r\n"
		content = content + track(tr)
		content = content + "</tr>\r\n"

	content = content + "</table>\r\n"
	return content

def track(tr):
	artists = "not found"
	album = "not found"
	title = "not found"

	if tr["artists"] is not None:
		artists = trackArtists(tr["artists"])

	if tr["album"] is not None:
		if tr["album"]["name"] is not None:
			album = tr["album"]["name"]

	if tr["title"] is not None:
		title = tr["title"]

	content = ""
	content = content + "<td>\r\n"
	content = content + artists + "\r\n"
	content = content + "</td>\r\n"
	content = content + "<td>\r\n"
	content = content + album + "\r\n"
	content = content + "</td>\r\n"
	content = content + "<td>\r\n"
	content = content + title + "\r\n"
	content = content + "</td>\r\n"

	return content

def trackArtists(artists):
	al = []
	for ar in artists:
		name = "not found"
		if ar["name"] is not None:
			name = ar["name"]
		al.append(name)

	return ", ".join(al)

def metaRefreshPlaylists():
	global ytmplaylists

	ytmplaylists = []
	rsp = ytm.get_library_playlists(limit = None)
	ytmplaylists = [ { "playlistId": pl["playlistId"], "title": bleach.clean(pl["title"]) } for pl in rsp]

def metaRefreshTracks():
	global playlistmeta

	playlistmeta["tracks"] = []

	if playlistmeta["id"] == "":
		raise Exception("BUG")

	rsp = ytm.get_playlist(playlistmeta["id"], limit = None)
	for tr in rsp["tracks"]:
		tr["title"] = bleach.clean(tr["title"])
		if tr["album"] is not None:
			tr["album"]["name"] = bleach.clean(tr["album"]["name"])
		if tr["artists"] is not None:
			for ar in tr["artists"]:
				ar["name"] = bleach.clean(ar["name"])
		playlistmeta["tracks"].append(tr)

@app.route("/", methods = ["GET"])
def hRoot():
	global ytmplaylists, playlistmeta

	if len(ytmplaylists) == 0:
		metaRefreshPlaylists()

	if playlistmeta["name"] == "":
		playlistmeta["name"] = "Pick one!"
		playlistmeta["id"] = ""

	return dtd(html(head(), body()))

@app.route("/refresh", methods = ["POST"])
def hRefresh():
	global playlistmeta, ytmplaylists

	elems = request.form["playlist"].split("/")
	if len(elems) != 2:
		raise Exception("BUG")
		return redirect("/")

	ii = 0
	for ii in range(len(ytmplaylists)):
		if ytmplaylists[ii]["playlistId"] == elems[1]:
			break
	if ii >= len(ytmplaylists):
		# Somebody tried an injection attack?
		print("ERROR: posted unknown id: ", elems[1])
	else:
		if playlistmeta["id"] != elems[1]:
			playlistmeta["name"] = elems[0]
			playlistmeta["id"] = elems[1]
			playlistmeta["tracks"] = []
			metaRefreshTracks()

	return redirect("/")

hostip = "192.168.0.74"
hostport = "5678"
if len(sys.argv) > 1:
	hostip = sys.argv[1]
if len(sys.argv) > 2:
	hostport = sys.argv[2]

if __name__ == "__main__":
	app.run(host = hostip, port = hostport)

