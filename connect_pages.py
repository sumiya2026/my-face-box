import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # යටින්ම තියෙන Verify Identity බොත්තම එබූ විට ලියාපදිංචි පිටුවට (Popup හෝ වෙනම කොටසකට) යන ලෙස සැකසීම
    # බොත්තමට onclick event එකක් සහ ලියාපදිංචි වීමේ පෝරමය (Signup Form) ප්‍රධාන පිටුව ඇතුළටම ලස්සනට බස්සමු
    
    signup_form_html = """
    <!-- ලියාපදිංචි වීමේ උත්පතන පෝරමය (Signup Popup Modal) -->
    <div id="signupModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 99999; justify-content: center; align-items: center; padding: 20px;">
        <div style="background: white; padding: 20px; border-radius: 10px; width: 100%; max-width: 400px; box-shadow: 0px 5px 15px rgba(0,0,0,0.3); position: relative; max-height: 90vh; overflow-y: auto;">
            <span onclick="document.getElementById('signupModal').style.display='none'" style="position: absolute; right: 15px; top: 10px; font-size: 24px; cursor: pointer; font-weight: bold; color: #888;">&times;</span>
            <h3 style="color: #FF6B00; text-align: center; margin-bottom: 20px;" data-i18n="verifyBtn">My Face BOX ලියාපදිංචිය</h3>
            
            <label style="font-weight: bold; display: block; margin-bottom: 5px;">දුරකථන අංකය (Phone Number):</label>
            <input type="text" placeholder="0712345678" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 5px;">
            
            <label style="font-weight: bold; display: block; margin-bottom: 5px;">සම්පූර්ණ නම (Full Name):</label>
            <input type="text" placeholder="ඔබේ නම මෙහි ලියන්න" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 5px;">
            
            <label style="font-weight: bold; display: block; margin-bottom: 5px;">ජාතික හැඳුනුම්පත් අංකය (ID Number):</label>
            <input type="text" id="nicInput" placeholder="ID Number" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 5px; font-weight: bold;">
            
            <button onclick="alert('OTP කේතය ඔබගේ දුරකථනයට යවන ලදී!')" style="width: 100%; background: #FF6B00; color: white; border: none; padding: 12px; border-radius: 5px; font-weight: bold; cursor: pointer;">ඉදිරියට යන්න (Proceed to OTP)</button>
        </div>
    </div>
    """

    # ප්‍රධාන පිටුවේ බොත්තම සොයා එයට ක්‍රියාකාරීත්වය දීම
    if "Verify Identity & Create Account" in content:
        content = content.replace(
            'Verify Identity & Create Account (Real Users Only)',
            'Verify Identity & Create Account (Real Users Only)'
        )
        # බොත්තම ඇති කෝඩ් එකට onclick එකතු කිරීම
        content = content.replace(
            'style="', 
            'onclick="document.getElementById(\'signupModal\').style.display=\'flex\'" style="'
        )

    if "signupModal" not in content:
        content = content.replace("</body>", f"{signup_form_html}\n</body>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] Main Page and Verification Page successfully linked together!")
else:
    print("[ERROR] index.html not found.")
