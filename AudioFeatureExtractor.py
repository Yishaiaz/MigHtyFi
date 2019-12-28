import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import copy
import os
import warnings
import time


class AudioFeatureExtractor:
    def __new__(cls, song_path, *args, **kwargs):
        try:
            instance = super(AudioFeatureExtractor, cls).__new__(cls)
            instance.__audio_path = song_path
            instance.__audio_time_series, instance.__sampling_rate = librosa.load(song_path)
            return instance
        except FileNotFoundError:
            return None

    def __init__(self, song_path):
        self.__hop_length = 512
        self.__features = {}
        self.keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.current_milli_time = lambda: int(round(time.time() * 1000))
        # self.times = {}

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

    def extract_features_with_time(self):
        """
        extract features and a dict with the time it took for each group of features
        :return: np.array(features) - see more in extract_features,
                            dict(time_per_feature_group)
        """
        times = {}
        start = self.current_milli_time()
        self.__beat_features()
        end = self.current_milli_time()
        times['beat'] = (end-start)/1000
        start = self.current_milli_time()
        self.__volume_features()
        end = self.current_milli_time()
        times['volume'] = (end-start)/1000
        start = self.current_milli_time()
        self.__zcr()
        end = self.current_milli_time()
        times['zcr'] = (end-start)/1000
        start = self.current_milli_time()
        self.__poly_features()
        end = self.current_milli_time()
        times['poly'] = (end-start)/1000
        start = self.current_milli_time()
        self.__flatness()
        end = self.current_milli_time()
        times['flatness'] = (end-start)/1000
        return np.array(list(self.__features.values())), times

    def extract_features(self):
        """
        extracting all features from given song
        :return: a NumpyArray with the values of the features by this order:
                    [tempo, first beat, max_volume(amplitude to dB), volume_sd(amplitude to dB),
                    max_volume(perceptual weighting), volume_sd(perceptual weighting), zero_crossing, zcr,
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
        add the beat features to the features list
        """
        y_harmonic, y_percussive = librosa.effects.hpss(self.__audio_time_series)
        self.__harmonic_time_series = y_harmonic
        tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=self.__sampling_rate)
        beat_times = librosa.frames_to_time(frames=beat_frames, sr=self.__sampling_rate)
        self.__features['tempo'] = tempo
        self.__features['first_beat'] = beat_times[0]

    def __volume_features(self):
        fmin = librosa.note_to_hz('A1')
        c = np.abs(librosa.cqt(self.__audio_time_series, sr=self.__sampling_rate, fmin=fmin))
        amplitude_to_decibels = librosa.amplitude_to_db(c, ref=np.max)
        max_volume_decibels = np.max(amplitude_to_decibels)
        self.__features['max_volume(dB)'] = max_volume_decibels
        volume_sd_decibels = np.std(amplitude_to_decibels)
        self.__features['volume_sd(dB)'] = volume_sd_decibels
        freqs = librosa.cqt_frequencies(c.shape[0], fmin=fmin)
        perceptual_cqt = librosa.perceptual_weighting(c**2, freqs, ref=np.max)
        max_volume_pw = np.max(perceptual_cqt)
        self.__features['max_volume(PW)'] = max_volume_pw
        volume_sd_pw = np.std(perceptual_cqt)
        self.__features['volume_sd(PW)'] = volume_sd_pw

    def __zcr(self):
        zcr = librosa.feature.zero_crossing_rate(self.__audio_time_series, frame_length=self.__audio_time_series.shape[0],
                                                 hop_length=self.__audio_time_series.shape[0] + 1)
        zc = np.nonzero(librosa.zero_crossings(self.__audio_time_series))[0]
        self.__features['zero_crossing'] = len(zc)
        self.__features['zcr'] = zcr[0][0]

    def __poly_features(self):
        s = np.abs(librosa.stft(self.__audio_time_series))
        p2 = librosa.feature.poly_features(S=s, order=2)
        self.__features['mean_fit_coefficient0'] = np.mean(p2[2])
        self.__features['mean_fit_coefficient1'] = np.mean(p2[1])
        self.__features['mean_fit_coefficient2'] = np.mean(p2[0])

    def __flatness(self):
        flatness = librosa.feature.spectral_flatness(self.__audio_time_series)
        harmonic_flatness = librosa.feature.spectral_flatness(self.__harmonic_time_series)
        self.__features['mean_flatness'] = np.mean(flatness)
        self.__features['mean_harmonic_flatness'] = np.mean(harmonic_flatness)


def test_features():
    wav = '.wav'
    mp3 = '.mp3'
    # temp_song_path = '{0}{1}data{1}2015{1}00{2}'.format(os.getcwd(), os.sep, mp3)  ## Ed Sheeran
    temp_song_path = '{0}{1}data{1}C{2}'.format(os.getcwd(), os.sep, wav) ## Do Re Mi...
    # temp_song_path = '{0}{1}data{1}4Chords_A{2}'.format(os.getcwd(), os.sep, wav) ## Four chords song in A

    fe = AudioFeatureExtractor(temp_song_path)
    fe.extract_features()
    print(fe)


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        test_features()
