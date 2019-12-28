import threading
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import os
from urllib.request import Request, urlopen
import urllib.request
import re


class ViewsCrawler:


    '''
    this class represents a youtube crawler, givven the youube query, the crawler will retrieve the data of the first result.
    '''

    def __init__(self):
        self.songsCompleted = 0;
        self.errorCount = 0

    def getSongData(self,songName):

        try:
            '''
            :param songName: the name of the song to search
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
        '''

        :param directoryPath: the path of the directory to iterate over
        :param jsonFile: the output json file (if does not exist -> will be created)
        :param verify: if true, will verify for each file, that an entry exists in the JSON file (by default is true)
        :return: for each song in the directory, appends the songs youtube data to the data.json file
        '''

        self.total_songs = len(os.listdir(directoryPath))
        threads = list()
        error = {}
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
                self.addSongData(songName,data,error, filename)
        #         # create new Thread to activate a crawler to get song data from YouTube
        #         thread = threading.Thread(target=self.addSongData, args=(songName,data,error))
        #         threads.append(thread)
        #         thread.start()
        #
        # # save the JSON file
        # for index, thread in enumerate(threads):
        #     thread.join()
        with open(jsonFile, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

        if (len(error) > 0):
            print("\n\nNo Lyrics Found For(" + str(self.errorCount) + "):\n" + str(error))
        # verify the data
        if verify:
            print("\n----------------------------------------------")
            self.verifyData(directoryPath,jsonFile)


    def verifyData(self, directoryPath, jsonFile):
        '''
        the function verifies that all songs in the directory have a valid "NUMBER_OF_VIEWS" (and over 10) in the JSON file
        :param directoryPath: the path of the directory to iterate over its files
        :param jsonFile: the json file with the data
        :return: nothing, will print the results
        '''

        try:
            print("Validating data...\n")
            error = 0;
            min = -1;
            minSong = ""

            # open data file
            with open(jsonFile) as json_file:
                data = json.load(json_file)

            # iterate over all songs in directory
            for filename in os.listdir(directoryPath):
                songName = self.getSongName(filename)
                try:
                    # get number of views
                    views_raw = data[songName]["NUMBER_OF_VIEWS"].split(" ")
                    views = int(views_raw[0].replace(",",""))

                    #   update "min views"
                    if min == -1:
                        min = views
                        minSong = songName
                    else:
                        if views < min:
                            min = views
                            minSong = songName

                    # indicate less than 10 views
                    if views < 10:
                        print("*** NOTE: The song "+ songName + " has less than 10 views (" + str(views) + ")  ***\n")

                except:
                    error += 1
                    print("--------  Missing \"NUMBER_OF_VIEWS\" for: \"" + songName + "\"--------\n")

            #   no errors found indication
            if error == 0 :
                print("All songs have a valid \"VIEWS\" field")
                print("NOTE: the song with the least views is \"" + minSong + "\", views: " + str(min))

        except:
            print("something went wrong\n")
            return



    def addSongData(self,songName, dictionary,error,fileName):
        '''
        the functions gets the song data from youtube and adds it to the given dictionary.
        :param songName: the song to search for.
        :param dictionary: a dictionary to add the data to
        :param total_songs: the total number of songs that are being searched (for progress)
        :return: nothing -> prints the progress %
        '''
        #   get song data
        # print("33333333 " + songName)
        query = songName + " " + self.getArtist(fileName)
        info = self.getSongData(query)

        if not info:
            error[songName] = "no data"
            self.errorCount = self.errorCount + 1;

        #   add song data to dictionary
        dictionary[fileName] = info
        dictionary[fileName]['song_name'] = songName

        #   update and print progress
        self.songsCompleted += 1
        percent = int(self.songsCompleted / self.total_songs * 100)
        print("\rCompleted: " + str(percent) + "%", end='')


    def getSongName(self,filename):
        try:
            filename = filename.replace('–', '-')
            songName = filename.split(" - ")[1]
            songName = songName[:-4]
            if "(" in songName:
                songName = songName[0: songName.find('(') - 1] + ".mp3"

                songName = songName[:-4]
            if songName == None:
                print("this song is None: - " + filename )
                return "error"
            if songName == "null" or songName =="":
                print("this song ins null - " + filename)
                return "error"
            return songName
        except:
            print("Error for song name - " + filename)
            return "Unknown songName"


    def getArtist(self,filename):
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
