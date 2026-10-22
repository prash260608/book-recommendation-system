# 📜 The Enchanted Athenaeum — Book Recommendation Engine

An interactive, theme-switchable book recommendation engine built with Python, Streamlit, and Scikit-learn. Utilizing **TruncatedSVD Matrix Factorization** on the Goodbooks-10k dataset, *The Enchanted Athenaeum* computes item-to-item latent vector similarities in real time to uncover personalized book recommendations based on collective reader behavior.

---

## ✨ Features

* **Latent Matrix Factorization:** Employs `TruncatedSVD` to decompose user-item rating interaction matrices into 30-dimensional latent representations.
* **Instant Item Similarity Search:** Computes normalized cosine similarities ($L_2$ normalized dot-products) across 10,000+ volumes in under 1ms.
* **Dual Aesthetic UI (Custom CSS Injection):**
  * 🌙 **Dark Academia Mode:** Cowhide cocoa, toasted caramel, and spiced wine tones with antique serif styling (`Playfair Display`, `PoisonedHeart`).
  * 🌸 **Cottagecore Mode:** Parchment surfaces, linen accents, and sage highlights (`Almendra`, `Anaktoria`).
* **Dynamic Font Engine:** Features custom Base64 local font loader with automatic Google Fonts fallback.
* **Interactive Filtering:** Customize recommendation counts dynamically via Streamlit widgets.

---

## 🛠️ Tech Stack

| Domain | Tools & Libraries |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Machine Learning** | `scikit-learn` (`TruncatedSVD`) |
| **Data & Linear Algebra** | `pandas`, `numpy`, `scipy` |
| **Frontend & UI** | `streamlit` |
| **Dataset** | Goodbooks-10k (Goodreads) |

---

## 📁 Repository Structure

```text
.
├── app.py                   # Main Streamlit web application & CSS UI logic
├── svd_cf_model.pkl         # Trained TruncatedSVD model weights & feature vectors
├── final_dataset.csv        # Processed book metadata & mapped lookup table
├── requirements.txt         # Environment dependencies
└── README.md                # Project documentation
