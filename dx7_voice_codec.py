#!/usr/bin/env python3

# dx7_voice_codec.py

class DX7Voice:
    """
    Class to represent and manipulate a Yamaha DX7 voice (patch).
    Provides encoding and decoding functionality for a 128-byte voice structure.
    """

    def __init__(self, data=None):
        """
        Initialize a DX7Voice instance.

        :param data: Optional. A 128-byte array to decode into a voice.
        """
        self.voice_data = data if data else [0] * 128
        self.parameters = {}
        if data:
            self.decode(data)

    def decode(self, data):
        """
        Decode 128 bytes of voice data into a parameter dictionary.

        :param data: 128-byte array representing a DX7 voice.
        """
        if len(data) != 128:
            raise ValueError("Data must be exactly 128 bytes.")

        # Decode operator parameters
        for op in range(6):
            offset = op * 17
            self.parameters[f'Operator {op + 1}'] = {
                'Rate 1': data[offset],
                'Rate 2': data[offset + 1],
                'Rate 3': data[offset + 2],
                'Rate 4': data[offset + 3],
                'Level 1': data[offset + 4],
                'Level 2': data[offset + 5],
                'Level 3': data[offset + 6],
                'Level 4': data[offset + 7],
                'Breakpoint': data[offset + 8],
                'Depth': data[offset + 9],
                'Curve Left': data[offset + 10],
                'Curve Right': data[offset + 11],
                'Detune': data[offset + 12],
                'Frequency Coarse': data[120 + op],
                'Frequency Fine': data[121 + op],
                'Oscillator Detune': data[122 + op],
            }

        # Decode pitch envelope parameters
        self.parameters['Pitch Envelope'] = {
            'Rate 1': data[88],
            'Rate 2': data[89],
            'Rate 3': data[90],
            'Rate 4': data[91],
            'Level 1': data[92],
            'Level 2': data[93],
            'Level 3': data[94],
            'Level 4': data[95],
        }

        # Decode general parameters
        self.parameters['General'] = {
            'Algorithm': data[96],
            'Feedback Level': data[97],
            'Oscillator Sync': data[98],
            'LFO Speed': data[99],
            'LFO Delay': data[100],
            'LFO Pitch Mod Depth': data[101],
            'LFO Amplitude Mod Depth': data[102],
            'LFO Sync': data[103],
            'LFO Waveform': data[104],
            'Pitch Mod Sensitivity': data[105],
            'Amplitude Mod Sensitivity': data[106],
            'Transpose': data[107],
            'Name': ''.join(chr(c) for c in data[108:120]).strip(),
        }

    def encode(self):
        """
        Encode the parameter dictionary back into a 128-byte array.
        """
        data = [0] * 128

        # Encode operator parameters
        for op in range(6):
            offset = op * 17
            operator = self.parameters[f'Operator {op + 1}']
            data[offset] = operator['Rate 1']
            data[offset + 1] = operator['Rate 2']
            data[offset + 2] = operator['Rate 3']
            data[offset + 3] = operator['Rate 4']
            data[offset + 4] = operator['Level 1']
            data[offset + 5] = operator['Level 2']
            data[offset + 6] = operator['Level 3']
            data[offset + 7] = operator['Level 4']
            data[offset + 8] = operator['Breakpoint']
            data[offset + 9] = operator['Depth']
            data[offset + 10] = operator['Curve Left']
            data[offset + 11] = operator['Curve Right']
            data[offset + 12] = operator['Detune']
            data[120 + op] = operator['Frequency Coarse']
            data[121 + op] = operator['Frequency Fine']
            data[122 + op] = operator['Oscillator Detune']

        # Encode pitch envelope parameters
        pitch_env = self.parameters['Pitch Envelope']
        data[88] = pitch_env['Rate 1']
        data[89] = pitch_env['Rate 2']
        data[90] = pitch_env['Rate 3']
        data[91] = pitch_env['Rate 4']
        data[92] = pitch_env['Level 1']
        data[93] = pitch_env['Level 2']
        data[94] = pitch_env['Level 3']
        data[95] = pitch_env['Level 4']

        # Encode general parameters
        general = self.parameters['General']
        data[96] = general['Algorithm']
        data[97] = general['Feedback Level']
        data[98] = general['Oscillator Sync']
        data[99] = general['LFO Speed']
        data[100] = general['LFO Delay']
        data[101] = general['LFO Pitch Mod Depth']
        data[102] = general['LFO Amplitude Mod Depth']
        data[103] = general['LFO Sync']
        data[104] = general['LFO Waveform']
        data[105] = general['Pitch Mod Sensitivity']
        data[106] = general['Amplitude Mod Sensitivity']
        data[107] = general['Transpose']

        # Encode voice name (12 bytes, ASCII)
        name = general['Name']
        for i in range(12):
            data[108 + i] = ord(name[i]) if i < len(name) else 32  # pad with spaces

        self.voice_data = data
        return data

# Example usage
if __name__ == "__main__":
    # Load voice from byte data
    voice_data = [0] * 128  # Replace with actual byte data as needed
    dx7_voice = DX7Voice(voice_data)

    # Modify parameters
    dx7_voice.parameters['General']['Name'] = 'NewPatch'
    dx7_voice.parameters['Operator 1']['Rate 1'] = 99

    # Encode parameters back to bytes
    encoded_data = dx7_voice.encode()
    print(encoded_data)
