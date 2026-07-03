"""Re-render the roadmap Gantt diagram with better readability."""
import requests
import base64
import zlib
import time
from pathlib import Path

BASE_DIR = Path(r"c:\Users\agaev\Documents\GitHub\aerial-net-defense-research\images\diagrams")

DIAGRAM = """gantt
    title Development Roadmap
    dateFormat YYYY-MM
    axisFormat %b %Y
    
    section Phase 1: POC ($2-5M)
    CF mesh impact testing            :a1, 2026-08, 90d
    Wind tunnel testing               :a2, 2026-08, 60d
    Aerostat + CF net trial           :a3, 2026-09, 180d
    Net deployment prototype          :a4, 2026-09, 120d
    
    section Phase 2: Prototype ($10-20M)
    Aerostat multi-layer system       :b1, 2027-03, 365d
    C-UAS radar integration           :b2, 2027-04, 180d
    Live-fire testing                 :b3, 2027-07, 180d
    
    section Phase 3: Deployment ($50-150M)
    Airlander 10 + CF net             :c1, 2028-02, 730d
    Formation operations              :c2, 2028-07, 540d
    Hydrogen transition               :c3, 2028-07, 540d"""

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
    render(DIAGRAM, BASE_DIR / "diagram-roadmap.png")
