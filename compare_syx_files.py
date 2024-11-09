import sys

def compare_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    if len(data1) != len(data2):
        print(f"Files differ in size: {len(data1)} vs {len(data2)} bytes")
        min_length = min(len(data1), len(data2))
    else:
        min_length = len(data1)

    differences = []
    for i in range(min_length):
        byte1 = data1[i]
        byte2 = data2[i]
        if byte1 != byte2:
            differences.append((i, byte1, byte2))

    if not differences:
        print("Files are identical.")
    else:
        print(f"Found {len(differences)} differences:")
        for index, byte1, byte2 in differences:
            print(f"Byte {index}: {byte1:02X} != {byte2:02X}")

    if len(data1) != len(data2):
        print("Additional bytes in the longer file:")
        longer_data = data1 if len(data1) > len(data2) else data2
        for i in range(min_length, len(longer_data)):
            print(f"Byte {i}: {longer_data[i]:02X}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_syx_files.py <file1> <file2>")
        sys.exit(1)

    compare_files(sys.argv[1], sys.argv[2])
