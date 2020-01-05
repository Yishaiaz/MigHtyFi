import pandas as pd
import numpy as np
import librosa
import librosa.display
import copy
import os
import warnings
warnings.filterwarnings('ignore')


class AudioFeatureExtractor:
    """
    Extract features from all the audio files in a given directory
    """
    def __new__(cls, dir_path, *args, **kwargs):
        """
        check if the directory is a valid path, else not creating the instance
        :param dir_path: the given directory path
        :return: an instance of this class iff the given directory path is a valid directory path
        :raise: ValueError if the given directory path is not a valid path
        """
        instance = super(AudioFeatureExtractor, cls).__new__(cls)
        if not os.path.isdir(dir_path):
            raise ValueError('{} is not a directory path'.format(dir_path))
        return instance

    def __init__(self, dir_path):
        """
        initializing the instance
        :param dir_path: the path to the given directory where all the audio files are
        """
        self.dir_path = dir_path
        self.file_types = ['mp3', 'wav']
        self.file_names = [f for f in os.listdir(dir_path) if self.insert_to_files(f)]
        # self.__features = {'tempo': [], 'first_beat': [], 'max_volume(dB)': [],
        #                    'volume_sd(dB)': [], 'max_volume(PW)': [], 'volume_sd(PW)': [], 'zero_crossing': [],
        #                    'zcr': [], 'mean_fit_coefficient0': [], 'mean_fit_coefficient1': [],
        #                    'mean_fit_coefficient2': [], 'mean_flatness': [], 'mean_harmonic_flatness': []}

        self.__features = {'tempo': [], 'first_beat': [], 'max_volume(PW)': [], 'volume_sd(PW)': [], 'zcr': [],
                           'mean_fit_coefficient0': [], 'mean_fit_coefficient1': [], 'mean_fit_coefficient2': [],
                           'mean_flatness': [], 'mean_harmonic_flatness': []}

    def insert_to_files(self, file_path):
        """
        check if a given file is an audio file
        :param file_path: the path to the file
        :return: True if file is an audio file
        """
        return os.path.isfile(os.path.join(self.dir_path, file_path)) and file_path.split('.')[-1] in self.file_types

    def __repr__(self):
        data = pd.DataFrame(self.__features)
        return str(data.reindex(data['song']))

    def extract_features(self):
        """
        extract the features for each song in directory
        :return: (pandas DataFrame) the features for all the songs
        """
        for song in self.file_names:
            song = os.path.join(self.dir_path, song)
            y, sr = librosa.load(song)
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            self.__beat_features(y_percussive, sr)
            self.__volume_features(y, sr)
            self.__zcr(y)
            self.__poly_features(y)
            self.__flatness(y, y_harmonic)

        ans = pd.DataFrame(self.__features, index=self.file_names)
        return ans

    def __beat_features(self, y_percussive, sr):
        """
        add the beat features to their list
        :param y_percussive: (np array) the percussive part of the original audio time series
        :param sr: (int) sampling rate of the audio
        """
        tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)
        beat_times = librosa.frames_to_time(frames=beat_frames, sr=sr)
        self.__features['tempo'].append(tempo)
        self.__features['first_beat'].append(beat_times[0])

    def __volume_features(self, y, sr):
        """
        add the volume features to their list
        :param y: (np array) the audio time series
        :param sr: (int) sampling rate of the audio
        """
        fmin = librosa.note_to_hz('A1')
        c = np.abs(librosa.cqt(y, sr=sr, fmin=fmin))
        # amplitude_to_decibels = librosa.amplitude_to_db(c, ref=np.max)
        # self.__features['max_volume(dB)'].append(np.max(amplitude_to_decibels))
        # self.__features['volume_sd(dB)'].append(np.std(amplitude_to_decibels))

        freqs = librosa.cqt_frequencies(c.shape[0], fmin=fmin)
        perceptual_cqt = librosa.perceptual_weighting(c**2, freqs, ref=np.max)
        self.__features['max_volume(PW)'].append(np.max(perceptual_cqt))
        self.__features['volume_sd(PW)'].append(np.std(perceptual_cqt))

    def __zcr(self, y):
        """
        add the zero crossing features to their list
        :param y: (np array) the audio time series
        """
        zcr = librosa.feature.zero_crossing_rate(y, frame_length=y.shape[0],
                                                 hop_length=y.shape[0] + 1)
        # zc = np.nonzero(librosa.zero_crossings(y))[0]
        # self.__features['zero_crossing'].append(len(zc))
        self.__features['zcr'].append(zcr[0][0])

    def __poly_features(self, y):
        """
        add the coefficients fitting of the polynomial(of degree 2) to spectrogram to their list
        :param y: (np array) the audio time series
        """
        s = np.abs(librosa.stft(y))
        p2 = librosa.feature.poly_features(S=s, order=2)
        self.__features['mean_fit_coefficient0'].append(np.mean(p2[2]))
        self.__features['mean_fit_coefficient1'].append(np.mean(p2[1]))
        self.__features['mean_fit_coefficient2'].append(np.mean(p2[0]))

    def __flatness(self, y, y_harmonic):
        """
        add the flatness features to their list
        :param y: (np array) the audio time series
        :param y_harmonic: (np array) the harmonic part of the original audio time series
        :return:
        """
        flatness = librosa.feature.spectral_flatness(y)
        harmonic_flatness = librosa.feature.spectral_flatness(y_harmonic)
        self.__features['mean_flatness'].append(np.mean(flatness))
        self.__features['mean_harmonic_flatness'].append(np.mean(harmonic_flatness))


