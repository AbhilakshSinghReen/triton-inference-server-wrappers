from json import load as json_load


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json_load(f)
    
    return data
