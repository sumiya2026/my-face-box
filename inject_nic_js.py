import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # ID Input එක හඳුනාගැනීමට id tag එකක් දීම සහ පරීක්ෂා කිරීමේ JavaScript එකතු කිරීම
    # සාමාන්‍යයෙන් ID අංකය ඇතුළත් කරන input එකට placeholder එකක් තියෙන නිසා එය සොයා වෙනස් කරමු
    if 'placeholder="ID Number"' in content or 'type="text"' in content:
        content = content.replace('placeholder="ID Number"', 'id="nicInput" placeholder="ID Number"')
        
    js_nic_verification = """
    <script>
    // ID Input එකෙන් ඉවතට යන විට (හෝ ටයිප් කර අවසන් වූ විට) ඔටෝ සර්ච් කර පරීක්ෂා කිරීම
    const nicInput = document.getElementById('nicInput');
    if(nicInput) {
        nicInput.addEventListener('blur', function() {
            const nicValue = this.value.trim();
            if(nicValue === "") return;
            
            fetch('/api/verify-nic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nic: nicValue })
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    nicInput.style.borderColor = "green";
                    nicInput.style.backgroundColor = "#e6ffe6";
                    alert(data.message);
                } else {
                    nicInput.style.borderColor = "red";
                    nicInput.style.backgroundColor = "#ffe6e6";
                    alert(data.message);
                    nicInput.value = ""; // ව්‍යාජ එකක් නම් අගය මකා දමයි
                }
            }).catch(err => console.error("Verification Error:", err));
        });
    }
    </script>
    """
    
    if "verify-nic" not in content:
        content = content.replace("</body>", f"{js_nic_verification}\n</body>")
        
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] HTML Signup form updated with Auto-Search Verification!")
else:
    print("[ERROR] index.html not found.")
