import os

def split_file_to_chunks(file_path, chunks_dir, chunk_size_kb=64):
    os.makedirs(chunks_dir, exist_ok=True)
    chunk_size = chunk_size_kb * 1024
    base_name = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        part_num = 0
        while chunk := f.read(chunk_size):
            chunk_filename = f"{base_name}.part{part_num}"
            chunk_path = os.path.join(chunks_dir, chunk_filename)
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            part_num += 1

    print(f"[INFO] Split '{base_name}' into {part_num} parts")

def join_chunks_to_file(chunks_dir, output_path):
    base_name = os.path.basename(output_path)
    part_num = 0
    with open(output_path, 'wb') as out_file:
        while True:
            part_path = os.path.join(chunks_dir, f"{base_name}.part{part_num}")
            if not os.path.exists(part_path):
                break
            with open(part_path, 'rb') as part_file:
                out_file.write(part_file.read())
            part_num += 1
    print(f"[INFO] Joined {part_num} parts into '{output_path}'")
