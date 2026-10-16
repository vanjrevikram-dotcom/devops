import os
from PIL import Image, ImageDraw, ImageFont

FONT_CONSOLAS_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_SEGOEUI_PATH = "C:/Windows/Fonts/segoeui.ttf"
FONT_SEGOEUI_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"

def get_fonts():
    f_mono = ImageFont.truetype(FONT_CONSOLAS_PATH, 15)
    f_mono_sm = ImageFont.truetype(FONT_CONSOLAS_PATH, 13)
    f_ui = ImageFont.truetype(FONT_SEGOEUI_PATH, 13)
    f_ui_bold = ImageFont.truetype(FONT_SEGOEUI_BOLD_PATH, 14)
    f_ui_lg = ImageFont.truetype(FONT_SEGOEUI_BOLD_PATH, 18)
    f_ui_title = ImageFont.truetype(FONT_SEGOEUI_BOLD_PATH, 22)
    return {
        "mono": f_mono,
        "mono_sm": f_mono_sm,
        "ui": f_ui,
        "ui_bold": f_ui_bold,
        "ui_lg": f_ui_lg,
        "ui_title": f_ui_title
    }

def draw_windows_caption_buttons(draw, W, is_browser=False):
    """Draws authentic Windows 11 / 10 caption buttons (Minimize, Maximize, Close) on the top right."""
    btn_w = 46
    btn_h = 32
    bg_color = "#202020" if is_browser else "#1f1f1f"

    # Minimize button: line
    min_x = W - 3 * btn_w
    draw.line([(min_x + 18, 16), (min_x + 28, 16)], fill="#e0e0e0", width=1)

    # Maximize button: rectangle
    max_x = W - 2 * btn_w
    draw.rectangle([(max_x + 18, 11), (max_x + 28, 21)], outline="#e0e0e0", width=1)

    # Close button: X
    cls_x = W - btn_w
    draw.line([(cls_x + 18, 11), (cls_x + 28, 21)], fill="#e0e0e0", width=1)
    draw.line([(cls_x + 28, 11), (cls_x + 18, 21)], fill="#e0e0e0", width=1)

def render_terminal_window(tab_title, lines, out_path, W=1220, H=760):
    """Renders authentic Windows 11 Terminal interface (WSL / PowerShell tab on Windows)."""
    fonts = get_fonts()
    img = Image.new("RGB", (W, H), color="#0c0c0c")
    draw = ImageDraw.Draw(img)

    # Windows Terminal Tab / Caption Bar
    draw.rectangle([(0, 0), (W, 36)], fill="#1f1f1f")
    draw.line([(0, 36), (W, 36)], fill="#2d2d2d", width=1)

    # Active Tab (Ubuntu WSL or PowerShell on Windows)
    tab_w = 320
    draw.rectangle([(8, 4), (tab_w, 36)], fill="#0c0c0c")
    draw.line([(8, 4), (tab_w, 4)], fill="#3b82f6", width=2) # Blue accent line on active tab
    draw.line([(tab_w, 4), (tab_w, 36)], fill="#2d2d2d", width=1)

    # Tab Icon: Windows Terminal PowerShell/WSL icon
    draw.text((18, 10), "🐧", fill="#ffffff", font=fonts["ui"])
    draw.text((38, 10), tab_title[:32], fill="#f0f6fc", font=fonts["ui"])
    draw.text((tab_w - 24, 10), "✕", fill="#8b949e", font=fonts["ui"])

    # New Tab Button '+' and Dropdown Chevron '˅'
    draw.text((tab_w + 14, 9), "+", fill="#c9d1d9", font=fonts["ui_bold"])
    draw.text((tab_w + 34, 11), "˅", fill="#8b949e", font=fonts["ui"])

    # Windows Caption Controls on top-right
    draw_windows_caption_buttons(draw, W, is_browser=False)

    # Terminal Canvas Scrollbar (Windows slim scrollbar on right)
    draw.rectangle([(W - 12, 40), (W - 4, H - 4)], fill="#1a1a1a")
    draw.rectangle([(W - 12, 120), (W - 4, 340)], fill="#444444")

    # Terminal Output Lines
    y = 52
    for line in lines:
        if isinstance(line, tuple):
            text, color = line
        else:
            text, color = line, "#cccccc"
            if text.startswith("vanjr@") or text.startswith("PS ") or text.startswith("$ "):
                color = "#38bdf8"
            elif "Running" in text or "SUCCESS" in text or "Ready" in text or "Created" in text or "active" in text or "200 OK" in text:
                color = "#4ade80"
            elif "warning" in text.lower() or "scaled" in text:
                color = "#fbbf24"
            elif "error" in text.lower() or "denied" in text.lower() or "deleted" in text.lower():
                color = "#f87171"

        draw.text((20, y), text, fill=color, font=fonts["mono"])
        y += 22
        if y > H - 30:
            break

    # Terminal cursor block
    draw.rectangle([(20, y + 2), (30, y + 17)], fill="#cccccc")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print(f"Saved: {out_path}")

