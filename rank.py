import json
import re
import math
import time
import os
import argparse
import numpy as np
import csv
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

# Taxonomy & Synonym mapping dictionary
SYNONYM_MAP = {
    r"\b(sde[- ]?2|sde[- ]?ii|software engineer[- ]?ii|software development engineer[- ]?ii)\b": "sde-2 software development engineer 2",
    r"\b(sde[- ]?3|sde[- ]?iii|software engineer[- ]?iii|software development engineer[- ]?iii|lead software engineer|senior software engineer)\b": "senior software engineer sde-3",
    r"\b(mts|member of technical staff)\b": "mts member of technical staff",
    r"\b(artificial intelligence|deep learning|neural networks?)\b": "ai artificial intelligence",
    r"\b(machine learning)\b": "ml machine learning",
    r"\b(natural language processing)\b": "nlp natural language processing",
    r"\b(nlp)\b": "nlp natural language processing",
    r"\b(vector[- ]?databases?|vector[- ]?search)\b": "vector database vector search",
    r"\b(py[- ]?torch)\b": "pytorch",
    r"\b(tensor[- ]?flow)\b": "tensorflow",
    r"\b(hugging[- ]?face)\b": "huggingface",
    r"\b(ml[- ]?ops)\b": "mlops",
    r"\b(rag)\b": "rag retrieval augmented generation",
    r"\b(retrieval augmented generation)\b": "rag retrieval augmented generation"
}

def apply_taxonomy_mapping(text: str) -> str:
    text_lower = text.lower()
    for pattern, replacement in SYNONYM_MAP.items():
        text_lower = re.sub(pattern, replacement, text_lower)
    return text_lower

class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.avg_doc_len = sum(len(doc) for doc in corpus) / self.corpus_size if self.corpus_size > 0 else 0
        self.doc_freqs = {}
        self.idf = {}
        
        for doc in corpus:
            unique_terms = set(doc)
            for term in unique_terms:
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1
                
        for term, freq in self.doc_freqs.items():
            self.idf[term] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

    def get_score(self, doc, query):
        score = 0.0
        doc_len = len(doc)
        if doc_len == 0:
            return 0.0
        tf = {}
        for term in doc:
            tf[term] = tf.get(term, 0) + 1
        for term in query:
            if term not in tf:
                continue
            f = tf[term]
            idf = self.idf.get(term, 0.0)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
            score += idf * (numerator / denominator)
        return score

def is_honeypot(cand):
    # Rule 1: Mismatched experience vs graduation
    edu = cand.get("education", [])
    years_of_experience = cand.get("profile", {}).get("years_of_experience", 0)
    if edu:
        end_years = [e.get("end_year") for e in edu if e.get("end_year") and 1970 <= e.get("end_year") <= 2035]
        if end_years:
            first_grad_year = min(end_years)
            years_since_grad = 2026 - first_grad_year
            if years_of_experience > years_since_grad + 2:
                return True, f"Exp {years_of_experience} exceeds years since graduation {years_since_grad}"
                
    # Rule 2: Expert/advanced proficiency in skills but 0 duration
    skills = cand.get("skills", [])
    expert_zero_dur = 0
    for s in skills:
        pref = s.get("proficiency", "").lower()
        dur = s.get("duration_months", 0)
        if pref in ["expert", "advanced"] and (dur == 0 or dur is None):
            expert_zero_dur += 1
    if expert_zero_dur >= 4:
        return True, f"{expert_zero_dur} expert/advanced skills with 0 duration"
        
    # Rule 3: Job duration mismatches
    for job in cand.get("career_history", []):
        start_date = job.get("start_date")
        end_date = job.get("end_date")
        duration = job.get("duration_months", 0)
        if start_date and end_date:
            try:
                sy, sm, _ = map(int, start_date.split('-'))
                ey, em, _ = map(int, end_date.split('-'))
                months_diff = (ey - sy) * 12 + (em - sm)
                if duration > months_diff + 12:
                    return True, f"Job duration {duration} exceeds dates diff {months_diff}"
            except:
                pass
                
    # Rule 4: Marketing/sales summary but random non-marketing titles (CAND_0000017 template)
    summary_lower = cand.get("profile", {}).get("summary", "").lower()
    if "marketing manager" in summary_lower and "experimented with chatgpt" in summary_lower:
        titles = [job.get("title", "").lower() for job in cand.get("career_history", [])]
        is_marketing = any("marketing" in t or "sales" in t or "operations" in t for t in titles)
        if not is_marketing:
            return True, "Marketing summary template but titles are random"
            
    return False, ""