class SingleAudioFeatureExtractor:
    """
    Extract features from a single audio file
    """
    def __new__(cls, song_path, *args, **kwargs):
        """
        check if the given song path is a valid path, else not creating the instance
        :param song_path: the given song path
        :return: an instance of this class iff the given song path is a valid audio file path, else return None
        """
        try:
            instance = super(SingleAudioFeatureExtractor, cls).__new__(cls)
            instance.__audio_time_series, instance.__sampling_rate = librosa.load(song_path)
            return instance
        except FileNotFoundError:
            return None

    def __init__(self, song_path):
        """
        initialize the instance
        :param song_path:
        """
        self.__audio_path = song_path
        self.__hop_length = 512
        self.__features = {}
        self.keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __repr__(self):
        frame = '='*50
        labels = list(self.__features.keys())
        values = list(self.__features.values())
        ans = [frame] + ['{i}. {lbl} = {val}'.format(i=i, lbl=labels[i], val=values[i]) for i in range(len(self.__features))]
        ans.append(frame)
        return '\n'.join(ans)

    def __modulate(self, modulate=0):
        """
        modulating the keys list
        :param modulate: float in tone (multiple of 0.5)
        :raise: ValueError if modulate is not a multiple of 0.5
        """
        if (abs(modulate) * 10) % 10 not in (0, 5, 0.0, 5.0):
            raise ValueError('modulate must be a multiple of 0.5')
        modulate = [self.keys[int(k+2*modulate) % 12] for k in range(12)]
        self.keys = modulate

    def get_feature_dict(self):
        """
        getter for the dictionary of the features(keys = feature labels, values = feature values)
        :return: a dictionary of the features
        """
        return copy.deepcopy(self.__features)

    def get_features_labels(self):
        """
        get the label for every feature extracted
        :return: a list full of the features labels ordered by the feature vector
        """
        return list(self.__features.keys())

    def extract_features(self):
        """
        extracting all features from given song
        :return: a NumpyArray with the values of the features by this order:
                    [tempo, first beat, max_volume(perceptual weighting), volume_sd(perceptual weighting), zcr,
                    mean_fit_coefficient(const), mean_fit_coefficient(linear), mean_fit_coefficient(quadratic),
                    mean_flatness, mean_harmonic_flatness]
        """
        self.__beat_features()
        self.__volume_features()
        self.__zcr()
        self.__poly_features()
        self.__flatness()
        return np.array(list(self.__features.values()))

    def __beat_features(self):
        """
        add the beat features to the features dict
        """
        y_harmonic, y_percussive = librosa.effects.hpss(self.__audio_time_series)
        self.__harmonic_time_series = y_harmonic
        tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=self.__sampling_rate)
        beat_times = librosa.frames_to_time(frames=beat_frames, sr=self.__sampling_rate)
        self.__features['tempo'] = tempo
        self.__features['first_beat'] = beat_times[0]

    def __volume_features(self):
        """
        add the volume features to the features dict
        """
        fmin = librosa.note_to_hz('A1')
        c = np.abs(librosa.cqt(self.__audio_time_series, sr=self.__sampling_rate, fmin=fmin))
        # amplitude_to_decibels = librosa.amplitude_to_db(c, ref=np.max)
        # max_volume_decibels = np.max(amplitude_to_decibels)
        # self.__features['max_volume(dB)'] = max_volume_decibels
        # volume_sd_decibels = np.std(amplitude_to_decibels)
        # self.__features['volume_sd(dB)'] = volume_sd_decibels
        freqs = librosa.cqt_frequencies(c.shape[0], fmin=fmin)
        perceptual_cqt = librosa.perceptual_weighting(c**2, freqs, ref=np.max)
        # max_volume_pw = np.max(perceptual_cqt)
        self.__features['max_volume(PW)'] = np.max(perceptual_cqt)
        # volume_sd_pw = np.std(perceptual_cqt)
        self.__features['volume_sd(PW)'] = np.std(perceptual_cqt)

    def __zcr(self):
        """
        add the zero crossing rate to the features dict
        """
        zcr = librosa.feature.zero_crossing_rate(self.__audio_time_series, frame_length=self.__audio_time_series.shape[0],
                                                 hop_length=self.__audio_time_series.shape[0] + 1)
        # zc = np.nonzero(librosa.zero_crossings(self.__audio_time_series))[0]
        # self.__features['zero_crossing'] = len(zc)
        self.__features['zcr'] = zcr[0][0]

    def __poly_features(self):
        """
        add the polynomial fitting coefficients to the features dict
        """
        s = np.abs(librosa.stft(self.__audio_time_series))
        p2 = librosa.feature.poly_features(S=s, order=2)
        self.__features['mean_fit_coefficient0'] = np.mean(p2[2])
        self.__features['mean_fit_coefficient1'] = np.mean(p2[1])
        self.__features['mean_fit_coefficient2'] = np.mean(p2[0])

    def __flatness(self):
        """
        add the flatness features to features dict
        """
        flatness = librosa.feature.spectral_flatness(self.__audio_time_series)
        harmonic_flatness = librosa.feature.spectral_flatness(self.__harmonic_time_series)
        self.__features['mean_flatness'] = np.mean(flatness)
        self.__features['mean_harmonic_flatness'] = np.mean(harmonic_flatness)


# wav = '.wav'
# mp3 = '.mp3'


# def test_multi_audio():
#     global wav, mp3
#     temp_dir_path = '{0}{1}data'.format(os.getcwd(), os.sep)
#     afe = AudioFeatureExtractor(temp_dir_path)
#     df = afe.extract_features()
#     print(df)
#     print(afe)


# def test_single_audio():
#     global wav, mp3
#     temp_song_path = '{0}{1}data{1}2015{1}00{2}'.format(os.getcwd(), os.sep, mp3)  ## Ed Sheeran
    # temp_song_path = '{0}{1}data{1}C{2}'.format(os.getcwd(), os.sep, wav) ## Do Re Mi...
    # temp_song_path = '{0}{1}data{1}4Chords_A{2}'.format(os.getcwd(), os.sep, wav) ## Four chords song in A
    #
    # fe = SingleAudioFeatureExtractor(temp_song_path)
    # fe.extract_features()
    # names = list(fe.get_feature_dict().keys())
    # print('\n'.join(names))


# if __name__ == '__main__':
#     with warnings.catch_warnings():
#         warnings.simplefilter('ignore')
#         test_single_audio()
#         test_multi_audio()
