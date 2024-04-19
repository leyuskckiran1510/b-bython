from pathlib import Path

SAMPLE_PATH = Path("samples")


def load_sample(file_index: int):
    files = list(SAMPLE_PATH.glob(f"sample{file_index}.*"))
    if not files:
        raise ValueError(f"No file exsist with id {file_index}")
    for file in files:
        with open(str(file), "r") as fp:
            yield file, fp.read()
