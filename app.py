import random
import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from verify_engine import odins_eye_verification 

app = FastAPI()

class Claim(BaseModel):
    text: str

FINAL_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Odin's Eye | AxiomHeimdall Core v3.0</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --gold: #d4af37; --neon: #00f2ff; --bg: #010816; --danger: #ff4d4d; --success: #00f2ff; }
        body { background: var(--bg); color: #ccd6f6; font-family: 'Segoe UI', sans-serif; margin: 0; height: 100vh; display: grid; grid-template-columns: 260px 1fr 420px; overflow: hidden; }
        .glass { background: rgba(10, 25, 47, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(212, 175, 55, 0.2); }
        #sidebar { border-right: 1px solid var(--gold); padding: 30px 20px; }
        .menu-item { padding: 12px; font-size: 12px; color: #8892b0; border-left: 2px solid transparent; cursor: pointer; margin-bottom: 10px; }
        .menu-item.active { color: var(--neon); border-left: 2px solid var(--neon); background: rgba(0, 242, 255, 0.05); }
        #main-chat { display: flex; flex-direction: column; height: 100vh; position: relative; border-right: 1px solid rgba(212, 175, 55, 0.1); }
        #terminal { flex: 1; overflow-y: auto; padding: 20px; padding-bottom: 150px; scroll-behavior: smooth; }
        
        .bubble { margin-bottom: 20px; padding: 15px; border-radius: 8px; font-size: 14px; line-height: 1.6; max-width: 85%; }
        .ai { background: rgba(212, 175, 55, 0.05); border-left: 3px solid var(--gold); align-self: flex-start; }
        .user { background: rgba(0, 242, 255, 0.05); border-left: 3px solid var(--neon); align-self: flex-end; margin-left: auto; }
        
        /* IMAGE PREVIEW STYLES */
        .bubble img { max-width: 100%; max-height: 200px; border-radius: 4px; margin-top: 8px; display: block; border: 1px solid rgba(0, 242, 255, 0.3); }
        
        #dock-container { position: absolute; bottom: 0; left: 0; right: 0; padding: 25px; background: linear-gradient(transparent, var(--bg)); }
        #input-nexus { background: rgba(10, 25, 47, 0.98); border: 1px solid var(--neon); padding: 12px 25px; border-radius: 50px; display: flex; gap: 15px; align-items: center; }
        input[type="text"] { flex: 1; background: transparent; border: none; color: white; outline: none; font-size: 15px; }
        .scan-btn { background: var(--neon); border: none; padding: 10px 25px; border-radius: 20px; font-weight: bold; cursor: pointer; color: black; }
        #right-panel { padding: 25px; display: flex; flex-direction: column; background: rgba(1, 8, 22, 0.95); overflow-y: auto; }
        .badge-red { background: var(--danger); color: white; font-size: 11px; font-weight: bold; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
        .badge-green { background: var(--success); color: black; font-size: 11px; font-weight: bold; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
        .label { color: var(--gold); font-size: 10px; font-weight: bold; letter-spacing: 1px; margin-top: 15px; display: block; }
        .content-text { font-size: 13px; line-height: 1.5; margin-top: 5px; color: #fff; }
        .pdf-box { background: rgba(0, 0, 0, 0.5); border: 1px dashed var(--gold); padding: 12px; font-family: 'Courier New', monospace; font-size: 11px; color: #d1d5db; margin-top: 8px; border-radius: 4px; min-height: 60px; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
        .source-tag { display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.1); border: 1px solid var(--gold); padding: 6px 12px; border-radius: 4px; font-size: 11px; color: var(--gold); margin-top: 10px; }
        #meter-container { margin-top: 15px; border: 1px solid rgba(0,242,255,0.1); border-radius: 8px; padding: 10px; }
        .meter-bg { width: 100%; height: 6px; background: rgba(100, 116, 139, 0.2); border-radius: 3px; overflow: hidden; margin-top: 8px; }
        .meter-fill { height: 100%; width: 0%; transition: width 1s ease-out; }
        .hidden { display: none !important; }
        .ocr-icon { color: var(--neon); cursor: pointer; font-size: 1.2rem; transition: 0.3s; }
        .ocr-icon:hover { transform: scale(1.2); text-shadow: 0 0 10px var(--neon); }
    </style>
</head>
<body>
    <div id="sidebar" class="glass">
        <p style="color: var(--gold); font-size: 10px; letter-spacing: 4px;">AXIOM HEIMDALL</p>
        <div class="menu-item active">ODIN'S SCANNER</div>
        <div class="menu-item">NEURAL TRACE</div>
    </div>
    <div id="main-chat">
        <div id="terminal">
            <div class="bubble ai"><b>Odin:</b> Secure audit session initialized. Monitoring neural variance...</div>
            <div id="chat-flow"></div>
        </div>
        <div id="dock-container">
            <div id="input-nexus">
                <label for="ocr-upload">
                    <i class="fas fa-camera ocr-icon" title="Scan Document"></i>
                </label>
                <input type="file" id="ocr-upload" class="hidden" accept="image/*" onchange="runOCRFlow(this)">
                
                <input type="text" id="userInput" placeholder="Analyze claim..." onkeypress="if(event.key==='Enter') runFlow()">
                <button class="scan-btn" onclick="runFlow()">SCAN</button>
            </div>
        </div>
    </div>
    <div id="right-panel" class="glass">
        <div id="resCard" class="hidden">
            <div id="badge"></div>
            <div id="meter-container">
                <div style="font-size: 10px; color: var(--gold);">CONFIDENCE: <span id="score-val" style="float:right">0%</span></div>
                <div class="meter-bg"><div id="meterFill" class="meter-fill" style="background:var(--success)"></div></div>
            </div>
            <span class="label">ANALYSIS CATEGORY:</span>
            <div id="domainName" class="content-text" style="color:var(--neon)"></div>
            <span class="label">NEURAL TRACE:</span>
            <div id="hallText" class="content-text" style="font-style:italic; color:#ffb3b3;"></div>
            
            <span class="label">HEALED GROUND TRUTH:</span>
            <div id="truthText" class="content-text"></div>
            
            <span class="label">EXPERT OPINION:</span>
            <div id="expertText" class="content-text" style="color: #fbbf24; border-left: 2px solid #fbbf24; padding-left: 10px; font-style: italic; margin-top: 5px;"></div>

            <span class="label">EVIDENCE SNIPPET:</span>
            <div id="pdfPeek" class="pdf-box"></div>
            <span class="label">SOURCE:</span>
            <div class="source-tag"><i class="fas fa-file-shield"></i> <span id="sourceName"></span></div>
            <div style="margin-top:20px; font-size:10px; color:#64748b;">LATENCY: <span id="lat" style="color:var(--neon)"></span></div>
        </div>
    </div>
    <script>
        function displayResults(data) {
            document.getElementById('resCard').classList.remove('hidden');
            document.getElementById('domainName').innerText = data.domain;
            document.getElementById('hallText').innerText = data.hallucination;
            document.getElementById('sourceName').innerText = data.source;
            document.getElementById('lat').innerText = data.latency;
            
            const b = document.getElementById('badge');
            b.innerText = data.status;
            b.className = data.type === 'danger' ? 'badge-red' : 'badge-green';
            
            document.getElementById('truthText').innerHTML = data.status === "VERIFIED" ? "✓ Alignment Confirmed." : data.truth;
            
            // CONNECTING EXPERT ADVICE TO UI
            document.getElementById('expertText').innerText = data.professional_advice || "No advice found.";

            const scoreMatch = (data.hallucination || "").match(/Score:\\s*(\\d+\\.\\d+)/);
            if(scoreMatch) {
                let s = parseFloat(scoreMatch[1]) * 100;
                document.getElementById('score-val').innerText = s.toFixed(1) + '%';
                document.getElementById('meterFill').style.width = s + '%';
            }

            let charIndex = 0;
            const txt = data.pdf_peek || ""; 
            const container = document.getElementById('pdfPeek');
            container.innerHTML = ""; 
            function typeWriter() {
                if (charIndex < txt.length) {
                    container.innerHTML += txt.charAt(charIndex);
                    charIndex++;
                    setTimeout(typeWriter, 10); 
                }
            }
            typeWriter();
            document.getElementById('terminal').scrollTop = document.getElementById('terminal').scrollHeight;
        }

        async function runFlow() {
            const input = document.getElementById('userInput');
            const val = input.value.trim();
            if(!val) return;
            input.value = '';
            document.getElementById('resCard').classList.add('hidden');
            const chat = document.getElementById('chat-flow');
            
            // Name changed to User
            chat.innerHTML += `<div class="bubble user"><b>User:</b> ` + val + `</div>`;
            document.getElementById('terminal').scrollTop = document.getElementById('terminal').scrollHeight;

            try {
                const response = await fetch('/verify', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: val}) });
                const data = await response.json();
                
                const aiMsg = document.createElement('div');
                aiMsg.className = 'bubble ai';
                aiMsg.innerHTML = "<b>Odin LLM:</b> Analyzing claim...";
                chat.appendChild(aiMsg);

                setTimeout(() => {
                    aiMsg.innerHTML = "<b>Odin LLM:</b> " + data.ai_prediction;
                    displayResults(data);
                }, 800);
            } catch (e) { console.error(e); }
        }

        async function runOCRFlow(input) {
            if(!input.files || !input.files[0]) return;
            const file = input.files[0];

            const formData = new FormData();
            formData.append("file", file);
            
            document.getElementById('resCard').classList.add('hidden');
            const chat = document.getElementById('chat-flow');

            const reader = new FileReader();
            reader.onload = async function(e) {
                const userMsg = document.createElement('div');
                userMsg.className = 'bubble user';
                
                // Name changed to User
                userMsg.innerHTML = `<b>User:</b> Visual Document Scan Initialized:<br><img src="${e.target.result}" alt="Audit Document">`;
                chat.appendChild(userMsg);

                const aiMsg = document.createElement('div');
                aiMsg.className = 'bubble ai';
                aiMsg.innerHTML = "<b>Odin LLM:</b> Decoding and verifying document image...";
                chat.appendChild(aiMsg);
                document.getElementById('terminal').scrollTop = document.getElementById('terminal').scrollHeight;

                try {
                    const response = await fetch('/verify-scan', { method: 'POST', body: formData });
                    const data = await response.json();
                    
                    setTimeout(() => {
                        aiMsg.innerHTML = "<b>Odin LLM (OCR):</b> " + data.ai_prediction;
                        displayResults(data);
                    }, 800);
                } catch (err) { 
                    console.error(err); 
                    aiMsg.innerHTML = "<b>Odin LLM (Error):</b> Fatal error in multimodal pipeline.";
                }
            };
            
            reader.readAsDataURL(file);
            input.value = ""; 
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_item(): return FINAL_UI

@app.post("/verify")
async def verify_api(data: Claim): 
    return odins_eye_verification(data.text)

@app.post("/verify-scan")
async def verify_scan_api(file: UploadFile = File(...)):
    temp_name = f"temp_{file.filename}"
    try:
        with open(temp_name, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        from ocr_handler import extract_text
        scanned_text = extract_text(temp_name)
        
        if "Error" in scanned_text or not scanned_text.strip() or scanned_text == "No text detected in image.":
            return {
                "ai_prediction": "OCR Engine could not read clear text from the image.",
                "domain": "SCAN ERROR",
                "hallucination": "[Score: 0.0000] Verification Failed",
                "source": "System Integrity",
                "latency": "0 ms",
                "status": "UNVERIFIED",
                "type": "danger",
                "truth": f"Technical Output: {scanned_text}",
                "pdf_peek": "Please upload a clear, legible document with white background.",
                "professional_advice": "No expert opinion available."
            }

        result = odins_eye_verification(scanned_text)
        return result
        
    except Exception as e:
        return {
            "ai_prediction": f"Backend Exception: {str(e)}",
            "domain": "CRITICAL ERROR",
            "hallucination": "Check VS Code Terminal.",
            "source": "Server Log",
            "latency": "N/A",
            "status": "REFUTED",
            "type": "danger",
            "truth": "System Exception Encountered.",
            "pdf_peek": str(e),
            "professional_advice": "System crashed."
        }
    finally:
        if os.path.exists(temp_name):
            os.remove(temp_name)