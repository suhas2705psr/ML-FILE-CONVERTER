from PIL import Image, ImageDraw
from app.core.table_extractor import extract_table_from_image, extract_table_to_csv

# Create a test image that looks like a table
img = Image.new('RGB', (600, 220), color='white')
d = ImageDraw.Draw(img)

# Header row
d.text((20,  20), 'Name',   fill='black')
d.text((200, 20), 'Score',  fill='black')
d.text((380, 20), 'Grade',  fill='black')

# Data rows
d.text((20,  70), 'Suhas', fill='black')
d.text((200, 70), '95',    fill='black')
d.text((380, 70), 'A',     fill='black')

d.text((20,  120), 'Alice', fill='black')
d.text((200, 120), '88',    fill='black')
d.text((380, 120), 'B',     fill='black')

d.text((20,  170), 'Bob',  fill='black')
d.text((200, 170), '72',   fill='black')
d.text((380, 170), 'C',    fill='black')

img.save('tmp/test_table.png')

# Extract table
df = extract_table_from_image('tmp/test_table.png', col_count=3)
print("=== Extracted Table ===")
print(df.to_string())

# Save to CSV
out = extract_table_to_csv('tmp/test_table.png', 'tmp/test_table.csv', col_count=3)
print(f"\nSaved to: {out}")