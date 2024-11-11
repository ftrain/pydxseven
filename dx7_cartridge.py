# dx7_cartridge.py

from dx7_voice_codec import DX7Voice

class DX7Cartridge:
    """
    Class to represent and manipulate a Yamaha DX7 cartridge containing 32 voices.
    Provides functionality for loading, validating, and saving a cartridge file.
    """

    def __init__(self, data=None):
        """
        Initialize a DX7Cartridge instance.

        :param data: Optional. A byte array representing the entire cartridge.
        """
        self.cartridge_data = data if data else [0xF0, 0x43, 0x00, 0x09, 0x20, 0x00] + [0] * (4096 + 2)  # Header + voices + checksum + end byte
        self.voices = []
        if data:
            self.load(data)

    def load(self, data):
        """
        Load and parse cartridge data, decoding each voice.

        :param data: A byte array representing the entire cartridge (4104 bytes).
        """
        if len(data) != 4104:
            raise ValueError("Cartridge data must be exactly 4104 bytes.")

        # Verify header (first 6 bytes)
        if data[:6] != [0xF0, 0x43, 0x00, 0x09, 0x20, 0x00]:
            raise ValueError("Invalid cartridge header.")

        # Extract each voice
        for i in range(32):
            start = 6 + i * 128
            voice_data = data[start:start + 128]
            voice = DX7Voice(voice_data)
            self.voices.append(voice)

        # Validate checksum
        if not self.validate_checksum(data):
            raise ValueError("Checksum is invalid.")

    def save(self):
        """
        Serialize the cartridge and recalculate the checksum.
        """
        data = [0xF0, 0x43, 0x00, 0x09, 0x20, 0x00]

        # Add serialized voices
        for voice in self.voices:
            data.extend(voice.encode())

        # Calculate and append checksum
        checksum = self.calculate_checksum(data[6:4102])
        data.append(checksum)

        # Append end byte
        data.append(0xF7)

        self.cartridge_data = data
        return data

    @staticmethod
    def calculate_checksum(data):
        """
        Calculate the checksum for the given data.

        :param data: List of bytes (voice data only, excluding header).
        :return: Checksum byte.
        """
        checksum = 128 - (sum(data) % 128)
        return checksum & 0x7F  # Ensure checksum is a single byte

    @staticmethod
    def validate_checksum(data):
        """
        Validate the checksum of the cartridge data.

        :param data: List of bytes representing the entire cartridge.
        :return: True if checksum is valid, False otherwise.
        """
        calculated_checksum = DX7Cartridge.calculate_checksum(data[6:4102])
        return calculated_checksum == data[4102]

    def load_from_file(self, filename):
        """
        Load cartridge data from a file.

        :param filename: Path to the file containing cartridge data.
        """
        with open(filename, 'rb') as file:
            data = list(file.read())
            self.load(data)

    def save_to_file(self, filename):
        """
        Save the cartridge data to a file with a valid checksum.

        :param filename: Path to save the cartridge data.
        """
        data = self.save()
        with open(filename, 'wb') as file:
            file.write(bytearray(data))

# Example usage
if __name__ == "__main__":
    # Load a cartridge from a file
    cartridge = DX7Cartridge()
    cartridge.load_from_file("example_cartridge.syx")

    # Modify a voice parameter
    cartridge.voices[0].parameters['General']['Name'] = "NewSound"

    # Save cartridge back to a file with recalculated checksum
    cartridge.save_to_file("modified_cartridge.syx")
