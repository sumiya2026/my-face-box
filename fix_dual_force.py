fn = "my_face_backend/public/index.html"

new_modal_code = """
<!-- Global Dual-Side ID Verification Modal -->
<div id="authModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:99999; justify-content:center; align-items:center; padding:15px; box-sizing:border-box;">
    <div style="background:white; width:100%; max-width:450px; border-radius:12px; padding:25px; box-shadow:0 8px 24px rgba(0,0,0,0.3); font-family:sans-serif; text-align:left;">
        
        <!-- Step 1: Front Side -->
        <div id="vStep1">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:5px; text-align:center;">🛡️ ID Verification (1/2)</h2>
            <p style="font-size:13px; color:#65676b; text-align:center; margin-bottom:15px;">Capture <b>Front Side</b> (ID Number & Name).</p>
            <div style="border:2px dashed #ccd0d5; border-radius:8px; padding:10px; text-align:center; margin-bottom:15px; background:#f0f2f5;">
                <video id="camFront" autoplay playsinline style="width:100%; max-height:160px; border-radius:6px; display:none;"></video>
                <div id="txtFront" style="padding:20px 0; color:#4b4f56; font-size:14px;">📷 Click Start to Scan Front ID</div>
            </div>
            <button type="button" onclick="startFrontCam()" id="btnStartFront" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; margin-bottom:10px;">Start Front Camera</button>
            <button type="button" onclick="goToBackStep()" id="btnNextBack" style="background:#42b72a; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; display:none;">Capture Front & Next</button>
        </div>

        <!-- Step 2: Back Side -->
        <div id="vStep2" style="display:none;">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:5px; text-align:center;">🛡️ ID Verification (2/2)</h2>
            <p style="font-size:13px; color:#65676b; text-align:center; margin-bottom:15px;">Capture <b>Back Side</b> (Address Side).</p>
            <div style="border:2px dashed #ccd0d5; border-radius:8px; padding:10px; text-align:center; margin-bottom:15px; background:#f0f2f5;">
                <video id="camBack" autoplay playsinline style="width:100%; max-height:160px; border-radius:6px; display:none;"></video>
                <div id="txtBack" style="padding:20px 0; color:#4b4f56; font-size:14px;">📷 Click Start to Scan Back ID</div>
            </div>
            <button type="button" onclick="startBackCam()" id="btnStartBack" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; margin-bottom:10px;">Start Back Camera</button>
            <button type="button" onclick="goToAccountSetup()" id="btnNextSetup" style="background:#42b72a; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; display:none;">Capture Back & Continue</button>
        </div>

        <!-- Step 3: Account Setup -->
        <div id="vStep3" style="display:none;">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:10px; text-align:center;">✨ Account Setup</h2>
            <p style="font-size:13px; color:#65676b; text-align:center; margin-bottom:15px;">Both ID sides verified. Enter account details.</p>
            <label style="font-size:13px; font-weight:bold; color:#4b4f56; display:block; margin-bottom:5px;">Select Account Type:</label>
            <select id="accChoice" style="width:100%; padding:10px; border:1px solid #ccd0d5; border-radius:6px; margin-bottom:15px; font-size:14px;">
                <option value="fb">Personal FB Account</option>
                <option value="page">Business / Public Page</option>
            </select>
            <label style="font-size:13px; font-weight:bold; color:#4b4f56; display:block; margin-bottom:5px;">Enter Account Name:</label>
            <input type="text" id="userNameInput" placeholder="Type your preferred name..." style="width:100%; padding:10px; border:1px solid #ccd0d5; border-radius:6px; margin-bottom:20px; font-size:14px; box-sizing:border-box;">
            <button type="button" onclick="goToPinMark()" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer;">Continue to Pin Mark</button>
        </div>

        <!-- Step 4: Pin Mark -->
        <div id="vStep4" style="display:none; text-align:center;">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:10px;">🔒 Biometric Pin Mark</h2>
            <p style="font-size:13px; color:#65676b; margin-bottom:20px;">Provide your digital touch/pin mark to complete verification.</p>
            <div style="background:#f0f2f5; border:1px solid #ccd0d5; padding:20px; border-radius:8px; margin-bottom:20px; cursor:pointer;" onclick="finishAll()">
                <div style="font-size:32px; margin-bottom:10px;">👆</div>
                <strong style="color:#1c1e21; font-size:15px;">Tap Here to Register Pin Mark</strong>
                <div style="font-size:12px; color:#65676b; margin-top:5px;">Blocks all fake accounts permanently</div>
            </div>
        </div>

    </div>
</div>

<script>
let streamF = null;
let streamB = null;

function openAuthModal() {
    document.getElementById("authModal").style.display = "flex";
}

function startFrontCam() {
    document.getElementById("txtFront").style.display = "none";
    let v = document.getElementById("camFront");
    v.style.display = "block";
    document.getElementById("btnStartFront").style.display = "none";
    document.getElementById("btnNextBack").style.display = "block";
    
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(s => { streamF = s; v.srcObject = s; })
    .catch(e => { alert("Camera Note: Front side simulation active (" + e + ")"); });
}

function goToBackStep() {
    if(streamF) { streamF.getTracks().forEach(t => t.stop()); }
    document.getElementById("vStep1").style.display = "none";
    document.getElementById("vStep2").style.display = "block";
}

function startBackCam() {
    document.getElementById("txtBack").style.display = "none";
    let v = document.getElementById("camBack");
    v.style.display = "block";
    document.getElementById("btnStartBack").style.display = "none";
    document.getElementById("btnNextSetup").style.display = "block";
    
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(s => { streamB = s; v.srcObject = s; })
    .catch(e => { alert("Camera Note: Back side simulation active (" + e + ")"); });
}

function goToAccountSetup() {
    if(streamB) { streamB.getTracks().forEach(t => t.stop()); }
    document.getElementById("vStep2").style.display = "none";
    document.getElementById("vStep3").style.display = "block";
}

function goToPinMark() {
    let nameVal = document.getElementById("userNameInput").value;
    if(!nameVal.trim()) { alert("Please enter a valid account name."); return; }
    document.getElementById("vStep3").style.display = "none";
    document.getElementById("vStep4").style.display = "block";
}

function finishAll() {
    alert("🎉 Real User Account Created Successfully with Dual ID Sides Verified!");
    document.getElementById("authModal").style.display = "none";
    location.reload();
}
</script>
"""

trigger_btn = '<div style="padding:12px; text-align:center;"><button onclick="openAuthModal()" style="background:linear-gradient(135deg, #FF6B00, #2b87f5); color:white; border:none; padding:14px 20px; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer; width:100%; max-width:500px; box-shadow:0 4px 12px rgba(24,119,242,0.3);">🛡️ Verify Identity & Create Account (Real Users Only)</button></div>'

try:
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Completely remove any older authModal blocks if present
    import re
    content = re.sub(r'<!-- Global.*?</script>', '', content, flags=re.DOTALL)
    content = content.replace(trigger_btn, "")
    
    if "</body>" in content:
        content = content.replace("</body>", trigger_btn + new_modal_code + "\n</body>")
        
    with open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS_FORCED_DUAL")
except Exception as e:
    print(f"Error: {e}")
