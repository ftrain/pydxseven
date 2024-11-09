import sys
import os
from dx7_voice import DX7Cartridge
from compare_syx_files import compare_files

def disassemble_reassemble(input_file, output_file):
    # Read the original cartridge
    original_cartridge = DX7Cartridge.from_file(input_file)

    # Disassemble into voices
    voices = original_cartridge.voices

    # Reassemble into a new cartridge
    new_cartridge = DX7Cartridge(b''.join(voice.to_bytes() for voice in voices))
    new_cartridge.to_file(output_file)

    # Compare the original and new cartridge files
    compare_files(input_file, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python disassemble_reassemble.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    disassemble_reassemble(input_file, output_file)
    print("Disassembly and reassembly completed. Files compared successfully.")
