import json
import random
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_FILE = BASE_DIR / "raw" / "raw.jsonl"
TRAIN_FILE = BASE_DIR / "processed" / "train.jsonl"
VAL_FILE = BASE_DIR / "processed" / "val.jsonl"
PLOT_FILE = BASE_DIR / "processed" / "length_distribution.png"

MIN_TOKENS = 30
MAX_TOKENS = 800
VAL_RATIO = 0.1


def is_valid(sample):
    for key in ["instruction", "input", "output"]:
        if key not in sample:
            return False
        if not isinstance(sample[key], str):
            return False
        if sample[key].strip() == "":
            return False
    return True


def token_count(sample):
    text = sample["instruction"] + " " + sample["input"] + " " + sample["output"]
    return len(text.split()) 


def main():
    samples = []
    lengths = []

    with open(RAW_FILE, "r", encoding="utf-8") as f:
        for line in f:
            s = json.loads(line)

            if not is_valid(s):
                continue

            length = token_count(s)
            if MIN_TOKENS <= length <= MAX_TOKENS:
                samples.append(s)
                lengths.append(length)

    assert len(samples) >= 1000, "Need at least 1000 samples"

    # plot
    plt.hist(lengths, bins=40)
    plt.xlabel("Length (approx tokens)")
    plt.ylabel("Samples")
    plt.title("Instruction Length Distribution")
    plt.savefig(PLOT_FILE)
    plt.close()

    random.shuffle(samples)
    split = int(len(samples) * (1 - VAL_RATIO))

    train = samples[:split]
    val = samples[split:]

    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s) + "\n")

    with open(VAL_FILE, "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(s) + "\n")

    print(" Done")
    print(f"Train samples: {len(train)}")
    print(f"Val samples: {len(val)}")
    print(f"Plot saved: {PLOT_FILE}")


if __name__ == "__main__":
    main()
