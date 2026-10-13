import glob
for f in glob.glob("templates/**/*.html", recursive=True) + glob.glob("*.html"):
    t=open(f,'r',encoding='utf-8',errors='ignore').read()
    if 'MY FACE' in t or 'FACE BOX' in t:
        t=t.replace('#FF6B00','#FF6B00').replace('#FF6B00','#FF6B00').replace('blue','orange')
        open(f,'w',encoding='utf-8').write(t)
        print(f"Fixed {f} -> Orange!")
print("Done")
