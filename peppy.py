# peppy.py

import random
import sys
from dx7_voice_codec import DX7Voice
from dx7_cartridge import DX7Cartridge

def generate_bright_peppy_voice():
    """
    Generate a bright, loud, and peppy DX7 voice with fun parameters.

    :return: A DX7Voice instance with parameters set for a bright and energetic sound.
    """
    voice = DX7Voice()

    # Helper function to maximize brightness and peppiness
    def bright_random(base, variation=20):
        return min(99, max(0, int(base + random.uniform(-1, 1) * variation)))

    # Set each operator’s parameters to be bright and peppy
    for op_num in range(1, 7):
        voice.parameters[f'Operator {op_num}'] = {
            'Rate 1': bright_random(99, 5),           # Fast attack for brightness
            'Rate 2': bright_random(80, 10),          # High decay rate for punchiness
            'Rate 3': bright_random(60, 10),          # Mid-level sustain rate
            'Rate 4': bright_random(30, 10),          # Moderate release rate
            'Level 1': bright_random(99),             # Full initial level for loudness
            'Level 2': bright_random(80, 10),         # Strong level after decay
            'Level 3': bright_random(60, 10),         # Moderate sustain for brightness
            'Level 4': bright_random(0, 10),          # Low release level
            'Breakpoint': bright_random(60, 10),      # Mid-to-high breakpoint
            'Depth': bright_random(40, 10),           # Moderate depth for brightness
            'Curve Left': random.choice([1, 2]),      # Exponential or linear curve
            'Curve Right': random.choice([1, 2]),
            'Detune': random.randint(0, 3),           # Mild detuning for extra peppiness
            'Frequency Coarse': random.choice([1, 2, 3, 4, 8, 16]), # Harmonic relationships
            'Frequency Fine': random.randint(0, 50),  # Moderate fine adjustment for tone
            'Oscillator Detune': random.randint(0, 4) # Subtle detuning for variety
        }

    # Peppy pitch envelope for energetic sound
    voice.parameters['Pitch Envelope'] = {
        'Rate 1': bright_random(80, 10),
        'Rate 2': bright_random(60, 10),
        'Rate 3': bright_random(50, 10),
        'Rate 4': bright_random(20, 10),
        'Level 1': bright_random(70, 10),
        'Level 2': bright_random(50, 10),
        'Level 3': bright_random(30, 10),
        'Level 4': bright_random(0, 5)
    }

    # General parameters optimized for brightness and peppiness
    voice.parameters['General'] = {
        'Algorithm': random.randint(0, 31),              # Use any algorithm for variety
        'Feedback Level': bright_random(5, 3),           # Moderate feedback for energy
        'Oscillator Sync': random.randint(0, 1),         # Random sync for variety
        'LFO Speed': bright_random(70, 20),              # Fast LFO speed for liveliness
        'LFO Delay': bright_random(10, 5),               # Quick LFO onset
        'LFO Pitch Mod Depth': bright_random(20, 10),    # Peppy vibrato
        'LFO Amplitude Mod Depth': bright_random(15, 5), # Subtle tremolo
        'LFO Sync': random.randint(0, 1),                # Random sync for variety
        'LFO Waveform': random.randint(0, 5),            # Variety of waveforms for fun
        'Pitch Mod Sensitivity': random.randint(2, 7),   # High vibrato response
        'Amplitude Mod Sensitivity': random.randint(1, 3), # Moderate tremolo sensitivity
        'Transpose': 24                                  # Standard pitch
    }

    # Generate a fun, random name for the voice
    adjectives = ["Bright", "Snappy", "Peppy", "Sparkly", "Bubbly", "Cheery", "Zippy", "Spunky", "Jazzed", "Vivid"]
    nouns = ["Burst", "Wave", "Tone", "Flash", "Spark", "Glow", "Twist", "Zap", "Pulse", "Chime"]
    voice_name = f"{random.choice(adjectives)} {random.choice(nouns)}"
    voice_name = voice_name[:12].upper().ljust(12)  # Truncate or pad to 12 characters
    voice.parameters['General']['Name'] = voice_name

    return voice

def generate_bright_cartridge(filename):
    """
    Generate a DX7 cartridge with 32 bright and peppy voices, then save it to a file.

    :param filename: The file path to save the cartridge data.
    """
    # Create an empty cartridge
    cartridge = DX7Cartridge()

    # Generate 32 bright and peppy voices
    for _ in range(32):
        bright_voice = generate_bright_peppy_voice()
        cartridge.voices.append(bright_voice)

    # Save the cartridge to a file
    cartridge.save_to_file(filename)
    print(f"Cartridge with 32 bright, loud, and peppy voices saved to {filename}")

if __name__ == "__main__":
    # Parse command line argument for filename
    if len(sys.argv) != 2:
        print("Usage: python peppy.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    generate_bright_cartridge(filename)
