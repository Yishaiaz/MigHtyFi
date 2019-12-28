import threading
import os
from PyLyrics import *
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

from textFeatureExtraction import TextFeatureExtractor


class LyricsCrawler:


    '''
    this class represents a youtube crawler, givven the youube query, the crawler will retrieve the data of the first result.
    '''

    def __init__(self):
        self.songsCompleted = 0;
        self.errorCount = 0;



    def processDirectory(self,directoryPath,jsonFile, verify=True):
        '''

        :param directoryPath: the path of the directory to iterate over
        :param jsonFile: the output json file (if does not exist -> will be created)
        :param verify: if true, will verify for each file, that an entry exists in the JSON file (by default is true)
        :return: for each song in the directory, appends the songs youtube data to the data.json file
        '''

        print("entered")
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
                try:
                    songName = self.getSongName(filename)
                    if not songName:
                        continue
                    artist = self.getArtist(filename)
                except:
                    error[filename + "-> song: " +songName+ ", artist: " + artist] = "error"
                    continue


                self.addSongLyrics(songName,artist,data,error,filename)

                # # create new Thread to activate a crawler to get song lyrics
                # thread = threading.Thread(target=self.addSongLyrics, args=(songName,artist,data,error))
                # # print(songName + ", " + artist)
                # threads.append(thread)
                # thread.start()

        # save the JSON file
        # for index, thread in enumerate(threads):
        #     thread.join()
        with open(jsonFile, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

        if(len(error) > 0):
            print("\n\nNo Lyrics Found For(" + str(self.errorCount) + "):\n" + str(error))





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



    def getFeatures(self,lyrics):
        tfe = TextFeatureExtractor()
        return tfe.start(lyrics)

    def addSongLyrics(self,songName, artist, dictionary,error,fileName):
        '''
        the functions gets the song data from youtube and adds it to the given dictionary.
        :param songName: the song to search for.
        :param dictionary: a dictionary to add the data to
        :param total_songs: the total number of songs that are being searched (for progress)
        :return: nothing -> prints the progress %
        '''
        #   get song data
        # if dictionary[songName] != None:
        #     return

        try:
            lyrics = self.getLyrics(songName,artist)

            if not lyrics:
                error[songName+ "->" + artist] = "no Lyrics"
                self.errorCount = self.errorCount + 1;

            #   add song data to dictionary
            else:
                dictionary[fileName]['lyrics'] = lyrics
                dictionary[fileName]['features'] = self.getFeatures(lyrics)

            #   update and print progress
            self.songsCompleted += 1
            percent = int(self.songsCompleted / self.total_songs * 100)
            print("\rCompleted: " + str(percent) + "%", end='')
        except:
            print("something went wrong: " + songName + ", " + artist)









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
                return None
            return songName
        except:
            print("Error for song name - " + filename)
            return None




    def getLyrics(self,songName,artist):
        try:
            lyrics = PyLyrics.getLyrics(artist, songName)
            return lyrics
        except:
            try:
                lyrics = PyLyrics.getLyrics(artist.lower(), songName.lower())
                return lyrics
            except:
                # print(songName + "," + artist)
                return None
            # print(songName +"," + artist)
            #     return None

