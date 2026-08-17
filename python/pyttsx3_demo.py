import pyttsx3
import csv
VOLUME = 0 
RATE = 0
VOICES = {}
CURRENT_VOICE = ""
VOICE_LIST = "Index: Name, Age, Gender\n"
HELP = "Available commands:\n\thelp (h) - Lists all available commands, what they do, and how to use them\n\tList (l) - List the available voice models to choose from and their index value. The command also lists the voice's age and gender (though not always available)\n\tvolume # (d #) - Sets the TTS volume to the supplied value. Volume must be between 0 and 100\n\trate # (r #) - Sets the speaking rate of the TTS. Expects a nonnegative whole number\n\tvoice # (v #) - Sets the TTS voice to the supplied voice number. This command expects an index value from the voice list. To determine these values, please refer to the \"list\" command\n\tfile filename (f filename) - Plays all the test messages in the supplied file\n\tsay text (s text) - Speaks the supplied text. Allows for interactive experiments\n\tquit (q) - quits the application"


def init():
    """
    This function builds the initial TTS engine and sets the initial global state
    returns:
        engine (pyttsx3.engine.Engine) - the TTS engine used by the file
    """
    global VOLUME
    global RATE
    global VOICES
    global CURRENT_VOICE
    global VOICE_LIST

    engine = pyttsx3.init()
    VOLUME = engine.getProperty("volume") * 100
    RATE = engine.getProperty("rate")
    CURRENT_VOICE = engine.getProperty("voice")
    temp_voice_list = engine.getProperty("voices")
    count = 0
    for voice in temp_voice_list:  # Convert the voices object to a dictionary and help string for ease
        VOICES[count] = voice.name 
        VOICE_LIST += f"\t{count}: {voice.name}, {voice.age}, {voice.gender}\n"
        count += 1
    return engine


def set_volume(engine, volume):
    """
    Sets the volume to the user supplied level. Pyttsx3 volume is actually a float between 0.0 and 1.0
      however, for ease of understanding we have the user enter a number between 0 and 100
    params:
        engine (pyttsx3.engine.Engine) - the TTS engine whose properties to set (I got tired of globals)
        volume (int) - the volume level to use
    returns:
        engine (pyttsx3.engine.Engine) - the TTS engine (unsure if needed or not)
    """
    global VOLUME
    VOLUME = volume
    engine.setProperty("volume", 1.0*(volume/100))
    return engine


def set_rate(engine, rate):
    """
    Sets the rate with which the TTS engine speaks
    params:
        engine (pyttsx3.engine.Engine) - The TTS engine whomst rate you wish to set
        rate (int) - the rate of speed to set the engine to 
    returns:
        engine (pyttsx3.engine.Engine) - the updated engine object
    """
    global RATE
    RATE = rate
    engine.setProperty("rate", rate)
    return engine


def set_voice(engine, voice):
    """
    Sets the voice of the TTS engine to the specified voice
    params:
        engine (pyttsx3.engine.Engine) - The TTS engine to update
        voice (int) - The index of the voice to use from the VOICES dictionary
    returns:
        engine (pyttsx3.engine.Engine) - The updated engine
    """
    global VOICES
    global CURRENT_VOICE

    CURRENT_VOICE = VOICES[voice]
    engine.setProperty("voice", voice)
    return engine


def play_from_file(engine, filename):
    """
    Loads a test dataset from the supplied files and plays them all. Allows for easier testing
    params:
        engine (pyttsx3.engine.Engine) - The TTS engine to test with
        filename (str) - The name of the test file to use
    returns:
        None
    """
    try: 
        with open(filename, "r") as input_file:
            csv_reader = csv.reader(input_file)
            for row in csv_reader:
                engine.say(f"{row[0]} says {row[1]}")
                engine.runAndWait()
    except Exception as e:  # I'm lazy and not building proper error detection
        print(f"Error: {e}")


def main():
    """
    The main method. Loads the initial TTS engine and then starts an interactive loop to allow for testing the engine
    returns:
        None
    """

    tts_engine = init()

    command = input(f"Current settings:\n\tVoice - {CURRENT_VOICE}\n\tVolume - {VOLUME}\n\tRate - {RATE}\n\nEnter a command to test pyttsx3 (h for help, q to quit): ").strip().split(" ", 1)
    command[0] = command[0].lower()
    while command[0] != "q" and command[0] != "quit": 

        if command[0] == "h" or command[0] == "help":
            print(HELP)
        elif command[0] == "l" or command[0] == "list":  # Simply list the available voices to the user
            print(VOICE_LIST)
        elif command[0] == "d" or command[0] == "volume":  # Why d? Maybe decibels, nah I just ran out of letters
            try:
                tts_engine = set_volume(tts_engine, int(command[1].strip()))
            except Exception as e:  # Again, being lazy
                print(f"Error: {e}")
        elif command[0] == "r" or command[0] == "rate":
            try:
                tts_engine = set_rate(tts_engine, int(command[1].strip()))
            except Exception as e:
                print(f"Error: {e}")
        elif command[0] == "v" or command[0] == "voice":
            try:  
                tts_engine = set_voice(tts_engine, int(command[1].strip()))
            except Exception as e:
                print(f"Error: {e}")
        elif command[0] == "f" or command[0] == "file":
            play_from_file(tts_engine, command[1].strip())
        elif command[0] == "s" or command[0] == "say":  # Literally all you need to use it
            tts_engine.say(command[1].strip())
            tts_engine.runAndWait()
        else:  # For typos
            print(f"Unknown command \"{command[0]}\". Run \"help\" (h) to see a list of available commands or \"quit\" (q) to quit\n")
    


        command = input(f"\nCurrent settings:\n\tVoice - {CURRENT_VOICE}\n\tVolume - {VOLUME}\n\tRate - {RATE}\n\nEnter a command to test pyttsx3 (h for help, q to quit): ").strip().split(" ", 1)
        command[0] = command[0].lower()
        
    



if __name__ == "__main__":
    main()

