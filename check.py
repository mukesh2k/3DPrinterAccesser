a = ""
with open("this.gcode") as f:
    a += "".join(line for line in f if not line.isspace())
a = a.splitlines()
i = 0
for each in a:
    if ';' in each:
        each = each[:each.index(';')]
        if each == '':
            continue
    print(each)
