"""
Content Repurposer Backend
Converts videos to platform-specific formats
"""

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import tempfile
from werkzeug.utils import secure_filename
from utils.video_processor import VideoProcessor
from utils.claude_optimizer import ClaudeOptimizer

load_dotenv()

app = Flask(__name__)
CORS(app)

# Config
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'webm', 'avi', 'mkv'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

processor = VideoProcessor()
optimizer = ClaudeOptimizer()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'service': 'content-repurposer-api'})


@app.route('/api/repurpose', methods=['POST'])
def repurpose_video():
    """
    Convert video to platform-specific versions

    Request:
        - video: File upload (mp4, mov, webm, etc)
        - watermark: bool (optional, default false)

    Response:
        - {
            "id": "uuid",
            "status": "processing",
            "formats": {
              "tiktok": {"url": "/download/...", "status": "done"},
              "instagram": {"url": "/download/...", "status": "done"},
              ...
            }
          }
    """
    try:
        # Check if file in request
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {ALLOWED_EXTENSIONS}'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get options
        add_watermark = request.form.get('watermark', 'false').lower() == 'true'

        # Process video
        repurposed = processor.repurpose(filepath, add_watermark=add_watermark)

        # Cleanup
        os.remove(filepath)

        return jsonify({
            'status': 'success',
            'formats': repurposed,
            'message': 'Video repurposed to all platforms'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimize-caption', methods=['POST'])
def optimize_caption():
    """
    (Phase 2) Use Claude to optimize caption for platform

    Request:
        - caption: str
        - platform: "tiktok" | "instagram" | "youtube" | "linkedin"

    Response:
        - {"optimized_caption": "...", "hashtags": ["#..."], "emojis": ["🎬", ...]}
    """
    try:
        data = request.get_json()
        caption = data.get('caption', '')
        platform = data.get('platform', 'instagram')

        if not caption:
            return jsonify({'error': 'Caption required'}), 400

        optimized = optimizer.optimize_for_platform(caption, platform)

        return jsonify({
            'status': 'success',
            'optimized_caption': optimized['caption'],
            'hashtags': optimized['hashtags'],
            'emojis': optimized['emojis']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """Download repurposed video file"""
    try:
        # TODO: Implement file serving from storage
        # For now, placeholder
        return jsonify({'error': 'Download endpoint not yet implemented'}), 501
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    """Serve frontend"""
    return jsonify({'message': 'Content Repurposer API', 'version': '0.1.0'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
