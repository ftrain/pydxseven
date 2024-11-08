import sys
from dx7_voice import DX7Cartridge

def main(filename):
    cartridge = DX7Cartridge.from_file(filename)
    for i, voice in enumerate(cartridge.voices, start=1):
        print(f"Voice {i}:")
        voice.pretty_print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python print_cartridge.py <cartridge_file>")
        sys.exit(1)
    main(sys.argv[1])
