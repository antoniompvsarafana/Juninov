from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from main import main_pipeline
from pydub import AudioSegment
import tempfile
import sentiment
import audio_to_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Enable CORS for API routes so other servers can POST files
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio provided'}), 400
    
    file = request.files['audio_file']
    phone = request.form.get('phone', '')
    
    if not phone:
        return jsonify({'error': 'Phone number is required'}), 400
    
    if not file:
        return jsonify({'error': 'No audio recorded'}), 400
    
    # Save the uploaded audio (could be webm, ogg, etc.)
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
    file.save(temp_input.name)
    temp_input.close()
    
    # Convert to WAV format
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_output.close()
    
    try:
        # Load audio and convert to WAV
        audio = AudioSegment.from_file(temp_input.name)
        audio.export(temp_output.name, format="wav")
        
        # Get transcription and sentiment for display
        transcription = audio_to_text.transcribe_audio(temp_output.name)
        sentiment_label = sentiment.analyze_sentiment(temp_output.name)
        
        # Run the full pipeline
        main_pipeline(temp_output.name, phone)
        
        return jsonify({
            'success': True, 
            'message': 'Pipeline executed successfully',
            'transcription': transcription or 'Could not transcribe audio',
            'sentiment': sentiment_label
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary files
        for filepath in [temp_input.name, temp_output.name]:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass


@app.route('/api/upload_mp3', methods=['POST'])
def upload_mp3():
    """Accepts an uploaded MP3 file (form field 'file' or 'mp3') and stores it as
    uploads/last_received.mp3 (overwriting any previous file). Returns JSON.

    This endpoint is CORS-enabled above and intended to be reachable from other
    servers. It only stores the MP3 as-is; further processing can be added later.
    """
    if 'file' not in request.files and 'mp3' not in request.files:
        return jsonify({'error': 'No mp3 file provided (expected form field "file" or "mp3")'}), 400

    file = request.files.get('file') or request.files.get('mp3')

    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Ensure filename is safe, but we store to a fixed name 'last_received.mp3'
    try:
        dest_path = os.path.join(app.config['UPLOAD_FOLDER'], 'last_received.mp3')
        # If the uploaded file is not .mp3, still save it as .mp3 (caller should send mp3)
        file.save(dest_path)

        return jsonify({
            'success': True,
            'message': 'MP3 received and stored as last_received.mp3',
            'stored_path': dest_path
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Listen on 0.0.0.0 so the server can be reached from other machines/services.
    app.run(host='0.0.0.0', debug=True, port=5000)

