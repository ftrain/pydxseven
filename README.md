# Yamaha DX7 Cartridge Specification Documentation

The Yamaha DX7 synthesizer uses a unique file structure to store patches (voices) on its cartridges. This document outlines the byte-level specification of Yamaha DX7 cartridge files, including headers, checksums, final bytes, and the number of voices each cartridge contains. This information is essential for creating or editing DX7 cartridge files for accurate voice loading and saving.

---

## 1. **Cartridge Structure Overview**
Each Yamaha DX7 cartridge file (typically with a `.syx` or `.bin` extension) contains 32 voices. The DX7's memory architecture allows each voice (patch) to be defined individually, with a specific structure for parameters, headers, and metadata. These cartridges follow a strict byte order and layout for proper loading by the DX7.

---

## 2. **File Header**

- **Length:** 6 bytes
- **Description:** The header provides the initial identification for the cartridge and specifies the type of data being loaded.
- **Format:**
  - **Byte 0:** Fixed value `0xF0` (MIDI System Exclusive start byte).
  - **Byte 1:** Manufacturer ID for Yamaha, typically `0x43`.
  - **Byte 2:** Device/channel identifier (can vary but often set to `0x00` for the DX7).
  - **Byte 3:** Data type for voice data, usually `0x09` (indicating 32-voice data).
  - **Byte 4:** Data length MSB (Most Significant Byte), usually `0x20`.
  - **Byte 5:** Data length LSB (Least Significant Byte), usually `0x00`.

---

## 3. **Voice Data Structure**

Each DX7 voice in the cartridge is structured with a set of parameters that define its timbre and behavior. The 32 voices are stored sequentially.

- **Voice Count:** 32 voices, with each voice occupying 128 bytes.
- **Total Size of Voice Data:** 4,096 bytes (128 bytes per voice * 32 voices).

**Voice Parameter Breakdown:** Each voice includes parameters for operator settings, envelopes, pitch, modulation, etc., organized into the following sections:
  - **Algorithm and routing parameters:** Define operator relationships.
  - **Pitch and modulation parameters:** Define pitch envelope and modulation sensitivity.
  - **Operator parameters (x6):** Define the envelopes, frequency ratios, and amplitude scaling for each of the six operators.
  - **Miscellaneous parameters:** Name of the patch, level, etc.

---

## 4. **Checksum**

- **Position:** The checksum byte follows the voice data, specifically at byte 4102 in the file.
- **Calculation:** The checksum is calculated by summing all bytes from the start of the voice data to the end of the last voice (bytes 6 to 4101), taking the least significant 7 bits of the sum, and subtracting from 128 (`0x80`). This value ensures data integrity by detecting potential errors during data transmission.
- **Example Calculation:**  
  ```plaintext
  Checksum = 128 - (sum of bytes 6 to 4101) % 128
  ```

---

## 5. **End of File (Final Bytes)**

- **Length:** 1 byte
- **Description:** The end of the file is marked by a single `0xF7` byte, which serves as the System Exclusive (SysEx) end byte.
- **Position:** Byte 4103.

---

## 6. **Summary Table**

| Section                  | Byte Range      | Description                                     |
|--------------------------|-----------------|-------------------------------------------------|
| Header                   | 0-5             | 6-byte header for SysEx start, Yamaha ID, etc.  |
| Voice Data               | 6-4101          | 32 voices, each occupying 128 bytes             |
| Checksum                 | 4102            | Checksum for voice data                         |
| End of File (SysEx End)  | 4103            | `0xF7` to signal end of SysEx message           |

---

## Example Cartridge Data Layout

Here's an example byte sequence for a typical DX7 cartridge file:

- **Header:** `F0 43 00 09 20 00`
- **Voice 1 to Voice 32 Data:** (Sequential 128-byte blocks for each voice)
- **Checksum:** Calculated byte after all voices
- **End Byte:** `F7`

## Important Notes

- **Data Editing:** Any modification to the voice data requires recalculating the checksum.
- **Cartridge Limits:** DX7 cartridges can only hold 32 voices. Exceeding this limit will result in data overflow and may cause the DX7 to reject the cartridge.

---

This structure ensures compatibility with the Yamaha DX7 and maintains data integrity through structured headers, defined data segments, and the checksum verification. Proper adherence to this specification is essential for creating functional and reliable DX7 cartridges.

# Voices

Each voice in a Yamaha DX7 cartridge is structured with 128 bytes that define the parameters for timbre, envelopes, and modulation for a given patch. Here is a complete breakdown of the byte structure and function for each voice in a DX7 cartridge file.

### DX7 Voice Parameter Byte Breakdown (128 bytes per voice)

