# Redrob Hackathon Candidate Ranking System

An offline, CPU-only, production-grade candidate ranking system designed to discover the top 100 matches for the **Senior AI Engineer — Founding Team** role from a pool of 100,000 profiles (`candidates.jsonl`).

## System Architecture

Our solution utilizes a multi-stage funnel designed to run efficiently on a 16GB CPU-only machine within a 5-minute time limit:

```
                  [100,000 Candidates Pool]
                             │
                             ▼
              [Programmatic Honeypot Filter] (Screen out impossible profiles)
                             │
                             ▼
                  [BM25 Lexical Funnel] (Filters pool down to top 2,000)
                             │
                             ▼
            [Local SentenceTransformer Embeddings] (all-MiniLM-L6-v2)
                             │
                             ▼
              [Advanced Modifiers & Modulations] (Experience fit & Redrob signals)
                             │
                             ▼
             [Local Cross-Encoder Re-ranking] (ms-marco-MiniLM-L-6-v2)
                             │
                             ▼
                    [Top 100 Selection] (Deterministic tie-breaking)
```

1. **Stream-Parsing & Honeypot Filtering**: Reads the JSONL file line-by-line to minimize RAM usage. Excludes trap profiles with incoherent timelines (e.g. experience exceeding years since graduation) or skills fraud (expert proficiency with 0 months duration).
2. **Stage 1 (Lexical Search)**: Funnels the pool from 100,000 candidates to the top 2,000 candidates using a custom BM25 index over target keywords (PyTorch, vector databases, RAG, etc.). Runs in ~10 seconds.
3. **Stage 2 (Local Semantic Embedding)**: Generates dense embeddings for the top 2,000 candidate summaries on CPU using cached SentenceTransformer weights, calculating L2-normalized cosine similarity. Runs in ~15 seconds.
4. **Stage 3 (Advanced Modulation)**: Applies specialized modifiers (experience fit, notice period agility, relocation, and recruiter activity signals).
5. **Stage 4 (Cross-Encoder Re-ranking)**: Evaluates the top 200 candidates with a local Cross-Encoder to compute a joint semantic-context score, selecting the final top 100. Runs in ~2 seconds.
6. **Reasoning Generation**: Programmatically writes specific, honest, fact-based 1-2 sentence rationales referencing actual experience, titles, skills, and notice periods to ensure zero hallucinations.

---

## Installation & Setup

All required model weights are pre-downloaded and checked into the `models/` directory, ensuring **zero network calls** are made during execution.

### Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

---

## Reproduction Command

To run the pipeline and generate the submission CSV, execute the following command at the repository root:

```bash
python rank.py --candidates ./candidates.jsonl --out ./team_2+.csv
```

### Format Validation
To verify the output CSV matches the hackathon submission format:
```bash
python validate_submission.py team_2+.csv
```

---

## Interactive Sandbox Demo

We have built a premium, interactive web dashboard using Gradio to showcase the multi-stage pipeline's behavior in real-time.

To launch the dashboard locally, run:
```bash
python app.py
```
Then open `http://127.0.0.1:7860/` in your browser. 

This app allows you to:
* View a live ranking shortlist leaderboard.
* Upload a custom candidate profile list or edit the Job Description in real-time.
* Click on any candidate to inspect their headline, summary, skills tags, and detailed score meters (Technical Stack Match, Behavioral Signals, and Joint Cross-Attention Similarity).
* Download the validated format-compliant CSV shortlist directly.

