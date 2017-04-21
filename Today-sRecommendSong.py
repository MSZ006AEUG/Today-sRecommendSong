import sys, random, urllib.request, json, requests
import io #デバッグ用
from lxml import etree
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#Read XML
xml_path = "C:/Users/ZETA/Music/iTunes/iTunes Music Library.xml"
tree = etree.parse(xml_path)
root = tree.getroot()

songs = root.findall("dict/dict/dict")


#Get information of each songs
song_info_list = []
for song in songs:
    song_info = {}
    key = ""
    for element in song:
        if element.tag == "key":
            key = element.text
        else:
            song_info[ key ] = element.text
    song_info_list.append( song_info )


#Decide Today's song
TodaysSong = random.choice(song_info_list)


#Get information of a song
SongTitle = TodaysSong["Name"]
ArtistName = TodaysSong["Artist"]
AlbumTitle = TodaysSong["Album"]
SongYear = TodaysSong["Year"]


#Get Artwork
'''JsonURL = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch?"
JsonURL = JsonURL + "term=" + SongTitle + "&term=" + ArtistName  + "&term=" + AlbumTitle  + "&country=JP&entity=musicTrack"

response = urllib.request.urlopen(JsonURL)
content = json.loads(response.read().decode("utf-8"))
print(content)
print(":{}".format(content['collectionViewUrl']))
iTunesURL = ":{}".format(content['collectionViewUrl'])'''


#Post to Slack
PostText = "本日の1曲\n" + SongTitle + " / " + ArtistName + " (" + SongYear + ") from " + AlbumTitle
requests.post("https://hooks.slack.com/services/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", data = json.dumps({
    "text": PostText,
    "username": u"Today's Recommend Song",
    "icon_emoji": u":psychedelic:",
    "link_names": 1,
}))

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
#print(song_info_list)