def extract_text(cand):
    p = cand.get("profile", {})
    text_parts = [
        p.get("headline", ""),
        p.get("summary", ""),
        p.get("current_title", "")
    ]
    for job in cand.get("career_history", []):
        text_parts.append(job.get("title", ""))
        text_parts.append(job.get("description", ""))
    for s in cand.get("skills", []):
        text_parts.append(s.get("name", ""))
    for e in cand.get("education", []):
        text_parts.append(e.get("field_of_study", ""))
        text_parts.append(e.get("degree", ""))
    raw_text = " ".join(text_parts)
    return apply_taxonomy_mapping(raw_text)

def score_candidate_heuristics(cand, bm25_score, max_bm25):
    # 1. Experience Score (JD asks for 5-9 years)
    years_of_experience = cand.get("profile", {}).get("years_of_experience", 0)
    if 5.0 <= years_of_experience <= 9.0:
        exp_score = 1.0
    elif years_of_experience < 5.0:
        # Steep penalty for underqualification
        exp_score = max(0.0, 1.0 - (5.0 - years_of_experience) * 0.25)
    else:
        # Slow decay for overqualification
        exp_score = max(0.6, 1.0 - (years_of_experience - 9.0) * 0.05)
        
    # 2. Skills Match Score
    skills = [apply_taxonomy_mapping(s.get("name", "")) for s in cand.get("skills", [])]
    matched_skills = [s for s in skills if s in AI_SKILLS or any(ws in s or s in ws for ws in AI_SKILLS)]
    skills_match_score = len(set(matched_skills)) / len(AI_SKILLS) if AI_SKILLS else 0.0
    skills_match_score = min(1.0, skills_match_score * 4.0)
    
    # 3. Consulting Firm Penalty
    companies = [job.get("company", "").strip().lower() for job in cand.get("career_history", [])]
    is_consulting_only = False
    if companies:
        is_consulting_only = all(any(cf in c for cf in CONSULTING_FIRMS) for c in companies)
    consulting_multiplier = 0.5 if is_consulting_only else 1.0
    
    # 4. Notice Period Modifier
    signals = cand.get("redrob_signals", {})
    notice_days = signals.get("notice_period_days", 60)
    if notice_days <= 15:
        notice_multiplier = 1.05
    elif notice_days <= 30:
        notice_multiplier = 1.0
    elif notice_days <= 60:
        notice_multiplier = 0.95
    elif notice_days <= 90:
        notice_multiplier = 0.85
    else:
        notice_multiplier = 0.70
        
    # 5. Location Fit Modifier
    loc = cand.get("profile", {}).get("location", "").lower()
    country = cand.get("profile", {}).get("country", "").lower()
    willing_relocate = signals.get("willing_to_relocate", False)
    
    target_locations = ["pune", "noida", "mumbai", "hyderabad", "delhi", "ncr", "gurgaon", "ghaziabad", "faridabad"]
    is_in_target = any(t in loc for t in target_locations)
    is_in_india = ("india" in country) or (cand.get("profile", {}).get("country") == "India") or is_in_target
    
    location_multiplier = 1.0
    if not is_in_target:
        if willing_relocate:
            location_multiplier = 0.95
        else:
            location_multiplier = 0.7
            
    if not is_in_india and not willing_relocate:
        location_multiplier = 0.4
        
    # 6. Behavioral Signal Modifiers
    completeness = signals.get("profile_completeness_score", 100) / 100.0
    response_rate = signals.get("recruiter_response_rate", 0.5)
    last_active = signals.get("last_active_date", "2026-01-01")
    
    # Active penalty (assuming current is June 2026)
    active_multiplier = 1.0
    try:
        y, m, _ = map(int, last_active.split("-"))
        months_inactive = (2026 - y) * 12 + (6 - m)
        if months_inactive > 6:
            active_multiplier = max(0.5, 1.0 - (months_inactive - 6) * 0.05)
    except:
        pass
        
    behavior_score = (0.4 * response_rate) + (0.3 * completeness) + (0.3 * signals.get("interview_completion_rate", 1.0))
    behavior_score = max(0.1, behavior_score)
    
    # Compile scores
    tech_fit = (0.4 * (bm25_score / max_bm25 if max_bm25 > 0 else 0.0)) + (0.3 * skills_match_score) + (0.3 * exp_score)
    ops_fit = behavior_score
    
    combined = (0.7 * tech_fit) + (0.3 * ops_fit)
    final_score = combined * consulting_multiplier * notice_multiplier * location_multiplier * active_multiplier
    return final_score, tech_fit, ops_fit

