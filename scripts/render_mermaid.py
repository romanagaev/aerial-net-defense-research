"""Render Mermaid diagrams to PNG using Kroki.io public API."""
import requests
import base64
import zlib
from pathlib import Path

BASE_DIR = Path(r"c:\Users\agaev\Documents\GitHub\llm-generation-design\docs\research\carbon-fiber-net-defense")

DIAGRAMS = {
    "diagram-defense-layers.png": """graph TD
    A[Threat Detection<br/>Radar / EO-IR] --> B{Threat Altitude}
    B -->|0-15m| C[Ground Mesh Barrier<br/>Poles + CF Net]
    B -->|300-1500m| D[TCOM 74K Aerostat<br/>+ CF Net Curtain]
    B -->|1000-3660m| E[TCOM 420K Aerostat<br/>+ CF Net Curtain]
    B -->|3000-6096m| F[Airlander 10<br/>+ CF Net Canopy]
    C --> G[Drone Entangled /<br/>Destroyed]
    D --> G
    E --> H[Missile Fuse Triggered<br/>Premature Detonation]
    F --> H
    G --> I[Zero Cost Per Intercept<br/>Net Repaired if Needed]
    H --> I""",

    "diagram-material-weight.png": """pie title Material Weight Comparison - grams per sqm
    "Carbon Fiber 150g" : 150
    "UHMWPE 300g" : 300
    "Aramid 375g" : 375
    "Stainless Steel 3500g" : 3500""",

    "diagram-lebanon-deployment.png": """graph LR
    subgraph Israel-Lebanon Border - 79-120 km
        A1[Ground CF Mesh<br/>3-15m altitude<br/>3.95M sqm] --> B1[16-24x TCOM 74K<br/>300-500m<br/>Every 5km]
        B1 --> C1[8-12x TCOM 420K<br/>1000-2000m<br/>Every 10km]
        C1 --> D1[2-3x Airlander 10<br/>2000-5000m<br/>Mobile patrol]
    end""",

    "diagram-golan-deployment.png": """graph LR
    subgraph Israel-Syria Golan - 80 km
        A2[UNDOF Zone CF Mesh<br/>5-20m altitude<br/>2.4M sqm] --> B2[10-16x TCOM 74K<br/>500-1500m]
        B2 --> C2[4-6x TCOM 420K<br/>2000-3600m]
        C2 --> D2[1-2x Airlander 10<br/>3000-6000m]
    end""",

    "diagram-jordan-deployment.png": """graph LR
    subgraph Israel-Jordan - 482 km
        A3[Chokepoint CF Mesh<br/>Key corridors] --> B3[28-44x TCOM 74K<br/>300-2000m]
        B3 --> C3[12-20x TCOM 420K<br/>500-2000m]
        C3 --> D3[1x Airlander 10<br/>Eilat sector]
    end""",

    "diagram-roadmap.png": """gantt
    title Development Roadmap
    dateFormat YYYY-MM
    section Phase 1 - POC - 2-5M USD
    CF mesh impact testing       :a1, 2026-08, 3M
    Wind tunnel testing          :a2, 2026-08, 2M
    Aerostat + CF net trial      :a3, 2026-09, 6M
    Net deployment prototype     :a4, 2026-09, 4M
    section Phase 2 - Prototype - 10-20M USD
    Aerostat multi-layer system  :b1, 2027-02, 12M
    C-UAS integration            :b2, 2027-03, 6M
    Live-fire testing            :b3, 2027-06, 6M
    section Phase 3 - Deployment - 50-150M USD
    Airlander 10 + CF net        :c1, 2028-01, 24M
    Formation operations         :c2, 2028-06, 18M
    Hydrogen transition          :c3, 2028-06, 18M""",

    "diagram-curtain-concept.png": """graph TB
    subgraph Net Curtain - Ground to Altitude
        Z1[Aerostat at 300-1000m] --- |CF Net Curtain<br/>Vertical barrier<br/>250-1000m tall| G1[Ground Anchor<br/>Winch + Cable]
        Z2[Aerostat at 300-1000m] --- |CF Net Curtain| G2[Ground Anchor]
        Z3[Aerostat at 300-1000m] --- |CF Net Curtain| G3[Ground Anchor]
        Z1 --- |Horizontal Cable<br/>250-300m span| Z2
        Z2 --- |Horizontal Cable<br/>250-300m span| Z3
    end
    D1[FPV Drone 1-10m] -.->|BLOCKED| G1
    D2[Shahed 50-500m] -.->|BLOCKED| Z1
    D3[Cruise Missile 30-70m] -.->|FUSE TRIGGERED| Z2""",

    "diagram-self-protection.png": """graph TD
    subgraph Airship Self-Protection Layers
        A[Layer 1: Inherent Survivability] --> A1[Helium low pressure - slow leak]
        A --> A2[Hundreds of bullet holes = still flyable]
        A --> A3[Missiles pass through without fusing]
        B[Layer 2: Operational Protection] --> B1[50-200km behind front lines]
        B --> B2[3-6km altitude above MANPADS range]
        B --> B3[Low radar + IR + acoustic signatures]
        C[Layer 3: Active Countermeasures] --> C1[Interceptor drones launched from platform]
        C --> C2[EW suite + radar + IR sensors]
        C --> C3[Decoy and chaff dispensers]
        D[Layer 4: Design Resilience] --> D1[Dispersed engines and fuel lines]
        D --> D2[Self-sealing envelope materials]
        D --> D3[Controlled descent after severe damage]
    end""",
}


def render_mermaid_kroki(diagram_code: str, output_path: Path):
    import time
    compressed = zlib.compress(diagram_code.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    url = f"https://kroki.io/mermaid/png/{encoded}"

    for attempt in range(4):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                output_path.write_bytes(resp.content)
                print(f"  OK: {output_path.name} ({len(resp.content)} bytes)")
                return True
            else:
                print(f"  FAIL: {output_path.name} - HTTP {resp.status_code}")
        except Exception as e:
            print(f"  Retry {attempt+1}/4 for {output_path.name}: {type(e).__name__}")
            time.sleep(3)
    return False


if __name__ == '__main__':
    import time
    print("Rendering Mermaid diagrams via Kroki.io...")
    success = 0
    for name, code in DIAGRAMS.items():
        path = BASE_DIR / name
        if path.exists() and path.stat().st_size > 1000:
            print(f"  SKIP (exists): {name}")
            success += 1
            continue
        if render_mermaid_kroki(code, path):
            success += 1
        time.sleep(2)

    print(f"\nRendered {success}/{len(DIAGRAMS)} diagrams successfully.")
