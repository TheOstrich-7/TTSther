import csv
import wave
import piper
import playsound3
CUDA = False  # Enable CUDA/GPU calculations
VOICE = "../data/en_US-ryan-high.onnx"  # Change this to the path to the desired file
HELP = "\nAvailable Commands:\n\thelp (h) - Lists the commands available and how to use them\n\tvolume (v) - Lists the current volume and prompts for a new volume level. Volumes are based on ratios, i.e., 0.5 = half as loud\n\trate (r) - Lists the current speaking rate and prompts for a new rate. Again based on ratios, i.e., 2.0 = twice as fast\n\taudio_variance (a) - Lists the current waveform variance and prompts for a new variance level. Expects a decimal with <1.0 being more stable and >1.0 being more unstable\n\tspeaker_variance (w) - Lists the current pronunciation variation level of the model and prompts for a new value. Also expects a decimal where values less than 1.0 are more stable, while greater than 1 is more unstable.\n\tnormalize (n) - Select whether the audio should be normalized.\n\tfile filename (f filename) - Loads the supplied file and runs it through the TTS engine.\n\tsay message (s message) - Speak the supplied message"

def play(message, tts, config):
    """
    Converts the desired message to audio and plays it
    params:
        message (str) - The message to play
        tts (piper.PiperVoice?) - The TTS engine to use
        config (piper.SynthesisConfig) - The TTS configuration to use
    returns:
        None
    """
    with wave.open("piper_output.wav", "wb") as ofp:
        tts.synthesize_wav(message, ofp, syn_config=config)
                
    playsound3.playsound("piper_output.wav")


def play_from_file(filename, tts, config):
    """
    Loads test messages from the specified file and runs them through TTS
    params:
        filename (str) - The test file to use
        tts (piper.PiperVoice) - The TTS engine being used
        config (piper.SynthesisConfig) - The configuration for the TTS to use
    returns:
        None
    """
    with open(filename, "r") as ifp:
        csv_reader = csv.reader(ifp)
        for row in csv_reader:
            play(f"{row[0]} says {row[1]}", tts, config)


def main():
    """
    The main method to play with the piper library
    """
    volume = 1
    rate = 1
    audio_variation = 1
    speaker_variation = 1
    normalize = 1
    config = piper.SynthesisConfig(volume=volume, length_scale=rate, noise_scale=audio_variation, noise_w_scale=speaker_variation, normalize_audio=normalize)
    update = 0  # A sentinel to determine whether I need to change the config dictionary

    tts = piper.PiperVoice.load(VOICE, use_cuda=CUDA)

    command = input(f"Enter a command to test Piper1 (h for help, q to quit): ").strip().split(" ", 1)
    command[0] = command[0].lower().strip()

    while command[0] != "q" and command[0] != "quit":
        if command[0] == "h" or command[0] == "help":
            print(HELP)
        elif command[0] == "v" or command[0] == "volume":   # I dont know why I felt like changing up my loop method
            try:
                volume = float(input(f"Enter the desired volume scalar (Current volume: {volume}): ").strip())
            except ValueError as ve:
                print(f"\033[31mError:\033[0m {ve}\nPlease enter a valid number")

            if volume < 0:
                volume = 0
            update = 1  # Mark that a setting has changed
        elif command[0] == "r" or command[0] == "rate":
            try:
                rate = float(input(f"Enter the desired speech rate scalar (Current rate: {rate}): ").strip())
            except ValueError as ve:
                print(f"\033[31mError:\033[0m {ve}\nPlease enter a valid number")
            
            if rate < 0:
                rate = 0
            update = 1
        elif command[0] == "a" or command[0] == "audio_variance":
            try:
                audio_variation = float(input(f"Enter the desired audio variability scalar (Current audio variability: {audio_variation}): ").strip())
            except ValueError as ve:
                print(f"\033[31mError:\033[0m {ve}\nPlease enter a valid number")
            
            if audio_variation < 0:
                audio_variation = 0
            update = 1
        elif command[0] == "w" or command[0] == "speaker_variance":  # W was the letter used by the config scalar so why not
            try:
                speaker_variation = float(input(f"Enter the desired speaker variability scalar (Current speaker variability: {speaker_variation}): ").strip())
            except ValueError as ve:
                print(f"\033[31mError:\033[0m {ve}\nPlease enter a valid number")
            
            if speaker_variation < 0:
                speaker_variation = 0
            update = 1
        elif command[0] == "n" or command[0] == "normalize":
            temp = input(f"Should the audio be normalized? Enter 1 for yes (Current setting {not normalize})").strip()
            if temp == "1":  # I dont know why the documentation has it this way. Why is it backwards
               normalize = 1
            else:
                normalize = 0
            update = 1 
        elif command[0] == "f" or command[0] == "file":
            if update:
                config = piper.SynthesisConfig(volume=volume, length_scale=rate, noise_scale=audio_variation, noise_w_scale=speaker_variation, normalize_audio=normalize)
                update = 0
            
            try:
                play_from_file(command[1].strip(), tts, config)
            except Exception as e:
                print(f"\033[31mError:\033[0m {e}")  
        elif command[0] == "s" or command[0] == "say":
            if update:  # If any settings have changed, update the config
                config = piper.SynthesisConfig(volume=volume, length_scale=rate, noise_scale=audio_variation, noise_w_scale=speaker_variation, normalize_audio=normalize)
                update = 0

            try:
                play(command[1].strip(), tts, config)
            except Exception as e:
                print(f"\033[31mError:\033[0m {e}")  
        else:
            print(f'Unknown command \"{command[0]}\". Run \"help\" (h) to see a list of available commands or \"quit\" (q) to quit\n')


        command = input(f"Enter a command to test Piper1 (h for help, q to quit): ").strip().split(" ", 1)
        command[0] = command[0].lower().strip()


if __name__ == "__main__":
    main()