import re
import json

def parse_receipt(text):
    items = []
    item_pattern = re.compile(
        r'^\d+\.\n(.+?)\n([\d\s]+),(\d+)\s+x\s+([\d\s]+),(\d+)\n([\d\s]+),(\d+)',
        re.MULTILINE
    )
    for m in item_pattern.finditer(text):
        name = m.group(1).strip()
        qty = float(m.group(2).replace(' ', '') + '.' + m.group(3))
        price = float(m.group(4).replace(' ', '') + '.' + m.group(5))
        total = float(m.group(6).replace(' ', '') + '.' + m.group(7))
        items.append({"name": name, "quantity": qty, "unit_price": price, "total": total})

    total_match = re.search(r'ИТОГО:\s*([\d\s]+),(\d+)', text)
    total_amount = float(total_match.group(1).replace(' ', '') + '.' + total_match.group(2)) if total_match else None

    date_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', text)
    date = date_match.group(1) if date_match else None
    time = date_match.group(2) if date_match else None

    payment_match = re.search(r'(Банковская карта|Наличные):\s*([\d\s]+),(\d+)', text)
    payment_method = payment_match.group(1) if payment_match else None
    payment_amount = float(payment_match.group(2).replace(' ', '') + '.' + payment_match.group(3)) if payment_match else None

    return {
        "store": re.search(r'Филиал (.+)', text).group(1).strip() if re.search(r'Филиал (.+)', text) else None,
        "date": date,
        "time": time,
        "items": items,
        "calculated_total": round(sum(i["total"] for i in items), 2),
        "receipt_total": total_amount,
        "payment_method": payment_method,
        "payment_amount": payment_amount,
    }

with open('raw.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

result = parse_receipt(raw)
print(json.dumps(result, ensure_ascii=False, indent=2))