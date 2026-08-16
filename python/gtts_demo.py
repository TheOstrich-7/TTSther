import csv
import gtts
import playsound3
ACCENTS = f"Known Accents:\n\nEnglish ('en'):\n\tAustralia - 'com.au'\n\tUnited Kingdom - 'co.uk'\n\tUnited States - 'us'\n\tCanada - 'ca'\n\tIndia - 'co.in'\n\tIreland - 'ie'\n\tSouth Africa - 'co.za'\n\tNigeria - 'com.ng'\n\nFrench ('fr')\n\tCanada - 'ca'\n\tFrance - 'fr'\n\nPortuguese ('pt'):\n\tBrazil - 'com.br'\n\tPortugal - 'pt'\n\nSpanish ('es'):\n\tMexico - 'com.mx'\n\tSpain - 'es'\n\tUnited States - 'us'\n"
ACCENTS_SET = {"com.au", "co.uk", "us", "ca", "co.in", "ie", "co.za", "com.ng", "fr", "com.br", "pt", "com.mx", "es"}
HELP = "\nAvailable commands:\n\thelp (h) - List the available commands and how to use them\n\tlist_voices (lv) - Lists all available language options in 'code - language' format. Use these codes to change the tts language/voice\n\tset_voices voice (v voice) - Sets the TTS language to the specified voice. For available voice codes refer to 'list_voices'\n\tlist_accents (la) - lists know goolge top level domanis (TLDs) that can change the accent of select languages.\n\tset_accent accent (a accent) - Sets the TLD to use for beaconing out to google in order to change the accent of the voice. For known accents, refer to the 'list_accents' command\n\tfile filename (f filename) - Loads test messages from the file specified and runs them\n\t say text (s text) - Speak the provided message\n\tquit (q) - Closes the program\n"

def list_languages(voices):
    """
    Cleanly displays the voice/language options google provides
    params:
        voices (dict(str,str)) - A dictionary of available languages and their coressponding codes
    returns:
        None
    """
    print("Available voices:")
    for voice in voices.items():
        print(f'\t"{voice[0]}" - {voice[1]}')
    print()


def play(message, language, tld):
    """
    Uses Google Translate's TTS to create the audio then plays the message
    params:
        message (str) - The message to voice
        language (str) - The voice for the model to use
        tld (str) - The top level domain to reach out to google on 
    returns:
        None
    """
    tts = gtts.gTTS(message, lang=language, tld=tld)
    with open("temp_gtts.mp3", "wb") as ofp:  # save to a temporary file, then reopen to play
        tts.write_to_fp(ofp)                  # there is probably a better solution but this is a demo
    playsound3.playsound("temp_gtts.mp3", "wb")


def play_from_file(filename, language, tld):
    """
    Loads test messages from a supplies test file and runs them all through the TTS engine
    params:
        filename (str) - The name of the test file to use
        language (str) - The TTS voice/language to use
        tld (str) - The domain with which to contact google
    """
    with open(filename, "r") as input_file:
        csv_reader = csv.reader(input_file)
        for row in csv_reader:
            play(f"{row[0]} says {row[1]}", language, tld)


def main():
    """
    The main method. Loops over user input to allow for interactive testing of the library
    """
    current_voice = "en"  # I got fed up with globals 
    current_tld = "com"  # I forgot how annoying python globals can be
    voice_list = gtts.lang.tts_langs()


    command = input(f"Current settings:\n\tVoice - {voice_list[current_voice]}\n\tTLD - {current_tld}\nEnter a command to test gTTS (h for help, q to quit): ").strip().split(" ", 1)
    command[0] = command[0].lower().strip()
    while command[0] != "q" and command[0] != "quit":
        if command[0] == "h" or command[0] == "help":
            print(HELP)
        elif command[0] == "lv" or command[0] == "list_voices":
            list_languages(voice_list) 
        elif command[0] == "la" or command[0] =="list_accents":
            print(ACCENTS)
        elif command[0] == "v" or command[0] =="set_voices":
            temp = command[1].strip()
            if temp in voice_list.keys():
                current_voice = temp
            else:
                print(f"Error: Unkown language '{temp}'")
        elif command[0] == "a" or command[0] =="set_accents":
            current_tld = command[1].strip()
            if current_tld not in ACCENTS_SET:  # This does not mean its a bad TLD, but just not one we can confirm works
                print("Warning: Unkown TLD declared, program behavior cannot be guarenteed")
        elif command[0] == "f" or command[0] =="file":
            try:
                play_from_file(command[1].strip(), current_voice, current_tld)
            except Exception as e:
                print(f"Error running test file: {e}")
        elif command[0] == "s" or command[0] =="say":
            try:
                play(command[1].strip(), current_voice, current_tld)
            except Exception as e:
                print(f"Error playing TTS: {e}")
        else:
            print(f'Unknown command \"{command[0]}\". Run \"help\" (h) to see a list of available command or \"quit\" (q) to quit\n')

        command = input(f"Current settings:\n\tVoice - {voice_list[current_voice]}\n\tTLD - {current_tld}\nEnter a command to test gTTS (h for help, q to quit): ").strip().split(" ", 1)
        command[0] = command[0].lower().strip()



if __name__ == "__main__":
    main()