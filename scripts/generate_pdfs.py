"""Generate PDF from markdown research documents using fpdf2."""
import re
from pathlib import Path
from fpdf import FPDF

BASE_DIR = Path(r"c:\Users\agaev\Documents\GitHub\llm-generation-design\docs\research\carbon-fiber-net-defense")

IMAGE_MAP = {
    "cf-net-defense-concept.png": BASE_DIR / "cf-net-defense-concept.png",
    "cost-comparison-infographic.png": BASE_DIR / "cost-comparison-infographic.png",
    "border-deployment-map.png": BASE_DIR / "border-deployment-map.png",
    "altitude-threat-coverage.png": BASE_DIR / "altitude-threat-coverage.png",
    "net-curtain-concept.png": BASE_DIR / "net-curtain-concept.png",
    "diagram-defense-layers.png": BASE_DIR / "diagram-defense-layers.png",
    "diagram-material-weight.png": BASE_DIR / "diagram-material-weight.png",
    "diagram-lebanon-deployment.png": BASE_DIR / "diagram-lebanon-deployment.png",
    "diagram-golan-deployment.png": BASE_DIR / "diagram-golan-deployment.png",
    "diagram-jordan-deployment.png": BASE_DIR / "diagram-jordan-deployment.png",
    "diagram-roadmap.png": BASE_DIR / "diagram-roadmap.png",
    "diagram-curtain-concept.png": BASE_DIR / "diagram-curtain-concept.png",
    "diagram-self-protection.png": BASE_DIR / "diagram-self-protection.png",
}


class ResearchPDF(FPDF):
    def __init__(self, title="Research Document"):
        super().__init__()
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 5, self.doc_title, 0, 0, 'L')
        self.cell(0, 5, f'Page {self.page_no()}', 0, 1, 'R')
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, 'UNCLASSIFIED - Open Source Research | July 2026', 0, 0, 'C')

    def add_title(self, text):
        self.set_font('Helvetica', 'B', 18)
        self.multi_cell(0, 8, self._sanitize(text), align='C')
        self.ln(5)

    def add_h1(self, text):
        self.ln(3)
        self.set_font('Helvetica', 'B', 14)
        self.multi_cell(0, 7, self._sanitize(text))
        self.ln(2)

    def add_h2(self, text):
        self.ln(2)
        self.set_font('Helvetica', 'B', 12)
        self.multi_cell(0, 6, self._sanitize(text))
        self.ln(1)

    def add_h3(self, text):
        self.ln(1)
        self.set_font('Helvetica', 'B', 10)
        self.multi_cell(0, 5, self._sanitize(text))
        self.ln(1)

    def add_body(self, text):
        self.set_x(self.l_margin)
        self.set_font('Helvetica', '', 10)
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        clean = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', clean)
        clean = re.sub(r'`(.+?)`', r'\1', clean)
        clean = self._sanitize(clean)
        self.multi_cell(0, 5, clean)
        self.ln(1)

    @staticmethod
    def _sanitize(text):
        replacements = {
            '\u2014': '--', '\u2013': '-', '\u2018': "'", '\u2019': "'",
            '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u2022': '*',
            '\u2713': '[x]', '\u2717': '[ ]', '\u2265': '>=', '\u2264': '<=',
            '\u00d7': 'x', '\u2192': '->', '\u2190': '<-', '\u25bc': 'v',
            '\u25b2': '^', '\u2502': '|', '\u2500': '-', '\u250c': '+',
            '\u2510': '+', '\u2514': '+', '\u2518': '+', '\u251c': '+',
            '\u2524': '+', '\u2524': '+', '\u252c': '+', '\u2534': '+',
            '\u253c': '+', '\u2550': '=', '\u2551': '||',
            '\u2554': '+', '\u2557': '+', '\u255a': '+', '\u255d': '+',
            '\u2560': '+', '\u2563': '+', '\u2566': '+', '\u2569': '+',
            '\u256c': '+', '\u2591': '#', '\u2588': '#', '\u2592': '#',
            '\u25cf': '*', '\u2756': '*', '\u27a4': '>',
            '\u2705': '[x]', '\u274c': '[ ]',
            '\u2611': '[x]', '\u2610': '[ ]',
            '\u2716': 'x', '\u00b2': '2',
            '\u2248': '~', '\u00b0': 'deg',
        }
        for char, repl in replacements.items():
            text = text.replace(char, repl)
        result = ''
        for ch in text:
            try:
                ch.encode('latin-1')
                result += ch
            except UnicodeEncodeError:
                result += '?'
        return result

    def add_bullet(self, text):
        self.set_x(self.l_margin)
        self.set_font('Helvetica', '', 10)
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        clean = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', clean)
        clean = self._sanitize(clean)
        self.multi_cell(0, 5, f"  - {clean}")

    def add_table(self, headers, rows):
        self.set_font('Helvetica', '', 8)
        num_cols = len(headers)
        page_width = self.w - 2 * self.l_margin
        col_width = page_width / num_cols
        
        if col_width < 15:
            col_width = 15
            
        self.set_font('Helvetica', 'B', 8)
        for h in headers:
            text = self._sanitize(h[:int(col_width/2)] if len(h) > col_width/2 else h)
            self.cell(col_width, 5, text, 1, 0, 'C')
        self.ln()
        
        self.set_font('Helvetica', '', 7)
        for row in rows:
            max_height = 5
            for j, cell in enumerate(row[:num_cols]):
                text = self._sanitize(cell[:int(col_width/1.8)] if len(cell) > col_width/1.8 else cell)
                self.cell(col_width, 5, text, 1, 0, 'L')
            self.ln()
        self.ln(2)

    def add_code(self, text):
        self.set_x(self.l_margin)
        self.set_font('Courier', '', 8)
        for line in text.split('\n'):
            self.set_x(self.l_margin)
            sanitized = self._sanitize(line[:90])
            self.multi_cell(0, 4, sanitized)
        self.ln(2)


