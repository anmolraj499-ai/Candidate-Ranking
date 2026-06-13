import gradio as gr
import json
import re
import os
import time
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder

# Define core directories relative to script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BI_ENCODER_PATH = os.path.join(BASE_DIR, "models", "all-MiniLM-L6-v2")
CROSS_ENCODER_PATH = os.path.join(BASE_DIR, "models", "ms-marco-MiniLM-L-6-v2")

# Core AI/ML skills required for the founding Senior AI Engineer role
AI_SKILLS = {"pytorch", "tensorflow", "jax", "transformers", "huggingface", "embeddings", 
             "vector database", "vector databases", "pinecone", "weaviate", "qdrant", 
             "milvus", "opensearch", "elasticsearch", "faiss", "rag", "retrieval", 
             "nlp", "ranking", "recommender", "recommendation", "mlops", "python"}

# Service consulting firms list for screening
CONSULTING_FIRMS = {"tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini", 
                    "tata consultancy", "infosys limited", "wipro technologies", "cognizant technology",
                    "tata consultancy services"}

# Re-use exact logic from rank.py to guarantee consistency
from rank import (
    is_honeypot, extract_text, score_candidate_heuristics, 
    apply_taxonomy_mapping, generate_reasoning, BM25
)

# Custom CSS for Premium Glassmorphism Look & Feel
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

body, .gradio-container {
    font-family: 'Outfit', sans-serif !important;
    background: radial-gradient(circle at top right, #1e1b4b, #0f172a 70%) !important;
    color: #e2e8f0 !important;
}

/* Header Container */
.header-box {
    text-align: center;
    padding: 2.5rem;
    margin-bottom: 2rem;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(12px);
}

.header-box h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #ff7e5f, #feb47b, #86efac);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.header-box p {
    font-size: 1.1rem;
    color: #94a3b8;
}

/* Panel Containers */
.panel-card {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.25) !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(8px) !important;
}

/* Custom Buttons */
.btn-primary {
    background: linear-gradient(135deg, #ff7e5f, #feb47b) !important;
    border: none !important;
    color: #0f172a !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 126, 95, 0.3) !important;
}

.btn-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 126, 95, 0.4) !important;
}

/* Score Metrics */
.metric-grid {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.metric-card {
    flex: 1;
    text-align: center;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1rem;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
}

.metric-card-title {
    font-size: 0.85rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}

.metric-card-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #ff7e5f;
}

/* Detail Card Styling */
.detail-card {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
}

.badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.75rem 0;
}

.badge {
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
}

.badge-skill {
    background: rgba(255, 126, 95, 0.15);
    color: #feb47b;
    border: 1px solid rgba(255, 126, 95, 0.3);
}

.badge-status-green {
    background: rgba(134, 239, 172, 0.15);
    color: #86efac;
    border: 1px solid rgba(134, 239, 172, 0.3);
}

.badge-status-yellow {
    background: rgba(253, 224, 71, 0.15);
    color: #fde047;
    border: 1px solid rgba(253, 224, 71, 0.3);
}

.badge-status-red {
    background: rgba(248, 113, 113, 0.15);
    color: #f87171;
    border: 1px solid rgba(248, 113, 113, 0.3);
}

/* Progress bar layout */
.progress-bar-container {
    margin: 1rem 0;
}

.progress-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #94a3b8;
    margin-bottom: 0.25rem;
}

