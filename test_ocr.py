from PIL import Image, ImageDraw, ImageFont
from app.core.ocr import extract_text, extract_words_with_boxes

# Create a clean test image with clear text
img = Image.new('RGB', (600, 200), color='white')
d = ImageDraw.Draw(img)
d.text((20, 30),  'Invoice Number: INV-2024-001', fill='black')
d.text((20, 70),  'Amount Due:     $4,500.00',    fill='black')
d.text((20, 110), 'Due Date:       March 31 2026', fill='black')
d.text((20, 150), 'Status:         Unpaid',        fill='black')
img.save('tmp/test_invoice.png')

# Test plain text extraction
text = extract_text('tmp/test_invoice.png')
print("=== Extracted Text ===")
print(text)

# Test word boxes
words = extract_words_with_boxes('tmp/test_invoice.png')
print(f"=== Words detected: {len(words)} ===")
for w in words[:5]:
    print(f"  '{w['text']}' at x={w['x']}, y={w['y']}, confidence={w['conf']}%")