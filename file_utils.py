import os

def split_file_to_chunks(filepath, chunks_dir, chunk_size_kb=64):
    os.makedirs(chunks_dir, exist_ok=True)
    fname = os.path.basename(filepath)
    try:
        with open(filepath, "rb") as f:
            i = 0
            while True:
                chunk = f.read(chunk_size_kb * 1024)
                if not chunk:
                    break
                part_path = os.path.join(chunks_dir, f"{fname}.part{i}")
                with open(part_path, "wb") as part_file:
                    part_file.write(chunk)
                i += 1
    except Exception as e:
        print(f"[ERROR] Failed to split {fname}: {e}")

def join_chunks_to_file(chunks_dir, output_path):
    base = os.path.basename(output_path)
    i = 0
    try:
        with open(output_path, "wb") as out:
            while True:
                part_path = os.path.join(chunks_dir, f"{base}.part{i}")
                if not os.path.exists(part_path):
                    break
                with open(part_path, "rb") as part:
                    out.write(part.read())
                i += 1
    except Exception as e:
        print(f"[ERROR] Failed to join chunks for {base}: {e}")

def count_parts(chunks_dir, filename):
    return sum(
        1 for f in os.listdir(chunks_dir)
        if f.startswith(f"{filename}.part") and os.path.isfile(os.path.join(chunks_dir, f))
    )
