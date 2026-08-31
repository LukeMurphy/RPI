import linecache
from pathlib import Path
script_dir = Path(__file__).resolve().parent
print(script_dir)

filename =  f"{script_dir}/cfglist.txt"
# filename = "combsets.txt"

fileRef = open(filename, "r")
lines = fileRef.readlines()

sections = []
lineCount = 0
lastLine = 0
pieceCount = 0
for _l in lines:
    if _l.startswith("["):
        pieceCount += 1
        sections.append(lineCount)
        # lastLine = lineCount - 1

    lineCount += 1
sections.append(lineCount)
fileRef.close()

print(sections)



with open(filename, "r", encoding="utf-8") as file:
    lines = file.readlines()
    for _s in range(0,len(sections)-1):
        _firstLine = sections[_s]
        _lastLine = sections[_s+1] - 1
        cfgName = f"{lines[_firstLine].strip()}".replace("[", "").replace("]", "")
        fOpen = open(f"{cfgName}.cfg", "w+")
        print(f"Making: {cfgName}.cfg {_firstLine} {_lastLine}")
        for _cfgLine in range(_firstLine, _lastLine):
            try:
                fOpen.write(f"{lines[_cfgLine].rstrip()}\n") 
            except Exception as e:
                print(e)
        fOpen.close()


