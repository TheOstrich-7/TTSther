# TTS Experiments
## Firebot custom endpoints

From my brief poking of Firebot, Firebot seems to provide 4 ways to impelement custom events. First Firebot allows you to directly run a JavaScript code snippet in response to an event. While JavaScript does have many TTS options available, without having the rest of the supporting enviornment, I am unsure what can be done with a single snippet alone

Similarly, Firebot also allows you run a full custom JavaScript script. This should allow for more complicated operations. Similarly it would allow you to declare libraries to use. That said, im not sure what enviornment Firebot uses to run the script. If its running it on your host things shoulf be fine, but if Firebot has its own restrictive JS engine it may prevent some of the actions. As such, it may still not be possible for the full script to access many of the TTS libraries offered by JS.

Going a step further, it is also possible to register an event to run a program. This opens up additional TTS possiblities with different programming languages. Similarly this should just be running on your host, removing any enviornment concerns. The down side is it would require starting and stopping a program 86 thousand times. However, depending on how simple the model, that may not be an issue.

Finally Firebot allows you to issue an HTTP request to a website. This is likely the most viable option as it both allows for the use of Cloud based TTS solutions but similarly allows us to set up our scripsts as a web server running in the background and constantly listening for new commands.

## Directory Structure
## Data

The data directory holds some test file used to experiment with the different TTS systems. All the tests were derived from both the Noita and Valheim streams where the initial stream TTS was introduced. The full chat transcripts for each stream are labeled with their respective game, the tag "raw", and the date of the stream (i.e., `noita_raw_8_9_26.csv`). These files were then cleaned to remove unnecessary columns from the table. The resulting data was saved using the "cleaned" tag (`noita_cleaned_8_9_26.csv`). We base our test data off these streams as chat was intentionally trying to break the system during stream. As such, these files provide a good collection of messages to stress test any engine and see how it performs. Similarly, by using prior streams' chats, we have a baseline to compare the TTS behavior to.

These files were also distilled into smaller collections of messages to make testing easier. At time of writing, the only derived file is `sampler.csv`. Also note that the last time I looked at sampler, the file seemed pretty and we are not sure why.

## JavaScript and Node.JS
## Python

In this section, we discuss all python based TTS packages that we tests

### pyttsx3

