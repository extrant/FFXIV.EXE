import os
import json


def parse_opcode_file(file_path):
    opcode_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                if ' = ' in line:
                    key, values_str = line.split(' = ', 1)
                    values = []
                    if ', ' in values_str:
                        values = [int(val.strip(), 16) for val in values_str.split(', ')]
                    else:
                        values = [int(values_str.strip(), 16)]
                    opcode_dict[key] = values
    return opcode_dict



def merge_opcode_files(file_paths):
    all_opcodes = {}
    for file_path in file_paths:
        version = os.path.splitext(os.path.basename(file_path))[0]
        opcodes = parse_opcode_file(file_path)
        all_opcodes[version] = opcodes
    return all_opcodes


def save_to_json(data, json_path):
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)


def query_opcode(data, version, opcode_name):
    if version in data and opcode_name in data[version]:
        return data[version][opcode_name]
    return None


current_dir = os.getcwd()
txt_files = [os.path.join(current_dir, f) for f in os.listdir(current_dir) if f.endswith('.txt')]

all_opcodes = merge_opcode_files(txt_files)

json_path = 'all_opcodes.json'
save_to_json(all_opcodes, json_path)

version = 'opcodes_710_2025.02.13.0000.0000'
opcode_name = 'UP_ActionSend'
result = query_opcode(all_opcodes, version, opcode_name)
if result:
    print(f"Version {version}, Opcode {opcode_name}: {result}")
else:
    print(f"Opcode {opcode_name} not found in version {version}.")