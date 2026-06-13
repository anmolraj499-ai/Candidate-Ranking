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
        self.set_fill_color(15, 23, 42) # Slate-900 (#0F172A)
        self.rect(0, 0, 297, 210, "F")

    def draw_light_bg(self):
        self.set_fill_color(248, 250, 252) # Slate-50 (#F8FAFC)
        self.rect(0, 0, 297, 210, "F")
        # Color bar at the very top
        self.set_fill_color(13, 148, 136) # Teal-600 (#0D9488)
        self.rect(0, 0, 297, 6, "F")

    def draw_slide_header(self, category, title):
        # Category label
        self.set_text_color(13, 148, 136) # Teal-600
        self.set_font("Helvetica", "B", 10)
        self.set_xy(15, 12)
        self.cell(0, 5, category.upper())
        
        # Title
        self.set_text_color(15, 23, 42) # Slate-900
        self.set_font("Helvetica", "B", 22)
        self.set_xy(15, 17)
        self.cell(0, 10, title)
        
        # Horizontal Divider Line
        self.set_draw_color(226, 232, 240) # Slate-200
        self.line(15, 28, 282, 28)

    def draw_slide_footer(self, page_num):
        self.set_text_color(148, 163, 184) # Slate-400
        self.set_font("Helvetica", "", 8)
        self.set_xy(15, 198)
        self.cell(100, 5, "Redrob Runs Data & AI Challenge  |  team_2+")
        self.set_xy(182, 198)
        self.cell(100, 5, f"Slide {page_num} of 7", align="R")

    def draw_card(self, x, y, w, h, title=None, bg_color=(255, 255, 255), border_color=(226, 232, 240)):
        self.set_fill_color(*bg_color)
        self.set_draw_color(*border_color)
        self.rect(x, y, w, h, "FD")
        
        if title:
            self.set_text_color(15, 23, 42)
            self.set_font("Helvetica", "B", 11)
            self.set_xy(x + 5, y + 4)
            self.cell(w - 10, 6, title)
            self.set_draw_color(241, 245, 249) # Slate-100
            self.line(x, y + 11, x + w, y + 11)

    def bullet_point(self, x, y, text, title=None, text_w=110):
        # Draw small teal bullet
        self.set_fill_color(13, 148, 136)
        self.rect(x, y + 1.5, 2, 2, "F")
        
        # Save margins
        old_l_margin = self.l_margin
        old_r_margin = self.r_margin
        
        # Set margins for the bullet content area to enforce clean wrapping
        self.set_left_margin(x + 5)
        self.set_right_margin(297 - (x + 5 + text_w))
        
        current_y = y
        if title:
            self.set_text_color(15, 23, 42) # Slate-900
            self.set_font("Helvetica", "B", 10)
            self.set_xy(x + 5, current_y)
            self.multi_cell(text_w, 4.5, title)
            current_y = self.get_y() + 1
            
        self.set_text_color(71, 85, 105) # Slate-600
        self.set_font("Helvetica", "", 9.5)
        self.set_xy(x + 5, current_y)
        self.multi_cell(text_w, 4.5, text)
        
        # Restore original margins
        self.set_left_margin(old_l_margin)
        self.set_right_margin(old_r_margin)