def md_to_pdf(md_path: Path, pdf_path: Path, title: str):
    pdf = ResearchPDF(title=title)
    pdf.add_page()
    
    content = md_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    in_code_block = False
    code_lines = []
    in_table = False
    table_headers = []
    table_rows = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('```'):
            if in_code_block:
                pdf.add_code('\n'.join(code_lines))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue
        
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
        
        if '|' in line and line.count('|') >= 2 and not line.strip().startswith('```'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if cells and all(set(c.strip()) <= {'-', ':', ' ', '|'} for c in cells):
                i += 1
                continue
            if not in_table:
                in_table = True
                table_headers = cells
                table_rows = []
            else:
                table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            if table_headers:
                try:
                    pdf.add_table(table_headers, table_rows)
                except Exception:
                    pass
            in_table = False
            table_headers = []
            table_rows = []
        
        img_match = re.match(r'!\[.*?\]\((.+?)\)', line)
        if img_match:
            img_file = img_match.group(1)
            img_path = IMAGE_MAP.get(img_file)
            if img_path and img_path.exists():
                pdf.set_x(pdf.l_margin)
                avail_w = pdf.w - 2 * pdf.l_margin
                try:
                    pdf.image(str(img_path), x=pdf.l_margin, w=avail_w)
                except Exception:
                    pdf.add_body(f"[Image: {img_file}]")
                pdf.ln(4)
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            pdf.add_title(line[2:].strip())
        elif line.startswith('## '):
            pdf.add_h1(line[3:].strip())
        elif line.startswith('### '):
            pdf.add_h2(line[4:].strip())
        elif line.startswith('#### '):
            pdf.add_h3(line[5:].strip())
        elif line.startswith('- ') or line.startswith('* '):
            pdf.add_bullet(line[2:].strip())
        elif line.startswith('---'):
            pdf.add_page()
        elif line.strip() == '':
            pdf.ln(2)
        elif line.strip():
            pdf.add_body(line)
        
        i += 1
    
    if in_table and table_headers:
        try:
            pdf.add_table(table_headers, table_rows)
        except Exception:
            pass
    
    pdf.output(str(pdf_path))
    print(f"Generated: {pdf_path}")


if __name__ == '__main__':
    en_md = BASE_DIR / "research-en.md"
    en_pdf = BASE_DIR / "research-en.pdf"
    md_to_pdf(en_md, en_pdf, "Carbon Fiber Net Defense - Feasibility Research")
    
    summary_en = BASE_DIR / "executive-summary-en.md"
    summary_en_pdf = BASE_DIR / "executive-summary-en.pdf"
    md_to_pdf(summary_en, summary_en_pdf, "Executive Summary - CF Net Defense")
    
    print("\nPDF files generated.")
    print("Note: Hebrew PDF requires Unicode font support. The DOCX version")
    print("supports Hebrew natively - export to PDF from Microsoft Word for best results.")
