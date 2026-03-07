import re

text = "hello helo hllo heeeello world"

result = re.findall(r"he*llo", text)
print(f"* → {result}")  # 0 or more occurrences

result = re.findall(r"he+llo", text)
print(f"+ → {result}")  # 1 or more occurrences

result = re.findall(r"he?llo", text)
print(f"? → {result}")  # 0 or 1 occurrence

result = re.findall(r"he{4}llo", text)
print(f"{{n}} → {result}")  # Exactly 4 occurrences

result = re.findall(r"he{2,4}llo", text)
print(f"{{n,m}} → {result}")  # Between 2 and 4 occurrences

result = re.findall(r"he{2,}llo", text)
print(f"{{n,}} → {result}")  # 2 or more occurrences

result = re.findall(r"he*?llo", text)
print(f"*? → {result}")  # 0 or more (non-greedy)

result = re.findall(r"he+?llo", text)
print(f"+? → {result}")  # 1 or more (non-greedy)

result = re.findall(r"he??llo", text)
print(f"?? → {result}")  # 0 or 1 (non-greedy)

result = re.findall(r"\d+", "abc 123 def 4567")
print(f"greedy → {result}")  # Greedy: matches as much as possible

result = re.findall(r"\d+?", "abc 123 def 4567")
print(f"non-greedy → {result}")  # Non-greedy: matches as little as possible