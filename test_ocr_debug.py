import pytesseract
from PIL import Image, ImageDraw, ImageFont
from app.config import settings

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH

# Test 1: Raw PIL image directly — no preprocessing
img = Image.new('RGB', (600, 250), color='white')
d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
except:
    font = ImageFont.load_default()

d.text((20, 20),  'Name  Score  Grade', fill='black', font=font)
d.text((20, 80),  'Suhas  95  A',       fill='black', font=font)
d.text((20, 140), 'Alice  88  B',       fill='black', font=font)
img.save('tmp/debug.png')

# Direct tesseract — no cv2 preprocessing
result = pytesseract.image_to_string(img, config='--psm 6')
print("=== Direct PIL result ===")
print(result)