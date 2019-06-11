# Import necessary libraries
from pydub import AudioSegment
from pydub.silence import split_on_silence  
from pydub.playback import play
import speech_recognition as speechRec

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

# function for separating out silent chunks and normalize audio.
def audio_processing(audio):
    # Split track where the silence is 0.5 seconds or more and get chunks using the imported function
    dBFS = audio.dBFS
    chunks = split_on_silence(audio,
        min_silence_len=500,
        silence_thresh=dBFS-16,
        keep_silence=250
    )

    # Create a empty chunk for normalized output
    normalized_audio = AudioSegment.empty()

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(chunk, -20.0)

        # Export the audio chunk with new bitrate.
        # print("Exporting chunk{0}.wav.".format(i))
        # filename = ".//chunk{0}.wav".format(i)
        # normalized_chunk.export(
        #     filename,
        #     bitrate="192k",
        #     format="wav"
        # )
        normalized_audio += normalized_chunk

    return normalized_audio

# Text file to write the recognized audio
def speech_recognition(filename):
    text_file = open(".//output//recognized.txt", "w+")

    # Specify the audio file to recognize 
    AUDIO_FILE = filename 

    # Initialize the recognizer 
    recognizer = speechRec.Recognizer() 

    # Traverse the audio file and listen to the audio 
    with speechRec.AudioFile(AUDIO_FILE) as source: 
        audio_listened = recognizer.listen(source) 

    # Try to recognize the listened audio 
    # And catch expections. 
    try:     
        rec = recognizer.recognize_google(audio_listened) 
            
        # If recognized, write into the file. 
        text_file.write(rec+"\n") 
        
    # If google could not understand the audio 
    except speechRec.UnknownValueError: 
        print("Could not understand audio") 

    # If the results cannot be requested from Google. 
    # Probably an internet connection error. 
    except speechRec.RequestError: 
        print("Could not request results.") 

    text_file.close()

# Load Audio
def load_audio(filename):
    audio = AudioSegment.from_wav(filename)
    print("Loading Done")
    return audio

# Play Audio
def play_audio(audio):
    play(audio)

# Draw Audio Signal
def draw_signal():
    pass
