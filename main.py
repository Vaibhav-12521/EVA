from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the chatbot function
try:
    from chatbot import ChatBot as ChatBotFunction
    CHATBOT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import chatbot: {e}")
    CHATBOT_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """Serve the main HTML file"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>File Not Found</title>
        </head>
        <body>
            <h1>Error: index.html not found</h1>
            <p>Make sure index.html is in the same directory as this server file.</p>
        </body>
        </html>
        """, 404

@app.route('/styles.css')
def styles():
    """Serve the CSS file"""
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/css'}
    except FileNotFoundError:
        return "/* CSS file not found */", 404, {'Content-Type': 'text/css'}

@app.route('/script.js')
def script():
    """Serve the JavaScript file"""
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'application/javascript'}
    except FileNotFoundError:
        return "// JavaScript file not found", 404, {'Content-Type': 'application/javascript'}

@app.route('/chat', methods=['GET'])
def chat_status():
    """Check if the chat service is available"""
    if CHATBOT_AVAILABLE:
        return jsonify({
            'status': 'available',
            'message': 'Chatbot service is running'
        })
    else:
        return jsonify({
            'status': 'unavailable',
            'message': 'Chatbot service is not available'
        }), 503

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        if not CHATBOT_AVAILABLE:
            return jsonify({
                'error': 'Chatbot service is not available',
                'response': 'Sorry, the AI chatbot service is currently unavailable. Please check the backend configuration.'
            }), 503

        # Get the message from the request
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Invalid request format',
                'response': 'Please provide a message in the request body.'
            }), 400

        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'response': 'Please provide a non-empty message.'
            }), 400

        # Get response from the chatbot
        try:
            bot_response = ChatBotFunction(user_message)
            
            if not bot_response:
                bot_response = "I'm sorry, I couldn't generate a response. Please try again."
            
            return jsonify({
                'response': bot_response,
                'status': 'success'
            })
            
        except Exception as chatbot_error:
            print(f"Chatbot error: {chatbot_error}")
            return jsonify({
                'error': 'Chatbot processing error',
                'response': 'I encountered an error while processing your message. Please try again.'
            }), 500

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({
            'error': 'Server error',
            'response': 'An unexpected server error occurred. Please try again.'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'chatbot_available': CHATBOT_AVAILABLE,
        'timestamp': str(__import__('datetime').datetime.now())
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found.'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred.'
    }), 500

if __name__ == '__main__':
    # Check if required files exist
    required_files = ['index.html', 'styles.css', 'script.js']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"Warning: Missing files: {', '.join(missing_files)}")
        print("Make sure all HTML, CSS, and JS files are in the same directory as this server.")
    
    # Check if .env file exists for the chatbot
    if not os.path.exists('.env'):
        print("Warning: .env file not found. Make sure it contains GroqAPIKey, Username, and Assistantname.")
    
    print("Starting Flask server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',  # Accept connections from any IP
        port=5000,
        debug=True,
        threaded=True
    )