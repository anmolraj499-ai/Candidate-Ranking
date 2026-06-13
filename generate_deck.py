import os
import sys
from fpdf import FPDF

class SlideDeck(FPDF):
    def __init__(self):
        # Landscape A4 size: 297mm x 210mm
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_margin(0)
        self.set_auto_page_break(False)

    def draw_dark_bg(self):
        # Rich deep indigo gradient simulation (solid dark purple-indigo)
        self.set_fill_color(30, 27, 75) # Deep Indigo-950 (#1E1B4B)
        self.rect(0, 0, 297, 210, "F")
        
        # Subtle horizontal purple highlight at the bottom
        self.set_fill_color(79, 70, 229) # Indigo-600 (#4F46E5)
        self.rect(0, 202, 297, 8, "F")

    def draw_light_bg(self):
        self.set_fill_color(255, 255, 255) # Clean White background
        self.rect(0, 0, 297, 210, "F")
        
        # Black header bar (Top 20mm)
        self.set_fill_color(0, 0, 0)
        self.rect(0, 0, 297, 20, "F")
        
        # Purple color bar at the very bottom (Bottom 8mm)
        self.set_fill_color(79, 70, 229) # Indigo-600 (#4F46E5)
        self.rect(0, 202, 297, 8, "F")

    def draw_slide_header(self, title):
        # Header Left Logo: redrob | H2S
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 13)
        self.set_xy(15, 7)
        self.cell(50, 6, "redrob  |  H2S")
        
        # Header Right Logo: INDIA.RUNS
        self.set_font("Helvetica", "BI", 15)
        self.set_xy(232, 7)
        self.cell(50, 6, "INDIA.RUNS", align="R")
        
        # Slide Title (Left-aligned in content area)
        self.set_text_color(15, 23, 42) # Slate-900
        self.set_font("Helvetica", "B", 22)
        self.set_xy(15, 30)
        self.cell(0, 10, title)

    def draw_slide_footer(self, page_num):
        # Slide page number helper
        self.set_text_color(148, 163, 184) # Slate-400
        self.set_font("Helvetica", "", 8)
        self.set_xy(15, 195)
        self.cell(100, 5, "team_2+  |  Candidate Ranking Submission")
        self.set_xy(182, 195)
        self.cell(100, 5, f"Slide {page_num} of 6", align="R")

    def draw_card(self, x, y, w, h, title=None, bg_color=(250, 250, 250), border_color=(226, 232, 240)):
        self.set_fill_color(*bg_color)
        self.set_draw_color(*border_color)
        self.rect(x, y, w, h, "FD")
        
        if title:
            self.set_text_color(15, 23, 42)
            self.set_font("Helvetica", "B", 10.5)
            self.set_xy(x + 5, y + 4)
            self.cell(w - 10, 6, title)
            self.set_draw_color(226, 232, 240) # Slate-200
            self.line(x, y + 11, x + w, y + 11)

    def bullet_point(self, x, y, text, title=None, text_w=72):
        # Draw small purple bullet
        self.set_fill_color(79, 70, 229) # Indigo
        self.rect(x, y + 1.5, 1.8, 1.8, "F")
        
        # Save margins
        old_l_margin = self.l_margin
        old_r_margin = self.r_margin
        
        # Set margins for content area to prevent wrap overflows
        self.set_left_margin(x + 4)
        self.set_right_margin(297 - (x + 4 + text_w))
        
        current_y = y
        if title:
            self.set_text_color(15, 23, 42) # Slate-900
            self.set_font("Helvetica", "B", 9)
            self.set_xy(x + 4, current_y)
            self.multi_cell(text_w, 4, title)
            current_y = self.get_y() + 0.8
            
        self.set_text_color(71, 85, 105) # Slate-600
        self.set_font("Helvetica", "", 8.5)
        self.set_xy(x + 4, current_y)
        self.multi_cell(text_w, 4, text)
        
        # Restore margins
        self.set_left_margin(old_l_margin)
        self.set_right_margin(old_r_margin)