| Byte | Parameter                           | Range        | Description                                                                                           |
|------|-------------------------------------|--------------|-------------------------------------------------------------------------------------------------------|
| 0    | Operator 1 Rate 1                   | 0-99         | Determines the attack rate of operator 1's envelope                                                   |
| 1    | Operator 1 Rate 2                   | 0-99         | Second segment rate of operator 1's envelope                                                          |
| 2    | Operator 1 Rate 3                   | 0-99         | Third segment rate of operator 1's envelope                                                           |
| 3    | Operator 1 Rate 4                   | 0-99         | Release rate of operator 1's envelope                                                                 |
| 4    | Operator 1 Level 1                  | 0-99         | Initial level of operator 1's envelope (higher values produce louder output)                          |
| 5    | Operator 1 Level 2                  | 0-99         | Second segment level of operator 1's envelope                                                         |
| 6    | Operator 1 Level 3                  | 0-99         | Third segment level of operator 1's envelope                                                          |
| 7    | Operator 1 Level 4                  | 0-99         | Release level of operator 1's envelope                                                                |
| 8    | Operator 1 Break Point              | 0-99         | Key scaling breakpoint for operator 1                                                                  |
| 9    | Operator 1 Depth                    | 0-99         | Key scaling depth for operator 1                                                                       |
| 10   | Operator 1 Curve Left               | 0-3          | Left curve for key scaling (0 = linear, 1 = exponential, etc.)                                        |
| 11   | Operator 1 Curve Right              | 0-3          | Right curve for key scaling                                                                            |
| 12   | Operator 1 Detune                   | 0-14         | Detunes operator 1 slightly to create a chorusing effect                                              |
| 13-27| **Operator 2-6 Parameters**         | -            | The next 75 bytes (13-87) repeat the same parameter structure for operators 2 through 6               |
| 88   | Pitch Envelope Rate 1               | 0-99         | Attack rate of pitch envelope                                                                         |
| 89   | Pitch Envelope Rate 2               | 0-99         | Second segment rate of pitch envelope                                                                 |
| 90   | Pitch Envelope Rate 3               | 0-99         | Third segment rate of pitch envelope                                                                  |
| 91   | Pitch Envelope Rate 4               | 0-99         | Release rate of pitch envelope                                                                        |
| 92   | Pitch Envelope Level 1              | 0-99         | Initial pitch level (value is added to the base pitch)                                                |
| 93   | Pitch Envelope Level 2              | 0-99         | Second level of pitch envelope                                                                        |
| 94   | Pitch Envelope Level 3              | 0-99         | Third level of pitch envelope                                                                         |
| 95   | Pitch Envelope Level 4              | 0-99         | Release pitch level                                                                                   |
| 96   | Algorithm                           | 0-31         | Selects which FM algorithm (routing of operators) to use                                              |
| 97   | Feedback Level                      | 0-7          | Determines feedback amount for operators                                                              |
| 98   | Oscillator Sync                     | 0-1          | Sets oscillator sync on or off                                                                        |
| 99   | LFO Speed                           | 0-99         | Sets the LFO speed                                                                                    |
| 100  | LFO Delay                           | 0-99         | Sets the LFO delay                                                                                    |
| 101  | LFO Pitch Mod Depth                 | 0-99         | Sets the depth of pitch modulation by the LFO                                                         |
| 102  | LFO Amplitude Mod Depth             | 0-99         | Sets the depth of amplitude modulation by the LFO                                                     |
| 103  | LFO Sync                            | 0-1          | Turns LFO sync on or off                                                                              |
| 104  | LFO Waveform                        | 0-5          | Selects LFO waveform (sine, square, triangle, etc.)                                                   |
| 105  | Pitch Modulation Sensitivity        | 0-7          | Controls the pitch modulation sensitivity of the entire patch                                         |
| 106  | Amplitude Modulation Sensitivity    | 0-3          | Controls amplitude modulation sensitivity                                                             |
| 107  | Transpose                           | 0-48         | Transposes the voice (0 = -24 semitones, 24 = standard pitch, 48 = +24 semitones)                     |
| 108-119 | Name of the Voice                | ASCII (A-Z,  | 12 bytes for the name of the voice (in ASCII characters)                                             |
| 120  | Operator 1 Oscillator Frequency Coarse | 0-31     | Coarse frequency setting for operator 1                                                               |
| 121  | Operator 1 Oscillator Frequency Fine   | 0-99     | Fine frequency setting for operator 1                                                                 |
| 122  | Operator 1 Oscillator Detune        | 0-14         | Detune value for operator 1                                                                           |
| 123-127 | **Operator 2-6 Frequency and Detune** | -     | Each operator has corresponding coarse, fine, and detune values, totaling 24 bytes                    |

Each voice structure precisely outlines the settings for each operator, ensuring control over each aspect of sound design in the DX7’s FM synthesis framework. This specification allows fine control of sound characteristics, from envelope shaping to frequency modulation, across all six operators.
