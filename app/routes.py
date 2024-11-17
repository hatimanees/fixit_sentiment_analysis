# app/routes.py (Flask backend)
from flask import Blueprint, request, jsonify, current_app
from app.sentiment import analyze_sentiment
from app.utils import save_uploaded_file
import os

main = Blueprint('main', __name__)


@main.route('/upload', methods=['POST'])
def upload_transcript():
    try:
        # Get the transcript from form data
        transcript = request.form.get('transcript')
        if not transcript:
            return jsonify({'error': 'No transcript received'}), 400

        # Get the upload folder from current_app config
        upload_folder = current_app.config['UPLOAD_FOLDER']

        # Save transcript to temporary file
        file_path = os.path.join(upload_folder, 'temp_transcript.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(transcript)

        # Analyze sentiment
        sentiment_result = analyze_sentiment(file_path)

        # Clean up the temporary file
        os.remove(file_path)

        return jsonify({'sentiment': sentiment_result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500