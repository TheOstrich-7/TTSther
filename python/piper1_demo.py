import csv
import wave
import piper
import playsound3
CUDA = False
VOICE = "../data/en_US-ryan-high.onnx"


def play(message, tts, config):
    with wave.open("piper_output.wav", "wb") as ofp:
        tts.synthesize_wav(message, ofp, syn_config=config)
                
    playsound3.playsound("piper_output.wav")


def play_from_file(filename, tts, config):
    with open(filename, "r") as ifp:
        csv_reader = csv.reader(ifp)
        for row in csv_reader:
            play(f"{row[0]} says {row[1]}", tts, config)


def main():
    volume = 1
    rate = 1
    audio_variation = 1
    speaker_variation = 1
    normalize = 0
    config = piper.SynthesisConfig(volume=volume, length_scale=rate, noise_scale=audio_variation, noise_w_scale=speaker_variation, normalize_audio=normalize)
    update = 0

    tts = piper.PiperVoice.load(VOICE)

    command = input(f"Enter a command to test Piper1 (h for help, q to quit): ").strip().split(" ", 1)
    command[0] = command[0].lower().strip()

    while command[0] != "q" and command[0] != "quit":
        if command[0] == "h" or command[0] == "help":
            pass
        elif command[0] == "v" or command[0] == "volume":
            try:
                volume = float(input(f"Enter the desired volume scalar (Current volume: {volume}): ").strip())
            except ValueError as ve:
                print(f"\033[31mError:\033[0m {ve}\nPlease enter a valid number")

            if volume < 0:
                volume = 0
            update = 1
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
        elif command[0] == "w" or command[0] == "speaker_variance":
            try:
                speaker_variation = float(input(f"Enter the desired speaker variability scalar (Current speaker variability: {speaker_variation}): ").strip())
            except ValueError as ve:
                print(f"\033[31mError:\033[0m {ve}\nPlease enter a valid number")
            
            if speaker_variation < 0:
                speaker_variation = 0
            update = 1
        elif command[0] == "n" or command[0] == "normalize":
            temp = input(f"Should the audio be normalized? Enter 1 for yes (Current setting {not normalize})").strip()
            if temp == "1":
               normalize = 0
            else:
                normalize = 1
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
            if update:
                config = piper.SynthesisConfig(volume=volume, length_scale=rate, noise_scale=audio_variation, noise_w_scale=speaker_variation, normalize_audio=normalize)
                update = 0

            try:
                play(command[1].strip(), tts, config)
            except Exception as e:
                print(f"\033[31mError:\033[0m {e}")  
        else:
            pass


        command = input(f"Enter a command to test Piper1 (h for help, q to quit): ").strip().split(" ", 1)
        command[0] = command[0].lower().strip()


if __name__ == "__main__":
    main()