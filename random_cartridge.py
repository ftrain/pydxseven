import sys
from dx7_voice import DX7Cartridge

def main(filename):
    cartridge = DX7Cartridge.random_cartridge()
    cartridge.to_file(filename)
    print(f"Random cartridge saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python random_cartridge.py <output_file>")
        sys.exit(1)
    main(sys.argv[1])
