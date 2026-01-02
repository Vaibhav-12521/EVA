# AI Chatbot with Web UI

A beautiful, animated web interface for an AI chatbot powered by Groq API.

## Features

- 🎨 **Beautiful Animated Interface**: Modern, responsive design with smooth animations
- 🤖 **AI-Powered Responses**: Uses Groq API with Llama model for intelligent conversations
- 💬 **Real-time Chat**: Live messaging with typing indicators
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎭 **Demo Mode**: Works offline for testing the interface
- 💾 **Chat History**: Persistent conversation history
- ⚡ **Fast & Lightweight**: Quick responses and minimal resource usage

## Quick Start

### Windows
1. Double-click `start.bat` to automatically set up and run the application
2. Open your browser and go to `http://localhost:5000`

### Manual Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
   ```
   Username=YourName
   Assistantname=AI Assistant
   GroqAPIKey=your_groq_api_key_here
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
ai_with_ui/
├── app.py              # Flask web server
├── index.html          # Main chat interface
├── styles.css          # UI styling and animations
├── script.js           # Client-side functionality
├── start.bat           # Windows startup script
├── requirements.txt    # Python dependencies
├── backend/
│   └── chatbot.py     # AI chatbot logic
└── Data/
    └── ChatLog.json   # Chat history storage
```

## Configuration

Create a `.env` file in the root directory with the following variables:

- `Username`: Your display name
- `Assistantname`: The AI assistant's name
- `GroqAPIKey`: Your Groq API key (get it from [Groq Console](https://console.groq.com/))

## API Endpoints

- `GET /`: Main chat interface
- `POST /chat`: Send message to chatbot
- `GET /health`: Health check
- `GET /chat`: Check chatbot availability

## Demo Mode

If the backend is not available or configured, the interface will run in demo mode, allowing you to test the UI functionality with simulated responses.

## Customization

### Styling
Edit `styles.css` to customize:
- Colors and gradients
- Animation speeds and effects
- Layout and spacing
- Responsive breakpoints

### Functionality
Edit `script.js` to modify:
- Chat behavior
- Message formatting
- Keyboard shortcuts
- Error handling

### Backend
Edit `backend/chatbot.py` to customize:
- AI model settings
- Response processing
- Chat history management
- System prompts

## Requirements

- Python 3.7+
- Groq API key
- Modern web browser

## Troubleshooting

1. **Port already in use**: Change the port in `app.py` line with `app.run(port=5000)`
2. **Missing .env file**: Create the file with required variables
3. **API errors**: Check your Groq API key and internet connection
4. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## License

This project is open source and available under the MIT License.