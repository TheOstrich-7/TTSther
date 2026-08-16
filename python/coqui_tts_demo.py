import csv
import torch
import playsound3
from TTS.api import TTS
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
HELP = "\nAvailable commands:\n\thelp (h) - Lists the known commands and what they do\n\tlist (l) - Displays all the voice profiles a model supports and their indicies\n\tvoice # (v #) - Selects the provided voice profile to use by the profile's index. Refer to the list command on how to find the index of a voice\n\tfile filename (f filename) - Load test messages from the provided file and run them through the TTS engine. \033[33mWarning:\033[0m Given the slow processing times of these models, large files are not recommended\n\tsay text (s text) - Have the TTS engine play the supplied text"


def print_speakers(speakers, clonable):
    """
    A function to display the available voice options for a model
    params:
        speakers (list(str)) - The list of available voice profiles
        clonable (bool) - A boolean indicating whether the model supports voice cloning (ints can act as bools)
    returns:
        None
    """
    default = 1  # Sentinel for models with no speaker options
    if speakers is not None and len(speakers) > 0: 
        default = 0  # if there are options, disable the defualt message
        print("\nAvailable Voice Models (Index: Model):")
        i = 0
        for speaker in speakers:
            print(f"{i}: {speaker}")
            i += 1

    if clonable:  # if cloning is allowed, indicate
        print("\nTo use voice cloning please enter -1")

    if default:  # A default message for models with cloning but no other options
        print("Just press enter to use the default voice")



def play(tts, message, multilingual, speaker, trained, training_data):
    """
    A function to run the supplied message through TTS
    params:
        tts (TTS.api.TTS.model?) - The tts engine to use
        message (str) - The message to speak
        multilingual (bool) - Whether the model is multilingual and thus needs a language specified
        speaker (str) -  The voice profile to use (if applicable)
        trained (bool) - If using a voice clone, whether the clone has already been generated and cached
        training_data (list(str)) - The training data to use for a voice clone if not already generated
    returns:
        trained (int) - The boolean indicating whether the current voice clone has been trained
    """
    if speaker != "":  
        if multilingual: 
            # If multilingual, we have to specify a language. I just always put english
            if speaker == "voice_clone":
                if trained:  # If the clone has been used before, grab the cached profile
                    tts.tts_to_file(text=message, speaker="Custom", language="en", file_path="coqui_output.wav")
                else:  # Otherwise, train a new clone
                    tts.tts_to_file(text=message, speaker_wav=training_data, speaker="Custom", language="en", file_path="coqui_output.wav")
                    trained = 1  # denote that the clone has now been trained
            else:  # If not a clone, use selected voice profile
                tts.tts_to_file(text=message, speaker=speaker, language="en", file_path="coqui_output.wav")
        else:
            # Same as above but this time we dont need to specify a language as the model is only lingual
            if speaker == "voice_clone":
                if trained:
                    tts.tts_to_file(text=message, speaker="Custom", file_path="coqui_output.wav")
                else:
                    tts.tts_to_file(text=message, speaker_wav=training_data, speaker="Custom", file_path="coqui_output.wav")
                    trained = 1
            else:
                tts.tts_to_file(text=message, speaker=speaker, file_path="coqui_output.wav")
    else: # If the speaker is empty, just play the message
        tts.tts_to_file(text=message, file_path="coqui_output.wav")
    
    playsound3.playsound("coqui_output.wav")
    return trained


def  play_from_file(filename, tts, multilingual, speaker, trained, training_data):
    """
    Loads test messages from the supplied file and runs them trough the TTS engine
    params:
        filename (str) - The name of the test file
        tts (TTs.api.TTS.model?) - The TTS engine being used
        multilingual (bool) - Whether the model supports multiple languages 
        speaker (str) - The voice profile to use (if applicable)
        trained (bool) - Whether the current voice clone has been used before (if applicable)
        training_data (list(str)) - A list of files to use for voice cloning 
    returns:
        trained (int) - The boolean indicating whether a voice clone has been trained
    """
    with open(filename, "r") as input_file:
        csv_reader = csv.reader(input_file)
        for row in csv_reader:
            trained = play(tts, f"{row[0]} says {row[1]}", multilingual, speaker, trained, training_data)
    return trained


