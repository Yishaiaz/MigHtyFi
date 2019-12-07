import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
import librosa


class FileSimpleAnalyse:

    def __init__(self, file_name):
        output_file("{0} entire sound.html".format(file_name))
        self.file_path = file_name

    def plot_entire_file(self):
        y, sr = librosa.load(self.file_path)
        p1 = figure(title="all file", x_axis_label='x', y_axis_label='y')
        p1.line(np.linspace(0, len(y)), y, legend="Temp.", line_width=2)
        show(p1)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

    def plot_percussions(self):
        y, sr = librosa.load(self.file_path)
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        p2 = figure(title="only percussions", x_axis_label='x', y_axis_label='y')
        p2.line(np.linspace(0, len(y_percussive)), y_percussive, legend="Temp.", line_width=2)
        show(p2)

    def plot_harmonics(self):
        y, sr = librosa.load(self.file_path)
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        p3 = figure(title="only harmonics", x_axis_label='x', y_axis_label='y')
        p3.line(np.linspace(0, len(y_harmonic)), y_harmonic, legend="Temp.", line_width=2)
        show(p3)

    def plot_all(self):
        y, sr = librosa.load(self.file_path)
        # create a new plot with a title and axis labels
        p1 = figure(title="all file", x_axis_label='x', y_axis_label='y')

        # add a line renderer with legend and line thickness
        p1.line(np.linspace(0, len(y)), y, legend="Temp.", line_width=2)
        # Set the hop length; at 22050 Hz, 512 samples ~= 23ms

        hop_length = 512

        # Separate harmonics and percussives into two waveforms
        y_harmonic, y_percussive = librosa.effects.hpss(y)

        p2 = figure(title="only percussions", x_axis_label='x', y_axis_label='y')
        p2.line(np.linspace(0, len(y_percussive)), y_percussive, legend="Temp.", line_width=2)

        p3 = figure(title="only harmonics", x_axis_label='x', y_axis_label='y')
        p3.line(np.linspace(0, len(y_harmonic)), y_harmonic, legend="Temp.", line_width=2)

        show(column(p1, p2, p3))
