import matplotlib.pyplot as plt
import numpy as np
import wave # wave module provides a convenient interface to the WAV sound format
from pydub import AudioSegment # Manipulate audio with an simple and easy high level interface. https://github.com/jiaaro/pydub/
import ffmpeg # A complete, cross-platform solution to record, convert and stream audio and video.
from image_match.goldberg import ImageSignature # this gives each image a specific signature
from pydub.playback import play

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from audio import Audio

engine = create_engine('sqlite:///audio.db')
Session = sessionmaker(bind = engine)
session = Session()

def read_audio(file_name): # need to read in the audio file, to get the name and audio for future functions
    global fname
    fname = file_name.split('.')[0] # going to need the name of this audio file to match name of image
    global audio
    audio = wave.open(file_name,'r') # r = read format; type: wave object - wave.Wave_read
    return audio

def play_audio(file_name, seconds = 0, first = False, last = False, reverse = False):
    play_ = AudioSegment.from_wav(file_name)
    if reverse == False:
        if seconds == 0:
            return play(play_)
        elif seconds < int(play_.duration_seconds):# play length is in milliseconds
            x_seconds = seconds*1000
            if first == True:
                return play(play_[:x_seconds])
            elif first == False:
                return play(play_[:x_seconds])
            elif last == True:
                return play(play_[-x_seconds:])
            elif last == False:
                return play(play_[:x_seconds])
        else:
            return 'Seconds exceeds duration of audio sample'
    else:
        if seconds == 0:
            return play(play_.reverse())
        elif seconds < int(play_.duration_seconds):# play length is in milliseconds
            x_seconds = seconds*1000
            if first == True:
                return play(play_[:x_seconds].reverse())
            elif first == False:
                return play(play_[:x_seconds].reverse())
            elif last == True:
                return play(play_[-x_seconds:].reverse())
            elif last == False:
                return play(play_[:x_seconds].reverse())
        else:
            return 'Seconds exceeds duration of audio sample'

def plot_audio(): # need to plot the audio wave to get the image that will be tattooed
    global signal_byte
    signal_byte = audio.readframes(-1) # gets bytes data; -1 means all frames (I believe)
    signal = np.fromstring(signal_byte, 'Int16') #A new 1-D array of integers from bytes. dtype = int16.
    freq = audio.getframerate() # returns frequency

    time = np.linspace(0, len(signal)/freq, num=len(signal))

    plt.figure(1, figsize=(10,9))
    plt.plot(time,signal)
    plt.axis('off') # neglect axes, they add noise
    plt.savefig('key.png') # saves plot to image file named key

    return plt.show()

def image2db(): # add image signature, corresponding audio bytes, and parameters to database
    name = fname
    gis = ImageSignature() # instantiate
    image_key = gis.generate_signature('key.png') #get signature for the tattooed image
    image_sig = str(list(image_key)) # convert to string to be stored in database
    audio_b = signal_byte # signal_bytes was globally defined above
    parameters = audio.getparams() # get the parameters of audio
    nchannels = parameters[0]
    sampwidth = parameters[1]
    framerate = parameters[2]
    nframes = parameters[3]
    comptype = parameters[4]
    compname = parameters[5]
    instance = Audio(name = name, image_signature = image_sig, \
    audio_bytes = audio_b, nchannels = nchannels, sampwidth = sampwidth, \
    framerate = framerate, nframes = nframes, comptype = comptype, compname = compname) # create an audio instance

    session.add(instance) # add to database
    session.commit()
