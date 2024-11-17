# app/sentiment.py
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import List, Dict
import torch
import re


class DialogueSentimentAnalyzer:
    def __init__(self, model_name: str = "microsoft/DialogRPT-updown"):
        """
        Initialize with a model specifically trained for dialogue analysis
        """
        self.device = 0 if torch.cuda.is_available() else -1

        # Initialize both dialogue-specific and general sentiment models
        self.dialogue_model = pipeline(
            'text-classification',
            model="microsoft/DialogRPT-updown",
            device=self.device
        )

        self.sentiment_model = pipeline(
            'sentiment-analysis',
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=self.device
        )

        self.max_length = 512

    def parse_dialogue(self, text: str) -> List[Dict]:
        """
        Parse dialogue into structured format
        """
        # Split into utterances
        lines = text.strip().split('\n')
        dialogue = []

        current_speaker = None
        current_text = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for speaker change
            speaker_match = re.match(r'^([^:]+):', line)
            if speaker_match:
                # Save previous speaker's text if exists
                if current_speaker and current_text:
                    dialogue.append({
                        'speaker': current_speaker,
                        'text': ' '.join(current_text)
                    })

                # Start new speaker
                current_speaker = speaker_match.group(1)
                current_text = [line[len(current_speaker) + 1:].strip()]
            else:
                # Continue current speaker's text
                if current_speaker:
                    current_text.append(line.strip())

        # Add final speaker's text
        if current_speaker and current_text:
            dialogue.append({
                'speaker': current_speaker,
                'text': ' '.join(current_text)
            })

        return dialogue

    def analyze_utterance(self, utterance: Dict) -> Dict:
        """
        Analyze single utterance with both dialogue and sentiment models
        """
        text = utterance['text']

        # Get dialogue engagement score
        dialogue_score = self.dialogue_model(text)[0]

        # Get sentiment score
        sentiment = self.sentiment_model(text)[0]

        # Analyze key phrases
        positive_phrases = [
            'thank you', 'thanks', 'appreciate', 'great', 'perfect',
            'looking forward', 'flexible', 'competitive'
        ]
        negative_phrases = [
            'concerned', 'worry', 'issue', 'problem', 'difficult',
            'unfortunately', 'sorry'
        ]

        # Count phrase occurrences
        text_lower = text.lower()
        positive_count = sum(1 for phrase in positive_phrases if phrase in text_lower)
        negative_count = sum(1 for phrase in negative_phrases if phrase in text_lower)

        # Combine scores with phrase analysis
        sentiment_score = float(sentiment['score'])
        if sentiment['label'] == 'NEGATIVE':
            sentiment_score = 1 - sentiment_score

        # Adjust score based on phrase counts
        final_score = sentiment_score
        if positive_count > negative_count:
            final_score = min(1.0, final_score + 0.1 * (positive_count - negative_count))
        elif negative_count > positive_count:
            final_score = max(0.0, final_score - 0.1 * (negative_count - positive_count))

        return {
            'speaker': utterance['speaker'],
            'text': text,
            'sentiment_score': final_score,
            'engagement_score': float(dialogue_score['score']),
            'positive_phrases': positive_count,
            'negative_phrases': negative_count
        }

    def analyze_dialogue(self, text: str) -> List[Dict]:
        """
        Analyze full dialogue with detailed results
        """
        # Parse dialogue
        dialogue = self.parse_dialogue(text)

        # Analyze each utterance
        utterance_results = [self.analyze_utterance(utterance) for utterance in dialogue]

        # Calculate overall metrics
        overall_sentiment = np.mean([r['sentiment_score'] for r in utterance_results])
        overall_engagement = np.mean([r['engagement_score'] for r in utterance_results])

        # Calculate confidence based on consistency
        sentiment_variance = np.std([r['sentiment_score'] for r in utterance_results])
        confidence = max(0.0, 1.0 - sentiment_variance)

        # Analyze conversation flow
        speaker_sentiments = {}
        for result in utterance_results:
            if result['speaker'] not in speaker_sentiments:
                speaker_sentiments[result['speaker']] = []
            speaker_sentiments[result['speaker']].append(result['sentiment_score'])

        # Calculate per-speaker metrics
        speaker_averages = {
            speaker: np.mean(scores)
            for speaker, scores in speaker_sentiments.items()
        }

        return [{
            'label': 'Overall Sentiment',
            'score': float(overall_sentiment)
        }, {
            'label': 'Confidence',
            'score': float(confidence)
        }, {
            'label': 'Engagement',
            'score': float(overall_engagement)
        }] + [
            {
                'label': f'{speaker} Sentiment',
                'score': float(score)
            }
            for speaker, score in speaker_averages.items()
        ]


def analyze_sentiment(file_path: str) -> List[Dict]:
    """
    Analyze sentiment of dialogue in the file
    """
    try:
        analyzer = DialogueSentimentAnalyzer()

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        return analyzer.analyze_dialogue(text)

    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        return [{
            'label': 'Error',
            'score': 0.5
        }]