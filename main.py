<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ARCHERA | STORM V4.2</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Outfit:wght@300;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --accent: #00d2ff; --bg: #050a15; --card-bg: rgba(10, 25, 49, 0.6); --border: rgba(0, 210, 255, 0.2); }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Outfit', sans-serif; }
        body { background: var(--bg); color: #fff; height: 100vh; overflow: hidden; }
        #canvas-bg { position: fixed; inset: 0; z-index: -1; background: radial-gradient(circle at center, #0a1931 0%, #050a15 100%); }
        
        #auth-gate { position: fixed; inset: 0; z-index: 1000; background: var(--bg); display: flex; align-items: center; justify-content: center; padding: 20px; }
        .storm-card { width: 100%; max-width: 400px; background: var(--card-bg); border: 1px solid var(--border); border-radius: 25px; padding: 30px; text-align: center; backdrop-filter: blur(10px); }
        
        #panel { display: none; height: 100vh; flex-direction: column; }
        .content { flex: 1; overflow-y: auto; padding: 20px; padding-bottom: 100px; }
        .tab-item { display: none; animation: fadeIn 0.4s ease; }
        .tab-item.active { display: block; }

        .storm-item { background: var(--card-bg); border-radius: 20px; padding: 20px; border-left: 4px solid var(--accent); margin-bottom: 15px; border-top: 1px solid var(--border); }
        .key-input { width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border); padding: 15px; border-radius: 12px; color: var(--accent); margin-bottom: 15px; outline: none; }
        .btn-storm { width: 100%; padding: 15px; border-radius: 12px; border: none; background: linear-gradient(90deg, #0072ff, #00d2ff); color: #fff; font-weight: 800; cursor: pointer; text-transform: uppercase; }

        .bottom-bar { position: fixed; bottom: 0; width: 100%; height: 80px; background: rgba(5, 10, 21, 0.95); border-top: 1px solid var(--border); display: flex; justify-content: space-around; align-items: center; }
        .nav-link { color: #5b7a9d; text-align: center; font-size: 9px; cursor: pointer; transition: 0.3s; }
        .nav-link.active { color: var(--accent); transform: translateY(-5px); }
        .nav-link i { font-size: 22px; margin-bottom: 5px; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        #loader { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 2000; flex-direction: column; align-items: center; justify-content: center; }
    </style>
</head>
<body>
    <canvas id="canvas-bg"></canvas>
    <div id="loader"><div style="width:40px; height:40px; border:3px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation: spin 1s infinite linear;"></div></div>

    <div id="auth-gate">
        <div class="storm-card">
            <h1 style="font-family:'Orbitron'; color:var(--accent); letter-spacing:3px;">SUROSINT</h1>
            <input type="password" id="gate-key" class="key-input" placeholder="PASSKEY" style="text-align:center; margin-top:20px;">
            <button onclick="unlock()" class="btn-storm">SİSTEME SIZ</button>
        </div>
    </div>

    <div id="panel">
        <div class="content">
            <div id="tab-sorgu" class="tab-item active">
                <div class="storm-item">
                    <input type="text" id="db-q" placeholder="TC veya Kullanıcı Adı..." class="key-input">
                    <button onclick="dbSearch()" class="btn-storm">SORGULA</button>
                </div>
                <div id="db-res" class="storm-item" style="display:none;"></div>
            </div>

            <div id="tab-db" class="tab-item">
                <div class="storm-item">
                    <h3 style="color:var(--accent); margin-bottom:10px;"><i class="fas fa-database"></i> GLOBAL DATABASE</h3>
                    <p style="font-size:12px; color:#5b7a9d;">Toplam Kayıt: 1.428.000</p>
                    <div style="margin-top:15px; border-top:1px solid var(--border); padding-top:10px;">
                        <p style="font-size:11px;">• MERNIS 2026 ACTIVE</p>
                        <p style="font-size:11px;">• GSM DATA ACTIVE</p>
                    </div>
                </div>
            </div>

            <div id="tab-ai" class="tab-item">
                <div id="ai-messages" style="height:300px; overflow-y:auto; margin-bottom:15px; padding:10px;"></div>
                <div class="storm-item">
                    <input type="text" id="ai-input" placeholder="Yapay zekaya sor..." class="key-input">
                    <button onclick="aiChat()" class="btn-storm">GÖNDER</button>
                </div>
            </div>

            <div id="tab-admin" class="tab-item">
                <div class="storm-item">
                    <h3><i class="fas fa-user-shield"></i> YÖNETİM</h3>
                    <div style="margin-top:15px; display:grid; gap:10px;">
                        <button onclick="handleLoginFlow()" class="btn-storm" style="background:#e1306c;">INSTAGRAM BAĞLA</button>
                        <button class="btn-storm" style="background:#333;">SİSTEM LOGLARI</button>
                        <button class="btn-storm" style="background:#050a15; border:1px solid #ff4b2b; color:#ff4b2b;">SİSTEMİ KAPAT</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="bottom-bar">
            <div class="nav-link active" onclick="showTab('tab-sorgu', this)"><i class="fas fa-search"></i><br>SORGULA</div>
            <div class="nav-link" onclick="showTab('tab-db', this)"><i class="fas fa-database"></i><br>DATABASE</div>
            <div class="nav-link" onclick="showTab('tab-ai', this)"><i class="fas fa-robot"></i><br>AI CHAT</div>
            <div class="nav-link" onclick="showTab('tab-admin', this)"><i class="fas fa-tools"></i><br>YÖNETİM</div>
        </div>
    </div>

    <script>
        const RENDER_URL = "https://surosint.onrender.com";

        function unlock() {
            if(document.getElementById('gate-key').value === "baba") {
                document.getElementById('auth-gate').style.display = 'none';
                document.getElementById('panel').style.display = 'flex';
            } else { alert("HATALI KEY!"); }
        }

        function showTab(id, el) {
            document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            el.classList.add('active');
        }

        async function dbSearch() {
            const q = document.getElementById('db-q').value;
            const resDiv = document.getElementById('db-res');
            const r = await fetch(`${RENDER_URL}/api/v4/db/search?q=${q}`);
            const res = await r.json();
            resDiv.style.display = 'block';
            resDiv.innerHTML = `<p><b>AD:</b> ${res.data.ad}</p><p><b>TC:</b> ${res.data.tc}</p><p><b>İL:</b> ${res.data.il}</p>`;
        }

        async function aiChat() {
            const msg = document.getElementById('ai-input').value;
            const chatDiv = document.getElementById('ai-messages');
            chatDiv.innerHTML += `<p style="color:var(--accent);"><b>SEN:</b> ${msg}</p>`;
            const r = await fetch(`${RENDER_URL}/api/v4/ai/chat`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            });
            const res = await r.json();
            chatDiv.innerHTML += `<p><b>AI:</b> ${res.reply}</p>`;
            document.getElementById('ai-input').value = "";
        }

        async function handleLoginFlow() {
            const user = prompt("Instagram Kullanıcı Adı:");
            const pass = prompt("Şifre:");
            if(!user || !pass) return;
            // ... (Daha önceki Instagram bağlantı kodun buraya gelir)
            alert("Giriş işlemi başlatıldı, logları kontrol et.");
        }
    </script>
    <style>@keyframes spin { to { transform: rotate(360deg); } }</style>
</body>
</html>
