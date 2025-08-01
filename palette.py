import sys
from PIL import Image
filename = sys.argv[1]
image_path = filename
image = Image.open(filename)
image = image.convert("RGB")
image.save(filename)
