import heapq
import os
import json

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    freq_table = {}
    for char in text:
        if char not in freq_table:
            freq_table[char] = 0
        freq_table[char] += 1
    return freq_table

def build_huffman_tree(freq_table):
    heap = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, current_code="", code_table={}):
    if node is None:
        return

    if node.char is not None:
        code_table[node.char] = current_code
        return

    build_codes(node.left, current_code + "0", code_table)
    build_codes(node.right, current_code + "1", code_table)

    return code_table

def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text

def get_byte_array(padded_encoded_text):
    if len(padded_encoded_text) % 8 != 0:
        raise ValueError("Encoded text not padded properly")

    byte_array = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte_chunk = padded_encoded_text[i:i+8]
        byte_array.append(int(byte_chunk, 2))
    return byte_array

def encode_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    freq_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    code_table = build_codes(huffman_tree)

    encoded_text = "".join(code_table[char] for char in text)
    padded_encoded_text = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_encoded_text)

    dir_name = os.path.dirname(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    bin_path = os.path.join(dir_name, base_name + ".bin")
    dict_path = os.path.join(dir_name, base_name + ".dict")

    with open(bin_path, 'wb') as bin_file:
        bin_file.write(byte_array)

    with open(dict_path, 'w', encoding='utf-8') as dict_file:
        json.dump(code_table, dict_file)

    print(f"[+] Encoded and saved {bin_path} and {dict_path}")


def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    encoded_text = padded_encoded_text[8:]
    encoded_text = encoded_text[:-extra_padding]

    return encoded_text

def decode_file(time: int):
    logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
    
    bin_path = os.path.join(logs_dir, f"{time}.bin")
    dict_path = os.path.join(logs_dir, f"{time}.dict")

    with open(bin_path, 'rb') as bin_file:
        bit_string = ""
        byte = bin_file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = bin_file.read(1)

    with open(dict_path, 'r', encoding='utf-8') as dict_file:
        code_table = json.load(dict_file)

    reversed_code_table = {v: k for k, v in code_table.items()}

    encoded_text = remove_padding(bit_string)
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reversed_code_table:
            decoded_text += reversed_code_table[current_code]
            current_code = ""

    return decoded_text


def batch_encode_logs():
    # Find logs folder relative to this file
    logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))

    if not os.path.exists(logs_dir):
        print(f"Error: Directory {logs_dir} does not exist.")
        return

    for filename in os.listdir(logs_dir):
        if filename.endswith('.txt'):
            base_name = os.path.splitext(filename)[0]
            bin_path = os.path.join(logs_dir, base_name + ".bin")
            dict_path = os.path.join(logs_dir, base_name + ".dict")

            if os.path.exists(bin_path) and os.path.exists(dict_path):
                print(f"[!] Skipping {filename} (already encoded)")
                continue

            filepath = os.path.join(logs_dir, filename)
            print(f"[*] Encoding {filepath}...")
            encode_file(filepath)

    print("[+] All .txt logs encoded successfully.")

#batch_encode_logs() - Call to encode all text files in logs/