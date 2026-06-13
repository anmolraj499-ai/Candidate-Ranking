import os
from sentence_transformers import SentenceTransformer, CrossEncoder

models_dir = "c:/Users/anmol/OneDrive/Pictures/candidate ranking1/redrob_hackathon/models"
os.makedirs(models_dir, exist_ok=True)

bi_encoder_path = os.path.join(models_dir, "all-MiniLM-L6-v2")
cross_encoder_path = os.path.join(models_dir, "ms-marco-MiniLM-L-6-v2")

print("Downloading bi-encoder (SentenceTransformer)...")
bi_encoder = SentenceTransformer("all-MiniLM-L6-v2")
bi_encoder.save(bi_encoder_path)
print(f"Bi-encoder saved to {bi_encoder_path}")

print("Downloading cross-encoder...")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
cross_encoder.model.save_pretrained(cross_encoder_path)
cross_encoder.tokenizer.save_pretrained(cross_encoder_path)
print(f"Cross-encoder saved to {cross_encoder_path}")

print("All models successfully cached locally!")
