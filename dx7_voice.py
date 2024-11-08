import struct

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
        if len(data) != 4096:
            raise ValueError("Cartridge data must be 4096 bytes long")
        self.voices = [DX7Voice(data[i:i+128]) for i in range(0, 4096, 128)]

    def to_bytes(self):
        return b''.join(voice.to_bytes() for voice in self.voices)

    @staticmethod
    def from_file(filename):
        with open(filename, 'rb') as f:
            data = f.read()
        if len(data) < 4096:
            raise ValueError(f"File '{filename}' is {len(data)} bytes long, but it must be at least 4096 bytes long")
        return DX7Cartridge(data[:4096])

    def to_file(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.to_bytes())
