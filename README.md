# Debunking Skin Motion Soundwave Tattoo

[Skin Motion Soundwave Tattoo](https://skinmotion.com/soundwave-tattoos/) is a technology that creates augmented reality tattoos. You're able to give them an audio clip, they convert this to a soundwave image, and with their app you can play that audio back! I recreate their technology using a SQL database and following the steps below:

1) Get audio clip and transform it so its file extension is "wav"
2) Visualize audio as a soundwave image using matplotlib
3) Get image signature with image_match.goldberg library. Store this, other parameters, and the audio (in bytes) into SQL database
4) Get tattoo (or just print the wave)
5) Take picture of that tattoo (I didn’t incorporate object detection so tattoo image must be stationary(png file))
6) Get image signature of the picture/tattoo and query the database for the image signatures of stored audios
7) Find the match — the match is the image with the shortest image signature distance to the tattoo image.
8) Play audio of that match

**Check out my [Medium blog post](https://towardsdatascience.com/debunking-skin-motion-tattoo-d05a65ed6826) for more information.**

**Visual aid:**  

![](https://github.com/ptbailey/debunk-soundwave-tattoo/blob/master/soundwave.gif)