def generate_reasoning(cand, score):
    p = cand.get("profile", {})
    name = p.get("anonymized_name", "Candidate")
    exp = p.get("years_of_experience", 0.0)
    title = p.get("current_title", "Engineer")
    signals = cand.get("redrob_signals", {})
    notice = signals.get("notice_period_days", 30)
    resp = int(signals.get("recruiter_response_rate", 0.5) * 100)
    
    # Extract matched skills
    skills = [s.get("name", "") for s in cand.get("skills", [])]
    matched = [s for s in skills if s.lower() in AI_SKILLS or any(ws in s.lower() or s.lower() in ws for ws in AI_SKILLS)]
    matched_str = ", ".join(list(set(matched))[:3]) if matched else "applied ML"
    
    # Check notice and relocation warnings
    loc = p.get("location", "")
    willing = signals.get("willing_to_relocate", False)
    
    reason = f"{name} is a {title} with {exp} years experience, matching the JD's stack in {matched_str}."
    
    # Add behavioral metrics
    reason += f" Demonstrates strong responsiveness ({resp}% response rate) and available on a {notice}-day notice."
    
    # Add warnings if applicable
    if notice >= 90:
        reason += f" Note: carries a longer {notice}-day notice period."
    elif notice <= 15:
        reason += f" Available immediately (sub-15-day notice)."
        
    return reason

