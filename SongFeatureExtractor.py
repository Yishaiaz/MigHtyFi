import numpy as np
import os
import warnings
from AudioFeatureExtractor import SingleAudioFeatureExtractor
from CrawlerTool import CrawlerTool


def song_processing(audio_file_path, song_name, artist_name):
    audio_feature_extractor = SingleAudioFeatureExtractor(audio_file_path)
    if not audio_feature_extractor:
        return None
    lyrics_feature_extractor = CrawlerTool()
    audio_features = audio_feature_extractor.extract_features()
    song_crawler_data = lyrics_feature_extractor.processSingleSong(songName=song_name, artist=artist_name)
    lyrics_features_dict = song_crawler_data['features']
    lyrics_features = np.array(list(lyrics_features_dict.values()))
    features = np.hstack((audio_features, lyrics_features))
    y = song_crawler_data['numberOfViews']
    youtube_title = song_crawler_data['youTube_title']
    lyrics = song_crawler_data['lyrics']
    return {'features': features, 'y': y, 'youtube_title': youtube_title, 'lyrics': lyrics}


file_path = 'C:\\Dan\\UNI\\Jarta.Projects\\MigHtyFi\\data\\2015\\01. Mark Ronson - Uptown Funk[www.musicbolt.com].mp3'
song_name = 'Uptown Funk'
artist = 'Mark Ronson'

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        print(song_processing(file_path, song_name, artist))
