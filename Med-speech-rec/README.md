# Medscribe

This repository contains a simple script for transcribing audio files (e.g. `.m4a`) into text
using an open source speech recognition model.

## Dependencies

- Python 3.8+
- [`openai-whisper`](https://github.com/openai/whisper) (MIT license)

Install with:

```powershell
pip install openai-whisper
```

Whisper will download the selected model weights when you run the script for the first time.

## Usage

# Using default paths
python speech-to-text.py

# Using custom directories
python speech-to-text.py C:\path\to\input C:\path\to\output

# With specific model size
python speech-to-text.py C:\path\to\input C:\path\to\output large

## Example

```powershell
python speech-to-text.py meeting.m4a
# writes meeting.txt containing the transcript
```

You can change the model size by editing the `model_size` parameter in
`speech-to-text.py` (options: `tiny`, `base`, `small`, `medium`, `large`).