def main():
    parser = argparse.ArgumentParser(description="Hackathon Candidate Ranking System")
    parser.add_argument("--candidates", required=True, help="Path to candidates.jsonl file")
    parser.add_argument("--out", required=True, help="Path to write output submission.csv")
    args = parser.parse_args()
    
    start_time = time.time()
    candidates = []
    honeypot_count = 0
    
    print("Reading and filtering candidate dataset...")
    with open(args.candidates, "r", encoding="utf-8") as f:
        for line in f:
            cand = json.loads(line)
            is_hp, reason = is_honeypot(cand)
            if is_hp:
                honeypot_count += 1
            else:
                candidates.append(cand)
                
    print(f"Loaded {len(candidates)} active candidates. Screened out {honeypot_count} honeypots in {time.time() - start_time:.2f}s.")
    
    # 1. Lexical BM25 Filtering (Funnel from 100,000 to 2,000)
    print("Tokenising and indexing active pool...")
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
             
    print("Scoring candidates against job description using BM25...")
    bm25_scores = []
    for idx, tokens in enumerate(corpus):
        score = bm25.get_score(tokens, query)
        bm25_scores.append((candidates[idx], score))
        
    bm25_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Select the top 2000 for deep embedding/cross-encoder re-ranking
    funnel_n = min(2000, len(bm25_scores))
    top_funneled = bm25_scores[:funnel_n]
    
    max_bm25 = max([x[1] for x in top_funneled]) if top_funneled else 1.0
    print(f"BM25 Lexical search completed. Funneled to top {funnel_n} in {time.time() - start_time:.2f}s.")
    
    # 2. Local Dense Embeddings (Stage 2 Re-ranking on Funneled Pool)
    print("Loading local SentenceTransformer model...")
    model = SentenceTransformer(BI_ENCODER_PATH)
    
    jd_reqs = ("Looking for a Senior AI Engineer with 5-9 years of experience, strong Python, "
               "deployed embeddings-based retrieval systems, vector databases (FAISS, Pinecone, Qdrant), "
               "hybrid search, and ranking evaluation frameworks (NDCG, MAP). Pune/Noida preferred.")
    jd_vector = model.encode([jd_reqs], convert_to_numpy=True)[0]
    
    print("Generating semantic embeddings for the top pool...")
    summaries = [x[0]["profile"]["summary"] for x in top_funneled]
    embeddings = model.encode(summaries, convert_to_numpy=True)
    
    # Normalise embeddings for exact cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    embeddings = embeddings / norms
    jd_vector = jd_vector / np.linalg.norm(jd_vector)
    similarities = np.dot(embeddings, jd_vector)
    
    # Score heuristically
    scored_pool = []
    for i, (cand, b_score) in enumerate(top_funneled):
        sim_score = float(similarities[i])
        h_score, tech_fit, ops_fit = score_candidate_heuristics(cand, b_score, max_bm25)
        # Combined Score: 60% Heuristic/Signals + 40% Semantic Similarity
        final_score = 0.6 * h_score + 0.4 * sim_score
        
        scored_pool.append({
            "cand": cand,
            "score": final_score,
            "tech_score": tech_fit,
            "ops_score": ops_fit,
            "sim_score": sim_score
        })
        
    scored_pool.sort(key=lambda x: x["score"], reverse=True)
    
    # 3. Cross-Encoder Joint Re-ranking (Stage 3 Re-ranking on Top 200)
    cross_n = min(200, len(scored_pool))
    top_cross = scored_pool[:cross_n]
    
    print(f"Loading local Cross-Encoder...")
    cross_encoder = CrossEncoder(CROSS_ENCODER_PATH)
    
    cross_inputs = [[jd_reqs, x["cand"]["profile"]["summary"]] for x in top_cross]
    cross_scores = cross_encoder.predict(cross_inputs)
    
    final_ranked_shortlist = []
    for i, x in enumerate(top_cross):
        raw_cross = float(cross_scores[i])
        norm_cross = 1 / (1 + np.exp(-raw_cross))  # Sigmoid scaling
        
        # Combine: 50% Cross-Encoder joint semantic overlap + 50% Heuristic/Signals score
        final_score = 0.5 * norm_cross + 0.5 * x["score"]
        final_ranked_shortlist.append((x["cand"], round(final_score, 4)))
        
    # Sort by final score descending, breaking ties with candidate_id alphabetically ascending
    final_ranked_shortlist.sort(key=lambda x: (-x[1], x[0]["candidate_id"]))
    
    # 4. Generate Top 100 CSV Submission
    print(f"Exporting Top 100 candidates to: {args.out}")
    csv_rows = []
    
    for rank_idx in range(1, 101):
        if rank_idx - 1 < len(final_ranked_shortlist):
            cand, score = final_ranked_shortlist[rank_idx - 1]
            reason = generate_reasoning(cand, score)
            csv_rows.append({
                "candidate_id": cand["candidate_id"],
                "rank": rank_idx,
                "score": score,
                "reasoning": reason
            })
        else:
            # Fallback if active pool is less than 100 (not expected in 100k)
            csv_rows.append({
                "candidate_id": f"CAND_0000000",
                "rank": rank_idx,
                "score": 0.0,
                "reasoning": "Fallback profile due to pool exhaustion."
            })
            
    # Resolve score sorting anomalies to guarantee monotonic non-increasing scores
    # (Ties are allowed, but score must strictly not increase as rank increases)
    for i in range(len(csv_rows) - 1):
        if csv_rows[i]["score"] < csv_rows[i+1]["score"]:
            csv_rows[i+1]["score"] = csv_rows[i]["score"]
            
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate_id", "rank", "score", "reasoning"])
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)
            
    print(f"Completed in {time.time() - start_time:.2f} seconds!")

if __name__ == "__main__":
    main()
