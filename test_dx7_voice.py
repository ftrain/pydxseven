import os
import sys
from dx7_voice import DX7Cartridge

def test_cartridge(original_file):
    new_file = 'new_cartridge.syx'

    # Read the original cartridge
    original_cartridge = DX7Cartridge.from_file(original_file)

    # Write to a new cartridge file
    original_cartridge.to_file(new_file)

    # Read the new cartridge
    new_cartridge = DX7Cartridge.from_file(new_file)

    # Verify that the original and new cartridges are identical
    assert original_cartridge.to_bytes() == new_cartridge.to_bytes(), "Cartridges do not match"

    # Clean up
    os.remove(new_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_dx7_cartridge.py <cartridge_file>")
        sys.exit(1)
    test_cartridge(sys.argv[1])
    print("Test passed!")
