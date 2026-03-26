from app.core.classifier import train_classifier, classify_text, classify_file

# Train the model
print("Training classifier...")
train_classifier()

# Test with sample texts
tests = [
    ("invoice",  "Invoice Number INV-001 Amount Due $4500 Tax Total Payable billing"),
    ("resume",   "Python SQL experience internship education bachelor degree skills"),
    ("contract", "Agreement parties hereby terms conditions obligations liabilities"),
    ("code",     "def function import class return variable method parameter type"),
    ("financial","Revenue profit loss balance sheet assets liabilities equity cash"),
]

print("\n=== Classification Tests ===")
for expected, text in tests:
    result = classify_text(text)
    status = "✅" if result["document_type"] == expected else "❌"
    print(f"{status} Expected: {expected:12} Got: {result['document_type']:12} Confidence: {result['confidence']:.1%}")

# Test on a real file
print("\n=== File Classification ===")
r = classify_file("tmp/test.pdf")
print(f"test.pdf → {r['document_type']} ({r['confidence']:.1%} confidence)")
print(f"Recommended outputs: {r['recommendations']}")