[pyttsx3](https://pypi.org/project/pyttsx3/) is a simple, lightweight, and fully offline TTS engine. For this, pyttsx3 works directly with audio drivers present on your devicely, namely pyttsx3 supports:

- SAPI5 for Windows
- NSSpeechSynthesizer for Mac
- espeak for Ubuntu

While pyttxs3 is fairly easy to use (simply start the engine and give it text), this ease also means its quite limited. For customization, you are only able to set the volume, rate of speech, and voice used by the TTS engine. However, these voices seem to stem from whatever your driver supports and nothing else. As of writing I don't see a way to add additional voices.

#### Running the demo

To run the demo file you will of course need python as well as the necessary packages. The demo file uses the `pyttsx3` and `csv` packages. To install these packages run:

```
pip3 install pyttsx3 csv
```
or 
```
python3 -m pip install pyttsx3 csv
```

Once installed, simply navigate to the demo in a terminal and run the file

```
python3 pyttsx3_demo.py
```

This will start an interactive loop for you to play with the engine. For a list of available commands simply enter `h`

#### Thoughts

As stated earlier, pyttsx3 is incredibly simple and lightweight. This makes it perfect for just starting and leaving running in the background. However, its also very limited. During my testing, the voices were very basic and often indistiguishable from each other. This may be as I was testing on Linux and other Operating Systems have better selections.

I was surprised with how well the TTS was able to handle a myriad of chat messages ranging from normal text to key smash, classic tts copypastas, special characters, and emojis. For the most part it read the messages fine. That said, there were a few places it struggled. When reading some foriegn text, the engine just said things like "Japanese character" rather than an actual charater name. Similarly for emojis and characters the engine didnt recognize, it either skipped them entirely (as with the pregnant man emoji) or read out the unicode sequence (as with the heiroglyphics). I will note that I am not sure whether the issue lies with the TTS engine itself or the character encoding of the CSV files used for the test data.

Another thing that I noticed was for more key smashy or memey messages the engine could start to break down. While this was funny, it would also sometimes cause like a whine in the background

#### Documentation

[pyttsx3 Documentation](https://pyttsx3.readthedocs.io/en/latest/index.html)

### gTTS

[gTTS](https://pypi.org/project/gTTS/) is a python text-to-speech library that uses Google Translate's TTS API to convert text into `mp3` files. This is another lightweight library that is very simple to use. However, as it relies on Google Translate, the machine must be online and options like rate of speech and volume seem fixed.

#### Running the demo

Once again, running the demo requires you have all necessary libraries installed. As such, you will need to make sure you install the `gTTS` package and `csv` package if it isn't installed already. 

```
pip3 install gTTS csv
```
or 
```
python3 -m pip install gTTS csv
```

Similarly, as gTTS only creates an `mp3`, we need something to play it. For that, we use the `playaudio3` package. Again this can be installed with pip.

```
pip3 install playaudio3
```

Once all packages are successfully installed, simply run the program with python

```
python3 gtts_demo.py
```

Once loaded, use the `help` command to show available commands

#### Thoughts

gTTS is an interesting package to work with. As stated, it is incredibly simple to work with. At minimum you just need 4 lines of code to give something voice. Similarly, as it relies on Google Translates TTS, the voices are pretty good in my opinion. If you have ever watched a Failboat stream or video, I'm pretty sure this is what he uses for Chatty. I am once again surprised at how well the system handled odd messages, emojis, and special characters. Similarly it is able to read foriegn speech, but that is to be expected of Google Translate I suppose.

That said there are several quirks to note. The biggest downside in my opinion is the lack of control. Not being able to change the rate of speech of the model can cause some longer/spammier messagges to really drag out. That said, there may be a work around for that with the actual playback library just speeding up the file but I'm not certain.

The other downside to note is that it does require an internet connection. Now this is not a problem beacuse it needs wifi (that feels like a prereq for streaming), but rather that the communication with Google can sometimes hang. For the most part, messages played one after the other. However for some messages it would take a couple seconds to start because it took the system longer to process. This seemed to happen for longer messages where the tokenizer didnt have a great space to split the message as well as when messages included a lot of punction.

Now something interesting was the models stability. For the most part, the model was stable. Its a little arbitrary on when it feels like spelling versus trying to sound a phrase out but thats fine I'd think. What more interesting is that for some of the spammier messages, the voice would sometime crack. It might speed up or slow down for a bit, get louder or quieter, and occasionaly the voice would shift/change a little. It could definetly be something fun as well as potentially a breaking point.

Another nuetral/slightly positive thing is that the package lets you define custom abbreviations, pre-processing passes, and tokenizer. As such you could further customize how messages are broken up and hopefully spoken, but I'm not sure how much you would be messing with that.

#### Documentation

[gTTS docs](https://gtts.readthedocs.io/en/latest/index.html)

## Cloud
## Other
JS
    Web Speech API 
        https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#speech_synthesis
    talkify
        https://github.com/Hagsten/Talkify
    inworld AI
        https://inworld.ai/resources/javascript-tts-api-tutorial
    responsiveVoice
        https://responsivevoice.org/
    browser_based_tts
        https://dev.to/linmingren/building-a-browser-based-text-to-speech-system-with-piper-tts-ljh
    puter.js
        https://developer.puter.com/tutorials/free-unlimited-text-to-speech-api/

Pyhton
    coqui-ai
        https://github.com/coqui-ai/tts
    smallest.aai
        https://smallest.ai/blog/python-packages-realistic-text-to-speech
    edge_tts
        https://medium.com/@tayeblagha/%EF%B8%8F-building-a-text-to-speech-tts-gui-with-python-61e83550ee19
    


Node
    text=to=speech-tts
        https://medium.com/@atlasaidev/add-text-to-speech-to-any-website-with-3-lines-of-javascript-c3df1e524031
    @lobehub/tts
        https://www.npmjs.com/package/@lobehub/tts
    say js
        https://github.com/marak/say.js/

    

Online
    google cloud text to speech
        https://codelabs.developers.google.com/codelabs/cloud-text-speech-node#0


general
    https://dev.to/pavkode/lightweight-offline-text-to-speech-solution-for-nodejs-applications-4n68
    https://medium.com/@ebinorpak/how-to-build-your-own-ai-text-to-speech-app-in-minutes-using-node-js-5721ec04287f
    https://www.reddit.com/r/learnmachinelearning/comments/1gbrbtm/free_humanlike_texttospeech_using_python_a_great/
    https://dev.to/mr_nova/text-to-speech-with-python-a-beginners-guide-to-pyttsx3-2pie
    https://picovoice.ai/blog/on-device-text-to-speech-in-python/
