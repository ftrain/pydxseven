import sys

def compare_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    if len(data1) != len(data2):
        print(f"Files differ in size: {len(data1)} vs {len(data2)} bytes")
        return

    differences = []
    for i, (byte1, byte2) in enumerate(zip(data1, data2)):
        if byte1 != byte2:
            differences.append((i, byte1, byte2))

    if not differences:
        print("Files are identical.")
    else:
        print(f"Found {len(differences)} differences:")
        for index, byte1, byte2 in differences:
            print(f"Byte {index}: {byte1} != {byte2}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_syx_files.py <file1> <file2>")
        sys.exit(1)

    compare_files(sys.argv[1], sys.argv[2])
