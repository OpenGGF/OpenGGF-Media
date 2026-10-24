"""Contact sheet of capture frames: python3 sheet.py <shot> <out.png> f0 f1 step  (or explicit frames)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
TASK = Path(__file__).resolve().parent.parent
shot, out = sys.argv[1], sys.argv[2]
nums = [int(a) for a in sys.argv[3:]]
frames = list(range(nums[0], nums[1] + 1, nums[2])) if len(nums) == 3 else nums
files = {int(p.stem.split("-")[-1]): p for p in (TASK / "captures" / shot / "frames").glob("*.png")}
cols = 4
W, H = 400, 224
sheet = Image.new("RGB", (cols * W, ((len(frames) + cols - 1) // cols) * (H + 16)), (20, 20, 30))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(frames):
    k = min(files, key=lambda n: abs(n - f))
    x, y = (i % cols) * W, (i // cols) * (H + 16)
    sheet.paste(Image.open(files[k]).convert("RGB"), (x, y + 16))
    d.text((x + 4, y + 2), f"{shot} {k}", fill=(255, 230, 80))
sheet.save(out)
