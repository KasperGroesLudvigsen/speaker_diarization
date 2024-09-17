# instantiate the pipeline
from pyannote.audio import Pipeline
import pyannote.core.json
import re
import json
from pydub import AudioSegment


file = open("token.txt", "r")
token = file.read()
print(token)
file.close()

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=token)

# run the pipeline on an audio file
diarization = pipeline("data/input/audio2.wav")

# dump the diarization output to disk using RTTM format
with open("data/output/audio2.rttm", "w") as rttm:
    diarization.write_rttm(rttm)

diarization.__str__()

diarization.for_json()

pyannote.core.json.dump(diarization)

import re
import json

# Original string
data = '''[ 00:00:01.330 -->  00:00:02.899] A SPEAKER_00
[ 00:00:03.389 -->  00:00:04.114] B SPEAKER_00
[ 00:00:05.177 -->  00:00:06.949] C SPEAKER_01
[ 00:00:08.215 -->  00:00:10.257] D SPEAKER_00
[ 00:00:11.269 -->  00:00:12.974] E SPEAKER_01'''

def convert_to_json(diarization_str):
  # Regular expression to match the pattern
  pattern = r'\[\s*([\d:.]+)\s*-->\s*([\d:.]+)\s*\]\s*(\w+)\s*(SPEAKER_\d{2})'

  # Find all matches in the string
  matches = re.findall(pattern, diarization_str)

  # Convert the matches into a list of dictionaries
  json_data = []
  for start, end, text, speaker in matches:
      json_data.append({
          "start_time": start,
          "end_time": end,
          "text": text,
          "speaker": speaker
      })

  return json_data

  # Convert the list to JSON
  json_output = json.dumps(json_data, indent=4)
  return json_output
  # Print or return the JSON output
  #print(json_output)

json_data = convert_to_json(diarization.__str__())
print(js)

# Combine time stamps if two or more consecutive time stamps are with the same speaker
segments = []
for i, el in enumerate(js):
    current_speaker_segments = []

    current_speaker_segments.append(js[i])

    speaker = js[i]["speaker"]

    next_speaker = js[i+1]["speaker"]
    
    if next_speaker == speaker:
        go_on = True
    
    while go_on:

        current_speaker_segments.append(js[i])

        #i += 1

        speaker = js[i+1]["speaker"]
        next_speaker = js[i+2]["speaker"]

        if next_speaker != speaker:

            go_on = False

            segments.append(current_speaker_segments)
            current_speaker_segments = []

segments[0]
   


speaker_order = [i["speaker"] for i in js]


go_on = True
segments = []
i = 0
all_segments = []
current_speaker_segments = []
#current_speaker_segments.append(js[i])

while i < len(js):

    #current_speaker_segments.append(js[i])

    current_speaker = js[i]["speaker"]

    next_speaker = js[i+1]["speaker"]

    if current_speaker == next_speaker:

        current_speaker_segments.append(js[i])
        current_speaker_segments.append(js[i+1])

        i += 2

    else:

        #go_on = False

        #current_speaker_segments.append(js[i])

        segments.append(current_speaker_segments)

        current_speaker_segments = []

        i += 1

segments[0]

js[2]



# The original JSON data
json_data = [
    {
        "start_time": "00:00:01.330",
        "end_time": "00:00:02.899",
        "text": "A",
        "speaker": "SPEAKER_00"
    },
    {
        "start_time": "00:00:03.389",
        "end_time": "00:00:04.114",
        "text": "B",
        "speaker": "SPEAKER_00"
    },
    {
        "start_time": "00:00:04.2",
        "end_time": "00:00:04.8",
        "text": "B",
        "speaker": "SPEAKER_00"
    },
    {
        "start_time": "00:00:05.177",
        "end_time": "00:00:06.949",
        "text": "C",
        "speaker": "SPEAKER_01"
    },
    {
        "start_time": "00:00:08.215",
        "end_time": "00:00:10.257",
        "text": "D",
        "speaker": "SPEAKER_00"
    },
    {
        "start_time": "00:00:11.269",
        "end_time": "00:00:12.974",
        "text": "E",
        "speaker": "SPEAKER_01"
    },
    {
        "start_time": "00:00:13.001",
        "end_time": "00:00:15.213",
        "text": "F",
        "speaker": "SPEAKER_01"
    }
]

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

#json_data = combine_consecutive_speakers(json_data)

diarization_list = convert_to_json(diarization_str=diarization.__str__())
## 
diarization_list = combine_consecutive_speakers(json_data=diarization_list)

segments = [{"start_time" : segment["start_time"], "end_time" : segment["end_time"]} for segment in diarization_list]




