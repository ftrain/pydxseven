import struct

class DX7Voice:
    def __init__(self, data):
        if len(data) != 128:
            raise ValueError("Voice data must be 128 bytes long")
        self.data = data

    def to_bytes(self):
        return self.data

class DX7Cartridge:
    def __init__(self, data):
        if len(data) != 4096:
            raise ValueError("Cartridge data must be 4096 bytes long")
        self.voices = [DX7Voice(data[i:i+128]) for i in range(0, 4096, 128)]

    def to_bytes(self):
        return b''.join(voice.to_bytes() for voice in self.voices)

    @staticmethod
    def from_file(filename):
        with open(filename, 'rb') as f:
            data = f.read()
        return DX7Cartridge(data)

    def to_file(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.to_bytes())
