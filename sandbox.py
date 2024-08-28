# instantiate the pipeline
from pyannote.audio import Pipeline

file = open("token.txt", "r")
token = file.read()
print(token)
file.close()

pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token=token)

# run the pipeline on an audio file
diarization = pipeline("data/input/audio2.wav")

# dump the diarization output to disk using RTTM format
with open("data/output/audio2.rttm", "w") as rttm:
    diarization.write_rttm(rttm)

import torch

torch.cuda.is_available()