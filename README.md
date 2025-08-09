# 🧠 Task: Extend and Analyze a League of Legends Champion Embedding Framework

You are a highly capable AI assistant helping a user refine a machine learning pipeline for embedding **League of Legends (LoL) champions** based on their in-game mechanics, strategic roles, and gameplay behavior. The user has already built a strong foundation using a fine-tuned LLaMA-based model and now seeks deeper insights, optimizations, or conceptual extensions.

---

## 🔧 Context

The user’s current pipeline works as follows:

### 🏗 Model Architecture
- **Base model**: LoRA + instruction fine-tuned **LLaMA 3.2B**, trained on League of Legends domain data (champion descriptions, gameplay roles, item builds, etc.).
- **Embedding method**: Uses the **mean-pooled last 4 hidden layers** of the LLM.
- A **prediction head** trained with **triplet loss** is added on top of frozen LLM embeddings to learn a semantic space of champions.

### 📊 Dataset & Training
- **Champion metadata** (e.g., roles, CC type, range, power curve, etc.) is used to compute pairwise **Jaccard similarity**.
- This yields (anchor, positive, negative) **triplets of champion names**.
- Each name is replaced with a full **champion description** (or “champion card”) constructed from structured data or extracted from domain corpora.
- **Negative mining** is done via a **graph-based approach**: the champion similarity graph is constructed, and negatives are sampled from non-neighbors.
- Multiple negatives (e.g., 10) are used per positive pair to improve contrastive signal.

### 🧠 Inference Plan
- The model will be used in downstream tasks such as:
  - **Game outcome prediction** based on champion drafts
  - **Draft synergy evaluation**
- At inference time, full **champion descriptions** (not names) are used to ensure consistency with training and preserve embedding semantics.

---

## 🔍 Goals for This Session

### 1. Representation Generalization
- Explore the trade-off and distinction between two paradigms:
  - **Champion Name Embedding**: Input is the name alone (e.g., `"Ahri"`), relying on internal model knowledge.
  - **Champion Description Embedding**: Input is a full natural language rationale (the champion’s abilities and role).
- Under what conditions can the model produce useful embeddings from names alone, and how does this compare to using full descriptions?
- Would a hybrid training approach (e.g., jointly training on names and descriptions) improve robustness, or introduce noise?
- How to avoid **distributional shift** if training is done on one format and inference is done on another?

### 2. Alternative Embedding Tasks
- Beyond similarity and retrieval, what other tasks can leverage this embedding space?
  - Clustering (e.g., discover latent champion archetypes)
  - Matchup modeling (e.g., counter relationships)
  - Draft simulation or completion
  - Champion recommendation for team comp

### 3. Data Augmentation
- How to paraphrase or synthesize new champion rationales effectively without semantic drift?
- Would synthetically generated edge-case champions (e.g., via interpolation or hybridization) help enrich the embedding space?
- Can LLM-based text augmentation improve generalization?

### 4. Team-Level Semantics
- How to combine multiple champion embeddings into a **team-level representation**?
  - Simple mean-pooling vs. attention mechanisms
  - Graph-based models to capture inter-champion synergy
- How to ensure that team embeddings capture dynamics like front-to-back comp, wombo combo potential, or double poke lanes?

### 5. Evaluation Metrics
- What are suitable offline evaluation strategies?
  - Champion retrieval given a prototype or query
  - Triplet accuracy on held-out pairs
  - Winrate prediction as a proxy downstream task
- How to detect shallow matching (e.g., lexical overlap) vs. deep semantic understanding of champion roles?

---

## 📂 Dataset Resource

Public dataset used in training:  
**Champion Similarity Dataset**  
🔗 [https://huggingface.co/datasets/avinot/Champion-Similarity](https://huggingface.co/datasets/avinot/Champion-Similarity)

It includes structured champion features and natural language rationales constructed to reflect gameplay behavior and synergy.

---
