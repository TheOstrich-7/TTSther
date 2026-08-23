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

    return value_json["MODELS"], value_json["MODEL_VALUES"], value_json["MODEL_QUALITY"], value_json["VOICES"], value_json["LANGUAGES"], value_json["LANGUAGE_CODES"], value_json["PAUSE_MODES"]
    

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

    print("\n\033[34mNote:\033[0m The first character denotes a voices nationality.\n    Key: a - American English, b - British English, j - Japanese, z - Mandarin Chinese, e - Spanish, f - French, h - Hindi, i - Italian, p - Brazilian Portuguese")
    print("\033[34mNote:\033[0m The second character denotes a voices geneder")
    print()


# TODO Spacy
def print_config(model, version, quality, voice, language, speed, pause_mode, clause, sentence, paragraph, variance, seed, short, trim):
     print("\nCurrent Kokoro Configuration:")
     print(f"\tPipeline Configuration:\n\t\tModel: {model} {version}\n\t\tModel Quality: {quality}\n\t\tVoice: {voice}")
     print(f"\n\tGenerator Configuration:\n\t\tLanguage: {language}\n\t\tSpeed: {speed}\n\t\tPause Mode: {pause_mode}\n\t\tClause Pause Length: {clause}\n\t\tSentence Pause Length: {sentence}\n\t\tParagraph Pause Length: {paragraph}\n\t\tPause Variance: {variance}\n\t\tRandom Seed: {"Unset" if seed is None else seed}\n\t\tShort Sentence Handling: {"Default to PipelineConfig" if short is None else short}")
     print(f"\n\tTrim Audio: {trim}\n")


def print_quality(model, version, qualities):
    print(f"{qualities["key"]}\n\nAvailable model quality for {model} {version}:")

    i = 0
    for quality in qualities[model+version]:
        print(f"\t{i}: {quality}")
        i += 1

    print("\n\033[34mNote:\033[0m 'fp32' provides the highest quality audio, however, for best performance 'q8' is recommended or 'fp16' when quality is critical")


def play(message, pipeline):
    audio = pipeline.run(message)
    soundfile.write("kokoro_temp.wav", audio.audio, audio.sample_rate)

    playsound3.playsound("kokoro_temp.wav")

    

