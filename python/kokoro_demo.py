import csv
import json
import playsound3
import pykokoro
import soundfile
# import time


def init():
    """
    A function to initialize several variables used by the demo. Mainly, it loads a
      bunch of strings and lists from a file for convenience and keeping things slightly
      cleaner
    returns:
        value_json["MODELS"] (list(str)) - A list of the pretty print version of available models
        value_json["MODEL_VALUES"] (list((str,str))) - A list of (model, version) pairs for easier processing
        value_json["MODEL_QUALITY"] (dict(str,list(str))) - A dictionary of the supported model quality for each available model
        value_json["VOICES"] (dict(str,list(str))) - A dictionary of available voices for each model version
        value_json["LANGUAGES"] (str) - A formatted string listing the available language options
        value_json["LANGUAGE_CODES"] (list(str)) - A list of supported languages' language codes
        value_json["PAUSE_MODES"] (str) - A formatted string of TTS pause options
        value_json["SPACY_MODES"] (str) - A formatted string of Spacy model sizes to choose from
        value_json["SHORT_MODES"] (str) - A formatted string of Short Sentence Handling resolvers
        value_json["HELP"] (str) - A formatted help message for the available commands
    """
    with open("kokoro_helper.json", "r") as ifp:
        value_json = json.load(ifp)

    return value_json["MODELS"], value_json["MODEL_VALUES"], value_json["MODEL_QUALITY"], value_json["VOICES"], value_json["LANGUAGES"], value_json["LANGUAGE_CODES"], value_json["PAUSE_MODES"], value_json["SPACY_MODES"], value_json["SHORT_MODES"], value_json["HELP"]
    

def print_models(models):
    """
    A function to display the available models to the user
    params:
        models (list(str)) -  A list of models to display
    returns:
        None
    """
    print("\nSupported Kokoro models:")

    i = 0
    for model in models:
        print(f"\t{i}: {model}")
        i += 1
    print()



def print_voices(version, voice_list):
    """
    A function to display the available voice profiles for the user
    params:
        version (str) - The model version selected
        voice_list (dict(str,list(str))) - A dictionary mapping model versions to their
          supported voice profiles
    returns: 
        None
    """
    print(f"\nSupported voice profiles for {version} models:")

    i = 0 
    for voice in voice_list[version]:
        print(f"\t{i}: {voice}")
        i += 1

    print("\n\033[34mNote:\033[0m The first character denotes a voices nationality.\n    Key: a - American English, b - British English, j - Japanese, z - Mandarin Chinese, e - Spanish, f - French, h - Hindi, i - Italian, p - Brazilian Portuguese")
    print("\033[34mNote:\033[0m The second character denotes a voices geneder")
    print()


def print_config(model, version, quality, voice, language, speed, pause_mode, clause, sentence, paragraph, variance, seed, short, spacy, short_conf):
    """
    A function to display the current value of all configurable settings to the user
    params:
        model (str) - The Kokoro model currently selected/being used
        version (str) - The version of the model being used
        quality (str) - The model quality selected
        voice (str) - The voice profile being used for the TTS engine
        language (str) - The current input text language set for the system
        speed (float) - A scalar representing the model's rate of speech
        pause_mode (str) - The currently chosen algorithm used to add pauses to TTS messages
        clause (float) - How long to pause after a clause
        sentence (float) - How long the model should pause at the end of a sentence
        paragraph (float) - How long the model should pause at the end of a paragraph
        variance (float) - Gaussian variance setting added to pauses to make them feel more natural
        seed (int) - The current random seed being used to generate pause variance
        short (boolean) - Whether to allow/override short sentence handling in the model
        spacy (str) - The current Spacy model size
        short_conf (pykokoro.short_sentence_handler.ShortSentenceConfig) - The current short sentence handling configuration
    returns:
        None
    """
    print("\nCurrent Kokoro Configuration:")
    print(f"\tPipeline Configuration:\n\t\tModel: {model} {version}\n\t\tModel Quality: {quality}\n\t\tVoice: {voice}\n\t\tShort Sentence Configuration:\n\t\t\tMinimum Phoneme Length: {'None' if short_conf is None else short_conf.min_phoneme_length}\n\t\t\tResolver: {'None' if short_conf is None else short_conf.resolve_mode}")
    print(f"\n\tGenerator Configuration:\n\t\tLanguage: {language}\n\t\tSpeed: {speed}\n\t\tPause Mode: {pause_mode}\n\t\tClause Pause Length: {clause}\n\t\tSentence Pause Length: {sentence}\n\t\tParagraph Pause Length: {paragraph}\n\t\tPause Variance: {variance}\n\t\tRandom Seed: {"Unset" if seed is None else seed}\n\t\tShort Sentence Handling: {"Default to PipelineConfig" if short is None else short}")
    print(f"\n\tSpacy Model Size: {spacy}")


