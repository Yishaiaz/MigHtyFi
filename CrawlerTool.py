import json
import pandas as pd
from ViewsCrawler import ViewsCrawler as vc
from textFeatureExtraction import TextFeatureExtractor
import os

class CrawlerTool:

    def __init__(self):
        self.vc = vc()


    def processMultiDirectories(self,directory):
        '''
        will iterate over a directory that has directories with songs
        :param directory: a directory with directories with songs
        :return: prints resalts
        '''
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            if os.path.isdir(path):
                self.processSingleDirectory(path)





    def processSingleDirectory(self,directory):
        '''
        iterates over all of the songs in a directory, retrievs data from you tube and lyrics features, saves them to a
        json file and a csv file in thislocal path
        :param directory: a directory with songs
        :return: prints resalts
        '''

        dataFile = directory.split('/')[-1] + ".json"
        print("******************************************************************************\nworking on -->" + dataFile)
        print('retrieving data from youtube:')
        self.vc.processDirectory(directory, dataFile, False)
        print("\nCreating SCV file: " + dataFile, end='')
        self.jsonToCSV(dataFile)
        print(' ----> Done!')






    def jsonToCSV(self,jsonFile):
        '''
        creates a csv file out of the "number of views" and "features in the json file
        :param jsonFile: the json file created bt the ViewCrawler
        :return: creates csv file
        '''
        try:
            name = []
            feature1 = []
            feature2 = []
            feature3 = []
            feature4 = []
            Y = []
            with open(jsonFile) as json_file:

                    data = json.load(json_file)
                    for song in data:
                        name.append(song)
                        if 'NUMBER_OF_VIEWS' in data[song]:
                            y = data[song]['NUMBER_OF_VIEWS'].split(' ')
                            Y.append(y[0].replace(',', ''))
                        else:
                            Y.append(None)

                        if 'features' in data[song]:
                            feature1.append(data[song]['features']['most Freq'])
                            feature2.append(data[song]['features']['repetitive'])
                            feature3.append(data[song]['features']['offensive'])
                            feature4.append(data[song]['features']['spellScheck'])
                        else:
                            feature1.append(None)
                            feature2.append(None)
                            feature3.append(None)
                            feature4.append(None)

                    dict = {'name': name, 'most Freq': feature1, 'repetitive': feature2, 'offensive' : feature3, 'spellScheck' : feature4, 'Y' : Y }
                    df = pd.DataFrame(dict)
                    # saving the dataframe
                    csv_file = jsonFile.split('.jso')[0] + '.csv'
                    df.to_csv(csv_file)
        except:
            print("error converting json to csv")



    def processSingleSong(self,songName,artist):
        '''
        will process a single given song
        :param songName: song name
        :param artist: the artist name
        :return: a dictianary containing the number of views and the features
        '''
        try:
            youtube_data = self.vc.getSongData(songName + " " + artist)
            lyrics = self.vc.getLyrics(songName,artist)
            tfe = TextFeatureExtractor()
            features = tfe.extract(lyrics)
            return {'numberOfViews' : youtube_data['NUMBER_OF_VIEWS'], 'features' : features,'youTube_title' : youtube_data['TITLE'] }
        except:
            print("error processing song: " + songName + " " + "("+artist+")")
            return None



crawlerTool = CrawlerTool()
# crawlerTool.processSingleDirectory('/Users/yanivleedon/Desktop/university/adir/Archive/Archive/test')
print(crawlerTool.processSingleSong('Perfect','Ed Sheeran'))