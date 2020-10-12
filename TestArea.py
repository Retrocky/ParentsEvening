time = '21:30'
(h, m) = time.split(':')
result = int(h) + int(m) / 60
print(result)
