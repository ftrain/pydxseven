import random
import serial

class DX7Voice:
    def __init__(self, data):
        # Ensure the data is 128 bytes long
        if len(data) != 128:
            raise ValueError("Voice data must be 128 bytes long, it is actually {}".format(len(data)))
        
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
    def byte_construct(rnd_num, rnd_low, rnd_high, ser_port=''):
        rnd_bytes = []
        with serial.Serial(ser_port, 19200, timeout=1) as ser:
            x = ser.read(rnd_num)
            while True:
                if len(rnd_bytes) == rnd_num:
                    break
                replace_bytes = 0
                for valid_byte in range(len(x)):
                    if rnd_high >= int(x[valid_byte]) >= rnd_low:
                        rnd_bytes.append(int(x[valid_byte]))
                    else:
                        replace_bytes += 1
                x = ser.read(replace_bytes)
        return rnd_bytes

    @staticmethod
    def op_construct(ser_port=''):
        op_bytes = []
        syx1 = DX7Voice.byte_construct(13, 0, 99, ser_port)
        for lvls in range(11):
            op_bytes.append(syx1[lvls])
        op_bytes.append(DX7Voice.byte_construct(1, 0, 15, ser_port)[0])
        op_bytes.append(DX7Voice.byte_construct(1, 0, 119, ser_port)[0])
        op_bytes.append(DX7Voice.byte_construct(1, 0, 31, ser_port)[0])
        op_bytes.append(syx1[11])
        op_bytes.append(DX7Voice.byte_construct(1, 0, 63, ser_port)[0])
        op_bytes.append(syx1[12])
        return op_bytes

    @staticmethod
    def random_voice(ser_port=''):
        data = bytearray(128)
        for ops in range(6):
            current_op = DX7Voice.op_construct(ser_port)
            for op in range(len(current_op)):
                data[ops * 17 + op] = current_op[op]
        syx1 = DX7Voice.byte_construct(12, 0, 99, ser_port)
        syx2 = DX7Voice.byte_construct(3, 97, 122, ser_port)
        patch_name = DX7Voice.byte_construct(16, 0, 255, ser_port)
        patch_name_count = sum(patch_name)
        patch_name = ''.join(chr(patch_name[i] % 26 + 65) for i in range(6))
        for param in range(8):
            data[102 + param] = syx1[param]
        data[110] = DX7Voice.byte_construct(1, 0, 31, ser_port)[0]
        data[111] = DX7Voice.byte_construct(1, 0, 15, ser_port)[0]
        for param in range(8, 12):
            data[112 + param] = syx1[param]
        data[120] = DX7Voice.byte_construct(1, 0, 123, ser_port)[0]
        data[121:127] = patch_name.encode('ascii', 'ignore').ljust(6)[:6]
        data[127] = syx2[2]
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
        if len(data) < 4096:
            raise ValueError("Cartridge data must be at least 4096 bytes long")

        # Skip the header and footer
        self.voices = [DX7Voice(data[i:i+128]) for i in range(0, 32 * 128, 128)]

    def to_bytes(self):
        return b''.join(voice.to_bytes() for voice in self.voices)

    @staticmethod
    def random_cartridge(ser_port=''):
        voices = [DX7Voice.random_voice(ser_port) for _ in range(32)]
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