def main():
    # Load the possible setting values for ease and cleanliness
    model_names = model_tokens = qualities = voices = languages = language_codes = pause_modes = 0
    model_names, model_tokens, qualities, voices, languages, language_codes, pause_modes = init()

    # Get the inital model to use
    current_model = ""
    current_version = ""
    model_index = -1
    print_models(model_names)
    while model_index < 0:
        try:
            model_index = int(input("Please select a model index to use: ").strip())
            current_model = model_tokens[model_index][0]
            current_version = model_tokens[model_index][1] 
        except ValueError:
            print(f"\033[31mError:\033[0m Please enter a valid number\n")
        except IndexError as ie:
            model_index = -1
            print(f"\033[31mError:\033[0m {ie}\n Please select a valid model\n")

        if current_model == "github":
            print("\033[33mWARNING:\033[0m In our testing neither github variant functioned properly\n")

    # TODO add voice blending
    # Grab the initial voice to use
    current_voice = ""
    voice_index = -1
    print_voices(current_version, voices)
    while voice_index < 0:
            try:
                voice_index = int(input("Please select a voice index to use: ").strip())
                current_voice = voices[current_version][voice_index] 
            except ValueError:
                print(f"\033[31mError:\033[0m Please enter a valid number\n")
            except IndexError as ie:
                voice_index = -1
                print(f"\033[31mError:\033[0m {ie}\n Please select a valid voice\n")

    print("\nInitializing TTS engine: ", end="")
    # TODO double check trim and short sentences
    # TODO Spacy
    # Initialize remianing configurable variables
    current_speed = 1.0
    current_quality = "fp32" if current_model == "github" and current_version == "v1.1-zh" else "q8"
    current_language = "en-us"
    current_spacy_size = "md"
    current_short_sentence_conf = ""
    current_pause_mode = "tts"
    current_clause_pause_len = 0.3
    current_sentence_pause_len = 0.6
    current_paragraph_pause_len = 1.0
    current_pause_variance = 0.05
    current_seed = None
    enable_short_sentence = None
    trim_audio = False
    update_generator = update_pipeline = 0

    generator_config = pykokoro.GenerationConfig(speed=current_speed,
                                                 lang=current_language,
                                                 pause_mode=current_pause_mode,
                                                 pause_clause=current_clause_pause_len,
                                                 pause_sentence=current_sentence_pause_len,
                                                 pause_paragraph=current_paragraph_pause_len,
                                                 pause_variance=current_pause_variance)
    pipeline_config = pykokoro.PipelineConfig(voice=current_voice,
                                              model_quality=current_quality,
                                              model_source=current_model,
                                              model_variant=current_version,
                                              provider="auto",
                                              generation=generator_config)

    # Finally start the engine
    pipeline = pykokoro.KokoroPipeline(pipeline_config)
    print("\033[32mComplete\033[0m")

    full_command = input("Enter a command to test Kokoro (h for help, q to quit): ").strip()
    command_tokens = full_command.split(" ", 1)
    command = command_tokens[0].strip().lower()
    while command != "q" and command != "quit":
        if command == "h" or command == "help":
            pass
        elif command == "c" or command == "config":
            print_config(current_model, current_version, current_quality, current_voice, 
                         current_language, current_speed, current_pause_mode, 
                         current_clause_pause_len, current_sentence_pause_len, 
                         current_paragraph_pause_len, current_pause_variance, current_seed,
                         enable_short_sentence, trim_audio)
        elif command == "m" or command == "model":
            print_models(model_names)
            try:
                model_index = int(input("Please select a model index to use: ").strip())
                temp_model = model_tokens[model_index][0]
                temp_version = model_tokens[model_index][1] 
            except ValueError:
                print(f"\033[31mError:\033[0m Please enter a valid number\n")
            except IndexError as ie:
                print(f"\033[31mError:\033[0m {ie}\n Please select a valid model\n")

            if temp_model != current_model or temp_version != current_version:
                current_model = temp_model
                current_version = temp_version
                current_voice = voices[current_version][0]
                current_quality = "fp32" if current_model == "github" and current_version == "v1.1-zh" else "q8"
                update_pipeline = 1

                print(f"Model Changed: Defaulting quality and voice to {current_quality} and {current_voice}, respectively\n")
                if current_model == "github":
                    print("\033[33mWARNING:\033[0m In our testing neither github variant functioned properly\n")
        elif command == "mq" or command == "quality":
            print_quality(current_model, current_version, qualities)
            try:
                quality_index = int(input("Please select which model quality to use (by index): ").strip())
                temp_quality = qualities[current_model+current_version][quality_index]
            except ValueError:
                print(f"\033[31mError:\033[0m Please enter a valid number\n")
            except IndexError as ie:
                print(f"\033[31mError:\033[0m {ie}\n Please select a valid model quality\n")

            if temp_quality != current_quality:
                current_quality = temp_quality
                update_pipeline = 1
        elif command == "v" or command == "voice":  # TODO voice blending
            print_voices(current_version, voices)
            try:
                voice_index = int(input("Please select a voice index to use: ").strip())
                temp_voice = voices[current_version][voice_index] 
            except ValueError:
                print(f"\033[31mError:\033[0m Please enter a valid number\n")
            except IndexError as ie:
                print(f"\033[31mError:\033[0m {ie}\n Please select a valid voice\n")

            if temp_voice != current_voice:
                current_voice = temp_voice
                update_pipeline = 1
        elif command == "r" or command == "rate":
            try:
                current_speed = float(input("Please enter a rate of speech scalar (Recommended range: 0.5 - 2.0): ").strip())
                update_generator = 1
            except ValueError:
                print(f"\033[31mError:\033[0m Please enter a valid number\n")
        elif command == "l" or command == "language":
            print(languages)
            try:
                language_index = int(input("Please select a text language to use (by index): ").strip())
                temp_language = language_codes[language_index] 
            except ValueError:
                print(f"\033[31mError:\033[0m Please enter a valid number\n")
            except IndexError as ie:
                print(f"\033[31mError:\033[0m {ie}\n Please select a valid language selection\n")

            if temp_language != current_language:
                current_language = temp_language
                update_generator = 1
        elif command == "p" or command == "set-pause": # TODO test better
            print(pause_modes)
            pause_index = input(f"Please select a pause mode to use (by index).\nTo keep the current value ({current_pause_mode}), just press enter: ").strip()
            if pause_index != "":
                if pause_index == "0":
                    current_pause_mode = "tts"
                    update_generator = 1
                elif pause_index == "1":
                    current_pause_mode = "manual"
                    update_generator = 1
                elif pause_index == "2":
                    current_pause_mode = "auto"
                    update_generator = 1
                else:
                    print(f"\033[31mError:\033[0m Invalid index {pause_index}\nAborting pause configuration\n")
                    continue

            temp_variance = input(f"Please enter the desired pause variance (variance >= 0.0)\nTo keep the current variance ({current_pause_variance}), just press enter: ").strip()
            if temp_variance != "":
                try:
                    current_pause_variance = float(temp_variance)
                    update_generator = 1
                except ValueError as ve:
                    print(f"\033[31mError:\033[0m {ve}\nAborting pause configuration. Partial config saved")
                    continue

            temp_seed = input(f"Seed the pause generation? Enter the desired seed (integer), otherwise just press enter to keep the current seed {current_seed}: ").strip()
            if temp_seed != "":
                try:
                    current_seed = int(temp_seed)
                    update_generator = 1
                except ValueError as ve:
                    print(f"\033[31mError:\033[0m {ve}\nAborting pause configuration. Partial config saved")
                    continue

            advanced_config = input("Perform advanced pause configuration? [y/n]: ").strip().lower()
            if advanced_config == "y":
                try:
                    current_clause_pause_len = int(input("Enter the desired clause pause length (float): ").strip())
                    current_sentence_pause_len = int(input("Enter the desired sentence pause length (float): ").strip())
                    current_paragraph_pause_len = int(input("Enter the desired paragraph pause length (float): ").strip())
                    update_generator = 1
                except ValueError as ve:
                    print(f"\033[31mError:\033[0m {ve}\nAborting pause configuration. Partial config saved")
        elif command == "s" or command == "say":
            if update_generator:
                generator_config = pykokoro.GenerationConfig(speed=current_speed,
                                                             lang=current_language,
                                                             pause_mode=current_pause_mode,
                                                             pause_clause=current_clause_pause_len,
                                                             pause_sentence=current_sentence_pause_len,
                                                             pause_paragraph=current_paragraph_pause_len,
                                                             pause_variance=current_pause_variance,
                                                             random_seed=current_seed)
                update_pipeline = 1
                update_generator = 0

            if update_pipeline:
                pipeline_config = pykokoro.PipelineConfig(voice=current_voice,
                                                          model_quality=current_quality,
                                                          model_source=current_model,
                                                          model_variant=current_version,
                                                          provider="auto",
                                                          generation=generator_config)
                pipeline = pykokoro.KokoroPipeline(pipeline_config)
                update_pipeline = 0
            try:
                play(command_tokens[1].strip(), pipeline)
            except Exception as e:
                print(f"\033[31mError:\033[0m {e}")
        else:
                    print(f'Unknown command \"{command[0]}\". Run \"help\" (h) to see a list of available commands or \"quit\" (q) to quit\n')

        full_command = input("Enter a command to test Kokoro (h for help, q to quit): ").strip()
        command_tokens = full_command.split(" ", 1)
        command = command_tokens[0].strip().lower()

"""
commands
    help - h
    say - s 
    file - f
    rate - r (change speed) DONE
    voice - v DONE
    model - m DONE
    quality - mq DONE
    language - l DONE
    set-pause - p DONE
    set-spacy - sp
    trim - t
    short-sentence - ss
"""    





if __name__ == "__main__":
    main()

#test = pykokoro.KokoroPipeline(pykokoro.PipelineConfig(voice="af_sarah", model_source="huggingface", model_variant="v1.0", model_quality="q8"))

#print(test.synth._kokoro.get_voices())