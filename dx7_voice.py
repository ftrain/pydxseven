import struct
import random
import string

class DX7Voice:
    def __init__(self, data):
        # Ensure the data is 128 bytes long
        if len(data) != 128:
            raise ValueError("Voice data must be 128 bytes long")
        
        # Operator parameters
        self.operators = []
        for i in range(6):
            offset = i * 17
            operator_data = data[offset:offset+17]
            self.operators.append({
                'rate1': operator_data[0],
                'rate2': operator_data[1],
                'rate3': operator_data[2],
                'rate4': operator_data[3],
                'level1': operator_data[4],
                'level2': operator_data[5],
                'level3': operator_data[6],
                'level4': operator_data[7],
                'break_point': operator_data[8],
                'left_depth': operator_data[9],
                'right_depth': operator_data[10],
                'left_curve': operator_data[11],
                'right_curve': operator_data[12],
                'rate_scaling': operator_data[13],
                'amp_mod_sensitivity': operator_data[14],
                'key_velocity_sensitivity': operator_data[15],
                'operator_output_level': operator_data[16],
            })
        
        # Pitch EG
        self.pitch_eg = {
            'rate1': data[102],
            'rate2': data[103],
            'rate3': data[104],
            'rate4': data[105],
            'level1': data[106],
            'level2': data[107],
            'level3': data[108],
            'level4': data[109],
        }
        
        # Other voice parameters
        self.algorithm = data[110]
        self.feedback = data[111]
        self.oscillator_sync = data[112]
        self.lfo_speed = data[113]
        self.lfo_delay = data[114]
        self.lfo_pitch_mod_depth = data[115]
        self.lfo_amp_mod_depth = data[116]
        self.lfo_sync = data[117]
        self.lfo_waveform = data[118]
        self.pitch_mod_sensitivity = data[119]
        self.transpose = data[120]
        self.name = data[121:127].decode('ascii').strip()
        self.reserved = data[127]
        if len(data) != 128:
            raise ValueError("Voice data must be 128 bytes long")
        self.data = data

    @staticmethod
    def random_voice():
        data = bytearray(128)

        # Define sound types with specific parameter ranges
        sound_types = {
            "Bass": {"algorithm": (0, 7), "feedback": (0, 3), "lfo_speed": (20, 40)},
            "Pluck": {"algorithm": (8, 15), "feedback": (4, 7), "lfo_speed": (40, 60)},
            "Brass": {"algorithm": (16, 23), "feedback": (2, 5), "lfo_speed": (60, 80)},
            "Piano": {"algorithm": (24, 31), "feedback": (0, 2), "lfo_speed": (80, 99)},
        }

        # Choose a random sound type
        sound_type = random.choice(list(sound_types.keys()))
        params = sound_types[sound_type]

        # Set operator parameters
        for i in range(6):
            offset = i * 17
            for j in range(17):
                data[offset + j] = random.randint(0, 99)

        # Set pitch EG
        for i in range(102, 110):
            data[i] = random.randint(0, 99)

        # Set other parameters based on sound type
        data[110] = random.randint(*params["algorithm"])  # Algorithm
        data[111] = random.randint(*params["feedback"])   # Feedback
        data[112] = random.randint(0, 1)                  # Oscillator Sync
        data[113] = random.randint(*params["lfo_speed"])  # LFO Speed
        data[114] = random.randint(0, 99)                 # LFO Delay
        data[115] = random.randint(0, 99)                 # LFO Pitch Mod Depth
        data[116] = random.randint(0, 99)                 # LFO Amp Mod Depth
        data[117] = random.randint(0, 1)                  # LFO Sync
        data[118] = random.randint(0, 5)                  # LFO Waveform
        data[119] = random.randint(0, 7)                  # Pitch Mod Sensitivity
        data[120] = random.randint(0, 48)                 # Transpose

        # Generate a random and silly name
        words = [
            "Fuzzy", "Bouncy", "Wobble", "Quirky", "Zappy", "Snappy", "Giggly", "Wiggly", "Jumpy", "Funky",
            "Zany", "Whacky", "Loopy", "Zippy", "Bubbly", "Silly", "Goofy", "Dizzy", "Wacky", "Jazzy",
            "Spunky", "Peppy", "Sparky", "Zesty", "Breezy", "Cheery", "Perky", "Chirpy", "Frisky", "Lively",
            "Sprightly", "Vibrant", "Vivacious", "Whimsical", "Playful", "Merry", "Jolly", "Sunny", "Radiant", "Gleeful"
        ]
        name = " ".join(random.sample(words, random.randint(2, 3)))
        data[121:127] = name.encode('ascii', 'ignore').ljust(6)[:6]

        data[127] = 0  # Reserved byte
        return DX7Voice(data)
    def to_bytes(self):
        data = bytearray(128)

        # Pack operator data
        for i, operator in enumerate(self.operators):
            offset = i * 17
            data[offset:offset+17] = [
                operator['rate1'],
                operator['rate2'],
                operator['rate3'],
                operator['rate4'],
                operator['level1'],
                operator['level2'],
                operator['level3'],
                operator['level4'],
                operator['break_point'],
                operator['left_depth'],
                operator['right_depth'],
                operator['left_curve'],
                operator['right_curve'],
                operator['rate_scaling'],
                operator['amp_mod_sensitivity'],
                operator['key_velocity_sensitivity'],
                operator['operator_output_level'],
            ]

        # Pack pitch EG
        data[102:110] = [
            self.pitch_eg['rate1'],
            self.pitch_eg['rate2'],
            self.pitch_eg['rate3'],
            self.pitch_eg['rate4'],
            self.pitch_eg['level1'],
            self.pitch_eg['level2'],
            self.pitch_eg['level3'],
            self.pitch_eg['level4'],
        ]

        # Pack other voice parameters
        data[110] = self.algorithm
        data[111] = self.feedback
        data[112] = self.oscillator_sync
        data[113] = self.lfo_speed
        data[114] = self.lfo_delay
        data[115] = self.lfo_pitch_mod_depth
        data[116] = self.lfo_amp_mod_depth
        data[117] = self.lfo_sync
        data[118] = self.lfo_waveform
        data[119] = self.pitch_mod_sensitivity
        data[120] = self.transpose
        data[121:127] = self.name.encode('ascii').ljust(6)
        data[127] = self.reserved

        return bytes(data)

    def pretty_print(self):
        print(f"Voice Name: {self.name}")
        print(f"Algorithm: {self.algorithm}, Feedback: {self.feedback}, Oscillator Sync: {self.oscillator_sync}")
        print("Operators:")
        for i, op in enumerate(self.operators, start=1):
            print(f"  Operator {i}:")
            for key, value in op.items():
                print(f"    {key}: {value}")
        print("Pitch EG:")
        for key, value in self.pitch_eg.items():
            print(f"  {key}: {value}")
        print(f"LFO Speed: {self.lfo_speed}, LFO Delay: {self.lfo_delay}, LFO Pitch Mod Depth: {self.lfo_pitch_mod_depth}")
        print(f"LFO Amp Mod Depth: {self.lfo_amp_mod_depth}, LFO Sync: {self.lfo_sync}, LFO Waveform: {self.lfo_waveform}")
        print(f"Pitch Mod Sensitivity: {self.pitch_mod_sensitivity}, Transpose: {self.transpose}")
        print("-" * 40)

