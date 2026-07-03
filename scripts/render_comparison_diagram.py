"""Render the Iron Beam comparison Mermaid diagram to PNG."""
import requests
import base64
import zlib
import time
from pathlib import Path

BASE_DIR = Path(r"c:\Users\agaev\Documents\GitHub\aerial-net-defense-research\images\diagrams")

DIAGRAM = """graph TD
    subgraph Active Defense Systems
        IB[Iron Beam 100kW Laser<br/>Cost: $3.50/shot<br/>System: $50-100M<br/>FAILS in fog/rain<br/>1 target per 3-5 sec]
        TR[Trophy APS<br/>Vehicle-only<br/>Close range 30m<br/>1 target at a time<br/>Cannot handle swarms]
        LB[Lite Beam 10kW<br/>Range: 2km<br/>FAILS in fog/rain<br/>Mobile units]
    end
    subgraph Passive CF Net Barrier
        NET[CF Net Curtain<br/>Cost: $0/intercept<br/>ALL weather<br/>ALL targets simultaneously<br/>24/7 passive<br/>No power needed]
    end
    IB -->|Fog/Rain/Dust| MISS1[Threats Pass Through]
    IB -->|Swarm 50+ drones| MISS2[Overwhelmed]
    TR -->|Beyond 30m| MISS3[Out of Range]
    LB -->|Fog/Rain| MISS4[Degraded]
    MISS1 --> NET
    MISS2 --> NET
    MISS3 --> NET
    MISS4 --> NET
    NET --> CAUGHT[All Threats Intercepted]"""

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
    render(DIAGRAM, BASE_DIR / "diagram-active-vs-passive.png")
"""
"""