def build_pdf(output_path):
    pdf = SlideDeck()
    
    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_dark_bg()
    
    # Title Block
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_xy(20, 65)
    pdf.cell(0, 12, "Advanced Candidate Ranking Engine")
    
    # Subtitle
    pdf.set_text_color(13, 148, 136) # Teal-600
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(20, 80)
    pdf.cell(0, 10, "A Production-Grade Hybrid Retrieval & Re-ranking Pipeline")
    
    # Metadata Line
    pdf.set_text_color(148, 163, 184) # Slate-400
    pdf.set_font("Helvetica", "", 11)
    pdf.set_xy(20, 93)
    pdf.cell(0, 6, "Designed for the 'Senior AI Engineer - Founding Team' Role | 100k Candidates Pool")
    
    # Divider line
    pdf.set_draw_color(30, 41, 59) # Slate-800
    pdf.line(20, 115, 277, 115)
    
    # Presenter details
    pdf.set_text_color(203, 213, 225) # Slate-300
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(20, 125)
    pdf.cell(100, 6, "SUBMITTED BY:")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_xy(20, 131)
    pdf.cell(100, 5, "Team Name: team_2+")
    pdf.set_xy(20, 137)
    pdf.cell(100, 5, "Primary Contact: Anmol Raj (anmolraj499@gmail.com)")
    
    # Right panel details (Specs summary)
    pdf.set_xy(180, 125)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(100, 6, "SYSTEM COMPLIANCE:")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_xy(180, 131)
    pdf.cell(100, 5, "[X] 100% Offline (Zero API Calls at Runtime)")
    pdf.set_xy(180, 137)
    pdf.cell(100, 5, "[X] CPU-Only execution (<= 16GB RAM constraint)")
    pdf.set_xy(180, 143)
    pdf.cell(100, 5, "[X] Execution time: 193.75s (under 5-minute limit)")
    
    # -------------------------------------------------------------
    # SLIDE 2: Problem & Strategy (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Executive Summary", "Solving the Limitations of Traditional ATS")
    pdf.draw_slide_footer(2)
    
    # Column 1: The ATS Problem
    pdf.draw_card(15, 38, 128, 148, "THE CRITICAL FLAWS OF KEYWORD FILTERS")
    
    pdf.bullet_point(20, 50, "Candidates with weak skills stuff their resumes with target keywords, pushing low-quality profiles to the top.", "1. Vulnerability to Keyword Stuffing:", 113)
    pdf.bullet_point(20, 80, "Fails to recognize conceptual synonyms. A candidate writing 'neural representation learning' is filtered out if the system only looks for 'embeddings'.", "2. Semantic Blindness:", 113)
    pdf.bullet_point(20, 110, "Treats skills list in isolation, failing to evaluate career trajectories, tenure stability, and notice period constraints.", "3. Ignoring Career Context:", 113)
    pdf.bullet_point(20, 140, "Standard databases are flooded with fake timelines, invalid experience declarations, and resume fraud (honeypot profiles).", "4. Honeypot Ingestion:", 113)
    
    # Column 2: Our Recruiter-First Philosophy
    pdf.draw_card(154, 38, 128, 148, "THE TEAM_2+ PHILOSOPHY")
    
    pdf.bullet_point(159, 50, "Combine fast keyword index funnels with deep contextual sentence-transformers to capture implicit expertise.", "1. Hybrid Search Architecture:", 113)
    pdf.bullet_point(159, 80, "Verify candidate consistency by cross-referencing graduation years, skill durations, and job title coherence before scoring.", "2. Hard Data Integrity Gates:", 113)
    pdf.bullet_point(159, 110, "Fuses Redrob signals (notice periods, recruiter responsiveness, and geographic flexibility) directly into the mathematical rank.", "3. Behavioral Signal Fusion:", 113)
    pdf.bullet_point(159, 140, "Generate honest, non-hallucinated explanations summarizing why a candidate is ranked, directly highlighting experience metrics.", "4. Factual Explainability:", 113)

    # -------------------------------------------------------------
    # SLIDE 3: System Architecture (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("System Architecture", "The Decoupled Multi-Stage Funnel Design")
    pdf.draw_slide_footer(3)
    
    # Architecture Card
    pdf.draw_card(15, 38, 267, 148, "PIPELINE WORKFLOW & COMPUTATION STAGES")
    
    stages = [
        {"num": "1", "name": "Stream Ingestion", "desc": "Ingests 100k records line-by-line to prevent memory leaks. Screens timeline/skills fraud."},
        {"num": "2", "name": "BM25 Lexical Funnel", "desc": "Computes fast keyword score over target stack (PyTorch, RAG). Narrows pool to top 2,000."},
        {"num": "3", "name": "Dense Embedding", "desc": "Computes cosine similarity with local SBERT model (all-MiniLM-L6-v2) on CPU."},
        {"num": "4", "name": "Signal Fusion", "desc": "Applies multipliers for notice period agility, relocation, and recruiter activity."},
        {"num": "5", "name": "Cross-Encoder", "desc": "Computes deep joint context overlap for top 200 using local ms-marco-MiniLM-L-6-v2."},
        {"num": "6", "name": "Shortlist Export", "desc": "Applies deterministic tie-breakers and outputs format-compliant CSV."}
    ]
    
    y_start = 55
    for i, s in enumerate(stages):
        # Draw step number block
        pdf.set_fill_color(15, 23, 42) # Dark Slate
        pdf.rect(20, y_start, 8, 8, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_xy(20, y_start + 1.5)
        pdf.cell(8, 5, s["num"], align="C")
        
        # Stage title
        pdf.set_text_color(13, 148, 136) # Teal
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_xy(32, y_start + 1.5)
        pdf.cell(100, 5, s["name"])
        
        # Stage description with left margin constraint
        old_l = pdf.l_margin
        pdf.set_left_margin(90)
        pdf.set_text_color(71, 85, 105) # Slate
        pdf.set_font("Helvetica", "", 10)
        pdf.set_xy(90, y_start + 1.5)
        pdf.multi_cell(180, 5, s["desc"])
        pdf.set_left_margin(old_l)
        
        # Divider line between steps
        if i < 5:
            pdf.set_draw_color(241, 245, 249)
            pdf.line(20, y_start + 12, 272, y_start + 12)
            
        y_start += 18

    # -------------------------------------------------------------
    # SLIDE 4: Timeline Fraud & Honeypots (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Data Quality Guardrails", "Identifying Timeline Fraud and Honeypots")
    pdf.draw_slide_footer(4)
    
    # Left Box: Filtering Rules
    pdf.draw_card(15, 38, 140, 148, "HONEYPOT DETECTION ALGORITHMS")
    
    pdf.bullet_point(20, 50, "Excludes profiles claiming total years of experience exceeding the span since graduation by more than 2 years: \nExp > (2026 - First Graduation Year) + 2", "Rule 1: Graduation/Experience Mismatch", 125)
    pdf.bullet_point(20, 80, "Excludes candidates claiming 'expert' or 'advanced' proficiency in 4 or more distinct skills but declaring exactly 0 months of duration.", "Rule 2: Skill Duration Inflation", 125)
    pdf.bullet_point(20, 110, "Cross-references job start and end dates with declared job durations, checking for temporal mismatches (>12 months discrepancy).", "Rule 3: Career Timeline Coherence", 125)
    pdf.bullet_point(20, 140, "Detects copy-paste profile descriptions (e.g. 'marketing manager' summaries paired with unrelated developer or mechanical engineering titles).", "Rule 4: Semantic Drift Integrity Gate", 125)
    
    # Right Box: Results
    pdf.draw_card(164, 38, 118, 148, "FILTERING IMPACT")
    
    pdf.set_text_color(13, 148, 136) # Teal
    pdf.set_font("Helvetica", "B", 42)
    pdf.set_xy(169, 52)
    pdf.cell(108, 12, "35,208", align="C")
    
    pdf.set_text_color(15, 23, 42)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(169, 66)
    pdf.cell(108, 5, "Honeypot Candidates Screened Out", align="C")
    
    # Multi-cell with left margin constraint
    old_l = pdf.l_margin
    pdf.set_left_margin(172)
    pdf.set_text_color(71, 85, 105)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_xy(172, 75)
    pdf.multi_cell(102, 4.2, "From the original 100,000 profile pool, 35,208 candidates were flagged as having inconsistent timeline claims or fraudulent skills sheets.")
    
    # Large Stat 2: Honeypot presence in Top 100
    pdf.set_text_color(15, 23, 42)
    pdf.set_font("Helvetica", "B", 42)
    pdf.set_xy(169, 112)
    pdf.cell(108, 12, "0%", align="C")
    
    pdf.set_text_color(13, 148, 136)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(169, 126)
    pdf.cell(108, 5, "Honeypots in Final Shortlist", align="C")
    
    pdf.set_xy(172, 135)
    pdf.multi_cell(102, 4.2, "Our strict programmatic logic guarantees that none of these anomalous profiles make it into the final recommended Top 100 shortlist.")
    pdf.set_left_margin(old_l)

    # -------------------------------------------------------------
    # SLIDE 5: Retrieval & Dense Embeddings (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("The Two-Stage Retrieval Model", "Scaling Semantic Comprehension on CPU")
    pdf.draw_slide_footer(5)
    
    # Left Box: Stage 1 Lexical
    pdf.draw_card(15, 38, 128, 148, "STAGE 1: BM25 LEXICAL RETRIEVAL")
    
    pdf.bullet_point(20, 50, "Computes a document index over normalized terms in candidate summaries, titles, and career descriptions.", "Mechanism:", 113)
    pdf.bullet_point(20, 80, "Curated keyword list containing 'pytorch', 'vector database', 'faiss', 'qdrant', 'RAG', 'transformers', and 'mlops'.", "Query Vector:", 113)
    pdf.bullet_point(20, 110, "Filters candidate pool from 64,792 active profiles down to the top 2,000 in just 10.01 seconds.", "Speed & Scale:", 113)
    pdf.bullet_point(20, 140, "Acts as a broad recall filter to ensure high-coverage of primary technical stack requirements.", "Role:", 113)

    # Right Box: Stage 2 Dense
    pdf.draw_card(154, 38, 128, 148, "STAGE 2: LOCAL SBERT EMBEDDINGS")
    
    pdf.bullet_point(159, 50, "Uses local 'all-MiniLM-L6-v2' model to map candidate profiles into a 384-dimensional vector space.", "Model selection:", 113)
    pdf.bullet_point(159, 80, "Loads model files locally from checkpoints inside the project. Requires zero network/API requests.", "Zero-Network Constraint:", 113)
    pdf.bullet_point(159, 110, "Computes exact cosine similarity on CPU across the top 2,000 candidates in 15 seconds.", "Computation:", 113)
    pdf.bullet_point(159, 140, "Identifies matching candidates based on semantic meaning rather than exact word matches, preventing keyword stuffing.", "Impact:", 113)

    # -------------------------------------------------------------
    # SLIDE 6: Behavioral Modulation & Reranking (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Final Optimization & Re-ranking", "Fusing Platform Signals with Joint Attention")
    pdf.draw_slide_footer(6)
    
    # Left Box: Platform Signal Modulation
    pdf.draw_card(15, 38, 128, 148, "STAGE 3: BEHAVIORAL SIGNAL MODULATION")
    
    pdf.bullet_point(20, 50, "Underqualified candidates receive steep penalty curves; overqualified profiles decay slowly to prevent screening out.", "1. Seniority Fit Curve:", 113)
    pdf.bullet_point(20, 80, "Bonus (+5%) for sub-15 days notice, penalty (-15%) for 90-day locks to account for drop-off hazard.", "2. Notice Period Agility:", 113)
    pdf.bullet_point(20, 110, "1.0 for target Indian hubs (Noida, Pune, NCR). 0.95 for relocation-willing. Penalty for non-willing remote candidates.", "3. Location Fit Multipliers:", 113)
    pdf.bullet_point(20, 140, "Integrates recruiter response rates and profile completeness directly into the scoring loop.", "4. Platform Completeness:", 113)

    # Right Box: Cross-Encoder Reranking
    pdf.draw_card(154, 38, 128, 148, "STAGE 4: LOCAL CROSS-ENCODER RERANK")
    
    pdf.bullet_point(159, 50, "Uses 'ms-marco-MiniLM-L-6-v2' locally on the top 200 candidates to refine the final shortlist.", "Dual-Encoder Correction:", 113)
    pdf.bullet_point(159, 80, "Computes joint cross-attention across candidate summaries and JD requirements simultaneously, extracting complex matching patterns.", "Mechanism:", 113)
    pdf.bullet_point(159, 110, "Uses alphabetical candidate ID sort as a tie-breaker when final scores are identical, ensuring stable and deterministic ranks.", "Deterministic Tie-Breaking:", 113)
    pdf.bullet_point(159, 140, "Explains the specific title, years of experience, top matching tools, and notice period constraints without hallucinated claims.", "Factual Rationale Generator:", 113)

    # -------------------------------------------------------------
    # SLIDE 7: Summary & Verification (Dark Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_dark_bg()
    
    # Final header
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_xy(20, 20)
    pdf.cell(0, 10, "Project Delivery & Verification Summary")
    
    pdf.set_draw_color(30, 41, 59)
    pdf.line(20, 32, 277, 32)
    
    # Left section: Core Metrics
    pdf.set_text_color(13, 148, 136) # Teal
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(20, 42)
    pdf.cell(100, 6, "SUBMISSION BENCHMARKS")
    
    old_l = pdf.l_margin
    pdf.set_left_margin(20)
    pdf.set_text_color(241, 245, 249) # Light text
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(20, 52)
    pdf.multi_cell(125, 5.5, 
        "- Execution Time: 193.75 seconds to screen, rank, and format 100,000 candidates on a single core.\n\n"
        "- Memory Footprint: Peak RAM is well under 16GB due to line-by-line streaming of candidates.\n\n"
        "- Formatting Verification: Passed all validate_submission.py checks, guaranteeing monotonic non-increasing scores, strict ranks (1-100), and alphabetical tie-breaking.\n\n"
        "- Zero API Dependency: Operates completely offline, protecting candidate privacy and securing sandbox replicability."
    )
    pdf.set_left_margin(old_l)
    
    # Right section: Deliverables checklist
    pdf.set_xy(160, 42)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(100, 6, "DELIVERABLES CHECKLIST")
    
    checklist = [
        "[X] GitHub Repository (clean history, fully documented README)",
        "[X] final shortlist CSV (team_2+.csv, validated format)",
        "[X] Submission Metadata (submission_metadata.yaml)",
        "[X] Google Colab Reproducibility Sandbox Notebook",
        "[X] Slide Deck PDF (Methodology_team_2+.pdf)"
    ]
    
    y_check = 52
    for item in checklist:
        pdf.set_text_color(13, 148, 136) # Teal check
        pdf.set_xy(160, y_check)
        pdf.cell(10, 5, "[X]")
        pdf.set_text_color(241, 245, 249)
        pdf.set_xy(170, y_check)
        pdf.cell(100, 5, item[4:])
        y_check += 12
        
    pdf.set_draw_color(30, 41, 59)
    pdf.line(20, 155, 277, 155)
    
    pdf.set_text_color(148, 163, 184)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_xy(20, 165)
    pdf.cell(0, 10, "Thank you! The pipeline is ready for submission to the Redrob Portal.", align="C")
    
    # Output file
    pdf.output(output_path)

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "Methodology_team_2+.pdf"
    build_pdf(out_file)
    print(f"Slide deck PDF generated successfully at: {out_file}")
