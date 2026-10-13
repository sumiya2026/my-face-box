import pathlib
p=pathlib.Path('index.html')
s=p.read_text(encoding='utf-8', errors='ignore')

# පරණ නිල් පාට force කරන එක අයින් කරමු
s=s.replace('color: #0b2265 !important;', '/* removed */')

# අපේ අලුත් Logo CSS එක
logo_css = """
<style id="final-white-f-fix">
.myface-box-logo{display:flex;align-items:center;gap:8px}
.myface-circle{width:38px;height:38px;background:#1877F2;border-radius:50%;display:flex;align-items:center;justify-content:center;position:relative}
.myface-circle b{color:white !important;font-size:24px;font-weight:900;font-family:Arial,sans-serif}
.mini-globe-logo{position:absolute;bottom:-5px;right:-5px;font-size:16px;animation:spinGlobe 3s linear infinite}
@keyframes spinGlobe{to{transform:rotate(360deg)}}
</style>
"""

# Logo එක head එකට දාමු
if 'final-white-f-fix' not in s:
    s=s.replace('</head>', logo_css + '</head>')
    # My Face BOX කියන තැනට F logo එක දාමු
    s=s.replace('My Face BOX', '<div class="myface-box-logo"><div class="myface-circle"><b>F</b><span class="mini-globe-logo">🌍</span></div><span>My Face BOX</span></div>')
    p.write_text(s, encoding='utf-8')
    print('SUCCESS - White F Added')
else:
    print('Already Done')