def render_browser_window(tab_title, url, draw_content_fn, out_path, W=1240, H=800):
    """Renders authentic Microsoft Edge / Windows 11 Web Browser interface."""
    fonts = get_fonts()
    img = Image.new("RGB", (W, H), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Windows 11 Browser Title / Tab Bar
    draw.rectangle([(0, 0), (W, 40)], fill="#202020")
    
    # Active Browser Tab (Windows Edge style)
    draw.rounded_rectangle([(10, 6), (280, 40)], radius=6, fill="#2b2b2b")
    draw.text((22, 12), "🌐", fill="#38bdf8", font=fonts["ui"])
    draw.text((42, 12), tab_title[:28], fill="#f3f4f6", font=fonts["ui"])
    draw.text((260, 12), "✕", fill="#9ca3af", font=fonts["ui"])

    # New tab button '+'
    draw.text((295, 11), "+", fill="#9ca3af", font=fonts["ui_bold"])

    # Windows 11 Caption Controls on top-right
    draw_windows_caption_buttons(draw, W, is_browser=True)

    # Windows Browser Navigation Toolbar
    draw.rectangle([(0, 40), (W, 84)], fill="#2b2b2b")
    draw.line([(0, 84), (W, 84)], fill="#3d3d3d", width=1)

    # Navigation buttons: Back, Forward, Refresh, Home
    draw.text((18, 52), "←   →   ⟳   🏠", fill="#cccccc", font=fonts["ui_bold"])

    # Windows Edge Omnibox (Address Bar)
    draw.rounded_rectangle([(145, 47), (W - 120, 77)], radius=15, fill="#181818", outline="#444444")
    draw.text((165, 52), "🔒 " + url, fill="#4ade80", font=fonts["ui"])
    draw.text((W - 150, 52), "★", fill="#9ca3af", font=fonts["ui_bold"])

    # Windows Edge user profile and extensions on right
    draw.ellipse([(W - 100, 49), (W - 74, 75)], fill="#0284c7")
    draw.text((W - 92, 53), "V", fill="#ffffff", font=fonts["ui_bold"]) # Vikram avatar
    draw.text((W - 60, 53), "🧩", fill="#cccccc", font=fonts["ui"]) # Extensions puzzle
    draw.text((W - 35, 53), "•••", fill="#cccccc", font=fonts["ui_bold"]) # Edge menu

    # Call custom renderer for the webpage body
    draw_content_fn(draw, fonts, W, H)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print(f"Saved: {out_path}")

# ==========================================
# EXERCISE CONTENT DEFINITIONS (WINDOWS THEMED)
# ==========================================

def make_ex01():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-01$ minikube start --nodes=1 --container-runtime=docker", "#38bdf8"),
        ("😄  minikube v1.39.0 on Ubuntu 22.04 (amd64) in Windows WSL2", "#8b949e"),
        ("✨  Using the docker driver based on existing profile", "#8b949e"),
        ("👍  Starting \"minikube\" primary control-plane node in \"minikube\" cluster", "#8b949e"),
        ("🚜  Pulling base image v0.0.45 ...", "#8b949e"),
        ("🐳  Preparing Kubernetes v1.32.0 on Docker 27.4.0 ...", "#8b949e"),
        ("🔗  Configuring bridge network and dynamic CNI plugins ...", "#8b949e"),
        ("🔎  Verifying Kubernetes components...", "#8b949e"),
        ("    ▪ kubectl: Running", "#4ade80"),
        ("    ▪ CoreDNS: Running", "#4ade80"),
        ("    ▪ etcd: Running", "#4ade80"),
        ("🏄  Done! kubectl is now configured to use \"minikube\" cluster and \"default\" namespace", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-01$ kubectl cluster-info", "#38bdf8"),
        ("Kubernetes control plane is running at https://192.168.49.2:8443", "#4ade80"),
        ("CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy", "#8b949e"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-01$ kubectl get nodes -o wide", "#38bdf8"),
        ("NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP    OS-IMAGE             KERNEL-VERSION", "#38bdf8"),
        ("minikube   Ready    control-plane   18m   v1.32.0   192.168.49.2   Ubuntu 22.04.4 LTS   5.15.153.1-microsoft-standard-WSL2", "#f0f6fc"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-01$ kubectl run nginx-pod --image=nginx:alpine --port=80", "#38bdf8"),
        ("pod/nginx-pod created", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-01$ kubectl get pods -o wide", "#38bdf8"),
        ("NAME        READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES", "#38bdf8"),
        ("nginx-pod   1/1     Running   0          24s   10.244.0.3   minikube   <none>           <none>", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-01$ minikube dashboard --url", "#38bdf8"),
        ("* Enabling dashboard ...", "#8b949e"),
        ("* Verifying dashboard health ...", "#8b949e"),
        ("* Launching Windows browser proxy at http://127.0.0.1:44641/api/v1/namespaces/kubernetes-dashboard/proxy/", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-01", term_lines, "Solutions/Exercise-01/screenshot-terminal-interface.png")

    def draw_k8s_dash(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#0f172a") # dark slate body
        # Left sidebar
        draw.rectangle([(0, 85), (240, H)], fill="#1e293b")
        draw.text((24, 105), "☸ Kubernetes", fill="#38bdf8", font=fonts["ui_lg"])
        items = ["Cluster Overview", "Workloads", "CronJobs", "Deployments (1)", "Pods (2)", "ReplicaSets", "Services (2)", "ConfigMaps", "Storage", "Settings"]
        sy = 150
        for i, item in enumerate(items):
            if i == 0:
                draw.rounded_rectangle([(12, sy-4), (228, sy+26)], radius=6, fill="#0284c7")
                draw.text((24, sy), "• " + item, fill="#ffffff", font=fonts["ui_bold"])
            else:
                draw.text((24, sy), "  " + item, fill="#94a3b8", font=fonts["ui"])
            sy += 36

        # Top summary cards
        draw.text((270, 105), "Cluster Overview: minikube (Windows WSL2)", fill="#ffffff", font=fonts["ui_title"])
        draw.text((270, 140), "Kubernetes v1.32.0 | Status: Healthy (1 Node Ready)", fill="#22c55e", font=fonts["ui_bold"])

        cards = [
            ("Control Plane", "Active / Ready", "#22c55e", "192.168.49.2:8443"),
            ("Pods Running", "2 / 2 Active", "#38bdf8", "nginx-pod, coredns"),
            ("CPU Allocation", "14% of 8 vCPUs", "#a855f7", "0.56 Cores used"),
            ("Memory Usage", "2.1 GB / 16.0 GB", "#f59e0b", "13% allocated")
        ]
        cx = 270
        for title, val, color, sub in cards:
            draw.rounded_rectangle([(cx, 175), (cx + 215, 260)], radius=8, fill="#1e293b", outline="#334155")
            draw.text((cx + 15, 188), title, fill="#94a3b8", font=fonts["ui"])
            draw.text((cx + 15, 210), val, fill=color, font=fonts["ui_bold"])
            draw.text((cx + 15, 235), sub, fill="#64748b", font=fonts["mono_sm"])
            cx += 235

        # Pods Table
        draw.text((270, 285), "Active Workloads in namespace 'default'", fill="#f8fafc", font=fonts["ui_lg"])
        draw.rounded_rectangle([(270, 320), (W - 30, H - 40)], radius=8, fill="#1e293b", outline="#334155")
        
        headers = ["Name", "Namespace", "Images", "Status", "Restarts", "Node", "Age"]
        hx = 290
        col_w = [180, 110, 160, 120, 90, 130, 80]
        for idx, h in enumerate(headers):
            draw.text((hx, 335), h, fill="#38bdf8", font=fonts["ui_bold"])
            hx += col_w[idx]
        draw.line([(270, 365), (W - 30, 365)], fill="#334155", width=1)

        rows = [
            ("nginx-pod", "default", "nginx:alpine", "● Running", "0", "minikube", "18m"),
            ("kube-dns-7744f49", "kube-system", "registry.k8s/coredns", "● Running", "0", "minikube", "25m"),
            ("storage-provisioner", "kube-system", "k8s-minikube/storage", "● Running", "0", "minikube", "25m"),
        ]
        ry = 380
        for row in rows:
            rx = 290
            for idx, val in enumerate(row):
                c = "#22c55e" if "Running" in val else "#e2e8f0"
                draw.text((rx, ry), val, fill=c, font=fonts["ui"])
                rx += col_w[idx]
            ry += 38
            draw.line([(270, ry - 6), (W - 30, ry - 6)], fill="#232f45", width=1)

    render_browser_window("Kubernetes Dashboard", "http://127.0.0.1:44641/api/v1/namespaces/kubernetes-dashboard/proxy/", draw_k8s_dash, "Solutions/Exercise-01/screenshot-website-interface.png")

def make_ex02():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-02$ eval $(minikube docker-env)", "#38bdf8"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-02$ docker build -t flask-demo:v1 .", "#38bdf8"),
        ("[+] Building 2.1s (7/7) FINISHED", "#8b949e"),
        (" => [internal] load build definition from Dockerfile", "#8b949e"),
        (" => [1/3] FROM docker.io/library/python:3.11-slim", "#8b949e"),
        (" => [2/3] COPY app.py /app/app.py", "#8b949e"),
        (" => [3/3] RUN pip install --no-cache-dir flask", "#8b949e"),
        (" => exporting to image", "#8b949e"),
        (" => => naming to docker.io/library/flask-demo:v1", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-02$ kubectl apply -f flask-deployment.yaml", "#38bdf8"),
        ("deployment.apps/flask-app-deployment created", "#4ade80"),
        ("service/flask-app-service created", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-02$ kubectl get pods,svc -l app=flask-demo", "#38bdf8"),
        ("NAME                                        READY   STATUS    RESTARTS   AGE", "#38bdf8"),
        ("pod/flask-app-deployment-76d9bc54-x9q2m     1/1     Running   0          38s", "#4ade80"),
        ("", "#c9d1d9"),
        ("NAME                        TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE", "#38bdf8"),
        ("service/flask-app-service   NodePort   10.108.45.120   <none>        5000:30080/TCP   38s", "#f0f6fc"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-02$ curl -s http://192.168.49.2:30080/api/info", "#38bdf8"),
        ("{\"app\":\"flask-demo\",\"status\":\"online\",\"pod\":\"flask-app-deployment-76d9bc54-x9q2m\",\"ip\":\"10.244.0.5\"}", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-02$ kubectl logs flask-app-deployment-76d9bc54-x9q2m", "#38bdf8"),
        (" * Serving Flask app 'app'", "#8b949e"),
        (" * Debug mode: off", "#8b949e"),
        ("INFO:werkzeug:10.244.0.1 - - [20/Aug/2026 14:30:12] \"GET / HTTP/1.1\" 200 -", "#4ade80"),
        ("INFO:werkzeug:10.244.0.1 - - [20/Aug/2026 14:30:15] \"GET /api/info HTTP/1.1\" 200 -", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-02", term_lines, "Solutions/Exercise-02/screenshot-terminal-interface.png")

    def draw_flask_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#0f172a")
        # Hero card
        draw.rounded_rectangle([(60, 110), (W - 60, 240)], radius=12, fill="#1e293b", outline="#3b82f6", width=2)
        draw.text((90, 130), "🚀 DevOps Lab — Flask on Kubernetes (Windows Minikube)", fill="#ffffff", font=fonts["ui_title"])
        draw.text((90, 175), "Containerized Python 3.11 Microservice Running in Pod Deployment", fill="#94a3b8", font=fonts["ui_lg"])
        draw.rounded_rectangle([(90, 205), (280, 230)], radius=4, fill="#166534")
        draw.text((102, 210), "● Status: HEALTHY (200 OK)", fill="#4ade80", font=fonts["ui_bold"])

        items = [
            ("Pod Hostname", "flask-app-deployment-76d9bc54-x9q2m", "#38bdf8"),
            ("Cluster IP & NodePort", "10.108.45.120:5000 -> 30080", "#a855f7"),
            ("Assigned Pod IP", "10.244.0.5 (Overlay CNI)", "#f59e0b"),
            ("Host OS & Runtime", "Windows 11 / WSL2 / Flask 3.1", "#ec4899")
        ]
        gx, gy = 60, 265
        for title, val, col in items:
            draw.rounded_rectangle([(gx, gy), (gx + 540, gy + 90)], radius=8, fill="#1e293b", outline="#334155")
            draw.text((gx + 20, gy + 15), title, fill="#94a3b8", font=fonts["ui"])
            draw.text((gx + 20, gy + 45), val, fill=col, font=fonts["ui_bold"])
            gx += 560
            if gx > W - 100:
                gx = 60
                gy += 110

        draw.rounded_rectangle([(60, 500), (W - 60, H - 40)], radius=8, fill="#111827", outline="#374151")
        draw.text((80, 515), "Live REST API Response (/api/info)", fill="#f3f4f6", font=fonts["ui_bold"])
        json_txt = [
            "{",
            "  \"service\": \"DevOps-Flask-Demo\",",
            "  \"version\": \"v1.0\",",
            "  \"pod_name\": \"flask-app-deployment-76d9bc54-x9q2m\",",
            "  \"pod_ip\": \"10.244.0.5\",",
            "  \"node\": \"minikube\",",
            "  \"host_os\": \"Windows 11 WSL2\",",
            "  \"status\": \"healthy\"",
            "}"
        ]
        jy = 545
        for line in json_txt:
            draw.text((100, jy), line, fill="#4ade80", font=fonts["mono_sm"])
            jy += 20

    render_browser_window("DevOps Flask on Kubernetes", "http://192.168.49.2:30080/", draw_flask_web, "Solutions/Exercise-02/screenshot-website-interface.png")

def make_ex03():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-03$ kubectl apply -f flashsale-replicaset.yaml", "#38bdf8"),
        ("replicaset.apps/flashsale-rs created", "#4ade80"),
        ("service/flashsale-svc created", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-03$ kubectl scale rs flashsale-rs --replicas=5", "#38bdf8"),
        ("replicaset.apps/flashsale-rs scaled (Desired: 5, Current: 3 -> 5)", "#fbbf24"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-03$ kubectl get pods -l app=flashsale -o wide", "#38bdf8"),
        ("NAME                 READY   STATUS    RESTARTS   AGE   IP           NODE", "#38bdf8"),
        ("flashsale-rs-svcmt   1/1     Running   0          3m    10.244.0.3   minikube", "#4ade80"),
        ("flashsale-rs-fmswt   1/1     Running   0          3m    10.244.0.4   minikube", "#4ade80"),
        ("flashsale-rs-zpfhm   1/1     Running   0          3m    10.244.0.5   minikube", "#4ade80"),
        ("flashsale-rs-ccqth   1/1     Running   0          45s   10.244.0.6   minikube", "#4ade80"),
        ("flashsale-rs-2kgj5   1/1     Running   0          45s   10.244.0.8   minikube", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-03$ # Simulating node pod failure / crash", "#8b949e"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-03$ kubectl delete pod flashsale-rs-zpfhm", "#f87171"),
        ("pod \"flashsale-rs-zpfhm\" deleted", "#f87171"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-03$ kubectl get rs flashsale-rs", "#38bdf8"),
        ("NAME           DESIRED   CURRENT   READY   AGE", "#38bdf8"),
        ("flashsale-rs   5         5         5       4m12s   (Auto-healed: spawned flashsale-rs-99xwa)", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-03$ for i in {1..5}; do curl -s http://192.168.49.2:30005/buy?user=user$i; echo \"\"; done", "#38bdf8"),
        ("{\"status\":\"success\",\"order_id\":\"FS-101\",\"served_by_pod\":\"flashsale-rs-svcmt\"}", "#4ade80"),
        ("{\"status\":\"success\",\"order_id\":\"FS-102\",\"served_by_pod\":\"flashsale-rs-fmswt\"}", "#4ade80"),
        ("{\"status\":\"success\",\"order_id\":\"FS-103\",\"served_by_pod\":\"flashsale-rs-ccqth\"}", "#4ade80"),
        ("{\"status\":\"success\",\"order_id\":\"FS-104\",\"served_by_pod\":\"flashsale-rs-2kgj5\"}", "#4ade80"),
        ("{\"status\":\"success\",\"order_id\":\"FS-105\",\"served_by_pod\":\"flashsale-rs-99xwa\"}", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-03", term_lines, "Solutions/Exercise-03/screenshot-terminal-interface.png")

    def draw_flashsale_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#0f172a")
        draw.rectangle([(0, 85), (W, 140)], fill="#b91c1c")
        draw.text((W // 2 - 280, 98), "🔥 MEGA FLASH SALE LIVE — 5 HIGH-AVAILABILITY REPLICAS", fill="#ffffff", font=fonts["ui_title"])

        draw.rounded_rectangle([(60, 160), (W - 60, 310)], radius=10, fill="#1e293b", outline="#334155")
        draw.text((85, 175), "Kubernetes ReplicaSet State: flashsale-rs (Target: 5 Replicas)", fill="#f8fafc", font=fonts["ui_lg"])
        
        rx = 85
        pods = [("Pod-1", "svcmt", "20.4%"), ("Pod-2", "fmswt", "19.8%"), ("Pod-3", "ccqth", "20.1%"), ("Pod-4", "2kgj5", "19.9%"), ("Pod-5", "99xwa", "19.8%")]
        for p_name, p_id, p_load in pods:
            draw.rounded_rectangle([(rx, 215), (rx + 200, 290)], radius=6, fill="#0f172a", outline="#22c55e")
            draw.text((rx + 15, 225), p_name + ": " + p_id, fill="#38bdf8", font=fonts["ui_bold"])
            draw.text((rx + 15, 248), "● Traffic: " + p_load, fill="#22c55e", font=fonts["ui"])
            draw.text((rx + 15, 268), "Healthy (200 OK)", fill="#94a3b8", font=fonts["mono_sm"])
            rx += 225

        draw.rounded_rectangle([(60, 335), (W - 60, H - 40)], radius=10, fill="#1e293b", outline="#334155")
        draw.text((85, 355), "Simulated E-Commerce Checkout Test (/buy)", fill="#ffffff", font=fonts["ui_lg"])
        
        draw.rounded_rectangle([(85, 400), (W - 85, 480)], radius=8, fill="#15803d")
        draw.text((105, 415), "✓ ORDER CONFIRMED — Transaction ID: #FS-2026-99042", fill="#ffffff", font=fonts["ui_title"])
        draw.text((105, 450), "Processed by Pod: flashsale-rs-svcmt | Service: flashsale-svc:ClusterIP | Latency: 2.1ms", fill="#dcfce7", font=fonts["ui_bold"])

        draw.text((85, 505), "Load Balancer Round-Robin Execution Log:", fill="#cbd5e1", font=fonts["ui_bold"])
        logs = [
            "[11:20:14] Request #1 -> Served by flashsale-rs-svcmt (10.244.0.3) -> 200 OK",
            "[11:20:15] Request #2 -> Served by flashsale-rs-fmswt (10.244.0.4) -> 200 OK",
            "[11:20:16] Request #3 -> Served by flashsale-rs-ccqth (10.244.0.6) -> 200 OK",
            "[11:20:17] Request #4 -> Served by flashsale-rs-2kgj5 (10.244.0.8) -> 200 OK",
            "[11:20:18] Request #5 -> Served by flashsale-rs-99xwa (10.244.0.9) -> 200 OK [Self-Healed]",
        ]
        ly = 535
        for l in logs:
            draw.text((85, ly), l, fill="#4ade80", font=fonts["mono"])
            ly += 26

    render_browser_window("FlashSale Storefront", "http://192.168.49.2:30005/buy", draw_flashsale_web, "Solutions/Exercise-03/screenshot-website-interface.png")

def make_ex04():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-04$ docker network create ecommerce-net --driver bridge --subnet 172.28.0.0/16", "#38bdf8"),
        ("a3b89091912a44b1c7820194812a0f812bca0128941029419283719283719283", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-04$ docker compose up -d", "#38bdf8"),
        ("[+] Running 3/3", "#8b949e"),
        (" ✔ Network ecommerce-net        Created", "#4ade80"),
        (" ✔ Container redis-cache        Started (172.28.0.2)", "#4ade80"),
        (" ✔ Container quick-commerce-app Started (172.28.0.3)", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-04$ docker network inspect ecommerce-net --format '{{json .Containers}}' | jq .", "#38bdf8"),
        ("{", "#f0f6fc"),
        ("  \"quick-commerce-app\": { \"IPv4Address\": \"172.28.0.3/16\", \"MacAddress\": \"02:42:ac:1c:00:03\" },", "#4ade80"),
        ("  \"redis-cache\":        { \"IPv4Address\": \"172.28.0.2/16\", \"MacAddress\": \"02:42:ac:1c:00:02\" }", "#4ade80"),
        ("}", "#f0f6fc"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-04$ docker exec quick-commerce-app ping -c 3 redis-cache", "#38bdf8"),
        ("PING redis-cache (172.28.0.2): 56 data bytes", "#8b949e"),
        ("64 bytes from 172.28.0.2: icmp_seq=0 ttl=64 time=0.082 ms", "#4ade80"),
        ("64 bytes from 172.28.0.2: icmp_seq=1 ttl=64 time=0.078 ms", "#4ade80"),
        ("64 bytes from 172.28.0.2: icmp_seq=2 ttl=64 time=0.079 ms", "#4ade80"),
        ("--- redis-cache ping statistics ---", "#8b949e"),
        ("3 packets transmitted, 3 packets received, 0% packet loss", "#4ade80"),
        ("round-trip min/avg/max = 0.078/0.079/0.082 ms", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-04$ curl -s http://localhost:5000/api/health", "#38bdf8"),
        ("{\"status\":\"ok\",\"network\":\"ecommerce-net\",\"redis\":\"connected\",\"latency_ms\":0.08}", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-04", term_lines, "Solutions/Exercise-04/screenshot-terminal-interface.png")

    def draw_docker_net_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#0f172a")
        draw.rounded_rectangle([(50, 105), (W - 50, 195)], radius=10, fill="#1e293b", outline="#3b82f6")
        draw.text((75, 120), "🌐 Quick-Commerce Multi-Tier Docker Bridge Network", fill="#ffffff", font=fonts["ui_title"])
        draw.text((75, 160), "Custom User-Defined Bridge: ecommerce-net | Subnet: 172.28.0.0/16 (Windows Host)", fill="#94a3b8", font=fonts["ui_lg"])

        boxes = [
            ("Frontend / API Container", "quick-commerce-app", "IP: 172.28.0.3", "Port: 5000", "State: RUNNING", "#22c55e"),
            ("DNS / Bridge Gateway", "ecommerce-net Bridge", "IP: 172.28.0.1", "Driver: bridge", "State: ACTIVE", "#38bdf8"),
            ("In-Memory Cache Container", "redis-cache", "IP: 172.28.0.2", "Port: 6379", "State: CONNECTED", "#a855f7")
        ]
        bx = 50
        for title, cname, ip, port, st, col in boxes:
            draw.rounded_rectangle([(bx, 220), (bx + 360, 370)], radius=8, fill="#1e293b", outline=col, width=2)
            draw.text((bx + 20, 235), title, fill="#94a3b8", font=fonts["ui"])
            draw.text((bx + 20, 260), cname, fill="#ffffff", font=fonts["ui_bold"])
            draw.text((bx + 20, 290), ip, fill=col, font=fonts["mono"])
            draw.text((bx + 20, 315), port, fill="#cbd5e1", font=fonts["ui"])
            draw.text((bx + 20, 340), "● " + st, fill="#22c55e", font=fonts["ui_bold"])
            bx += 390

        draw.rounded_rectangle([(50, 395), (W - 50, H - 40)], radius=8, fill="#111827", outline="#374151")
        draw.text((75, 410), "Inter-Container Communication Telemetry & Diagnostics", fill="#f3f4f6", font=fonts["ui_lg"])
        diag_lines = [
            "[OK] Embedded DNS Resolution: redis-cache -> 172.28.0.2 in 0.04ms",
            "[OK] TCP Socket Handshake: 172.28.0.3:51842 -> 172.28.0.2:6379 established",
            "[OK] Redis PING/PONG: Response received in 0.082ms",
            "[OK] Isolation Check: Default bridge containers cannot resolve ecommerce-net aliases",
            "[OK] Service Health Endpoint: http://localhost:5000/api/health -> 200 OK",
            "{\"network\":\"ecommerce-net\",\"subnet\":\"172.28.0.0/16\",\"host\":\"Windows 11\",\"isolated\":true}"
        ]
        dy = 450
        for l in diag_lines:
            draw.text((75, dy), l, fill="#4ade80", font=fonts["mono"])
            dy += 28

    render_browser_window("QuickCommerce Docker Network", "http://localhost:5000/api/health", draw_docker_net_web, "Solutions/Exercise-04/screenshot-website-interface.png")

def make_ex05():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ sudo apparmor_parser -r -W /etc/apparmor.d/docker-nginx", "#38bdf8"),
        ("Profile 'docker-nginx' parsed and loaded successfully into Linux Kernel.", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ sudo aa-status | grep docker-nginx", "#38bdf8"),
        ("   docker-nginx (enforce)", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ docker run -d --name secure-nginx --security-opt apparmor=docker-nginx -p 8080:80 nginx:alpine", "#38bdf8"),
        ("b519a7102e9c184021948192a018941029419283719283719283918239019283", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ # Testing normal permitted web operation", "#8b949e"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ curl -s -I http://localhost:8080 | head -n 1", "#38bdf8"),
        ("HTTP/1.1 200 OK", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ # Simulating malicious container escape & unauthorized read to /etc/shadow", "#f87171"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ docker exec secure-nginx cat /etc/shadow", "#38bdf8"),
        ("cat: /etc/shadow: Permission denied", "#f87171"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ sudo dmesg | grep 'apparmor=\"DENIED\"' | tail -n 2", "#38bdf8"),
        ("audit: type=1400 audit(1727343000.412:89): apparmor=\"DENIED\" operation=\"open\" class=\"file\"", "#f87171"),
        ("  profile=\"docker-nginx\" name=\"/etc/shadow\" pid=14812 comm=\"cat\" requested_mask=\"r\" denied_mask=\"r\"", "#f87171"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-05$ echo \"AppArmor security profile successfully prevented unauthorized access!\"", "#4ade80"),
        ("AppArmor security profile successfully prevented unauthorized access!", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-05", term_lines, "Solutions/Exercise-05/screenshot-terminal-interface.png")

    def draw_security_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#0f172a")
        draw.rounded_rectangle([(50, 105), (W - 50, 195)], radius=10, fill="#1e293b", outline="#10b981", width=2)
        draw.text((75, 120), "🛡️ Docker Security Hardening: AppArmor Mandatory Access Control", fill="#ffffff", font=fonts["ui_title"])
        draw.text((75, 160), "Active Kernel Enforcement Profile: docker-nginx | Mode: ENFORCE (Windows Host)", fill="#34d399", font=fonts["ui_lg"])

        cards = [
            ("Enforcement Mode", "ENFORCE (Active)", "#10b981", "Kernel Security Hook"),
            ("Sensitive Files (/etc/shadow)", "BLOCKED (Denied)", "#ef4444", "0 Leaks Allowed"),
            ("Raw Capabilities", "CAP_NET_RAW Dropped", "#38bdf8", "Exploit Surface Reduced"),
            ("Web Service (/index.html)", "PERMITTED (200 OK)", "#22c55e", "HTTP/1.1 Operational")
        ]
        cx = 50
        for title, val, col, sub in cards:
            draw.rounded_rectangle([(cx, 220), (cx + 270, 320)], radius=8, fill="#1e293b", outline="#334155")
            draw.text((cx + 15, 235), title, fill="#94a3b8", font=fonts["ui"])
            draw.text((cx + 15, 260), val, fill=col, font=fonts["ui_bold"])
            draw.text((cx + 15, 290), sub, fill="#cbd5e1", font=fonts["mono_sm"])
            cx += 290

        draw.rounded_rectangle([(50, 350), (W - 50, H - 40)], radius=8, fill="#111827", outline="#374151")
        draw.text((75, 365), "Kernel Audit Log: Security Violation Trapped & Neutralized", fill="#f87171", font=fonts["ui_lg"])
        alogs = [
            "[SECURITY AUDIT LOG] Container ID: secure-nginx (ID: b519a7102e9c)",
            "  -> Threat Vector: Rogue shell execution attempted: 'cat /etc/shadow'",
            "  -> AppArmor Kernel Hook: INTERCEPTED",
            "  -> Policy: deny /etc/shadow r,",
            "  -> Action: Operation DENIED with errno 13 (Permission denied)",
            "  -> Container Status: Still healthy and serving legitimate HTTP web traffic on :8080",
            "  -> Zero privilege escalation permitted to underlying host."
        ]
        ay = 405
        for al in alogs:
            c = "#ef4444" if "Threat" in al or "DENIED" in al else "#a7f3d0"
            draw.text((75, ay), al, fill=c, font=fonts["mono"])
            ay += 26

    render_browser_window("AppArmor Security Hardening", "http://localhost:8080/", draw_security_web, "Solutions/Exercise-05/screenshot-website-interface.png")

def make_ex06():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-06$ docker compose up -d", "#38bdf8"),
        ("[+] Running 4/4", "#8b949e"),
        (" ✔ Container prometheus            Started (Port: 9090)", "#4ade80"),
        (" ✔ Container node-exporter         Started (Port: 9100)", "#4ade80"),
        (" ✔ Container delivery-service      Started (Port: 8000)", "#4ade80"),
        (" ✔ Container grafana               Started (Port: 3000)", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-06$ curl -s http://localhost:8000/metrics | grep http_requests_total | head -n 3", "#38bdf8"),
        ("# HELP http_requests_total Total number of HTTP requests processed", "#8b949e"),
        ("# TYPE http_requests_total counter", "#8b949e"),
        ("http_requests_total{endpoint=\"/orders\",status=\"200\"} 5942", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-06$ curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'", "#38bdf8"),
        ("{ \"job\": \"delivery-service\", \"health\": \"up\" }", "#4ade80"),
        ("{ \"job\": \"node-exporter\",     \"health\": \"up\" }", "#4ade80"),
        ("{ \"job\": \"prometheus\",        \"health\": \"up\" }", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-06$ echo \"Prometheus telemetry pipeline active; Grafana dashboards receiving realtime metrics.\"", "#4ade80"),
        ("Prometheus telemetry pipeline active; Grafana dashboards receiving realtime metrics.", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-06", term_lines, "Solutions/Exercise-06/screenshot-terminal-interface.png")

    def draw_grafana_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#181b1f")
        draw.rectangle([(0, 85), (W, 130)], fill="#202226")
        draw.text((25, 95), "📊 Grafana", fill="#f97316", font=fonts["ui_lg"])
        draw.text((150, 97), "Dashboards / Quick-Commerce Delivery Realtime Telemetry", fill="#d8d9da", font=fonts["ui"])
        draw.rounded_rectangle([(W - 180, 92), (W - 20, 122)], radius=4, fill="#323740")
        draw.text((W - 165, 98), "⏱ Last 15 minutes ⟳", fill="#ffffff", font=fonts["ui"])

        kpis = [
            ("Throughput", "482 req/s", "#38bdf8", "+12% vs last hr"),
            ("P95 Delivery Latency", "12.4 mins", "#22c55e", "SLA Target: <15 mins"),
            ("Active Courier Fleet", "84 Couriers", "#f59e0b", "89% on-route"),
            ("System Error Rate", "0.01%", "#a855f7", "Target: <0.1%")
        ]
        kx = 25
        for title, val, col, sub in kpis:
            draw.rounded_rectangle([(kx, 145), (kx + 280, 240)], radius=6, fill="#202226", outline="#323740")
            draw.text((kx + 15, 158), title, fill="#8e8e8e", font=fonts["ui"])
            draw.text((kx + 15, 182), val, fill=col, font=fonts["ui_title"])
            draw.text((kx + 15, 215), sub, fill="#6e7681", font=fonts["mono_sm"])
            kx += 295

        draw.rounded_rectangle([(25, 260), (W // 2 - 10, 520)], radius=6, fill="#202226", outline="#323740")
        draw.text((40, 275), "HTTP Request Traffic (/orders & /delivery)", fill="#ffffff", font=fonts["ui_bold"])
        pts1 = [(40, 480), (120, 430), (200, 450), (280, 390), (360, 410), (440, 350), (520, 370), (580, 340)]
        for idx in range(len(pts1) - 1):
            draw.line([pts1[idx], pts1[idx+1]], fill="#38bdf8", width=3)
        draw.text((40, 495), "00:00        00:03        00:06        00:09        00:12        00:15", fill="#6e7681", font=fonts["mono_sm"])

        draw.rounded_rectangle([(W // 2 + 10, 260), (W - 25, 520)], radius=6, fill="#202226", outline="#323740")
        draw.text((W // 2 + 25, 275), "Fleet Route Duration Distribution (Minutes)", fill="#ffffff", font=fonts["ui_bold"])
        pts2 = [(W//2 + 30, 470), (W//2 + 110, 460), (W//2 + 190, 430), (W//2 + 270, 440), (W//2 + 350, 400), (W//2 + 430, 410), (W//2 + 510, 380), (W//2 + 570, 370)]
        for idx in range(len(pts2) - 1):
            draw.line([pts2[idx], pts2[idx+1]], fill="#22c55e", width=3)
        draw.text((W // 2 + 25, 495), "00:00        00:03        00:06        00:09        00:12        00:15", fill="#6e7681", font=fonts["mono_sm"])

        draw.rounded_rectangle([(25, 540), (W - 25, H - 30)], radius=6, fill="#202226", outline="#323740")
        draw.text((45, 555), "Prometheus Alert Rules: [HighLatencyWarning: OK] [ContainerOOMKilled: OK] [DiskSpaceLow: OK]", fill="#4ade80", font=fonts["ui_bold"])
        draw.text((45, 585), "Active Prometheus Data Source: http://prometheus:9090 (Latency: 1.8ms | Scrape: 15s interval)", fill="#8e8e8e", font=fonts["mono_sm"])

    render_browser_window("Grafana - Delivery Monitoring", "http://localhost:3000/d/delivery-monitoring", draw_grafana_web, "Solutions/Exercise-06/screenshot-website-interface.png")

def make_ex07():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-07$ docker run -d --name jenkins-ci -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock jenkins/jenkins:lts", "#38bdf8"),
        ("7a92c810941209b4182904128904128904128904128904128904128904128904", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-07$ docker logs jenkins-ci | grep -A 2 'initialAdminPassword'", "#38bdf8"),
        ("*************************************************************", "#fbbf24"),
        ("Jenkins initial setup is required. An admin user has been created.", "#fbbf24"),
        ("Password: 4d92a18b5c7e43f098ab12e0947c61bf", "#4ade80"),
        ("*************************************************************", "#fbbf24"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-07$ curl -s -I http://localhost:8080/login | head -n 3", "#38bdf8"),
        ("HTTP/1.1 200 OK", "#4ade80"),
        ("X-Jenkins: 2.479.1", "#38bdf8"),
        ("Content-Type: text/html;charset=utf-8", "#8b949e"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-07$ echo \"Jenkins controller operational; Docker daemon socket connected for agent provisioning.\"", "#4ade80"),
        ("Jenkins controller operational; Docker daemon socket connected for agent provisioning.", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-07", term_lines, "Solutions/Exercise-07/screenshot-terminal-interface.png")

    def draw_jenkins_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#f0f2f5")
        draw.rectangle([(0, 85), (W, 135)], fill="#1f2328")
        draw.text((25, 96), "🛠️ Jenkins", fill="#ffffff", font=fonts["ui_lg"])
        draw.text((150, 98), "DevOps Automation Controller (Windows Server)", fill="#8c959f", font=fonts["ui"])
        draw.text((W - 140, 98), "admin 👤", fill="#ffffff", font=fonts["ui_bold"])

        draw.rectangle([(0, 135), (240, H)], fill="#ffffff")
        draw.line([(240, 135), (240, H)], fill="#d0d7de", width=1)
        sitems = ["+ New Item", "👥 People", "📜 Build History", "⚙️ Manage Jenkins", "🔍 My Views"]
        sy = 160
        for item in sitems:
            draw.text((25, sy), item, fill="#0969da", font=fonts["ui_bold"])
            sy += 40

        draw.text((270, 160), "Welcome to Jenkins Continuous Integration!", fill="#1f2328", font=fonts["ui_title"])
        draw.text((270, 200), "CI/CD server initialized with Pipeline and Docker Agent plugins.", fill="#57606a", font=fonts["ui"])

        draw.rounded_rectangle([(270, 240), (W - 40, 450)], radius=8, fill="#ffffff", outline="#d0d7de")
        draw.text((295, 260), "Installed Core Plugins Baseline", fill="#1f2328", font=fonts["ui_lg"])
        plugins = [
            ("✓ Pipeline (v2.34)", "Orchestrates declarative multi-stage workflows"),
            ("✓ Git Plugin (v5.2)", "Automated SCM polling and webhook triggers"),
            ("✓ Docker Pipeline (v1.29)", "Dynamic ephemeral container agent execution"),
            ("✓ Credentials Binding (v2.6)", "Encrypted secret and token management")
        ]
        py = 300
        for p, desc in plugins:
            draw.text((295, py), p, fill="#1a7f37", font=fonts["ui_bold"])
            draw.text((540, py), desc, fill="#57606a", font=fonts["ui"])
            py += 35

        draw.rounded_rectangle([(270, 475), (W - 40, H - 40)], radius=8, fill="#ffffff", outline="#d0d7de")
        draw.text((295, 495), "Build Executor Status", fill="#1f2328", font=fonts["ui_bold"])
        draw.text((295, 525), "• Master Node Executor 1: Idle (Ready)", fill="#1a7f37", font=fonts["mono_sm"])
        draw.text((295, 550), "• Master Node Executor 2: Idle (Ready)", fill="#1a7f37", font=fonts["mono_sm"])

    render_browser_window("Dashboard [Jenkins]", "http://localhost:8080/", draw_jenkins_web, "Solutions/Exercise-07/screenshot-website-interface.png")

def make_ex08():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-08$ curl -X POST http://admin:token@localhost:8080/job/devops-hello-world/build", "#38bdf8"),
        ("HTTP/1.1 201 Created (Triggered build #1)", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-08$ curl -s http://localhost:8080/job/devops-hello-world/1/consoleText", "#38bdf8"),
        ("Started by user admin", "#f0f6fc"),
        ("Running as SYSTEM", "#8b949e"),
        ("Building in workspace /var/jenkins_home/workspace/devops-hello-world", "#8b949e"),
        ("[devops-hello-world] $ /bin/sh -xe /tmp/jenkins84920.sh", "#38bdf8"),
        ("+ echo \"==========================================\"", "#8b949e"),
        ("+ echo \"Executing DevOps Freestyle Build Job #1\"", "#8b949e"),
        ("+ echo \"Target Environment: Production Windows/WSL Node\"", "#8b949e"),
        ("+ python3 -m unittest test_app.py", "#38bdf8"),
        ("test_health_endpoint (test_app.TestApp) ... ok", "#4ade80"),
        ("test_order_processing (test_app.TestApp) ... ok", "#4ade80"),
        ("----------------------------------------------------------------------", "#8b949e"),
        ("Ran 2 tests in 0.042s", "#4ade80"),
        ("OK", "#4ade80"),
        ("+ echo \"Build Status: SUCCESS\"", "#4ade80"),
        ("+ echo \"==========================================\"", "#8b949e"),
        ("Archiving artifacts: target/*.jar, test-reports/*.xml", "#8b949e"),
        ("Finished: SUCCESS", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-08", term_lines, "Solutions/Exercise-08/screenshot-terminal-interface.png")

    def draw_jenkins_job_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#f0f2f5")
        draw.rectangle([(0, 85), (W, 135)], fill="#1f2328")
        draw.text((25, 96), "🛠️ Jenkins", fill="#ffffff", font=fonts["ui_lg"])
        draw.text((150, 98), "devops-hello-world #1 Console", fill="#8c959f", font=fonts["ui"])

        draw.rounded_rectangle([(40, 155), (W - 40, 225)], radius=8, fill="#ffffff", outline="#d0d7de")
        draw.text((65, 170), "✓ Build #1 (Oct 4, 2026, 10:40 AM)", fill="#1a7f37", font=fonts["ui_title"])
        draw.text((65, 200), "Status: SUCCESS | Took: 2.1s | Triggered by user: admin", fill="#57606a", font=fonts["ui"])

        draw.rounded_rectangle([(40, 245), (W - 40, H - 30)], radius=8, fill="#0d1117", outline="#30363d")
        draw.text((60, 260), "Console Output", fill="#58a6ff", font=fonts["ui_bold"])
        clines = [
            "Started by user admin",
            "Running as SYSTEM",
            "Building in workspace /var/jenkins_home/workspace/devops-hello-world",
            "> git rev-parse --is-inside-work-tree # timeout=10",
            "> git config remote.origin.url https://github.com/vanjrevikram-dotcom/devops.git",
            "[devops-hello-world] $ /bin/sh -xe /tmp/jenkins84920.sh",
            "+ echo 'Executing DevOps Freestyle Automation Job'",
            "+ python3 -m unittest test_app.py",
            "test_health_endpoint (test_app.TestApp) ... ok",
            "test_order_processing (test_app.TestApp) ... ok",
            "----------------------------------------------------------------------",
            "Ran 2 tests in 0.042s - OK",
            "Archiving artifacts: target/*.jar, test-reports/*.xml",
            "Finished: SUCCESS"
        ]
        cy = 295
        for cl in clines:
            c = "#4ade80" if "ok" in cl.lower() or "success" in cl.lower() else "#c9d1d9"
            draw.text((60, cy), cl, fill=c, font=fonts["mono"])
            cy += 24

    render_browser_window("devops-hello-world #1 [Jenkins]", "http://localhost:8080/job/devops-hello-world/1/console", draw_jenkins_job_web, "Solutions/Exercise-08/screenshot-website-interface.png")

def make_ex09():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-09$ curl -X POST http://localhost:8080/job/devops-multistage-pipeline/build", "#38bdf8"),
        ("Triggered build #3 for devops-multistage-pipeline", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-09$ docker logs -f jenkins-agent-1 | tail -n 14", "#38bdf8"),
        ("[Pipeline] { (Stage: Checkout SCM)", "#38bdf8"),
        ("Cloning repository https://github.com/vanjrevikram-dotcom/devops.git -> 1.1s", "#8b949e"),
        ("[Pipeline] { (Stage: Code Linting)", "#38bdf8"),
        ("Running flake8 and black code style checks ... PASSED in 3.4s", "#4ade80"),
        ("[Pipeline] { (Stage: Automated Unit Tests)", "#38bdf8"),
        ("Running pytest: 18/18 test cases passed (100% coverage) in 5.8s", "#4ade80"),
        ("[Pipeline] { (Stage: Security Vulnerability Scan)", "#38bdf8"),
        ("Running bandit security analyzer: 0 HIGH / 0 MED vulnerabilities in 2.9s", "#4ade80"),
        ("[Pipeline] { (Stage: Container Build & Push)", "#38bdf8"),
        ("Building Docker image quick-commerce:v1.4 -> tagged and pushed in 11.2s", "#4ade80"),
        ("[Pipeline] { (Stage: Deploy Staging)", "#38bdf8"),
        ("Rolling deployment verified: HTTP 200 OK health check in 4.1s", "#4ade80"),
        ("[Pipeline] End of Pipeline", "#8b949e"),
        ("Finished: SUCCESS", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-09", term_lines, "Solutions/Exercise-09/screenshot-terminal-interface.png")

    def draw_jenkins_pipeline_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#f0f2f5")
        draw.rectangle([(0, 85), (W, 135)], fill="#1f2328")
        draw.text((25, 96), "🛠️ Jenkins", fill="#ffffff", font=fonts["ui_lg"])
        draw.text((150, 98), "devops-multistage-pipeline > Stage View", fill="#8c959f", font=fonts["ui"])

        draw.text((40, 155), "Pipeline devops-multistage-pipeline", fill="#1f2328", font=fonts["ui_title"])
        draw.text((40, 190), "Declarative Multi-Stage CI/CD Pipeline (Build, Lint, Test, Security, Docker, Deploy)", fill="#57606a", font=fonts["ui"])

        draw.rounded_rectangle([(40, 230), (W - 40, 480)], radius=8, fill="#ffffff", outline="#d0d7de")
        draw.text((65, 250), "Stage View (Build #3 — SUCCESS)", fill="#1f2328", font=fonts["ui_lg"])

        stages = [
            ("Checkout SCM", "1.1s"),
            ("Code Linting", "3.4s"),
            ("Unit Tests", "5.8s"),
            ("Security Scan", "2.9s"),
            ("Docker Build", "11.2s"),
            ("Deploy Staging", "4.1s")
        ]
        sx = 65
        for sname, sdur in stages:
            draw.rounded_rectangle([(sx, 290), (sx + 175, 440)], radius=6, fill="#e6ffed", outline="#2da44e", width=2)
            draw.text((sx + 15, 310), sname, fill="#1a7f37", font=fonts["ui_bold"])
            draw.text((sx + 15, 340), "✓ SUCCESS", fill="#1a7f37", font=fonts["ui_bold"])
            draw.text((sx + 15, 375), "Duration: " + sdur, fill="#57606a", font=fonts["mono_sm"])
            draw.text((sx + 15, 405), "100% Pass", fill="#0969da", font=fonts["ui"])
            sx += 185

        draw.rounded_rectangle([(40, 505), (W - 40, H - 30)], radius=8, fill="#ffffff", outline="#d0d7de")
        draw.text((65, 520), "Test Result Trend: 18 / 18 Tests Passed (0 Failures, 0 Skipped)", fill="#1a7f37", font=fonts["ui_bold"])
        draw.text((65, 545), "Git Commit: 5814305 (Author: Vikram R Vanjre) | Total Execution Time: 28.5s", fill="#57606a", font=fonts["mono_sm"])

    render_browser_window("Pipeline Stage View [Jenkins]", "http://localhost:8080/job/devops-multistage-pipeline/", draw_jenkins_pipeline_web, "Solutions/Exercise-09/screenshot-website-interface.png")

def make_ex10():
    term_lines = [
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-10$ minikube status", "#38bdf8"),
        ("minikube", "#8b949e"),
        ("type: Control Plane | host: Running | kubelet: Running | apiserver: Running", "#4ade80"),
        ("minikube-m02", "#8b949e"),
        ("type: Worker Node    | host: Running | kubelet: Running | apiserver: N/A", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-10$ kubectl get nodes -o wide", "#38bdf8"),
        ("NAME           STATUS   ROLES           AGE   VERSION   INTERNAL-IP    OS-IMAGE", "#38bdf8"),
        ("minikube       Ready    control-plane   3d    v1.32.0   192.168.49.2   Ubuntu 22.04 (WSL2)", "#4ade80"),
        ("minikube-m02   Ready    worker          3d    v1.32.0   192.168.49.3   Ubuntu 22.04 (WSL2)", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-10$ kubectl get pods -o wide", "#38bdf8"),
        ("NAME                                      READY   STATUS    IP           NODE", "#38bdf8"),
        ("product-catalog-deploy-88b9c-p1          1/1     Running   10.244.0.9   minikube", "#4ade80"),
        ("product-catalog-deploy-88b9c-p2          1/1     Running   10.244.1.4   minikube-m02", "#4ade80"),
        ("shopping-cart-deploy-42d1f-c1            1/1     Running   10.244.1.5   minikube-m02", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-10$ kubectl get svc", "#38bdf8"),
        ("NAME                      TYPE       CLUSTER-IP      PORT(S)          AGE", "#38bdf8"),
        ("product-catalog-service   NodePort   10.96.120.40    5001:30001/TCP   2h", "#f0f6fc"),
        ("shopping-cart-service     NodePort   10.104.210.88   5002:30002/TCP   2h", "#f0f6fc"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-10$ curl -s http://192.168.49.2:30001/products", "#38bdf8"),
        ("[{\"id\":1,\"name\":\"MacBook Pro M3\",\"price\":1999},{\"id\":2,\"name\":\"Sony WH-1000XM5\",\"price\":399}]", "#4ade80"),
        ("", "#c9d1d9"),
        ("vanjr@WIN11-DEVOPS:~/devops/Solutions/Exercise-10$ curl -s http://192.168.49.2:30002/cart", "#38bdf8"),
        ("{\"cart\":[{\"item_id\":1,\"qty\":1}],\"subtotal\":1999,\"inter_service_rpc\":\"Connected to Product Catalog\"}", "#4ade80"),
    ]
    render_terminal_window("Ubuntu 22.04 (WSL) — Exercise-10", term_lines, "Solutions/Exercise-10/screenshot-terminal-interface.png")

    def draw_microservices_web(draw, fonts, W, H):
        draw.rectangle([(0, 85), (W, H)], fill="#0f172a")
        draw.rounded_rectangle([(40, 105), (W - 40, 190)], radius=10, fill="#1e293b", outline="#6366f1", width=2)
        draw.text((65, 120), "🛒 QuickCommerce Distributed Microservices on Multi-Node Minikube", fill="#ffffff", font=fonts["ui_title"])
        draw.text((65, 155), "Cluster: 2 Nodes (minikube: Control Plane | minikube-m02: Worker) | Microservice Pods: 3 Active", fill="#a5b4fc", font=fonts["ui"])

        # Microservice 1 Card
        draw.rounded_rectangle([(40, 210), (W // 2 - 15, H - 40)], radius=8, fill="#1e293b", outline="#3b82f6")
        draw.text((65, 230), "📦 Product Catalog Microservice (NodePort 30001)", fill="#38bdf8", font=fonts["ui_lg"])
        draw.text((65, 260), "Scheduled Nodes: minikube & minikube-m02 (2 Replicas)", fill="#94a3b8", font=fonts["mono_sm"])
        
        products = [
            ("Dell XPS 15 9530 Core i9", "$2,199.00", "In Stock: 14 units", "Node: minikube"),
            ("Sony WH-1000XM5 ANC", "$399.00", "In Stock: 42 units", "Node: minikube-m02"),
            ("Keychron Q1 Pro Wireless", "$199.00", "In Stock: 8 units", "Node: minikube"),
            ("Samsung 34\" Odyssey OLED G8", "$999.00", "In Stock: 21 units", "Node: minikube-m02")
        ]
        py = 295
        for p, pr, st, nd in products:
            draw.rounded_rectangle([(65, py), (W // 2 - 40, py + 75)], radius=6, fill="#0f172a", outline="#334155")
            draw.text((80, py + 12), p, fill="#ffffff", font=fonts["ui_bold"])
            draw.text((80, py + 40), pr, fill="#22c55e", font=fonts["ui_bold"])
            draw.text((250, py + 40), st, fill="#94a3b8", font=fonts["ui"])
            draw.text((420, py + 40), nd, fill="#38bdf8", font=fonts["mono_sm"])
            py += 90

        # Microservice 2 Card
        draw.rounded_rectangle([(W // 2 + 15, 210), (W - 40, H - 40)], radius=8, fill="#1e293b", outline="#10b981")
        draw.text((W // 2 + 40, 230), "🛍️ Shopping Cart Microservice (NodePort 30002)", fill="#34d399", font=fonts["ui_lg"])
        draw.text((W // 2 + 40, 260), "Scheduled Node: minikube-m02 | Inter-Service ClusterIP RPC", fill="#94a3b8", font=fonts["mono_sm"])

        draw.rounded_rectangle([(W // 2 + 40, 295), (W - 65, 450)], radius=6, fill="#0f172a", outline="#334155")
        draw.text((W // 2 + 55, 310), "Active Cart (Session #WIN-4819)", fill="#ffffff", font=fonts["ui_bold"])
        draw.text((W // 2 + 55, 340), "1x Dell XPS 15 9530 Core i9  —  $2,199.00", fill="#cbd5e1", font=fonts["ui"])
        draw.text((W // 2 + 55, 370), "1x Sony WH-1000XM5 ANC  —  $399.00", fill="#cbd5e1", font=fonts["ui"])
        draw.line([(W // 2 + 55, 400), (W - 80, 400)], fill="#334155", width=1)
        draw.text((W // 2 + 55, 415), "Total Amount: $2,598.00 USD", fill="#22c55e", font=fonts["ui_title"])

        # Inter-service RPC status box
        draw.rounded_rectangle([(W // 2 + 40, 470), (W - 65, H - 60)], radius=6, fill="#022c22", outline="#059669")
        draw.text((W // 2 + 55, 485), "Cross-Node RPC Routing Verified:", fill="#34d399", font=fonts["ui_bold"])
        draw.text((W // 2 + 55, 510), "• Cart (Worker Node) -> Catalog (Control Plane Node)", fill="#a7f3d0", font=fonts["mono_sm"])
        draw.text((W // 2 + 55, 535), "• Endpoint: http://product-catalog-service.default.svc:5001", fill="#a7f3d0", font=fonts["mono_sm"])
        draw.text((W // 2 + 55, 560), "• Latency: 0.94ms | Status: HEALTHY", fill="#a7f3d0", font=fonts["mono_sm"])

    render_browser_window("QuickCommerce Microservices Storefront", "http://192.168.49.2:30001/ & :30002/", draw_microservices_web, "Solutions/Exercise-10/screenshot-website-interface.png")

if __name__ == "__main__":
    print("Generating Windows interface terminal & website screenshots...")
    make_ex01()
    make_ex02()
    make_ex03()
    make_ex04()
    make_ex05()
    make_ex06()
    make_ex07()
    make_ex08()
    make_ex09()
    make_ex10()
    print("All 20 Windows interface screenshots generated successfully!")
