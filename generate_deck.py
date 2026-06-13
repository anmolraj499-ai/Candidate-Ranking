import os
import sys
from fpdf import FPDF

class SlideDeck(FPDF):
    def __init__(self):
        # Landscape A4 size: 297mm x 210mm
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_margin(0)
        self.set_auto_page_break(False)

    def draw_gradient_rect(self, x_start, y_start, w, h):
        # Horizontal gradient from Left (red-orange) to Center (purple) to Right (dark blue-indigo)
        # Matches the official redrob | H2S India.Runs gradient background
        for x in range(w):
            pct = x / w
            if pct < 0.3:
                # Interpolate from Red-Orange (194, 65, 12) to Purple (109, 40, 217)
                sub_pct = pct / 0.3
                r = int(194 + (109 - 194) * sub_pct)
                g = int(65 + (40 - 65) * sub_pct)
                b = int(12 + (217 - 12) * sub_pct)
            else:
                # Interpolate from Purple (109, 40, 217) to Dark Indigo (30, 27, 75)
                sub_pct = (pct - 0.3) / 0.7
                r = int(109 + (30 - 109) * sub_pct)
                g = int(40 + (27 - 40) * sub_pct)
                b = int(217 + (75 - 217) * sub_pct)
            self.set_fill_color(r, g, b)
            self.rect(x_start + x, y_start, 1.2, h, "F")

    def draw_cover_bg(self):
        # Slide 1: Top 55% (115mm) is gradient, bottom 45% (95mm) is white
        self.draw_gradient_rect(0, 0, 297, 115)
        
        self.set_fill_color(255, 255, 255)
        self.rect(0, 115, 297, 95, "F")
        
        # Bottom purple/indigo stripe (8mm height)
        self.set_fill_color(79, 70, 229) # Indigo-600 (#4F46E5)
        self.rect(0, 202, 297, 8, "F")

    def draw_thank_you_bg(self):
        # Slide 11: Full-page gradient background
        self.draw_gradient_rect(0, 0, 297, 210)
        
        # Bottom purple/indigo stripe (8mm height)
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
        self.set_text_color(148, 163, 184) # Slate-400
        self.set_font("Helvetica", "", 8)
        self.set_xy(15, 195)
        self.cell(100, 5, "team_2+  |  Candidate Ranking Submission")
        self.set_xy(182, 195)
        self.cell(100, 5, f"Slide {page_num} of 11", align="R")

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
        self.set_fill_color(79, 70, 229) # Indigo bullet
        self.rect(x, y + 1.5, 1.8, 1.8, "F")
        
        # Save margins
        old_l_margin = self.l_margin
        old_r_margin = self.r_margin
        
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
        
        self.set_left_margin(old_l_margin)
        self.set_right_margin(old_r_margin)

