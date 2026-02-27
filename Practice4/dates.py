from datetime import datetime, timedelta, date

print(datetime.now() - timedelta(days=5))

print(date.today() - timedelta(days=1))
print(date.today())
print(date.today() + timedelta(days=1))

print(datetime.now().replace(microsecond=0))

dt1 = datetime.now()
dt2 = datetime(2026, 12, 31)
print((dt2 - dt1).total_seconds())