def print_quality(model, version, qualities):
    """
    A function to display the available model qualities for a given model to the user
    params:
        model (str) - The current model selected/being used
        version (str) - The current version of the model used in the demo
        qualities (dict(str,list(str))) - A dictionary mapping the available model qualities to 
          each of the possible model combinations
    returns:
        None
    """
    print(f"{qualities["key"]}\n\nAvailable model quality for {model} {version}:")

    i = 0
    for quality in qualities[model+version]:
        print(f"\t{i}: {quality}")
        i += 1

    print("\n\033[34mNote:\033[0m 'fp32' provides the highest quality audio, however, for best performance, 'q8' is recommended or 'fp16' when quality is critical")


def play_from_file(filename, pipeline):
    """
    Load test messages from the supplied file and run them through the TTS engine
    params:
        filename (str) - The test file to load from
        pipeline (pykokoro.KokoroPipeline?) - The pipeline used to make the audio
    returns:
        None
    """
    # times = []
    with open(filename, "r") as ifp:
        csv_reader = csv.reader(ifp)
        for row in csv_reader:
            play(f"{row[0]} says {row[1]}", pipeline)
            # times.append(play(f"{row[0]} says {row[1]}", pipeline))

    # with open("gen_times.txt", "w") as ofp:
        # for value in times:
            # ofp.write(f"{value}\n")

def play(message, pipeline):
    """
    A function to convert the supplied message to audio using the TTS engine provided
    params:
        message (str) - The text to convert to audio
        pipeline (pykokoro.KokoroPipeline?) - The pipeline used to generate the audio
    returns:
        None
    """
    # start = time.time()
    audio = pipeline.run(message)
    # end = time.time()
    soundfile.write("kokoro_temp.wav", audio.audio, audio.sample_rate)
    playsound3.playsound("kokoro_temp.wav")
    # return end - start


