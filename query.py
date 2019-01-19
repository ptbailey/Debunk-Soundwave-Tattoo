import numpy as np
import wave # python: The wave module provides a convenient interface to the WAV sound format
from pydub import AudioSegment # Manipulate audio with an simple and easy high level interface. https://github.com/jiaaro/pydub/
from image_match.goldberg import ImageSignature
from pydub.playback import play
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from audio import Audio

engine = create_engine('sqlite:///audio.db')
Session = sessionmaker(bind = engine)
session = Session()

def find_distances(image):
    gis = ImageSignature()
    im_sig = gis.generate_signature(image) # get signature for image you're finding match for
                                           # http://www.cs.cmu.edu/~hcwong/Pdfs/icip02.ps for info on how signatures are made
    global all_signatures
    all_signatures = session.query(Audio.image_signature).all()
    global distances
    distances = []
    for signature in all_signatures:
        listy = [int(char) for char in signature[0][1:-1].split(',')]
        key_sig = np.array(listy)
        distance = gis.normalized_distance(key_sig, im_sig) # compute normalized distance between two points.
                                                            # computes || b - a || / ( ||b|| + ||a||)
        distances.append(distance)
    return distances

def find_match():
    value = min(distances) # the shortest distance is the most likely match.
                           # however, a threshold of 0.4 should be set as value to ensure match
    index = distances.index(value)
    audio_bytes, nchannels, sampwidth, framerate, nframes, comptype, compname = \
    session.query(Audio.audio_bytes, Audio.nchannels, Audio.sampwidth,\
    Audio.framerate, Audio.nframes, Audio.comptype, Audio.compname).filter(Audio.id \
    == index+1).first()

    tune = wave.open('playback.wav','wb') # create new audio file with write mode
    tune.setnchannels(nchannels) # channels 1 = mono 2 = stereo (two because of two ears)
    tune.setsampwidth(sampwidth)
    tune.setframerate(framerate) # specify frame rate to get number of frames. you have duration and rate
    tune.setnframes(nframes)
    tune.setcomptype(comptype, compname)
    tune.writeframes(audio_bytes)
    tune.close()
    playback = AudioSegment.from_wav('playback.wav')
    return play(playback)
