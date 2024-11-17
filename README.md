# **Sentiment Analysis on Call Transcripts**

This project is a sentiment analysis application designed to process call transcripts, extract insights about the overall sentiment, engagement, and speaker-specific metrics. Users can upload their call transcripts via a **Streamlit-based UI**, and the backend (built using Flask) performs the sentiment analysis using pre-trained models.

---

## **Features**
- Upload call transcripts (text files) via a user-friendly Streamlit interface.
- Analyze sentiment at the utterance, speaker, and overall conversation levels.
- Provides metrics such as:
  - Overall sentiment score.
  - Engagement score.
  - Speaker-specific sentiment averages.
  - Confidence based on sentiment consistency.
- Highlights positive and negative phrases for additional insights.

---

## **Technologies Used**
- **Backend:** Flask
- **Frontend:** Streamlit
- **Models:** Hugging Face Transformers
  - `microsoft/DialogRPT-updown` (dialogue engagement analysis)
  - `distilbert-base-uncased-finetuned-sst-2-english` (general sentiment analysis)
- **Libraries:**
  - `torch`, `transformers`, `numpy`, `re`

---

## **Installation and Setup**

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd sentiment-analysis
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask Backend**
   Navigate to the directory containing the `run.py` file and run:
   ```bash
   python run.py
   ```
   The Flask backend will start on `http://127.0.0.1:5000`.

5. **Run the Streamlit Frontend**
   Navigate to the directory containing the Streamlit app file (`ui/app.py`) and run:
   ```bash
   streamlit run app.py
   ```
   The Streamlit interface will open in your default browser.

---

## **Usage**
1. Open the Streamlit application in your browser.
2. Upload a call transcript file (supported format: `.txt`).
3. View the sentiment analysis results, including:
   - Speaker-specific sentiment metrics.
   - Overall sentiment and engagement scores.
   - Detailed insights into positive and negative phrases.

---

## **Project Structure**
```
sentiment-analysis/
│
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # Flask API routes
│   ├── sentiment.py          # Sentiment analysis logic
│   └── utils.py              # Utility functions (file handling, preprocessing)
│
├── ui/
│   ├── app.py                # Streamlit frontend application
│
├── run.py                 
│
├── uploads/                  # Folder to store uploaded files
│
├── requirements.txt          # Required Python libraries
├── README.md                 # Project documentation
└── .gitignore                # Git ignore file
```

---

## **Screenshots**
<img width="953" alt="image" src="https://github.com/user-attachments/assets/937b49e9-ad9a-49d7-b853-92de0eabe2c7">
<img width="958" alt="image" src="https://github.com/user-attachments/assets/5b8d2fbf-21bc-4882-9bcd-77e6f0e71c1c">
<img width="451" alt="image" src="https://github.com/user-attachments/assets/e25e30ff-3c44-4ddd-8aae-eaef1dd4c053">



