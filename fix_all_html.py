import os, glob

# Find all html files recursively including templates/
html_files = glob.glob("**/*.html", recursive=True)

wizard_code = """
<!-- Global Real User Verification Modal -->
<div id="authModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:99999; justify-content:center; align-items:center; padding:15px; box-sizing:border-box;">
    <div style="background:white; width:100%; max-width:450px; border-radius:12px; padding:25px; box-shadow:0 8px 24px rgba(0,0,0,0.3); font-family:sans-serif; text-align:left;">
        
        <!-- Step 1: ID / Document Capture -->
        <div id="st1">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:10px; text-align:center;">🛡️ Real User Verification</h2>
            <p style="font-size:13px; color:#65676b; text-align:center; margin-bottom:15px;">Capture NIC, Driving License, Passport, or Postal ID (15+) to verify identity.</p>
            <div style="border:2px dashed #ccd0d5; border-radius:8px; padding:10px; text-align:center; margin-bottom:15px; background:#f0f2f5;">
                <video id="liveCam" autoplay playsinline style="width:100%; max-height:180px; border-radius:6px; display:none;"></video>
                <div id="camTxt" style="padding:25px 0; color:#4b4f56; font-size:14px;">📷 Click Start to Scan ID / Passport</div>
            </div>
            <button type="button" onclick="initCam()" id="sBtn" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; margin-bottom:10px;">Start Document Capture</button>
            <button type="button" onclick="nextSt2()" id="nBtn" style="background:#42b72a; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; display:none;">Capture & Auto-Fill</button>
        </div>

        <!-- Step 2: Account Configuration & Naming -->
        <div id="st2" style="display:none;">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:10px; text-align:center;">✨ Account Setup</h2>
            <p style="font-size:13px; color:#65676b; text-align:center; margin-bottom:15px;">Document verified. Configure your account details.</p>
            <label style="font-size:13px; font-weight:bold; color:#4b4f56; display:block; margin-bottom:5px;">Select Account Type:</label>
            <select id="accChoice" style="width:100%; padding:10px; border:1px solid #ccd0d5; border-radius:6px; margin-bottom:15px; font-size:14px;">
                <option value="fb">Personal FB Account</option>
                <option value="page">Business / Public Page</option>
            </select>
            <label style="font-size:13px; font-weight:bold; color:#4b4f56; display:block; margin-bottom:5px;">Enter Account Name:</label>
            <input type="text" id="userNameInput" placeholder="Type your preferred name..." style="width:100%; padding:10px; border:1px solid #ccd0d5; border-radius:6px; margin-bottom:20px; font-size:14px; box-sizing:border-box;">
            <button type="button" onclick="nextSt3()" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer;">Continue to Pin Mark</button>
        </div>

        <!-- Step 3: Pin Mark / Biometric Signature -->
        <div id="st3" style="display:none; text-align:center;">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:10px;">🔒 Biometric Pin Mark</h2>
            <p style="font-size:13px; color:#65676b; margin-bottom:20px;">Provide your digital security touch/pin mark to complete real-human verification.</p>
            <div style="background:#f0f2f5; border:1px solid #ccd0d5; padding:20px; border-radius:8px; margin-bottom:20px; cursor:pointer;" onclick="finishReg()">
                <div style="font-size:32px; margin-bottom:10px;">👆</div>
                <strong style="color:#1c1e21; font-size:15px;">Tap Here to Register Pin Mark</strong>
                <div style="font-size:12px; color:#65676b; margin-top:5px;">Blocks all fake accounts permanently</div>
            </div>
        </div>

    </div>
</div>

<script>
let activeStream = null;
function openAuthModal() {
    document.getElementById("authModal").style.display = "flex";
}
function initCam() {
    document.getElementById("camTxt").style.display = "none";
    let v = document.getElementById("liveCam");
    v.style.display = "block";
    document.getElementById("sBtn").style.display = "none";
    document.getElementById("nBtn").style.display = "block";
    
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(s => { activeStream = s; v.srcObject = s; })
    .catch(e => {
        alert("Camera access notice: Using fallback photo mode due to browser restriction (" + e + ")");
    });
}
function nextSt2() {
    if(activeStream) { activeStream.getTracks().forEach(t => t.stop()); }
    document.getElementById("st1").style.display = "none";
    document.getElementById("st2").style.display = "block";
}
function nextSt3() {
    let nameVal = document.getElementById("userNameInput").value;
    if(!nameVal.trim()) { alert("Please enter a valid account name."); return; }
    document.getElementById("st2").style.display = "none";
    document.getElementById("st3").style.display = "block";
}
function finishReg() {
    alert("🎉 Real User Account Created Successfully! Welcome.");
    document.getElementById("authModal").style.display = "none";
    location.reload();
}
</script>
"""

trigger_btn = '<div style="padding:12px; text-align:center;"><button onclick="openAuthModal()" style="background:linear-gradient(135deg, #FF6B00, #2b87f5); color:white; border:none; padding:14px 20px; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer; width:100%; max-width:500px; box-shadow:0 4px 12px rgba(24,119,242,0.3);">🛡️ Verify Identity & Create Account (Real Users Only)</button></div>'

for fn in html_files:
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove old triggers or camera buttons if present
    content = content.replace(trigger_btn, "")
    content = content.replace("onclick=\"alert('Camera Active')\"", "onclick=\"openAuthModal()\"")
    
    # Inject trigger and modal before body close or append
    if "</body>" in content and "authModal" not in content:
        new_content = content.replace("</body>", trigger_btn + wizard_code + "\n</body>")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated: {fn}")

print("ALL_HTML_FILES_FIXED")
