import urllib.request
import urllib.parse
import urllib.error
import ssl
import os
from urllib.request import Request, urlopen
import urllib.request
import re
from PyLyrics import *
from textFeatureExtraction import TextFeatureExtractor


class ViewsCrawler:


    '''
    this class represents a youtube crawler, givven the youube query, the crawler will retrieve the data of the first result.
    '''

    def __init__(self):
        self.songsCompleted = 0;

    def getSongData(self,songName):

        try:
            '''
            :param songName: the query for youtube to search (updated to song and artist)
            :return: a jason object with the songs youtube data
            '''
            query_string = urllib.parse.urlencode({"search_query" : songName})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            if search_results[0]:
                url = "http://www.youtube.com/watch?v=" + search_results[0]
            else:
                print("no match found for "+songName)

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # Making the website believe that you are accessing it using a mozilla browser

            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()

            # Creating a BeautifulSoup object of the html page for easy extraction of data.

            soup = BeautifulSoup(webpage, 'html.parser')
            video_details = {}

            for span in soup.findAll('span',attrs={'class': 'watch-title'}):
                video_details['TITLE'] = span.text.strip()

            for script in soup.findAll('script',attrs={'type': 'application/ld+json'}):
                    channelDesctiption = json.loads(script.text.strip())
                    video_details['CHANNEL_NAME'] = channelDesctiption['itemListElement'][0]['item']['name']

            for div in soup.findAll('div',attrs={'class': 'watch-view-count'}):
                video_details['NUMBER_OF_VIEWS'] = div.text.strip()

            for button in soup.findAll('button',attrs={'title': 'I like this'}):
                video_details['LIKES'] = button.text.strip()

            for button in soup.findAll('button',attrs={'title': 'I dislike this'}):
                video_details['DISLIKES'] = button.text.strip()

            for span in soup.findAll('span',attrs={'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}):
                video_details['NUMBER_OF_SUBSCRIPTIONS'] = span.text.strip()

            hashtags = []
            for span in soup.findAll('span',attrs={'class': 'standalone-collection-badge-renderer-text'}):
                for a in span.findAll('a',attrs={'class': 'yt-uix-sessionlink'}):
                    hashtags.append(a.text.strip())
            video_details['HASH_TAGS'] = hashtags

            return video_details;
        except:
            if songName:
                print("error: "+ songName)
            else: print("song is null!!!!!!!!!!!!!!!")

    def processDirectory(self,directoryPath,jsonFile, verify=True):
        self.songsCompleted = 0;
        '''

        :param directoryPath: the path of the directory to iterate over
        :param jsonFile: the output json file (if does not exist -> will be created)
        :param verify: if true, will verify for each file, that an entry exists in the JSON file (by default is true)
        :return: for each song in the directory, appends the songs youtube data to the data.json file
        '''

        self.total_songs = len(os.listdir(directoryPath))
        error = {}
        no_lyrics = {}
        print("Total number of files: " + str(self.total_songs))

        # check if json file exists, if not, creates the file
        if os.path.isfile(jsonFile):
            print("File \"" + jsonFile + "\" exist")
        else:
            open(jsonFile,'w+').close()
            print("Created file \"" + jsonFile + "\"")

        # Open current JSON FILE
        with open(jsonFile) as json_file:
            try: # valid JSON file
                data = json.load(json_file)
            except:
                data = {}

            # iterate over all files in the given directory
            print("Sending crawlers...")
            for filename in os.listdir(directoryPath):
                songName = self.getSongName(filename)
                if not songName:
                    print(filename + " is null!!!")
                    continue

                self.addSongData(songName,data,error, filename,no_lyrics)
                with open(jsonFile, 'w', encoding='utf8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=4)

        if (len(error) > 0):
            print("\n\nerror in(" + str(len(error)) + "):\n" + str(error))
        if (len(no_lyrics) > 0):
            print("\n\nno lyrics for(" + str(len(no_lyrics)) + "):\n" + str(no_lyrics))
        # verify the data
        if verify:
            print("\n----------------------------------------------")



    def getFeatures(self,lyrics):

        '''
        breaks text into features
        :param lyrics: the text to break down
        :return: features
        '''
        tfe = TextFeatureExtractor()
        return tfe.extract(lyrics)


    def addSongData(self,songName, dictionary,error,fileName,no_lyrics):
        '''
        the functions gets the song data from youtube (views) and get the songs lyrics and text features, then adds it to the given dictionary(json file).
        the process is cached in the json file -> if you the song was allready processed and the lyrics where found, it will skip the song
        :param songName: song name
        :param dictionary: a valid json object
        :param error: list of files no youtub match found
        :param fileName: name of the file
        :param no_lyrics: a list with the number of songs that no lyrics were retrieved
        :return: adds data to the dictianary
        '''
        #   get song data from youtube
        artist = self.getArtist(fileName)
        if fileName not in dictionary:
            query = songName + " " + artist
            info = self.getSongData(query)
            #   add song data to dictionary
            dictionary[fileName] = info
            dictionary[fileName]['song_name'] = songName

        # get lyrics and fetures if they do not exist
        if 'lyrics' not in dictionary[fileName]:

            try:
                lyrics = self.getLyrics(songName,artist)

                if not lyrics:
                    no_lyrics[songName+ "->" + artist] = "no Lyrics"
                    self.errorCount = self.errorCount + 1;
                else:
                    dictionary[fileName]['lyrics'] = lyrics

                dictionary[fileName]['features'] = self.getFeatures(lyrics)
            except:
                print("error lyrics:" + songName)

        #   update and print progress
        self.songsCompleted += 1
        percent = int(self.songsCompleted / self.total_songs * 100)
        print("\rCompleted: " + str(percent) + "%", end='')




    def getSongName(self,filename):
        '''
        givan an audio file (with specific format) will retern the song name
        :param filename: the song file name
        :return: the name of the song
        '''
        try:
            filename = filename.replace('–', '-')
            songName = filename.split(" - ")[1]
            songName = songName[:-4]
            songName = songName.replace('.', '')
            if "(" in songName:
                songName = songName[0: songName.find('(') - 1] + ".mp3"

                songName = songName[:-4]
            if songName == None:
                print("this song is None: - " + filename )
                return "error"
            if songName == "null" or songName =="":
                print("this song ins null - " + filename)
                return "error"
            songName = songName.replace('[wwwmusicboltcom]', '')
            return songName
        except:
            print("Error for song name - " + filename)
            return "Unknown songName"


    def getArtist(self,filename):
        '''
        givan an audio file (with specific format) will retern the artists name
        :param filename: the song file name
        :return: the artist of the song
        '''
        try:
            filename.replace('–', '-')
            artist =filename.split(" - ")[0]
            artist = artist.split(".")[1]
            artist = artist[1:]
            if ',' in artist:
                artist = artist.split(',')[0]
            if ' feat' in artist:
                artist = artist.split(' feat')[0]

            return artist
        except:
            return "unKnowned"

    def getLyrics(self,songName,artist):
        '''
        retreves lyrics from Genius.com API
        :param songName: the song name
        :param artist: the artist name
        :return: lyrics if found, else 'None'.
        '''
        try:
            lyrics = PyLyrics.getLyrics(artist, songName)
            return lyrics
        except: #try again with lower case
            try:
                lyrics = PyLyrics.getLyrics(artist.lower(), songName.lower())
                return lyrics
            except: # not found -> return null
                return None
