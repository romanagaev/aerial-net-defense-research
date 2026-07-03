"""Render Mermaid replacements for ASCII diagrams."""
import requests
import base64
import zlib
import time
from pathlib import Path

BASE_DIR = Path(r"c:\Users\agaev\Documents\GitHub\aerial-net-defense-research\images\diagrams")

DIAGRAMS = {
    "diagram-feasibility-framework.png": """graph TD
    subgraph FEASIBILITY ASSESSMENT
        direction TB
        subgraph Technical
            P[Physics]
            MA[Materials]
            PL[Platforms]
            EN[Engineering]
        end
        subgraph Economic
            MC[Material Cost]
            PC[Platform Cost]
            OP[Operations]
            CO[Comparison]
        end
        subgraph Operational
            DT[Deployment Time]
            MT[Maintainability]
            SV[Survivability]
            SC[Scalability]
        end
    end
    Technical --> CS[CASE STUDY APPLICATION]
    Economic --> CS
    Operational --> CS
    CS --> IL[Israel-Lebanon]
    CS --> IS[Israel-Syria]
    CS --> IJ[Israel-Jordan]
    IL --> DR[DEVELOPMENT ROADMAP]
    IS --> DR
    IJ --> DR
    DR --> P1[Phase 1: 0-6 months]
    DR --> P2[Phase 2: 6-18 months]
    DR --> P3[Phase 3: 18-36 months]""",

    "diagram-system-architecture.png": """graph TD
    A10[AIRLANDER 10<br/>Strategic<br/>Alt: 3-6 km<br/>Coverage: 6 ha] -->|CF Net| A420_1[AEROSTAT 420K<br/>Alt: 1-3 km]
    A10 -->|CF Net| A420_2[AEROSTAT 420K<br/>Alt: 1-3 km]
    A10 -->|CF Net| A420_3[AEROSTAT 420K<br/>Alt: 1-3 km]
    A420_1 -->|CF Net| A74_1[AEROSTAT 74K<br/>Alt: 300m]
    A420_2 -->|CF Net| A74_2[AEROSTAT 74K<br/>Alt: 500m]
    A420_3 -->|CF Net| A74_3[AEROSTAT 74K<br/>Alt: 300m]
    A74_1 -->|CF Net| GL[GROUND LEVEL<br/>Poles + CF Mesh 3-15m]
    A74_2 -->|CF Net| GL
    A74_3 -->|CF Net| GL
    GL --> PZ[PROTECTED ZONE]""",

    "diagram-altitude-zones.png": """graph LR
    subgraph ZONE D: Strategic - Airlander 10
        D1[3000-6000m<br/>Shaheds high mode<br/>Recon drones]
    end
    subgraph ZONE C: High - TCOM 420K
        C1[1500-4600m<br/>Jet drones<br/>Shaheds variable]
    end
    subgraph ZONE B: Mid - TCOM 74K
        B1[200-1500m<br/>Shaheds low mode<br/>Kalibr approach]
    end
    subgraph ZONE A: Ground - Poles + Mesh
        A1[0-200m<br/>FPV drones 1-10m<br/>Kh-101 terrain-following<br/>Cruise missiles 30-70m]
    end
    D1 --> C1 --> B1 --> A1""",
}

def render(code, path):
    compressed = zlib.compress(code.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    url = f"https://kroki.io/mermaid/png/{encoded}"
    for attempt in range(4):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                path.write_bytes(resp.content)
                print(f"OK: {path.name} ({len(resp.content)} bytes)")
                return True
        except Exception as e:
            print(f"Retry {attempt+1}: {type(e).__name__}")
            time.sleep(3)
    return False

if __name__ == '__main__':
    for name, code in DIAGRAMS.items():
        path = BASE_DIR / name
        render(code, path)
        time.sleep(2)
