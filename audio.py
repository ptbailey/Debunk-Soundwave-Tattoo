from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# create a SQL database that takes in all the variables defined below in one row
class Audio(Base):
    __tablename__ = 'audio'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    image_signature = Column(String) # Couldn't store np.arrays in database, so converted to string
    audio_bytes = Column(BLOB) # audio is stored in its bytes form (BLOB)
    nchannels = Column(Integer) # parameter: 1 = mono, 2 = stereo (L and R)
    sampwidth = Column(Integer) # sample width
    framerate = Column(Integer) # sampling frequency
    nframes = Column(Integer) # number of audio frames
    comptype = Column(String) # so far, this returns 'None'. future it will return compression type
    compname = Column (String) # Human-readable version of getcomptype(). Usually 'not compressed' parallels 'NONE'

engine = create_engine('sqlite:///audio.db') # create database audio.db
Base.metadata.create_all(engine)
