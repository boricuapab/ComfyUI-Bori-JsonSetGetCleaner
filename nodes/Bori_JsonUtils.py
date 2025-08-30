from pathlib import Path

def gather_files(dir):
    return [f for f in Path(dir).iterdir() if f.is_file() and f.suffix == ".json"]