def build_pdf(output_path):
    pdf = SlideDeck()
    
    # -------------------------------------------------------------
    # SLIDE 1: Cover Slide (Custom Split Template)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_cover_bg()
    
    # 1. Top Section Details (Gradient area)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    # Logo
    pdf.set_xy(15, 12)
    pdf.cell(100, 6, "redrob  |  H2S")
    
    # Center INDIA.RUNS
    pdf.set_font("Helvetica", "BI", 48)
    pdf.set_xy(20, 40)
    pdf.cell(257, 18, "INDIA.RUNS", align="C")
    
    # Button: Build what next India runs on
    pdf.set_draw_color(255, 255, 255)
    pdf.rect(88, 68, 120, 10, "D")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(88, 70)
    pdf.cell(120, 6, "Build what next India runs on", align="C")
    
    # 2. Bottom Section Details (White area)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(20, 130)
    
    # Team Name
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(pdf.get_string_width("Team Name : "), 6, "Team Name : ")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(100, 6, "team_2+")
    
    # Team Leader Name
    pdf.set_xy(20, 142)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(pdf.get_string_width("Team Leader Name : "), 6, "Team Leader Name : ")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(100, 6, "Anmol Raj")
    
    # Problem Statement
    pdf.set_xy(20, 154)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(pdf.get_string_width("Problem Statement : "), 6, "Problem Statement : ")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(150, 6, "Senior AI Engineer - Founding Team Candidate Ranking")
    
    pdf.draw_slide_footer(1)

    # -------------------------------------------------------------
    # SLIDE 2: Team Details & Intro (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Team Details & Introduction")
    pdf.draw_slide_footer(2)
    
    pdf.draw_card(15, 45, 82, 140, "PRIMARY CONTACT")
    pdf.bullet_point(18, 60, "Anmol Raj", "Name:", 74)
    pdf.bullet_point(18, 85, "anmolraj499@gmail.com", "Email:", 74)
    pdf.bullet_point(18, 110, "+91-6204223789", "Phone:", 74)
    pdf.bullet_point(18, 135, "ML Engineer & Pipeline Developer", "Role:", 74)
    
    pdf.draw_card(107, 45, 82, 140, "DEVELOPMENT FOCUS")
    pdf.bullet_point(110, 60, "Engineering highly efficient algorithms designed to process massive candidate datasets locally without network latency.", "1. Offline Focus:", 74)
    pdf.bullet_point(110, 95, "Stream-reading data to prevent out-of-memory errors on typical recruiter computer hardware.", "2. Hardware Optimizations:", 74)
    pdf.bullet_point(110, 130, "Combining deep semantic transformers with keyword indexes to get explainable shortlists.", "3. Hybrid Search:", 74)
    
    pdf.draw_card(199, 45, 82, 140, "SUBMISSION COMPLIANCE")
    pdf.bullet_point(202, 60, "Official Team ID is team_2+, matching our registered team name for consistency across portals.", "1. Team ID Match:", 74)
    pdf.bullet_point(202, 95, "Metadata template fully populated and verified to match official hackathon requirements.", "2. Metadata Verified:", 74)
    pdf.bullet_point(202, 130, "All output rankings passed formatting validation. Excel and CSV variants checked.", "3. Output Conformity:", 74)

    # -------------------------------------------------------------
    # SLIDE 3: Problem Statement (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Problem Statement")
    pdf.draw_slide_footer(3)
    
    pdf.draw_card(15, 45, 128, 140, "THE RECRUITMENT BOTTLENECK")
    pdf.bullet_point(18, 60, "Reviewing 100k+ candidate profiles manually is a massive time sink. Recruiters struggle to find qualified profiles in reasonable timelines.", "1. Volume Overload:", 120)
    pdf.bullet_point(18, 95, "Traditional applicant tracking systems (ATS) rely on exact keyword matching, filtering out strong candidates who use adjacent terminology.", "2. Keyword Limitations:", 120)
    pdf.bullet_point(18, 130, "Unstructured text summaries in CVs contain massive context that standard relational database filters destroy.", "3. Semantic Blindness:", 120)
    
    pdf.draw_card(154, 45, 128, 140, "DATA INTEGRITY HAZARDS")
    pdf.bullet_point(157, 60, "Hackathon datasets contain trap profiles (honeypots) that claim impossible timeline metrics or fraudulent skill proficiencies.", "1. Resume Inflation:", 120)
    pdf.bullet_point(157, 95, "Profiles claiming years of experience that exceed their actual years since graduation bypass basic filters.", "2. Timeline Discrepancies:", 120)
    pdf.bullet_point(157, 130, "Long notice periods lead to severe recruiter drop-offs. Traditional sorting fails to integrate notice constraints dynamically.", "3. Notice Period Agility:", 120)

    # -------------------------------------------------------------
    # SLIDE 4: Proposed Solution (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Proposed Solution")
    pdf.draw_slide_footer(4)
    
    pdf.draw_card(15, 45, 82, 140, "DECOUPLED TWO-STAGE FUNNEL")
    pdf.bullet_point(18, 60, "Programmatic filters stream-read profiles to neutralize fraudulent honeypots before any model scoring.", "1. Data Integrity Gate:", 74)
    pdf.bullet_point(18, 95, "A fast BM25 lexical index filters 100k down to the top 2,000 candidates in 10 seconds.", "2. Sparse Recall:", 74)
    pdf.bullet_point(18, 130, "Dense vector encoders and Cross-Encoders score semantic fit locally on CPU within minutes.", "3. Semantic Re-ranking:", 74)
    
    pdf.draw_card(107, 45, 82, 140, "FUSION OF BEHAVIORAL SIGNALS")
    pdf.bullet_point(110, 60, "Integrates notice period constraints, relocation status, and recruiter response rates directly into the ranking equation.", "1. Signal Integration:", 74)
    pdf.bullet_point(110, 95, "Immediate availability triggers ranking bonuses; standard 90-day locks receive minor ranking penalties.", "2. Notice Agility:", 74)
    pdf.bullet_point(110, 130, "Weights scores based on candidates' active platform engagement and responsiveness metrics.", "3. Activity Weighting:", 74)
    
    pdf.draw_card(199, 45, 82, 140, "RECRUITER EXPLAINABILITY")
    pdf.bullet_point(202, 60, "Generates direct, factual, non-hallucinated explanations for why a candidate is shortlisted.", "1. Factual Reasonings:", 74)
    pdf.bullet_point(202, 95, "Gradio dashboard lets recruiters adjust Job Description in real-time and inspect candidates' score breakdowns.", "2. Interactive UI Sandbox:", 74)
    pdf.bullet_point(202, 130, "Enforces strict monotonic ranking format compliance, making the output instantly reliable.", "3. Verified Outputs:", 74)

    # -------------------------------------------------------------
    # SLIDE 5: System Architecture (Light Theme matching Slide 1)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("System Architecture")
    pdf.draw_slide_footer(5)
    
    pdf.draw_card(15, 45, 82, 140, "STAGE 1 & 2: DUAL RETRIEVAL")
    pdf.bullet_point(18, 60, "Stream-reads the JSONL candidate dataset record-by-record, keeping memory footprint under 2GB RAM.", "1. Streaming Honeypot Filtering:", 74)
    pdf.bullet_point(18, 92, "Evaluates total years of experience, skill durations, and job title coherence to filter out 35k trap candidates.", "2. Temporal Integrity Checks:", 74)
    pdf.bullet_point(18, 124, "Uses custom BM25 index over JD keywords to rapidly funnel pool from 64k down to 2,000 in ~10 seconds.", "3. BM25 Sparse Search Funnel:", 74)
    
    pdf.draw_card(107, 45, 82, 140, "STAGE 3: DENSE EMBEDDING")
    pdf.bullet_point(110, 60, "Computes 384-dimensional dense vectors for top 2,000 summaries locally on CPU using SBERT all-MiniLM-L6-v2.", "1. Local Dense Encoding:", 74)
    pdf.bullet_point(110, 92, "Generates cosine similarity matrix against expanded Job Description targets, avoiding simple keyword match constraints.", "2. Semantic Overlap Mapping:", 74)
    pdf.bullet_point(110, 124, "Fuses Redrob signals (immediate availability bonus, relocation willing, activity) directly into the score math.", "3. Platform Signal Modulation:", 74)
    
    pdf.draw_card(199, 45, 82, 140, "STAGE 4: DEEP RE-RANKING")
    pdf.bullet_point(202, 60, "Loads ms-marco-MiniLM-L-6-v2 locally on CPU to jointly evaluate JD-profile context on the top 200 candidates.", "1. Cross-Encoder Joint Attention:", 74)
    pdf.bullet_point(202, 92, "Generates a sigmoid-scaled relevance rating capturing deep contextual alignments that bi-encoders miss.", "2. Joint Relevance Calibration:", 74)
    pdf.bullet_point(202, 124, "Programmatically compiles non-templated rationales detailing years of experience, skills, and notice period constraints.", "3. Factual Reasonings Output:", 74)

    # -------------------------------------------------------------
    # SLIDE 6: Core Algorithms & Logic (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Core Algorithms & Logic")
    pdf.draw_slide_footer(6)
    
    pdf.draw_card(15, 45, 128, 140, "HONEYPOT IDENTIFICATION ENGINE")
    pdf.bullet_point(18, 60, "Flagged: Experience > (2026 - first_graduation_year) + 2. This filters profiles containing impossible career timelines.", "1. Experience-Graduation Audit:", 120)
    pdf.bullet_point(18, 95, "Flagged: 4+ skills claiming 'expert' or 'advanced' proficiency but specifying exactly 0 duration months.", "2. Skill Durations Audit:", 120)
    pdf.bullet_point(18, 130, "Flagged: Job duration in months exceeds the dates difference (start_date to end_date) by more than 12 months.", "3. Career Dates Verification:", 120)
    
    pdf.draw_card(154, 45, 128, 140, "HEURISTIC SCORING MATH")
    pdf.bullet_point(157, 60, "Notice period agility: +5% bonus for <= 15 days notice; -15% penalty for >= 90 days locked periods.", "1. Notice Period Modifiers:", 120)
    pdf.bullet_point(157, 95, "Seniority Fit: Underqualified candidates face a steep exponential penalty. Overqualified profiles are decayed slowly.", "2. Experience Fit Curve:", 120)
    pdf.bullet_point(157, 130, "Location: 1.0 multiplier for target hubs (Pune, Noida, Delhi NCR). 0.95 for relocation willing. 0.7 for non-willing.", "3. Geographic Modulations:", 120)

    # -------------------------------------------------------------
    # SLIDE 7: Technologies Used (Light Theme matching Slide 3)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Technologies Used")
    pdf.draw_slide_footer(7)
    
    pdf.draw_card(15, 45, 82, 140, "DEEP LEARNING & NLP WORKloads")
    pdf.bullet_point(18, 60, "Provides the core tensor computation framework, optimized for local CPU execution.", "PyTorch & Transformers:", 74)
    pdf.bullet_point(18, 92, "Computes fast dense text embedding vectors for candidates summary profiles.", "SentenceTransformers (all-MiniLM-L6-v2):", 74)
    pdf.bullet_point(18, 124, "Computes joint attention maps across candidates and JD requirements for fine-grained re-ranking.", "CrossEncoder (ms-marco-MiniLM-L-6-v2):", 74)
    
    pdf.draw_card(107, 45, 82, 140, "DASHBOARD & INTERACTION ENGINE")
    pdf.bullet_point(110, 60, "Powers our interactive, sandboxed web dashboard. Allows real-time JD changes and live shortlist monitoring.", "Gradio Web App:", 74)
    pdf.bullet_point(110, 92, "Manages index arrays, matrix similarity multiplications, and candidate data structures.", "Pandas & NumPy:", 74)
    pdf.bullet_point(110, 124, "Compiles the final validated candidate shortlist into spreadsheet format.", "OpenPyXL (XLSX Generator):", 74)
    
    pdf.draw_card(199, 45, 82, 140, "LOCAL ARCHITECTURE CHOICES")
    pdf.bullet_point(202, 60, "Pre-downloaded model weights cached directly in ./models/ for 100% network isolation during ranking runs.", "Zero-Network local Cache:", 74)
    pdf.bullet_point(202, 92, "O(N) streaming JSONL parser ensures memory consumption stays under 2GB, preventing out-of-memory errors.", "Low-Memory Streaming Parser:", 74)
    pdf.bullet_point(202, 124, "Cross-platform path resolution supports Windows, Linux, and macOS out-of-the-box.", "Portable OS Routing:", 74)

    # -------------------------------------------------------------
    # SLIDE 8: Results & Performance (Light Theme matching Slide 2)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Results & Performance")
    pdf.draw_slide_footer(8)
    
    pdf.draw_card(15, 45, 82, 140, "COMPUTE BENCHMARKS")
    pdf.bullet_point(18, 60, "Completes full filtering, BM25 indexing, dense vector similarity, and Cross-Encoder re-ranking in 193.75s.", "Execution Speed: 193.75 seconds", 74)
    pdf.bullet_point(18, 92, "Filters 100k candidates line-by-line using under 2GB peak RAM, ensuring compatibility with standard 16GB CPU laptops.", "Memory Footprint: <2GB Peak RAM", 74)
    pdf.bullet_point(18, 124, "Runs entirely offline with zero API calls, guaranteeing candidate data confidentiality.", "Network Independence: 100% Offline", 74)
    
    pdf.draw_card(107, 45, 82, 140, "RANKING & SCREENING QUALITY")
    pdf.bullet_point(110, 60, "Screened out 35,208 candidates with fraudulent skills or anomalous timelines, ensuring 0% honeypots in Top 100.", "Honeypot Screen Rate: 35,208 profiles", 74)
    pdf.bullet_point(110, 92, "Ensures scores strictly decrease as rank increases, with deterministic candidate_id sorting breaking duplicates.", "Monotonic Order compliance:", 74)
    pdf.bullet_point(110, 124, "Checked and passed by validate_submission.py for strict schema, column ordering, and tie-breaker conformity.", "Validation Suite: 100% Pass", 74)
    
    pdf.draw_card(199, 45, 82, 140, "INTERACTIVE WEB APP RUN")
    pdf.bullet_point(202, 60, "Allows real-time customization of Job Description and instantly compiles score meters (tech match, behavior).", "JD Modulator & UI Shortlist:", 74)
    pdf.bullet_point(202, 92, "Runs locally on port 7860, with web requests returning HTTP 200.", "Gradio Sandbox Server:", 74)
    pdf.bullet_point(202, 124, "Verified by urllib to successfully load and serve profile inspect tabs.", "Sandbox Port Verification:", 74)

    # -------------------------------------------------------------
    # SLIDE 9: Evaluation & Ranking Quality (Light Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Evaluation & Ranking Quality")
    pdf.draw_slide_footer(9)
    
    pdf.draw_card(15, 45, 128, 140, "SHORTLIST STACK ACCURACY")
    pdf.bullet_point(18, 60, "Candidate profiles match the founding AI/ML engineer profile: RAG pipeline experience, vector databases, and evaluation metrics.", "1. Match Quality Alignment:", 120)
    pdf.bullet_point(18, 95, "Taxonomy mapping identifies candidates matching 'sde-iii', 'member of technical staff', or 'lead AI engineer' roles correctly.", "2. Title Match Calibration:", 120)
    pdf.bullet_point(18, 130, "Re-ranking incorporates candidate relocation readiness to filter out candidates bound to overseas or remote-only modes.", "3. Geographic Availability:", 120)
    
    pdf.draw_card(154, 45, 128, 140, "SHORTLIST COHERENCE & TRUST")
    pdf.bullet_point(157, 60, "Programs generate transparent, non-generic descriptions (e.g. 'Software engineer with 6.9 years experience matching PyTorch, Milvus').", "1. Explanations Transparency:", 120)
    pdf.bullet_point(157, 95, "Zero hallucinated text or fabricated skills. Every claim is strictly backed by the candidate's career details.", "2. Factual Compliance:", 120)
    pdf.bullet_point(157, 130, "Verified to contain 0% honeypots or timeline fraud candidates in the final recommended Top 100.", "3. Honeypot Screening Proof:", 120)

    # -------------------------------------------------------------
    # SLIDE 10: Submission Assets (Light Theme matching Slide 5)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_light_bg()
    pdf.draw_slide_header("Submission Assets")
    pdf.draw_slide_footer(10)
    
    pdf.draw_card(15, 45, 82, 140, "GITHUB REPOSITORY")
    pdf.bullet_point(18, 60, "Contains fully working, clean, and complete code with local model caches and Gradio app.", "Clean Repository:", 74)
    pdf.bullet_point(18, 92, "https://github.com/anmolraj499-ai/Candidate-Ranking", "Repository Link:", 74)
    pdf.bullet_point(18, 124, "Detailed instructions on setup, environment, and pipeline execution.", "README Documentation:", 74)
    
    pdf.draw_card(107, 45, 82, 140, "REPRODUCIBILITY SANDBOX")
    pdf.bullet_point(110, 60, "Allows judges to run candidate evaluation sandbox on Google Colab's standard compute in seconds.", "Colab Notebook:", 74)
    pdf.bullet_point(110, 92, "https://colab.research.google.com/github/anmolraj499-ai/Candidate-Ranking/blob/main/sandbox_ranking.ipynb", "Sandbox Link:", 74)
    pdf.bullet_point(110, 124, "Clones the repo, installs dependencies, and runs ranker on sample_candidates.json.", "Automation Workflow:", 74)
    
    pdf.draw_card(199, 45, 82, 140, "SHORTLIST OUTPUTS")
    pdf.bullet_point(202, 60, "Format-compliant candidate rankings containing candidate_id, rank, score, and reasoning.", "Validated Shortlist CSV:", 74)
    pdf.bullet_point(202, 92, "Excel XLSX version created for easy upload through the portal's restricted format picker.", "Excel Shortlist XLSX:", 74)
    pdf.bullet_point(202, 124, "Official metadata detailing compute environment, team contact details, and algorithms used.", "Submission Metadata YAML:", 74)

    # -------------------------------------------------------------
    # SLIDE 11: Thank You Slide (Custom Gradient Theme)
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.draw_thank_you_bg()
    
    # Logo
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_xy(15, 12)
    pdf.cell(100, 6, "redrob  |  H2S")
    
    # Center INDIA.RUNS
    pdf.set_font("Helvetica", "BI", 48)
    pdf.set_xy(20, 40)
    pdf.cell(257, 18, "INDIA.RUNS", align="C")
    
    # Button: Build what next India runs on
    pdf.set_draw_color(255, 255, 255)
    pdf.rect(88, 68, 120, 10, "D")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(88, 70)
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
    pdf.draw_slide_footer(11)
    
    pdf.output(output_path)

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "Methodology_team_2+.pdf"
    build_pdf(out_file)
    print(f"Slide deck PDF generated successfully at: {out_file}")
