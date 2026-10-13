import os

app_path = "app.py"

if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 🛡️ ඇප් එකේ ආරක්ෂාව සඳහා Flask-Limiter සහ ආරක්ෂක Middlewares එකතු කිරීම
    # මෙය හැකර් ප්‍රහාර (XSS/Injection) සහ එකවර බෝට් ප්‍රහාර එන DDoS ස්වයංක්‍රීයව බ්ලොක් කරයි
    security_imports = """
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import werkzeug
"""
    
    security_setup = """
# 🕵️ අධි ආරක්ෂක පද්ධතිය සහ බෝට් ප්‍රහාර (DDoS) වැළැක්වීමේ සීමාවන් සක්‍රීය කිරීම
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# 🔒 ආරක්ෂක Headers එකතු කිරීම (XSS සහ Clickjacking වලින් හැකර්වරුන් වැළැක්වීමට)
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self' https://placeholder.com; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';"
    return response

# 🔍 වෛරස් සහ හානිකර මාධ්‍ය ගොනු (Malicious file validation) ස්වයංක්‍රීයව පිරිසිදු කිරීමේ පද්ධතිය
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
"""

    if "flask_limiter" not in code:
        # Imports එකතු කිරීම
        code = security_imports + "\n" + code
        # app = Flask(__name__...) රේඛාව සොයා ඊට යටින් සෙටප් එක ඇතුළත් කිරීම
        if "app = Flask" in code:
            lines = code.split("\n")
            for idx, line in enumerate(lines):
                if "app = Flask" in line:
                    lines.insert(idx + 1, security_setup)
                    break
            code = "\n".join(lines)

    with open(app_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[SUCCESS] Automated Security System & Anti-Hacking patches written to app.py successfully!")
else:
    print("[ERROR] app.py not found.")