.progress-bar-bg {
    background: rgba(30, 41, 59, 0.8);
    border-radius: 9999px;
    height: 8px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 9999px;
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
}
"""

DEFAULT_JD = """Looking for a Senior AI Engineer with 5-9 years of experience, strong Python, deployed embeddings-based retrieval systems, vector databases (FAISS, Pinecone, Qdrant), hybrid search, and ranking evaluation frameworks (NDCG, MAP). Pune/Noida preferred."""

def run_ui_pipeline(candidates_file, jd_text):
    if candidates_file is None:
        # Load sample candidates automatically if no file uploaded
        candidates_path = os.path.join(BASE_DIR, "sample_candidates.json")
    else:
        candidates_path = candidates_file.name

    candidates = []
    honeypot_count = 0
    
    # Ingest candidates (handling both JSON array and JSONL streams)
    try:
        if candidates_path.endswith(".json"):
            with open(candidates_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for cand in data:
                        is_hp, _ = is_honeypot(cand)
                        if is_hp:
                            honeypot_count += 1
                        else:
                            candidates.append(cand)
        else:
            with open(candidates_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        cand = json.loads(line)
                        is_hp, _ = is_honeypot(cand)
                        if is_hp:
                            honeypot_count += 1
                        else:
                            candidates.append(cand)
    except Exception as e:
        return None, {}, None, f"<div style='color:#f87171;'>Error parsing candidate dataset: {str(e)}</div>", 0, 0, "0.00%"

    total_ingested = len(candidates) + honeypot_count
    if len(candidates) == 0:
        return None, {}, None, f"<div style='color:#f87171;'>All {total_ingested} candidates were classified as honeypots! Shortlist empty.</div>", total_ingested, honeypot_count, "0.00%"

    # Stage 1: BM25 Lexical Funnel
    corpus = []
    for cand in candidates:
        text = extract_text(cand)
        tokens = re.findall(r'[a-zA-Z0-9]+', text)
        corpus.append(tokens)
        
    bm25 = BM25(corpus)
    
    query = ["pytorch", "embeddings", "retrieval", "vector", "database", "databases", "faiss", "qdrant", 
             "pinecone", "weaviate", "milvus", "opensearch", "elasticsearch", "ranking", "nlp", "natural", 
             "language", "processing", "transformers", "llm", "llms", "search", "recommender", 
             "recommendation", "mlops", "python", "rag", "augmented", "generation"]
             
    bm25_scores = []
    for idx, tokens in enumerate(corpus):
        score = bm25.get_score(tokens, query)
        bm25_scores.append((candidates[idx], score))
        
    bm25_scores.sort(key=lambda x: x[1], reverse=True)
    funnel_n = min(1000, len(bm25_scores))  # Sub-funnel for instant UI rendering
    top_funneled = bm25_scores[:funnel_n]
    max_bm25 = max([x[1] for x in top_funneled]) if top_funneled else 1.0

    # Stage 2: SBERT Dense Embeddings
    model = SentenceTransformer(BI_ENCODER_PATH)
    jd_vector = model.encode([jd_text], convert_to_numpy=True)[0]
    
    summaries = [x[0]["profile"]["summary"] for x in top_funneled]
    embeddings = model.encode(summaries, convert_to_numpy=True)
    
    # Normalise embeddings for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    embeddings = embeddings / norms
    jd_vector = jd_vector / np.linalg.norm(jd_vector)
    similarities = np.dot(embeddings, jd_vector)

    # Heuristics Modulation
    scored_pool = []
    for i, (cand, b_score) in enumerate(top_funneled):
        sim_score = float(similarities[i])
        h_score, tech_fit, ops_fit = score_candidate_heuristics(cand, b_score, max_bm25)
        final_score = 0.6 * h_score + 0.4 * sim_score
        
        scored_pool.append({
            "cand": cand,
            "score": final_score,
            "tech_score": tech_fit,
            "ops_score": ops_fit,
            "sim_score": sim_score
        })
        
    scored_pool.sort(key=lambda x: x["score"], reverse=True)
    
    # Stage 3: Cross-Encoder Joint Rerank
    cross_n = min(100, len(scored_pool))
    top_cross = scored_pool[:cross_n]
    
    cross_encoder = CrossEncoder(CROSS_ENCODER_PATH)
    cross_inputs = [[jd_text, x["cand"]["profile"]["summary"]] for x in top_cross]
    cross_scores = cross_encoder.predict(cross_inputs)
    
    final_ranked = []
    for i, x in enumerate(top_cross):
        raw_cross = float(cross_scores[i])
        norm_cross = 1 / (1 + np.exp(-raw_cross))
        final_score = 0.5 * norm_cross + 0.5 * x["score"]
        final_ranked.append((x["cand"], round(final_score, 4), x["tech_score"], x["ops_score"], x["sim_score"]))
        
    final_ranked.sort(key=lambda x: (-x[1], x[0]["candidate_id"]))
    
    # Guarantee monotonic non-increasing scores
    csv_rows = []
    for rank_idx in range(1, len(final_ranked) + 1):
        cand, score, tech_s, ops_s, sim_s = final_ranked[rank_idx - 1]
        reason = generate_reasoning(cand, score)
        csv_rows.append({
            "candidate_id": cand["candidate_id"],
            "rank": rank_idx,
            "score": score,
            "reasoning": reason,
            "name": cand["profile"]["anonymized_name"],
            "title": cand["profile"]["current_title"],
            "tech_s": round(tech_s, 4),
            "ops_s": round(ops_s, 4),
            "sim_s": round(sim_s, 4),
            "profile": cand
        })
        
    for i in range(len(csv_rows) - 1):
        if csv_rows[i]["score"] < csv_rows[i+1]["score"]:
            csv_rows[i+1]["score"] = csv_rows[i]["score"]

    # Export submission CSV
    out_csv_path = os.path.join(BASE_DIR, "sandbox_shortlist.csv")
    df_export = pd.DataFrame([{
        "candidate_id": r["candidate_id"],
        "rank": r["rank"],
        "score": r["score"],
        "reasoning": r["reasoning"]
    } for r in csv_rows])
    df_export.to_csv(out_csv_path, index=False)

    # Shortlist display table
    df_ui = pd.DataFrame([{
        "Rank": r["rank"],
        "Candidate ID": r["candidate_id"],
        "Anonymized Name": r["name"],
        "Current Title": r["title"],
        "Shortlist Score": f"{r['score']:.4f}"
    } for r in csv_rows])

    # Store profiles map in state dict format
    profiles_dict = {r["candidate_id"]: r for r in csv_rows}
    top_score_pct = f"{csv_rows[0]['score']*100:.2f}%" if csv_rows else "0.00%"

    return df_ui, profiles_dict, out_csv_path, total_ingested, honeypot_count, top_score_pct

# Render the rich details panel for the selected candidate
def render_inspector_card(selected_id, profiles_dict):
    if not selected_id or selected_id not in profiles_dict:
        return "<div style='color:#94a3b8; text-align:center; padding: 2rem;'>Select a candidate from the table dropdown to inspect details.</div>"
    
    cand_data = profiles_dict[selected_id]
    profile = cand_data["profile"]["profile"]
    signals = cand_data["profile"]["redrob_signals"]
    skills = cand_data["profile"]["skills"]
    
    # Color badge for notice period
    notice = signals.get("notice_period_days", 30)
    if notice <= 15:
        notice_badge = f"<span class='badge badge-status-green'>Immediate ({notice} Days Notice)</span>"
    elif notice <= 45:
        notice_badge = f"<span class='badge badge-status-yellow'>Standard ({notice} Days Notice)</span>"
    else:
        notice_badge = f"<span class='badge badge-status-red'>Long Lock ({notice} Days Notice)</span>"
        
    relocation = signals.get("willing_to_relocate", False)
    reloc_badge = f"<span class='badge badge-status-green'>Willing to Relocate</span>" if relocation else f"<span class='badge badge-status-red'>No Relocation</span>"
    
    # Skill Badges
    skill_badges_html = "".join([f"<span class='badge badge-skill'>{s.get('name', '')}</span>" for s in skills[:8]])
    
    # Score details
    tech_fit_pct = int(cand_data["tech_s"] * 100)
    ops_fit_pct = int(cand_data["ops_s"] * 100)
    sim_score_pct = int(cand_data["sim_s"] * 100)
    final_score_pct = int(cand_data["score"] * 100)
    
    html = f"""
    <div class="detail-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <div>
                <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600; color: #ff7e5f;">{cand_data['name']}</h3>
                <div style="color: #94a3b8; font-size: 0.95rem; font-weight: 500;">{profile.get('current_title', 'Software Engineer')}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Final Score</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #86efac; line-height: 1;">{final_score_pct}%</div>
            </div>
        </div>
        
        <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;">ID: <b>{cand_data['candidate_id']}</b> | Experience: <b>{profile.get('years_of_experience', 0)} years</b></div>
        
        <div class="badge-container">
            {notice_badge}
            {reloc_badge}
        </div>
        
        <div style="margin-bottom: 1rem;">
            <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #e2e8f0; margin-bottom: 0.25rem;">Headline</div>
            <div style="font-size: 0.9rem; color: #cbd5e1; background: rgba(30, 41, 59, 0.4); padding: 0.5rem; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.04); font-style: italic;">
                "{profile.get('headline', '')}"
            </div>
        </div>

        <div style="margin-bottom: 1rem;">
            <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #e2e8f0; margin-bottom: 0.25rem;">Candidate Summary</div>
            <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.5;">
                {profile.get('summary', 'No summary provided.')}
            </div>
        </div>
        
        <div style="margin-bottom: 1.5rem;">
            <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #e2e8f0; margin-bottom: 0.4rem;">Skills Inventory</div>
            <div class="badge-container">
                {skill_badges_html}
            </div>
        </div>
        
        <div style="margin-bottom: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1rem;">
            <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #e2e8f0; margin-bottom: 0.75rem;">Suitability Score Breakdown</div>
            
            <div class="progress-bar-container">
                <div class="progress-bar-label">
                    <span>Technical Stack Alignment</span>
                    <span>{tech_fit_pct}%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {tech_fit_pct}%;"></div>
                </div>
            </div>
            
            <div class="progress-bar-container">
                <div class="progress-bar-label">
                    <span>Recruiter Behavioral Signals</span>
                    <span>{ops_fit_pct}%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {ops_fit_pct}%;"></div>
                </div>
            </div>
            
            <div class="progress-bar-container">
                <div class="progress-bar-label">
                    <span>Cross-Attention Joint Semantic Match</span>
                    <span>{sim_score_pct}%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {sim_score_pct}%;"></div>
                </div>
            </div>
        </div>
        
        <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1rem;">
            <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #e2e8f0; margin-bottom: 0.4rem;">Factual Match Justification</div>
            <div style="background: rgba(134, 239, 172, 0.05); border-left: 3px solid #ff7e5f; padding: 0.75rem; border-radius: 0 6px 6px 0; font-size: 0.9rem; color: #86efac; line-height: 1.4;">
                {cand_data['reasoning']}
            </div>
        </div>
    </div>
    """
    return html

# Main Blocks App
with gr.Blocks() as demo:
    # State values to carry candidate matching information across interactions
    profiles_state = gr.State({})
    
    # Header Section
    gr.HTML("""
    <div class="header-box">
        <h1>Redrob AI Talent Discovery & Shortlist Sandbox</h1>
        <p>A production-ready candidate ranking engine utilizing multi-stage sparse-dense neural retrieval on CPU.</p>
    </div>
    """)
    
    # Input/Output Columns
    with gr.Row():
        with gr.Column(scale=1, elem_classes=["panel-card"]):
            gr.HTML("<h3>⚙️ Funnel Parameters</h3>")
            
            # File Upload or Fallback Check
            cand_input = gr.File(
                label="Candidate Dataset (.jsonl or .json)",
                file_types=[".jsonl", ".json"],
                interactive=True
            )
            gr.Markdown("**Note:** If no file is uploaded, the system automatically runs on our pre-loaded `sample_candidates.json` (50 candidate profiles) for testing.")
            
            # Job Description Editor
            jd_input = gr.Textbox(
                value=DEFAULT_JD,
                label="Target Job Description",
                lines=5,
                interactive=True
            )
            
            run_btn = gr.Button("⚡ Run Neural Shortlist Funnel", elem_classes=["btn-primary"])
            
            # Output Download Button (Hidden until execution completes)
            csv_downloader = gr.File(label="Download Validated Submission CSV", interactive=False, visible=False)

        with gr.Column(scale=2, elem_classes=["panel-card"]):
            gr.HTML("<h3>📊 Ranking short-list Results</h3>")
            
            # Metrics Dashboard Grid
            with gr.Row(elem_classes=["metric-grid"]):
                m_ingested = gr.HTML("""
                <div class="metric-card">
                    <div class="metric-card-title">Candidates Ingested</div>
                    <div class="metric-card-value">—</div>
                </div>
                """)
                m_honeypots = gr.HTML("""
                <div class="metric-card">
                    <div class="metric-card-title">Honeypots Blocked</div>
                    <div class="metric-card-value">—</div>
                </div>
                """)
                m_top_score = gr.HTML("""
                <div class="metric-card">
                    <div class="metric-card-title">Top Shortlist Match</div>
                    <div class="metric-card-value">—</div>
                </div>
                """)
                
            # Shortlist DataGrid
            out_table = gr.DataFrame(
                headers=["Rank", "Candidate ID", "Anonymized Name", "Current Title", "Shortlist Score"],
                datatype=["str", "str", "str", "str", "str"],
                interactive=False
            )
            
    # Candidate Deep Inspector Section (Rendered below table)
    with gr.Row(visible=False) as inspector_section:
        with gr.Column(elem_classes=["panel-card"]):
            gr.HTML("<h3>🔍 Profile Deep-Match Inspector</h3>")
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Interactive Dropdown to pick candidate to audit
                    selector = gr.Dropdown(
                        label="Select Shortlisted Candidate to Inspect",
                        choices=[],
                        interactive=True
                    )
                with gr.Column(scale=2):
                    # HTML Card displaying candidate details
                    inspector_card = gr.HTML(
                        value="<div style='color:#94a3b8; text-align:center; padding: 2rem;'>Select a candidate from the dropdown to audit their score.</div>"
                    )

    # Controller Actions
    def pipeline_callback(cand_file, jd_txt):
        df_ui, profiles_dict, csv_path, total, honeypots, top_score = run_ui_pipeline(cand_file, jd_txt)
        
        if df_ui is None:
            # Display error in HTML
            return [
                gr.update(value=f"<div class='metric-card'><div class='metric-card-title'>Error</div><div class='metric-card-value'>—</div></div>"),
                gr.update(value=f"<div class='metric-card'><div class='metric-card-title'>Error</div><div class='metric-card-value'>—</div></div>"),
                gr.update(value=f"<div class='metric-card'><div class='metric-card-title'>Error</div><div class='metric-card-value'>—</div></div>"),
                gr.update(value=None),
                profiles_dict,
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(choices=[])
            ]
            
        # Update metrics HTML panels
        html_ingested = f"""
        <div class="metric-card">
            <div class="metric-card-title">Candidates Ingested</div>
            <div class="metric-card-value">{total}</div>
        </div>
        """
        html_honeypots = f"""
        <div class="metric-card">
            <div class="metric-card-title">Honeypots Blocked</div>
            <div class="metric-card-value">{honeypots}</div>
        </div>
        """
        html_top_score = f"""
        <div class="metric-card">
            <div class="metric-card-title">Top Shortlist Match</div>
            <div class="metric-card-value">{top_score}</div>
        </div>
        """
        
        # Populate selector dropdown options
        shortlist_choices = [r["candidate_id"] for r in profiles_dict.values()]
        
        return [
            gr.update(value=html_ingested),
            gr.update(value=html_honeypots),
            gr.update(value=html_top_score),
            df_ui,
            profiles_dict,
            gr.update(value=csv_path, visible=True),
            gr.update(visible=True),
            gr.update(choices=shortlist_choices, value=shortlist_choices[0] if shortlist_choices else None)
        ]

    # Handle Run button
    run_btn.click(
        fn=pipeline_callback,
        inputs=[cand_input, jd_input],
        outputs=[
            m_ingested, m_honeypots, m_top_score, 
            out_table, profiles_state, csv_downloader, 
            inspector_section, selector
        ]
    )
    
    # Handle Inspector Dropdown select
    selector.change(
        fn=render_inspector_card,
        inputs=[selector, profiles_state],
        outputs=[inspector_card]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, theme=gr.themes.Default(), css=CUSTOM_CSS)
