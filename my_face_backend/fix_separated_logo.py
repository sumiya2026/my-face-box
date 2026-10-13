import os, glob
for f in glob.glob("**/*.html", recursive=True):
    try:
        t=open(f,'r',encoding='utf-8',errors='ignore').read()
        if 'logo' in t.lower() or 'M' in t:
            t=t.replace('#000',' #FF6B00').replace('black','orange').replace('#000000','#FF6B00')
            # Force orange M
            t=t.replace('>M<',' style="color:#FF6B00 !important;">M<')
            open(f,'w',encoding='utf-8').write(t)
            print(f"Fixed {f}")
    except: pass
print("Done! Now orange M!")
