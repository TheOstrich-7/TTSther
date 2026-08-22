import csv
import json
import playsound3
import pykokoro
import soundfile
import torch
"""
degrees of freedom/features
    voices
        voice blending
    model
    model quality
    language
    speed
    pause config
    scapy
    trim
    short sentences
    seed
"""


def init():

    with open("kokoro_helper.json", "r") as ifp:
        value_json = json.load(ifp)

    return value_json["MODELS"], value_json["MODEL_VALUES"], value_json["MODEL_QUALITY"], value_json["VOICES"], value_json["LANGUAGES"], value_json["LANGUAGE_CODES"]
    

def print_models(models):
    print("\nSupported Kokoro models:")

    i = 0
    for model in models:
        print(f"\t{i}: {model}")
        i += 1
    print()


# TODO add voice blending
def print_voices(version, voice_list):
    print(f"\nSupported voice profiles for {version} models:")

    i = 0 
    for voice in voice_list[version]:
        print(f"\t{i}: {voice}")
        i += 1

    print("\n\033[34mNote:\033[0m The first character denotes a voices nationality.\n\tKey: a - American English, b - British English, j - Japanese, z - Mandarin Chinese, e - Spanish, f - French, h - Hindi, i - Italian, p - Brazilian Portuguese")
    print("\033[34mNote:\033[0m The second character denotes a voices geneder")
    print()


def play(message, pipeline):
    audio = pipeline.run(message)
    soundfile.write("kokoro_temp.wav", audio.audio, audio.sample_rate)

    playsound3.playsound("kokoro_temp.wav")

    

def main():
    # Load the possible setting values for ease and cleanliness
    model_names = model_tokens = qualities = voices = languages = language_codes = 0
    model_names, model_tokens, qualities, voices, languages, language_codes = init()

    # Get the inital model to use
    current_model = ""
    current_version = ""
    model_index = -1
    print_models(model_names)
    while model_index < 0:
        try:
            model_index = int(input("Please select a model index to use: "))
            current_model = model_tokens[model_index][0]
            current_version = model_tokens[model_index][1] 
        except ValueError:
            print(f"\033[31mError:\033[0m Please enter a valid number\n")
        except IndexError as ie:
            model_index = -1
            print(f"\033[31mError:\033[0m {ie}\n Please select a valid model\n")

    # TODO add voice blending
    # Grab the initial voice to use
    current_voice = ""
    voice_index = -1
    print_voices(current_version, voices)
    while voice_index < 0:
            try:
                voice_index = int(input("Please select a voice index to use: "))
                current_voice = voices[current_version][voice_index] 
            except ValueError:
                print(f"\033[31mError:\033[0m Please enter a valid number\n")
            except IndexError as ie:
                voice_index = -1
                print(f"\033[31mError:\033[0m {ie}\n Please select a valid voice\n")

    print("\nInitializing TTS engine: ", end="")
    # TODO break update by config type
    # TODO double check trim and short sentences
    # Initialize remianing configurable variables
    current_speed = 1.0
    current_quality = "q8"
    current_lanquage = "en-us"
    current_spacy_size = "md"
    current_short_sentence_conf = ""
    current_pause_mode = "auto"
    current_pause_variance = 0.05
    current_seed = None
    enable_short_sentence = None
    trim_audio = 0
    update = 0

    current_config = pykokoro.PipelineConfig(voice=current_voice,
                                             model_quality=current_quality,
                                             model_source=current_model,
                                             model_variant=current_version,
                                             provider="auto",
                                             generation=pykokoro.GenerationConfig(speed=current_speed,
                                                                                  lang=current_lanquage,
                                                                                  pause_mode=current_pause_mode,
                                                                                  pause_variance=current_pause_variance))

    # Finally start the engine
    pipeline = pykokoro.KokoroPipeline(current_config)
    print("\033[32mComplete\033[0m")

    full_command = input("Enter a command to test Kokoro (h for help, q to quit)").strip()
    command_tokens = full_command.split(" ", 1)
    command = command_tokens[0].strip().lower()
    while command != "q" and command != "quit":

        if command == "s" or command == "say":
            try:
                play(command_tokens[1].strip(), pipeline)
            except Exception as e:
                print(f"\033[31mError:\033[0m {e}")


        full_command = input("Enter a command to test Kokoro (h for help, q to quit)").strip()
        command_tokens = full_command.split(" ", 1)
        command = command_tokens[0].strip().lower()

    





if __name__ == "__main__":
    main()

#test = pykokoro.KokoroPipeline(pykokoro.PipelineConfig(voice="af_sarah", model_source="huggingface", model_variant="v1.0", model_quality="q8"))

#print(test.synth._kokoro.get_voices())