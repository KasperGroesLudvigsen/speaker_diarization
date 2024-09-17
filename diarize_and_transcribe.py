# instantiate the pipeline
from pyannote.audio import Pipeline
import pyannote.core.json
import re
import json
from pydub import AudioSegment


import yaml

with open(local_model_path) as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
import os
##########

file = open("token.txt", "r")
token = file.read()
print(token)
file.close()

local_model_path = "local_model/config.yaml"

#PIPELINE = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=token)
PIPELINE = Pipeline.from_pretrained(local_model_path)

res = PIPELINE("data/input/audio2.wav")
res.__str__()

def combine_consecutive_speakers(json_data: list[dict]):
    """
    When two or more consecutive elements in the diarization are from the same speaker,
    combine the elements into one
    """

    # Initialize the list for the processed data
    merged_data = []

    # Iterate through the json_data
    for entry in json_data:
        # If merged_data is empty or the current entry's speaker is different from the last speaker
        if not merged_data or merged_data[-1]["speaker"] != entry["speaker"]:
            merged_data.append(entry.copy())  # Append a copy of the entry to avoid modifying the original data
        else:
            # If the speakers are the same, merge the text and update the end_time
            merged_data[-1]["end_time"] = entry["end_time"]  # Update the end_time
            merged_data[-1]["text"] += " " + entry["text"]  # Combine the texts

    # Print the merged data as JSON
    #json_output = json.dumps(merged_data, indent=4)
    #print(json_output)

    return merged_data

def time_to_milliseconds(time_str: str):
    """
    Paynnote time stamps look like this: '00:00:01.330' and needs to be converted to ms
    """
    # Split the string into hours, minutes, seconds, and milliseconds
    h, m, s = time_str.split(":")
    seconds, milliseconds = s.split(".")
    
    # Convert each part to milliseconds
    total_milliseconds = (int(h) * 3600000) + (int(m) * 60000) + (int(seconds) * 1000) + int(milliseconds)
    
    return total_milliseconds

def call_transcribe_api():
    return "lorem ipsum"

def transcribe(diarization_list: list[dict], audio_file_path):

    diarization_list_w_transcription = []

    audio = AudioSegment.from_file(audio_file_path)

    for i, segment in enumerate(diarization_list):

        start_time = time_to_milliseconds(segment["start_time"])

        end_time = time_to_milliseconds(segment["end_time"])
        
        # Extract the segment
        audio_segment = audio[start_time:end_time]
        
        # TODO: Instead of saving the segments, call the API directly
        transcription = call_transcribe_api()
        # Export the audio segment to a new file
        #output_filename = f"output_segment_{i+1}.mp3"
        #audio_segment.export(output_filename, format="mp3")
        #print(f"Segment {i+1} exported to {output_filename}")

        segment["transcription"] = transcription

        diarization_list_w_transcription.append(segment)

    return diarization_list_w_transcription


def diarize_and_transcribe(file_path):
    """
    The function that will be called when the API end point is requested
    """

    # run the pipeline on an audio file
    diarization = PIPELINE(file_path)

    # dump the diarization output to disk using RTTM format
    #with open("data/output/audio2.rttm", "w") as rttm:
    #    diarization.write_rttm(rttm)

    # Convert pyannote's string output to json-like list
    diarization_list = convert_to_json(diarization.__str__())

    # Consecutive elements in diarization_list may be from the same speaker. Combine those
    diarization_list = combine_consecutive_speakers(diarization_list)

    diarization_and_transcription = transcribe(diarization_list)

    return diarization_and_transcription