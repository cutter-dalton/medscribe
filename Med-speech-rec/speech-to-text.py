import sys
import os
import whisper
from pathlib import Path

# Open-source transcription using OpenAI's Whisper model (MIT licensed)
# The whisper package will download pretrained weights the first time it runs.
# Install requirements with:
#   pip install openai-whisper
# or see https://github.com/openai/whisper for alternatives and
# onnx/runtime-based projects if you need faster inference.


def transcribe(input_path: str, output_path: str | None = None, model_size: str = "small"):
    """Transcribe an audio file to text.

    Parameters
    ----------
    input_path : str
        Path to the source audio file (e.g. .m4a).
    output_path : str | None
        Path to save the transcript. If None, uses the same base name
        as `input_path` with a .txt extension.
    model_size : str
        Whisper model size to load (tiny, base, small, medium, large).
    """
    # normalize the input path for Windows compatibility
    # this will convert backslashes to the appropriate form and
    # resolve any relative components
    input_path = os.path.normpath(input_path)
    if not os.path.isabs(input_path):
        input_path = os.path.abspath(input_path)

    # load the model once
    model = whisper.load_model(model_size)
    result = model.transcribe(input_path)
    transcript = result.get("text", "")

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + f"{model_size}" + ".txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Transcript saved to {output_path}")

if __name__ == "__main__":
    # ensure CLI paths are normalized as well
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    input_file = os.path.normpath(input_file)
    if output_file:
        output_file = os.path.normpath(output_file)

    #print("INPUT FILE:", input_file)
   # print("This is the output file:", output_file)

    input_file = "C:/Users/Cutter/OneDrive/Desktop/Med-speech-rec/recording.m4a"
    print("INPUT FILE:", input_file)


    transcribe(input_file, output_path = None, model_size="small")