def build_pdf(output_path):
    pdf = SlideDeck()
    
    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme matching Slide 4)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_dark_bg()
    
    # Logo at the top
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_xy(15, 12)
    pdf.cell(100, 6, "redrob  |  H2S")
    
    # Large centered hackathon banner
    pdf.set_font("Helvetica", "BI", 48)
    pdf.set_xy(20, 60)
    pdf.cell(257, 18, "INDIA.RUNS", align="C")
    
    # Button-style text
    pdf.set_fill_color(79, 70, 229) # Indigo
    pdf.rect(78, 88, 140, 10, "F")
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(78, 90)
    pdf.cell(140, 6, "Team Name & ID: team_2+", align="C")
    
    # Subtitle
    pdf.set_text_color(203, 213, 225) # Slate-300
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_xy(20, 110)
    pdf.cell(257, 10, "Offline Candidate Ranking Pipeline", align="C")
    
    # Footer info
    pdf.set_text_color(148, 163, 184) # Slate-400
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(20, 125)
    pdf.cell(257, 5, "Designed for the 'Senior AI Engineer - Founding Team' Role", align="C")
    
    # Presenter Details
    pdf.set_xy(20, 160)
    pdf.cell(257, 5, "Submitted by: Anmol Raj  |  anmolraj499@gmail.com  |  +91-6204223789", align="C")

    # -------------------------------------------------------------
    # SLIDE 2: System Architecture (Light Theme matching Slide 1)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("System Architecture")
    pdf.draw_slide_footer(2)
    
    # Three column layout: width 82, gap 10
    # Column 1
    pdf.draw_card(15, 45, 82, 140, "STAGE 1 & 2: DUAL RETRIEVAL")
    pdf.bullet_point(18, 60, "Stream-reads the JSONL candidate dataset record-by-record, keeping memory footprint under 2GB RAM.", "1. Streaming Honeypot Filtering:", 74)
    pdf.bullet_point(18, 92, "Evaluates total years of experience, skill durations, and job title coherence to filter out 35k trap candidates.", "2. Temporal Integrity Checks:", 74)
    pdf.bullet_point(18, 124, "Uses custom BM25 index over JD keywords to rapidly funnel pool from 64k down to 2,000 in ~10 seconds.", "3. BM25 Sparse Search Funnel:", 74)
    
    # Column 2
    pdf.draw_card(107, 45, 82, 140, "STAGE 3: DENSE EMBEDDING")
    pdf.bullet_point(110, 60, "Computes 384-dimensional dense vectors for top 2,000 summaries locally on CPU using SBERT all-MiniLM-L6-v2.", "1. Local Dense Encoding:", 74)
    pdf.bullet_point(110, 92, "Generates cosine similarity matrix against expanded Job Description targets, avoiding simple keyword match constraints.", "2. Semantic Overlap Mapping:", 74)
    pdf.bullet_point(110, 124, "Fuses Redrob signals (immediate availability bonus, relocation willing, activity) directly into the score math.", "3. Platform Signal Modulation:", 74)
    
    # Column 3
    pdf.draw_card(199, 45, 82, 140, "STAGE 4: DEEP RE-RANKING")
    pdf.bullet_point(202, 60, "Loads ms-marco-MiniLM-L-6-v2 locally on CPU to jointly evaluate JD-profile context on the top 200 candidates.", "1. Cross-Encoder Joint Attention:", 74)
    pdf.bullet_point(202, 92, "Generates a sigmoid-scaled relevance rating capturing deep contextual alignments that bi-encoders miss.", "2. Joint Relevance Calibration:", 74)
    pdf.bullet_point(202, 124, "Programmatically compiles non-templated rationales detailing years of experience, skills, and notice period constraints.", "3. Factual Reasonings Output:", 74)

    # -------------------------------------------------------------
    # SLIDE 3: Technologies Used (Light Theme matching Slide 3)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Technologies Used")
    pdf.draw_slide_footer(3)
    
    # Three column cards:
    # Column 1: Core DL
    pdf.draw_card(15, 45, 82, 140, "DEEP LEARNING & NLP WORKloads")
    pdf.bullet_point(18, 60, "Provides the core tensor computation framework, optimized for local CPU execution.", "PyTorch & Transformers:", 74)
    pdf.bullet_point(18, 92, "Computes fast dense text embedding vectors for candidates summary profiles.", "SentenceTransformers (all-MiniLM-L6-v2):", 74)
    pdf.bullet_point(18, 124, "Computes joint attention maps across candidates and JD requirements for fine-grained re-ranking.", "CrossEncoder (ms-marco-MiniLM-L-6-v2):", 74)
    
    # Column 2: Dashboard & Utils
    pdf.draw_card(107, 45, 82, 140, "DASHBOARD & INTERACTION ENGINE")
    pdf.bullet_point(110, 60, "Powers our interactive, sandboxed web dashboard. Allows real-time JD changes and live shortlist monitoring.", "Gradio Web App:", 74)
    pdf.bullet_point(110, 92, "Manages index arrays, matrix similarity multiplications, and candidate data structures.", "Pandas & NumPy:", 74)
    pdf.bullet_point(110, 124, "Compiles the final validated candidate shortlist into spreadsheet format.", "OpenPyXL (XLSX Generator):", 74)
    
    # Column 3: Local Optimization
    pdf.draw_card(199, 45, 82, 140, "LOCAL ARCHITECTURE CHOICES")
    pdf.bullet_point(202, 60, "Pre-downloaded model weights cached directly in ./models/ for 100% network isolation during ranking runs.", "Zero-Network local Cache:", 74)
    pdf.bullet_point(202, 92, "O(N) streaming JSONL parser ensures memory consumption stays under 2GB, preventing out-of-memory errors.", "Low-Memory Streaming Parser:", 74)
    pdf.bullet_point(202, 124, "Cross-platform path resolution supports Windows, Linux, and macOS out-of-the-box.", "Portable OS Routing:", 74)

    # -------------------------------------------------------------
    # SLIDE 4: Results & Performance (Light Theme matching Slide 2)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Results & Performance")
    pdf.draw_slide_footer(4)
    
    # Column 1: Performance
    pdf.draw_card(15, 45, 82, 140, "COMPUTE BENCHMARKS")
    pdf.bullet_point(18, 60, "Completes full filtering, BM25 indexing, dense vector similarity, and Cross-Encoder re-ranking in 193.75s.", "Execution Speed: 193.75 seconds", 74)
    pdf.bullet_point(18, 92, "Filters 100k candidates line-by-line using under 2GB peak RAM, ensuring compatibility with standard 16GB CPU laptops.", "Memory Footprint: <2GB Peak RAM", 74)
    pdf.bullet_point(18, 124, "Runs entirely offline with zero API calls, guaranteeing candidate data confidentiality.", "Network Independence: 100% Offline", 74)
    
    # Column 2: Ranking Quality
    pdf.draw_card(107, 45, 82, 140, "RANKING & SCREENING QUALITY")
    pdf.bullet_point(110, 60, "Screened out 35,208 candidates with fraudulent skills or anomalous timelines, ensuring 0% honeypots in Top 100.", "Honeypot Screen Rate: 35,208 profiles", 74)
    pdf.bullet_point(110, 92, "Ensures scores strictly decrease as rank increases, with deterministic candidate_id sorting breaking duplicates.", "Monotonic Order compliance:", 74)
    pdf.bullet_point(110, 124, "Checked and passed by validate_submission.py for strict schema, column ordering, and tie-breaker conformity.", "Validation Suite: 100% Pass", 74)
    
    # Column 3: Sandbox Verification
    pdf.draw_card(199, 45, 82, 140, "INTERACTIVE WEB APP RUN")
    pdf.bullet_point(202, 60, "Allows real-time customization of Job Description and instantly compiles score meters (tech match, behavior).", "JD Modulator & UI Shortlist:", 74)
    pdf.bullet_point(202, 92, "Runs locally on port 7860, with web requests returning HTTP 200.", "Gradio Sandbox Server:", 74)
    pdf.bullet_point(202, 124, "Verified by urllib to successfully load and serve profile inspect tabs.", "Sandbox Port Verification:", 74)

    # -------------------------------------------------------------
    # SLIDE 5: Submission Assets (Light Theme matching Slide 5)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Submission Assets")
    pdf.draw_slide_footer(5)
    
    # Column 1: GitHub Code
    pdf.draw_card(15, 45, 82, 140, "GITHUB REPOSITORY")
    pdf.bullet_point(18, 60, "Contains fully working, clean, and complete code with local model caches and Gradio app.", "Clean Repository:", 74)
    pdf.bullet_point(18, 92, "https://github.com/anmolraj499-ai/Candidate-Ranking", "Repository Link:", 74)
    pdf.bullet_point(18, 124, "Detailed instructions on setup, environment, and pipeline execution.", "README Documentation:", 74)
    
    # Column 2: Colab Sandbox
    pdf.draw_card(107, 45, 82, 140, "REPRODUCIBILITY SANDBOX")
    pdf.bullet_point(110, 60, "Allows judges to run candidate evaluation sandbox on Google Colab's standard compute in seconds.", "Colab Notebook:", 74)
    pdf.bullet_point(110, 92, "https://colab.research.google.com/github/anmolraj499-ai/Candidate-Ranking/blob/main/sandbox_ranking.ipynb", "Sandbox Link:", 74)
    pdf.bullet_point(110, 124, "Clones the repo, installs dependencies, and runs ranker on sample_candidates.json.", "Automation Workflow:", 74)
    
    # Column 3: Shortlist Deliverables
    pdf.draw_card(199, 45, 82, 140, "SHORTLIST OUTPUTS")
    pdf.bullet_point(202, 60, "Format-compliant candidate rankings containing candidate_id, rank, score, and reasoning.", "Validated Shortlist CSV:", 74)
    pdf.bullet_point(202, 92, "Excel XLSX version created for easy upload through the portal's restricted format picker.", "Excel Shortlist XLSX:", 74)
    pdf.bullet_point(202, 124, "Official metadata detailing compute environment, team contact details, and algorithms used.", "Submission Metadata YAML:", 74)

    # -------------------------------------------------------------
    # SLIDE 6: Thank You / Title Slide (Dark Theme matching Slide 4)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_dark_bg()
    
    # Logo at the top
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_xy(15, 12)
    pdf.cell(100, 6, "redrob  |  H2S")
    
    # Center INDIA.RUNS
    pdf.set_font("Helvetica", "BI", 48)
    pdf.set_xy(20, 60)
    pdf.cell(257, 18, "INDIA.RUNS", align="C")
    
    # Button-style text
    pdf.set_fill_color(79, 70, 229) # Indigo
    pdf.rect(88, 88, 120, 10, "F")
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(88, 90)
    pdf.cell(120, 6, "Build what next India runs on", align="C")
    
    # Thank You text
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_xy(20, 115)
    pdf.cell(257, 12, "THANK YOU", align="C")
    
    # Footer
    pdf.set_text_color(148, 163, 184) # Slate-400
    pdf.set_font("Helvetica", "", 11)
    pdf.set_xy(20, 135)
    pdf.cell(257, 6, "Team: team_2+", align="C")
    
    pdf.output(output_path)

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "Methodology_team_2+.pdf"
    build_pdf(out_file)
    print(f"Slide deck PDF generated successfully at: {out_file}")
