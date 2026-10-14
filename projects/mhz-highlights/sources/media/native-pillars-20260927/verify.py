"""Check native MHZ2 pillar observations against loc_55552..loc_555FC.
Diagnostic only: reads observations.csv, never supplies engine state.
"""
import csv
from pathlib import Path
rows = list(csv.DictReader((Path(__file__).parent / "final-reference/observations.csv").open()))
def signed(value, bits):
    return (value + (1 << (bits - 1))) % (1 << bits) - (1 << (bits - 1))
words = helpers = clears = 0
for row in rows:
    camera, copied = int(row["camera"]), int(row["copy"])
    assert camera == copied
    if not int(row["bg1"]):
        continue
    distance = signed(camera - 0x4180, 16)
    scaled = signed(distance * 0x5600 * 2, 32)
    delta = signed(distance - signed(scaled >> 16, 16) - 0x18, 16)
    step = (abs(delta << 16) // 48) * (-1 if delta < 0 else 1)
    clear = distance < -0x140
    clears += clear
    for line in [0, 17, 30, 40, 47]:
        value = signed((-signed(copied - 0x80, 16) << 16) + line * step, 32)
        expected = 0 if clear else signed(value >> 16, 16)
        assert expected == int(row[f"bg_line{line}"]), (row["frame"], line, expected)
        words += 1
    if clear:
        continue
    for key, line in [("tall",47),("spike0",40),("spike1",40),("spike2",30),
                      ("spike3",30),("spike4",17),("spike5",17)]:
        actual = int(row[key])
        if actual == -1:
            continue
        expected = (((int(row[f"bg_line{line}"]) - 0x48) & 0x1FF) + camera) & 0xFFFF
        assert expected == actual, (row["frame"], key, expected, actual)
        helpers += 1
print(f"{len(rows)} rows; {words} scroll words; {helpers} helpers; {clears} clear frames; zero mismatches")