class DX7Cartridge:
    def __init__(self, data):
        # Ensure the data is at least 4096 bytes long (header + voices + footer)
        if len(data) < 4092:
            raise ValueError("Cartridge data must be at least 4092 bytes long")

        # Skip the header and footer
        self.voices = [DX7Voice(data[i:i+128]) for i in range(8, 8 + 32 * 128, 128)]

    def to_bytes(self):
        return b''.join(voice.to_bytes() for voice in self.voices)

    @staticmethod
    def random_cartridge():
        voices = [DX7Voice.random_voice() for _ in range(32)]
        return DX7Cartridge(b''.join(voice.to_bytes() for voice in voices))

    @staticmethod
    def from_file(filename):
        with open(filename, 'rb') as f:
            data = f.read()
        return DX7Cartridge(data)

    def to_file(self, filename):
        with open(filename, 'wb') as f:
            # Write the cartridge data with the correct header and format
            header = bytes.fromhex('F043000920000000')
            f.write(header)
            # Write the cartridge data without the header and footer
            cartridge_data = self.to_bytes()
            f.write(cartridge_data)
            # Calculate and write the checksum
            checksum = (~sum(cartridge_data) + 1) & 0x7F
            f.write(bytes([checksum]))
            # Write the footer
            footer = bytes.fromhex('F7')
            f.write(footer)
