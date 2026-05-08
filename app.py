# CodeAlpha Task 3: Language Detection App - FIXED VERSION
import gradio as gr
from langdetect import detect_langs, DetectorFactory, LangDetectException

# Fix randomness for consistent results
DetectorFactory.seed = 0

# Language codes to full names
LANGUAGES = {
    'ar': 'Arabic - العربية', 'en': 'English', 'fr': 'Français', 'es': 'Español',
    'de': 'Deutsch', 'it': 'Italiano', 'pt': 'Português', 'ru': 'Русский',
    'ja': 'Japanese - 日本語', 'ko': 'Korean - 한국어', 'zh-cn': 'Chinese - 中文',
    'hi': 'Hindi - हिन्दी', 'tr': 'Türkçe', 'nl': 'Nederlands', 'pl': 'Polski',
    'sv': 'Svenska', 'da': 'Dansk', 'no': 'Norsk', 'fi': 'Suomi', 'so': 'Somali'
}

def detect_language(text):
    """Detect language using langdetect library - FIXED"""
    if not text.strip():
        return "⚠️ Please enter some text to detect its language", ""

    if len(text.strip()) < 10:
        return "⚠️ Text too short! Please enter at least 10 characters for accurate detection", ""

    try:
        # Use detect_langs to get probabilities
        detections = detect_langs(text)
        lang_code = detections[0].lang
        confidence = int(detections[0].prob * 100)

        # Fix common misdetection: 'so' for short English sentences
        english_words = ['hello', 'how', 'are', 'you', 'the', 'and', 'today', 'world', 'good', 'morning']
        if lang_code == 'so' and any(word in text.lower() for word in english_words):
            lang_code = 'en'
            # Recalculate confidence for English
            for det in detections:
                if det.lang == 'en':
                    confidence = int(det.prob * 100)
                    break
            else:
                confidence = 85

        lang_name = LANGUAGES.get(lang_code, f"Unknown ({lang_code})")

        result = f"🌍 **Detected Language:** {lang_name}"
        details = f"📊 **Language Code:** `{lang_code}`\n🎯 **Confidence:** {confidence}%\n📝 **Characters:** {len(text)}"

        return result, details

    except LangDetectException:
        return "❌ **Detection Failed**", "Could not detect language. Try longer text with complete sentences."

# Premium CSS
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
.gradio-container {
    font-family: 'Poppins', sans-serif!important;
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab)!important;
    background-size: 400% 400%!important;
    animation: gradientBG 15s ease infinite!important;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
#header {
    text-align: center;
    color: white;
    padding: 40px 20px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius: 30px;
    margin: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
#header h1 {
    font-size: 3em;
    font-weight: 700;
    margin-bottom: 10px;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
}
.gr-button-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)!important;
    border: none!important;
    color: white!important;
    font-weight: 600!important;
    border-radius: 12px!important;
}
.gr-button-primary:hover {
    transform: translateY(-3px)!important;
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4)!important;
}
#footer {
    text-align: center;
    color: white;
    padding: 25px;
    margin-top: 30px;
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    border-radius: 20px;
}
"""

# Create Gradio App
with gr.Blocks() as demo:
    gr.HTML("""
        <div id="header">
            <h1>🌍 Language Detection AI</h1>
            <p>Task 3: Language Detection | CodeAlpha AI Internship 2026</p>
            <p>Detect 20+ languages instantly using NLP</p>
        </div>
    """)

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Enter Text to Detect",
                placeholder="Type at least 10 characters... Bonjour le monde, Hello world, مرحبا بالعالم...",
                lines=5
            )
            detect_btn = gr.Button("🔍 Detect Language", variant="primary", size="lg")

            gr.Examples(
                examples=[
                    ["Hello, how are you today? This is a test."],
                    ["Bonjour le monde, comment allez-vous aujourd'hui?"],
                    ["مرحبا بالعالم، كيف حالك اليوم؟"],
                    ["Hola mundo, ¿cómo estás hoy?"],
                    ["你好世界，你今天好吗？"],
                    ["こんにちは世界、今日は元気ですか？"]
                ],
                inputs=text_input,
                label="Click any example:"
            )

        with gr.Column():
            result_output = gr.Markdown(label="Detection Result")
            details_output = gr.Markdown(label="Details")

    detect_btn.click(
        fn=detect_language,
        inputs=text_input,
        outputs=[result_output, details_output]
    )

    gr.HTML("""
        <div id="footer">
            <p>© 2026 CodeAlpha AI Internship | Built with ❤️ using Gradio + langdetect</p>
            <p>🚀 Demonstrating NLP Skills: Language Detection + Text Analysis</p>
        </div>
    """)

demo.launch(css=custom_css, theme=gr.themes.Base())
