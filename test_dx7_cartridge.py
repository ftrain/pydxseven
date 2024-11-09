import os
import sys
from dx7_voice import DX7Cartridge

def test_cartridge(original_file):
    new_file = 'new_cartridge.syx'

    # Read the original cartridge
    original_cartridge = DX7Cartridge.from_file(original_file)

    # Check for the SysEx header
    expected_header = b'F0 43 00 09 20 00 00 00'
    with open(original_file, 'rb') as f:
        header = f.read(len(expected_header))
    assert header == expected_header, "Cartridge file does not start with the expected SysEx header"
    assert len(original_cartridge.voices) == 32, "Cartridge must contain 32 voices"
    for i, voice in enumerate(original_cartridge.voices, start=1):
        assert len(voice.to_bytes()) == 128, f"Voice {i} data must be 128 bytes long"
        # Additional checks can be added here for each voice parameter

    # Check the entire cartridge data
    cartridge_data = original_cartridge.to_bytes()
    assert len(cartridge_data) == 4096, "Cartridge data must be 4096 bytes long"
    print("Cartridge is valid.")

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
