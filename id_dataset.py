import os
import json
import uuid

def process_jsonl_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            file_path = os.path.join(directory, filename)
            temp_file_path = file_path + ".tmp"
            
            with open(file_path, 'r', encoding='utf-8') as infile, open(temp_file_path, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    try:
                        data = json.loads(line.strip())
                        if "id" not in data:
                            data = {"id": str(uuid.uuid4()), **data}
                        outfile.write(json.dumps(data) + '\n')
                    except json.JSONDecodeError:
                        print(f"Skipping invalid JSON line in file {filename}: {line.strip()}")
            
            os.replace(temp_file_path, file_path)

if __name__ == "__main__":
    directory_path = "./data/fill-mask/v6/"
    process_jsonl_files(directory_path)