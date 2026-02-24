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


def transcribe(input_path: str, output_path: str | None = None, model_size: str = "small") -> None:
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


def transcribe_directory(input_dir: str, output_dir: str, model_size: str = "small") -> None:
    """Transcribe all m4a files in a directory to text files.

    Parameters
    ----------
    input_dir : str
        Path to the directory containing .m4a files.
    output_dir : str
        Path to the directory where transcripts will be saved.
    model_size : str
        Whisper model size to load (tiny, base, small, medium, large).
    """
    # Normalize paths
    input_dir = os.path.normpath(input_dir)
    output_dir = os.path.normpath(output_dir)
    
    if not os.path.isabs(input_dir):
        input_dir = os.path.abspath(input_dir)
    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(output_dir)

    # Ensure input directory exists
    if not os.path.isdir(input_dir):
        raise ValueError(f"Input directory does not exist: {input_dir}")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Find all .m4a files in the input directory
    input_path = Path(input_dir)
    audio_files = list(input_path.glob("*.m4a"))

    if not audio_files:
        print(f"No .m4a files found in {input_dir}")
        return

    print(f"Found {len(audio_files)} audio file(s) to transcribe.")

    # Load the model once for efficiency
    model = whisper.load_model(model_size)
    
    # Process each audio file
    for audio_file in audio_files:
        input_path = str(audio_file)
        # Create output filename with same base name
        output_filename = audio_file.stem + ".txt"
        output_path = os.path.join(output_dir, output_filename)

        print(f"Processing: {audio_file.name}")
        result = model.transcribe(input_path)
        transcript = result.get("text", "")

        # Save transcript
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"  Saved to: {output_filename}")

    print(f"All transcripts saved to {output_dir}")


if __name__ == "__main__":
    # Check if user provided input and output directories
    if len(sys.argv) >= 3:
        # Use command-line arguments for input and output directories
        input_directory = sys.argv[1]
        output_directory = sys.argv[2]
        model_size = sys.argv[3] if len(sys.argv) > 3 else "small"
    else:
        # Default paths for testing/development
        base_dir = "C:/Users/Cutter/OneDrive/Desktop/Med-speech-rec"
        input_directory = os.path.join(base_dir, "data/input")
        output_directory = os.path.join(base_dir, "data/output")
        model_size = "small"

    print(f"Input directory: {input_directory}")
    print(f"Output directory: {output_directory}")
    print(f"Model size: {model_size}")
    print()

    try:
        transcribe_directory(input_directory, output_directory, model_size)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
