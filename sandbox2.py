from pyannote.audio import Pipeline

# How to use offline: https://github.com/pyannote/pyannote-audio/blob/develop/tutorials/applying_a_pipeline.ipynb

# fine tuning https://github.com/pyannote/pyannote-audio/blob/develop/tutorials/training_a_model.ipynb
  
#pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
pipeline = Pipeline.from_pretrained("model/pyannote/speaker-diarization-3.1")

# run the pipeline on an audio file
diarization = pipeline("data/input/audio2.wav")

# dump the diarization output to disk using RTTM format
with open("data/output/audio2.rttm", "w") as rttm:
    diarization.write_rttm(rttm)

# inference on an excerpt
from pyannote.core import Segment
excerpt = Segment(start=2.0, end=5.0)

from pyannote.audio import Audio
waveform, sample_rate = Audio().crop("file.wav", excerpt)
pipeline({"waveform": waveform, "sample_rate": sample_rate})