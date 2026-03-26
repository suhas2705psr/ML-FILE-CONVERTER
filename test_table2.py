from PIL import Image, ImageDraw, ImageFont
from app.core.table_extractor import extract_table_from_image

img = Image.new('RGB', (600, 250), color='white')
d = ImageDraw.Draw(img)

# Use a larger font size so Tesseract can read it
try:
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
except:
    font = ImageFont.load_default()

d.text((20,  20),  'Name',  fill='black', font=font)
d.text((200, 20),  'Score', fill='black', font=font)
d.text((380, 20),  'Grade', fill='black', font=font)

d.text((20,  80),  'Suhas', fill='black', font=font)
d.text((200, 80),  '95',    fill='black', font=font)
d.text((380, 80),  'A',     fill='black', font=font)

d.text((20,  140), 'Alice', fill='black', font=font)
d.text((200, 140), '88',    fill='black', font=font)
d.text((380, 140), 'B',     fill='black', font=font)

d.text((20,  200), 'Bob',   fill='black', font=font)
d.text((200, 200), '72',    fill='black', font=font)
d.text((380, 200), 'C',     fill='black', font=font)

img.save('tmp/test_table2.png')

df = extract_table_from_image('tmp/test_table2.png', col_count=3)
print("=== Extracted Table ===")
print(df.to_string())