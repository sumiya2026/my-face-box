window.FaceBoxIcons = window.FaceBoxIcons || {};
window.FaceBoxIcons.messenger = {
  icon: "💬",
  label: "Messenger",
  render: function(container) {
    container.innerHTML = `
      <div style="padding:15px;color:#fff;background:#0f0f0f;height:100%;font-family:sans-serif;">
        <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #222;padding-bottom:10px;">
          <h3>💬 Messenger</h3>
          <span onclick="document.getElementById('plugin-container').style.display='none'" style="font-size:22px;cursor:pointer;">✕</span>
        </div>
        <p style="font-size:12px;color:#888;">මේක වෙනම File එකෙන් ආපු Logic එක! 🚀</p>
        <div id="chatList" style="height:300px;overflow-y:auto;background:#111;padding:10px;border-radius:10px;margin-top:10px;"></div>
        <div style="display:flex;gap:8px;margin-top:10px;">
          <input id="msgInput" placeholder="Aa" style="flex:1;padding:11px 15px;border-radius:20px;border:none;background:#222;color:#fff;outline:none;">
          <button onclick="sendMsg()" style="background:#0084ff;border:none;border-radius:50%;width:38px;height:38px;color:#fff;cursor:pointer;">➤</button>
        </div>
      </div>
    `;
    container.style.display = 'block';
    window.sendMsg = function(){
      const input = document.getElementById('msgInput');
      const list = document.getElementById('chatList');
      if(!input.value.trim()) return;
      const d = document.createElement('div');
      d.style = "background:#0084ff;padding:8px 12px;border-radius:15px;margin:5px 0;margin-left:auto;max-width:70%;text-align:right;";
      d.innerText = input.value;
      list.appendChild(d);
      input.value='';
      list.scrollTop = list.scrollHeight;
    };
  }
};
