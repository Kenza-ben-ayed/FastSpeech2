import os
import librosa
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm
from text import _clean_text

def prepare_align(config):
    in_dir = config["path"]["corpus_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    cleaners = config["preprocessing"]["text"]["text_cleaners"]
    speaker = "Arabic"
    
    with open(os.path.join(in_dir, "metadata.csv"), encoding="utf-8") as f:
        for line in tqdm(f):
            parts = line.strip().split("|")
            base_name = parts[0]
            text = parts[1]
            text = _clean_text(text, cleaners)

            wav_path = os.path.join(in_dir, "wav", "{}.wav".format(base_name))
            if os.path.exists(wav_path):
                os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)

                # Corrected line: use sr as a keyword argument
                wav, _ = librosa.load(wav_path, sr=sampling_rate)

                # Normalize and scale the wav array
                wav = wav / max(abs(wav)) * max_wav_value
                
                # Write the wav file
                wavfile.write(
                    os.path.join(out_dir, speaker, "{}.wav".format(base_name)),
                    sampling_rate,
                    wav.astype(np.int16),
                )

                # Write the corresponding label file
                with open(
                    os.path.join(out_dir, speaker, "{}.lab".format(base_name)),
                    "w",
                     encoding="utf-8"  # Specify UTF-8 encoding
                ) as f1:
                    f1.write(text)
