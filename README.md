#  SharkTankAI: AI-Powered Classifier for Detecting Overpromising Startup Pitches

**SharkTankAI** is an intelligent, end-to-end platform built to assist investors, accelerators, and analysts in identifying **overpromising or exaggerated claims** in startup pitch descriptions. By leveraging cutting-edge transformer-based NLP models, this system flags unrealistic promises and helps filter high-risk proposals early in the funding pipeline.

Designed with a user-friendly Streamlit interface and powered by a fine-tuned DistilBERT model, the app delivers real-time classification of pitches as either **realistic** or **overpromising**, based on linguistic patterns learned from thousands of annotated startup descriptions.

---

##  Key Features

- **Transformer-Based NLP Model**: Fine-tuned `distilbert-base-uncased` classifier trained on 2000+ labeled startup pitches.
- **Real-Time Inference**: Upload or paste a startup pitch and get an instant prediction with probability scores.
- **VC-Ready Screening Tool**: Built for use in venture capital workflows, demo days, or internal startup filtering tools.
- **Lightweight Interface**: Built using Streamlit for a clean, accessible frontend experience.
- **Fully Transparent Pipeline**: Training notebooks and dataset included for reproducibility and experimentation.

---

##  Tech Stack

| Layer       | Tools Used                               |
|-------------|-------------------------------------------|
| Frontend    | `Streamlit`, `Pandas`, `Matplotlib`      |
| Backend     | `Python`, `PyTorch`, `Transformers` (Hugging Face) |
| NLP Models  | `TF-IDF + Logistic Regression`, `BERT`, `RoBERTa`, `DistilBERT` |
| Evaluation  | `scikit-learn`, `seaborn`, `confusion matrix`, `F1`, `precision`, `recall` |

---

##  Model Training

The included model was trained on a labeled dataset of startup pitches with binary annotations:
- **0** – Realistic
- **1** – Overpromising

### Training Details:
- Optimizer: `AdamW`
- Learning Rate: `2e-5`
- Epochs: `3–15`
- Loss Function: `CrossEntropyLoss`
- Evaluation: After each epoch
- Environment: Google Colab (T4 GPU)

Complete training pipeline (including preprocessing, tokenization, training loop, evaluation, and metrics) is available in the repo.

---

##  Results

| Model         | Accuracy | Precision | Recall | F1 Score |
|---------------|----------|-----------|--------|----------|
| TF-IDF        | 72.1%    | 70.4%     | 74.3%  | 72.3%    |
| DistilBERT    | 90.0%    | 89.1%     | 90.7%  | 89.9%    |
| BERT          | 91.3%    | 90.8%     | 92.1%  | 91.4%    |
| RoBERTa       | 93.1%    | 92.5%     | 93.8%  | 93.1%    |

>  *DistilBERT* was selected for deployment due to its optimal speed-performance balance.

---

##  Project Structure

