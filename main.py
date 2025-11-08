# ================================================
# Conversational Emotion AI Pipeline
# ================================================
import sentiment 
import audio_to_text
import requests
import http_request

def main_pipeline(audio_file_path,phone):
    try:
        # 1️⃣ Transcribe audio input
        text = audio_to_text.transcribe_audio(audio_file_path)
        print("Transcription:", text)

        # 2️⃣ Analyze sentiment
        sentiment_data = sentiment.analyze_sentiment(audio_file_path)
        print("Sentiment:", sentiment_data)


        # 4️⃣ Validate and process emotions
      #  validated_emotions = validate_emotions(sentiment_data)
       # print("Validated Emotions:", validated_emotions)

        # 5️⃣ Append emotions to text for context
        emotion_info = f'Note that I am feeling this emotion, adjust your answer accordingly:{sentiment_data}. Do not mention my emotional state'
        emotion_enriched_text = text + emotion_info
        print("Emotion-Enriched Text:", emotion_enriched_text)

        # 6️⃣ Send data via HTTP POST request
        #url = "https://antoniompvsarafana.app.n8n.cloud/webhook-test/upload-audio"


        http_request.transition(emotion_enriched_text, phone)


    except Exception as e:
        # Handle and log any error
        #handle_error(e)
        print("Error in pipeline:", e)