def main():
    """
    The main function that runs the interactive loop
    """

    # Choose the model
    cloning = 0
    multilingual = 0
    models = TTS().list_models()
    i = 0
    print("Available TTS models to choose from (Index: Model). Note that the XTTS, Tortoise, and Bark models offer voice cloning")
    for model in models:
        if model[:10] == "tts_models":  # Screen out non TTS models
            print(f"{i}: {model}")
        i += 1
    try:
        model_index = int(input("\nPlease enter the index of the model you want to use: ").strip())
    except ValueError as te:
        print(f"\033[31mError:\033[0m {te}\n  please enter a valid number")
        exit(-1)
    model = models[model_index]

    temp = model.split("/")[-1].strip()
    if "tortoise" in temp or "xtts" in temp or "bark" in temp:  # Check if model supports voice cloning
        cloning = 1
    if "multilingual" in model:  # Check if model requires us to specify a language
        multilingual = 1

    print(f"\nLoading {model}")
    tts = TTS(model).to(DEVICE)  # Fetch the model
    print(f"\n\033[32mLoading Complete\033[0m")

    # Time to set the initial voice profile
    voice_options = 0
    speaker = ""
    trained = 0
    training_data = []

    try:  # the bark model explodes here so we will squash the error
        speakers = tts.speakers
    except FileNotFoundError as fe:
        speakers = None

    # Remove any previous voice clone to make my life easier
    if speakers is not None and "Custom" in speakers:
        speakers.remove("Custom")  

    if speakers is not None and len(speakers) > 0:  # Check if the model supports multiple voices
        voice_options = 1

    if voice_options:  # If it does support multiple voices, choose one
        print_speakers(speakers, cloning)
        try:
            speaker_index = int(input("Enter the index of the desired voice to use: ").strip())
        except ValueError as ve:
            print(f"\033[31mError:\033[0m {ve}\n  please enter a valid number")
            exit(-1)
        if cloning and speaker_index == -1:  # If it also allows voice cloning
            speaker = "voice_clone"
            training_data = input("Enter a comma seperated list of training files to use for the clone: ").strip().split(",")
        else:
            try:
                speaker = speakers[speaker_index]
            except IndexError as ie:
                print(f"\033[31mError:\033[0m {ie}\n  please enter a valid number")
                exit(-1)    
    elif cloning:  # Otherwise, if it does not have multiple voices but can clone a voice
        print_speakers(speakers, cloning)
        speaker_index = input("Enter the index of the desired voice to use: ").strip()
        if speaker_index == "-1":
            speaker = "voice_clone"
            training_data = input("Enter a comma seperated list of training files to use for the clone: ").strip().split(",")

    # Clean any spaces off the data file names
    if len(training_data) > 0:
        for i in range(len(training_data)):
            training_data[i] = training_data[i].strip()

    # And now we are ready to begin the loop
    print(f"\n\n\033[32mInitialization Complete\033[0m")
    command = input(f"Current settings:\n\tModel - {model}\n\tVoice - {speaker if speaker != "" else 'Default'}\nEnter a command to test Coqui (h for help, q to quit): ").strip().split(" ", 1)
    command[0] = command[0].lower().strip()

    while command[0] != "q" and command[0] != "quit":
        if command[0] == "h" or command[0] == "help":
            print(HELP)
        elif command[0] == "l" or command[0] == "list":
            print_speakers(speakers, cloning)
        elif command[0] == "v" or command[0] == "voice":
            # Very similar to the logic above with a few tweaks
            if voice_options:  # If it supports multiple voice options
                try:
                    speaker_index = int(input("Enter the index of the desired voice to use: ").strip())
                except ValueError as te:
                    print(f"\033[31mError:\033[0m {te}\n  please enter a valid number")
                    continue
                
                if cloning and speaker_index == -1:  # Check for cloning support
                    speaker = "voice_clone"
                    trained = 0  # Indicate that we are making a new clone
                    training_data = input("Enter a comma seperated list of training files to use for the clone: ").strip().split(",")
                    for i in range(len(training_data)):  # Clean the filenames right away
                        training_data[i] = training_data[i].strip()
                else:
                    try:
                        speaker = speakers[speaker_index]
                    except IndexError as ie:
                        print(f"\033[31mError:\033[0m {ie}\n  please enter a valid number")
                        continue
            elif cloning:  # Otherwise, if it only supports cloning
                speaker_index = input("Enter the index of the desired voice to use: ").strip()
                if speaker_index == "-1":
                    speaker = "voice_clone"
                    trained = 0  # Again, signal this is a new clone
                    training_data = input("Enter a comma seperated list of training files to use for the clone: ").strip().split(",")
                    for i in range(len(training_data)):  # Clean the filenames
                        training_data[i] = training_data[i].strip()
                else:  # A new caveat is to blank out the name to use the defualt in some cases
                    speaker = ""
            else:
                print(f"\033[33mWarning:\033[0m Voice profiles are not supported by this model")

        elif command[0] == "f" or command[0] == "file":
            try:
                if "bark" in model and speaker == "voice_clone":  # bark has to be special
                    trained = play_from_file(command[1].strip(), tts, 0, speaker, trained, training_data)
                else:
                    trained = play_from_file(command[1].strip(), tts, multilingual, speaker, trained, training_data)
            except Exception as e:
                 print(f"\033[31mError:\033[0m {e}")
        elif command[0] == "s" or command[0] == "say":
            try:
                if "bark" in model and speaker == "voice_clone":  # Despite being labeled multilinqual this model apperently only is some of the time
                    trained = play(tts, command[1].strip(), 0, speaker, trained, training_data)
                else:
                    trained = play(tts, command[1].strip(), multilingual, speaker, trained, training_data)
            except Exception as e:
                print(f"\033[31mError:\033[0m {e}")
        else:
            print(f'Unknown command \"{command[0]}\". Run \"help\" (h) to see a list of available command or \"quit\" (q) to quit\n')

        command = input(f"\nCurrent settings:\n\tModel - {model}\n\tVoice - {speaker if speaker != "" else 'Default'}\nEnter a command to test Coqui (h for help, q to quit): ").strip().split(" ", 1)
        command[0] = command[0].lower().strip()
            
 


if __name__ == "__main__":
    main()

