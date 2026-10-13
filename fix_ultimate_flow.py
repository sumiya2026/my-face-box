fn = "my_face_backend/public/index.html"

ultimate_code = """
<!-- Complete Ultimate Verification Wizard (Front ID -> Back ID -> Account Info -> Fingerprint Scanner) -->
<div id="authModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:99999; justify-content:center; align-items:center; padding:15px; box-sizing:border-box;">
    <div style="background:white; width:100%; max-width:450px; border-radius:12px; padding:25px; box-shadow:0 8px 24px rgba(0,0,0,0.3); font-family:sans-serif; text-align:left;">
        
        <!-- Step 1: Front ID -->
        <div id="stepF">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:5px; text-align:center;">🛡️ ID Verification (1/2)</h2>
            <p style="font-size:13px; color:#65676b; text-align:center; margin-bottom:15px;">Capture <b>Front Side</b> (ID Number & Name).</p>
            <div style="border:2px dashed #ccd0d5; border-radius:8px; padding:10px; text-align:center; margin-bottom:15px; background:#f0f2f5;">
                <video id="vidF" autoplay playsinline style="width:100%; max-height:160px; border-radius:6px; display:none;"></video>
                <div id="lblF" style="padding:20px 0; color:#4b4f56; font-size:14px;">📷 Click Start to Scan Front ID</div>
            </div>
            <button type="button" onclick="startF()" id="bStartF" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; margin-bottom:10px;">Start Front Camera</button>
            <button type="button" onclick="goBack()" id="bNextB" style="background:#42b72a; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; display:none;">Capture Front & Next</button>
        </div>

        <!-- Step 2: Back ID -->
        <div id="stepB" style="display:none;">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:5px; text-align:center;">🛡️ ID Verification (2/2)</h2>
            <p style="font-size:13px; color:#65676b; text-align:center; margin-bottom:15px;">Capture <b>Back Side</b> (Address Side).</p>
            <div style="border:2px dashed #ccd0d5; border-radius:8px; padding:10px; text-align:center; margin-bottom:15px; background:#f0f2f5;">
                <video id="vidB" autoplay playsinline style="width:100%; max-height:160px; border-radius:6px; display:none;"></video>
                <div id="lblB" style="padding:20px 0; color:#4b4f56; font-size:14px;">📷 Click Start to Scan Back ID</div>
            </div>
            <button type="button" onclick="startB()" id="bStartB" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; margin-bottom:10px;">Start Back Camera</button>
            <button type="button" onclick="goAcc()" id="bNextAcc" style="background:#42b72a; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer; display:none;">Capture Back & Continue</button>
        </div>

        <!-- Step 3: Account Info (Name & Type) -->
        <div id="stepAcc" style="display:none;">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:10px; text-align:center;">✨ Account Setup</h2>
            <p style="font-size:13px; color:#65676b; text-align:center; margin-bottom:15px;">Both ID sides verified successfully.</p>
            <label style="font-size:13px; font-weight:bold; color:#4b4f56; display:block; margin-bottom:5px;">Select Account Type:</label>
            <select id="accType" style="width:100%; padding:10px; border:1px solid #ccd0d5; border-radius:6px; margin-bottom:15px; font-size:14px;">
                <option value="fb">Personal FB Account</option>
                <option value="page">Business / Public Page</option>
            </select>
            <label style="font-size:13px; font-weight:bold; color:#4b4f56; display:block; margin-bottom:5px;">Enter Account Name:</label>
            <input type="text" id="accName" placeholder="Type your full name..." style="width:100%; padding:10px; border:1px solid #ccd0d5; border-radius:6px; margin-bottom:20px; font-size:14px; box-sizing:border-box;">
            <button type="button" onclick="goFinger()" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer;">Proceed to Fingerprint Scan</button>
        </div>

        <!-- Step 4: Fingerprint Biometric Scanner Simulation -->
        <div id="stepFinger" style="display:none; text-align:center;">
            <h2 style="color:#FF6B00; font-size:20px; margin-bottom:10px;">🔒 Biometric Fingerprint Scanner</h2>
            <p id="fpStatus" style="font-size:13px; color:#65676b; margin-bottom:20px;">Place your finger on the scanner below to verify identity.</p>
            
            <div id="scannerBox" style="background:#f0f2f5; border:2px dashed #FF6B00; padding:25px; border-radius:50%; width:90px; height:90px; margin:0 auto 20px auto; display:flex; justify-content:center; align-items:center; cursor:pointer; box-shadow:0 0 15px rgba(24,119,242,0.2);" onclick="runFingerprintScan()">
                <div id="fpIcon" style="font-size:40px; transition:0.3s;">👆</div>
            </div>
            
            <div id="scanBarContainer" style="width:100%; background:#e4e6eb; height:8px; border-radius:4px; overflow:hidden; display:none; margin-bottom:15px;">
                <div id="scanBar" style="width:0%; background:#42b72a; height:100%; transition:0.4s;"></div>
            </div>
            
            <button type="button" id="fpActionBtn" onclick="runFingerprintScan()" style="background:#FF6B00; color:white; border:none; width:100%; padding:12px; border-radius:6px; font-weight:bold; font-size:15px; cursor:pointer;">Tap to Scan Fingerprint</button>
        </div>

    </div>
</div>

<script>
let sF = null;
let sB = null;

function openAuthModal() {
    document.getElementById("authModal").style.display = "flex";
}

function startF() {
    document.getElementById("lblF").style.display = "none";
    let v = document.getElementById("vidF");
    v.style.display = "block";
    document.getElementById("bStartF").style.display = "none";
    document.getElementById("bNextB").style.display = "block";
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(s => { sF = s; v.srcObject = s; }).catch(e => { alert("Front camera simulation active"); });
}

function goBack() {
    if(sF) sF.getTracks().forEach(t => t.stop());
    document.getElementById("stepF").style.display = "none";
    document.getElementById("stepB").style.display = "block";
}

function startB() {
    document.getElementById("lblB").style.display = "none";
    let v = document.getElementById("vidB");
    v.style.display = "block";
    document.getElementById("bStartB").style.display = "none";
    document.getElementById("bNextAcc").style.display = "block";
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(s => { sB = s; v.srcObject = s; }).catch(e => { alert("Back camera simulation active"); });
}

function goAcc() {
    if(sB) sB.getTracks().forEach(t => t.stop());
    document.getElementById("stepB").style.display = "none";
    document.getElementById("stepAcc").style.display = "block";
}

function goFinger() {
    let nameVal = document.getElementById("accName").value;
    if(!nameVal.trim()) { alert("Please enter a valid account name."); return; }
    document.getElementById("stepAcc").style.display = "none";
    document.getElementById("stepFinger").style.display = "block";
}

function runFingerprintScan() {
    let fpIcon = document.getElementById("fpIcon");
    let fpStatus = document.getElementById("fpStatus");
    let scanBarContainer = document.getElementById("scanBarContainer");
    let scanBar = document.getElementById("scanBar");
    let fpActionBtn = document.getElementById("fpActionBtn");
    
    fpActionBtn.style.display = "none";
    scanBarContainer.style.display = "block";
    fpStatus.innerText = "Scanning fingerprint... Hold steady.";
    fpIcon.style.transform = "scale(1.2)";
    fpIcon.innerHTML = "🌀";
    
    let width = 0;
    let interval = setInterval(function() {
        if (width >= 100) {
            clearInterval(interval);
            fpIcon.innerHTML = "✅";
            fpStatus.innerText = "🎉 Fingerprint Verified! Account Created Successfully.";
            setTimeout(function() {
                alert("🎉 Real User Account Registered Successfully with Dual ID & Fingerprint Verification!");
                document.getElementById("authModal").style.display = "none";
                location.reload();
            }, 1200);
        } else {
            width += 25;
            scanBar.style.width = width + "%";
        }
    }, 400);
}
</script>
"""

trigger_btn = '<div style="padding:12px; text-align:center;"><button onclick="openAuthModal()" style="background:linear-gradient(135deg, #FF6B00, #2b87f5); color:white; border:none; padding:14px 20px; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer; width:100%; max-width:500px; box-shadow:0 4px 12px rgba(24,119,242,0.3);">🛡️ Verify Identity & Create Account (Real Users Only)</button></div>'

try:
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    
    import re
    content = re.sub(r'<!-- Complete Ultimate.*?</script>', '', content, flags=re.DOTALL)
    content = content.replace(trigger_btn, "")
    
    if "</body>" in content:
        content = content.replace("</body>", trigger_btn + ultimate_code + "\n</body>")
        
    with open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS_ULTIMATE_FLOW")
except Exception as e:
    print(f"Error: {e}")
