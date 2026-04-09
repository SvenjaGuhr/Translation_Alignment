'''
Python Script for automated text splitting
Default = split into chunks of 1,000 words each

How to use in bash:

# Default: 1000-word chunks
python text_split_1000-word_chunks.py my_book.txt

# Custom chunk size (e.g. 500 words)
python text_split_1000-word_chunks.py my_book.txt 500

python text_split_1000-word_chunks.py '/Users/.../my_book.txt'

'''



import re
import sys
from pathlib import Path


def split_text_file(input_path: str, chunk_size: int = 1000) -> None:
    """
    Split a text file into multiple files of `chunk_size` words each.

    Output files are named:  <stem>_001.txt, <stem>_002.txt, ...
    and are written to the same directory as the input file.
    """
    input_file = Path(input_path)
    if not input_file.is_file():
        print(f"Error: '{input_path}' is not a valid file.")
        sys.exit(1)

    text = input_file.read_text(encoding="utf-8")

    # Split on whitespace while keeping track of word boundaries
    words = re.split(r"(\s+)", text)          # odd indices = whitespace runs
    tokens = [w for w in words if w.strip()]  # keep only actual words

    total_words = len(tokens)
    if total_words == 0:
        print("The file appears to be empty.")
        sys.exit(0)

    # Re-associate each word with any trailing whitespace from the original text
    # so line-breaks and spacing are preserved inside each chunk.
    segments: list[str] = []
    seg: list[str] = []
    word_count = 0
    for part in words:
        if part.strip():          # it's a word
            seg.append(part)
            word_count += 1
            if word_count == chunk_size:
                segments.append("".join(seg))
                seg = []
                word_count = 0
        else:                     # it's whitespace
            if seg:               # attach trailing whitespace to current chunk
                seg.append(part)

    if seg:                       # flush remaining words
        segments.append("".join(seg))

    total_chunks = len(segments)
    pad = len(str(total_chunks))  # e.g. 3 digits for up to 999 chunks

    output_dir = input_file.parent
    stem = input_file.stem

    for i, chunk in enumerate(segments, start=1):
        out_name = f"{stem}_{str(i).zfill(max(pad, 3))}.txt"
        out_path = output_dir / out_name
        out_path.write_text(chunk.strip(), encoding="utf-8")
        chunk_words = len(chunk.split())
        print(f"  Written: {out_name}  ({chunk_words} words)")

    print(f"\nDone. {total_words} words split into {total_chunks} file(s).")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_text.py <input_file.txt> [chunk_size]")
        print("       chunk_size defaults to 1000 words")
        sys.exit(1)

    input_path = sys.argv[1]
    chunk_size = int(sys.argv[2]) if len(sys.argv) >= 3 else 1000

    if chunk_size < 1:
        print("Error: chunk_size must be a positive integer.")
        sys.exit(1)

    print(f"Splitting '{input_path}' into {chunk_size}-word chunks...\n")
    split_text_file(input_path, chunk_size)
    
    
    
    