def main():
    """
    The main function responsible for accepting user input and allowing the user to interactively
      test the Kokoro package
    """
    # Load the possible setting values for ease and cleanliness
    model_names = model_tokens = qualities = voices = languages = language_codes = pause_modes = spacy_sizes = short_sentence_resolvers = help = 0
    model_names, model_tokens, qualities, voices, languages, language_codes, pause_modes, spacy_sizes, short_sentence_resolvers, help = init()

    # Get the initial model to use
    current_model = ""
    current_version = ""
    model_index = -1
    print_models(model_names)
    while model_index < 0:
        try:  # With each file, I end up adding more and more appropriate safety measures
            model_index = int(input("Please select a model index to use: ").strip())
            current_model = model_tokens[model_index][0]
            current_version = model_tokens[model_index][1] 
        except ValueError:
            print(f"\033[31mError:\033[0m Please enter a valid number\n")
        except IndexError as ie:
            model_index = -1
            print(f"\033[31mError:\033[0m {ie}\n Please select a valid model\n")

        """
        I had issues with the GitHub models. However it's hard to say if that's a valid error 
          or merely an issue in my environment. As such, I leave the option open for others to
          experiment with
        """
        if current_model == "github":
            print("\033[33mWARNING:\033[0m In our testing neither github variant functioned properly\n")

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

    # Output to help keep people in the office
    print("\nInitializing TTS engine: ", end="")

    # Initialize remaining configurable variables
    current_speed = 1.0
    current_quality = "fp32" if current_model == "github" and current_version == "v1.1-zh" else "q8"
    current_language = "en-us"
    current_spacy_size = "md"
    current_short_sentence_conf = None
    current_pause_mode = "tts"
    current_clause_pause_len = 0.3
    current_sentence_pause_len = 0.6
    current_paragraph_pause_len = 1.0
    current_pause_variance = 0.05
    current_seed = None
    enable_short_sentence = None
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
    print("\033[32mComplete\033[0m")  # Sanity output

    # Finally time for experiments
    full_command = input("Enter a command to test Kokoro (h for help, q to quit): ").strip()
    command_tokens = full_command.split(" ", 1)
    command = command_tokens[0].strip().lower()
    while command != "q" and command != "quit":
        if command == "h" or command == "help":
            print(help)
        elif command == "c" or command == "config":
            print_config(current_model, current_version, current_quality, current_voice, 
                         current_language, current_speed, current_pause_mode, 
                         current_clause_pause_len, current_sentence_pause_len, 
                         current_paragraph_pause_len, current_pause_variance, current_seed,
                         enable_short_sentence, current_spacy_size, current_short_sentence_conf)
        elif command == "m" or command == "model":
            print_models(model_names)
            try:  # attempt to change models
                model_index = int(input("Please select a model index to use: ").strip())
                temp_model = model_tokens[model_index][0]
                temp_version = model_tokens[model_index][1] 
            except ValueError:  # Did you actually give me a number?
                print(f"\033[31mError:\033[0m Please enter a valid number\n")
            except IndexError as ie:  # Is that number a valid index (i.e., is it actually in the list)? 
                print(f"\033[31mError:\033[0m {ie}\n Please select a valid model\n")

            # If we aren't actually changing anything, lets not actually take the time to update the config
            if temp_model != current_model or temp_version != current_version:
                current_model = temp_model
                current_version = temp_version
                current_voice = voices[current_version][0]
                current_quality = "fp32" if current_model == "github" and current_version == "v1.1-zh" else "q8"
                update_pipeline = 1

                # You have been warned
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
        elif command == "v" or command == "voice": 
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
        elif command == "p" or command == "set-pause": 
            print(pause_modes)
            pause_index = input(f"Please select a pause mode to use (by index).\nTo keep the current value ({current_pause_mode}), just press enter: ").strip()
            if pause_index != "":
                if pause_index == "0":  # Just like the other try cases, but I was too lazy to actually build it that way
                    current_pause_mode = "tts"
                    update_generator = 1
                elif pause_index == "1":
                    current_pause_mode = "manual"
                    update_generator = 1
                elif pause_index == "2":
                    current_pause_mode = "auto"
                    update_generator = 1
                else:
                    # It is possible for the command to break at any input
                    print(f"\033[31mError:\033[0m Invalid index {pause_index}\nAborting pause configuration\n")
                    continue

            temp_variance = input(f"Please enter the desired pause variance (variance >= 0.0)\nTo keep the current variance ({current_pause_variance}), just press enter: ").strip()
            if temp_variance != "":
                try:
                    current_pause_variance = float(temp_variance)
                    update_generator = 1
                except ValueError as ve:
                    # If it does break, any previously recorded changes are saved
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

            # Doubt we really want to play with this, but might as well give the option
            advanced_config = input("Perform advanced pause configuration? [y/n]: ").strip().lower()
            if advanced_config == "y":
                try:
                    current_clause_pause_len = float(input("Enter the desired clause pause length (float): ").strip())
                    current_sentence_pause_len = float(input("Enter the desired sentence pause length (float): ").strip())
                    current_paragraph_pause_len = float(input("Enter the desired paragraph pause length (float): ").strip())
                    update_generator = 1
                except ValueError as ve:
                    print(f"\033[31mError:\033[0m {ve}\nAborting pause configuration. Partial config saved")
        elif command == "sp" or command == "set-spacy":
            print(spacy_sizes)
            spacy_index = input(f"Please select a Spacy model size to use (by index): ").strip()
            if spacy_index == "0":  # Since these lists are fixed size, why go through the int and index hassle
                current_spacy_size = "sm"
                update_pipeline = 1
            elif spacy_index == "1":
                current_spacy_size = "md"
                update_pipeline = 1
            elif spacy_index == "2":
                current_spacy_size = "lg"
                update_pipeline = 1
            elif spacy_index == "3":
                current_spacy_size = "trf"
                update_pipeline = 1
            else:
                print(f"\033[31mError:\033[0m Invalid index {spacy_index}\n")            
        elif command == "ss" or command == "short-sentence":
            option = input("What would you like to do? [clear/disable/configure]: ").strip().lower()
            if option == "clear":
                enable_short_sentence = None
                current_short_sentence_conf = None
                update_generator = 1
            elif option == "disable":
                enable_short_sentence = False
                update_generator = 1
            elif option == "configure":
                min_phonemes = 30
                temp = input("Enter the minimum number of phonemes for a phrase to no longer be considered short. Press enter to use the default value of 30: ").strip()
                if temp != "":
                    try:
                        min_phonemes = int(temp)
                    except ValueError as ve:
                        print(f"\033[31mError:\033[0m {ve}\nDefaulting to 30 phonemes")

                resolver = "randomized-phrase"
                print(short_sentence_resolvers)
                resolver_index = input(f"Please select a resolver to use (by index): ").strip()
                if resolver_index == "0":  # Tired of these if statements yet?
                    resolver = "phrase"
                elif resolver_index == "1":
                    resolver = "randomized-phrase"
                elif resolver_index == "2":
                    resolver = "wrap"
                else:
                    print(f"\033[31mError:\033[0m Invalid index\nDefaulting to random-phrase")

                current_short_sentence_conf =  pykokoro.short_sentence_handler.ShortSentenceConfig(min_phoneme_length=min_phonemes,
                                                                                                   resolve_mode=resolver)
                enable_short_sentence = True
                update_generator = 1
        elif command == "f" or command == "file":
            # Its funny that I didnt want to pass stuff into play so this has to be copied I guess
            if update_generator:
                generator_config = pykokoro.GenerationConfig(speed=current_speed,
                                                             lang=current_language,
                                                             pause_mode=current_pause_mode,
                                                             pause_clause=current_clause_pause_len,
                                                             pause_sentence=current_sentence_pause_len,
                                                             pause_paragraph=current_paragraph_pause_len,
                                                             pause_variance=current_pause_variance,
                                                             random_seed=current_seed,
                                                             enable_short_sentence=enable_short_sentence)
                update_pipeline = 1
                update_generator = 0
            
            if update_pipeline:
                pipeline_config = pykokoro.PipelineConfig(voice=current_voice,
                                                          model_quality=current_quality,
                                                          model_source=current_model,
                                                          model_variant=current_version,
                                                          provider="auto",
                                                          generation=generator_config,
                                                          short_sentence_config=current_short_sentence_conf)
            
                if current_spacy_size != "md": 
                    pipeline_config = pykokoro.with_spacy_model_size(pipeline_config, size=current_spacy_size)
            
                pipeline = pykokoro.KokoroPipeline(pipeline_config)  # Finally generate the new engine
                update_pipeline = 0

            try:
                play_from_file(command_tokens[1].strip(), pipeline)
            except Exception as e:
                print(f"\033[31mError:\033[0m {e}")    
        elif command == "s" or command == "say":
            # First update the generator config, if needed, as it is the base config (at least for our purposes)
            if update_generator:
                generator_config = pykokoro.GenerationConfig(speed=current_speed,
                                                             lang=current_language,
                                                             pause_mode=current_pause_mode,
                                                             pause_clause=current_clause_pause_len,
                                                             pause_sentence=current_sentence_pause_len,
                                                             pause_paragraph=current_paragraph_pause_len,
                                                             pause_variance=current_pause_variance,
                                                             random_seed=current_seed,
                                                             enable_short_sentence=enable_short_sentence)
                update_pipeline = 1  # If we change the foundation, got to change everything
                update_generator = 0

            # Next update the pipeline config, if needed
            if update_pipeline:
                pipeline_config = pykokoro.PipelineConfig(voice=current_voice,
                                                          model_quality=current_quality,
                                                          model_source=current_model,
                                                          model_variant=current_version,
                                                          provider="auto",
                                                          generation=generator_config,
                                                          short_sentence_config=current_short_sentence_conf)

                # Defaults to medium so dont need to do this in that case
                if current_spacy_size != "md": 
                    pipeline_config = pykokoro.with_spacy_model_size(pipeline_config, size=current_spacy_size)

                pipeline = pykokoro.KokoroPipeline(pipeline_config)  # Finally generate the new engine
                update_pipeline = 0
            try:
                play(command_tokens[1].strip(), pipeline)
            except Exception as e:
                print(f"\033[31mError:\033[0m {e}")
        else:
            print(f'Unknown command \"{command}\". Run \"help\" (h) to see a list of available commands or \"quit\" (q) to quit\n')

        full_command = input("Enter a command to test Kokoro (h for help, q to quit): ").strip()
        command_tokens = full_command.split(" ", 1)
        command = command_tokens[0].strip().lower()


if __name__ == "__main__":
    main()

