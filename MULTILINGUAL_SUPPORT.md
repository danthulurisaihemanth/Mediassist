# MULTILINGUAL_SUPPORT.md

## 🌍 MediGenius Multilingual Support

MediGenius now supports **15 languages** with intelligent language detection and switching capabilities.

### 🗣️ Supported Languages

| Language Code | Language Name | Native Name |
|---------------|---------------|-------------|
| `en` | English | English |
| `es` | Spanish | Español |
| `fr` | French | Français |
| `de` | German | Deutsch |
| `hi` | Hindi | हिंदी |
| `bn` | Bengali | বাংলা |
| `zh-cn` | Chinese (Simplified) | 中文 |
| `ja` | Japanese | 日本語 |
| `ko` | Korean | 한국어 |
| `ar` | Arabic | العربية |
| `pt` | Portuguese | Português |
| `ru` | Russian | Русский |
| `it` | Italian | Italiano |
| `tr` | Turkish | Türkçe |
| `vi` | Vietnamese | Tiếng Việt |

### 🚀 How It Works

#### 1. **Language Selection**
- Users can select their preferred language from the dropdown menu
- The system remembers the language choice throughout the conversation

#### 2. **Automatic Language Detection**
- The AI can detect when users want to switch languages
- Examples of language switching phrases:
  - "Please answer in Spanish" → Switches to Spanish
  - "Habla español" → Switches to Spanish
  - "Réponds en français" → Switches to French
  - "हिंदी में जवाब दें" → Switches to Hindi

#### 3. **Intelligent Response Generation**
- All responses are generated in the selected language
- Medical terminology is appropriately translated
- Cultural context is maintained

### 💻 Usage Examples

#### Web Interface
```javascript
// Language is automatically sent with each message
fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
        message: "What are diabetes symptoms?", 
        language: "es" 
    })
})
```

#### API Usage
```python
# FastAPI example
response = requests.post("http://localhost:8000/chat", json={
    "message": "¿Cuáles son los síntomas de la diabetes?",
    "language": "es",
    "conversation_id": "optional_id"
})
```

#### CLI Usage
```bash
# The CLI defaults to English but can detect language changes
python main.py
# Ask: "What are diabetes symptoms? Please answer in Spanish"
# The system will automatically switch to Spanish
```

### 🔧 Technical Implementation

#### Core Components

1. **Language Utils** (`tools/language_utils.py`)
   - Contains language-specific prompts and responses
   - Handles language detection logic
   - Formats prompts in the selected language

2. **Updated Agents**
   - **LLM Agent**: Uses language-specific prompts
   - **Executor Agent**: Generates responses in selected language
   - **Explanation Agent**: Provides explanations in selected language

3. **State Management**
   - Language is stored in the conversation state
   - Persists throughout the conversation
   - Automatically updates when language changes

#### Language Detection Patterns

The system recognizes these patterns for automatic language switching:

```python
language_patterns = {
    "es": ["español", "spanish", "habla español", "responde en español"],
    "fr": ["français", "french", "parle français", "réponds en français"],
    "hi": ["हिंदी", "hindi", "हिंदी में", "hindi mein"],
    # ... and more
}
```

### 🧪 Testing

Run the multilingual test:
```bash
python test_multilingual.py
```

This will test:
- Language detection from user input
- Response generation in different languages
- Language switching during conversation

### 📝 Example Conversations

#### English → Spanish Switch
```
User: "What are diabetes symptoms?"
AI: "Diabetes symptoms include increased thirst, frequent urination, unexplained weight loss, fatigue, and blurred vision. If you experience these symptoms, consult a healthcare provider for proper evaluation."

User: "Please answer in Spanish"
AI: "Los síntomas de la diabetes incluyen sed excesiva, micción frecuente, pérdida de peso inexplicable, fatiga y visión borrosa. Si experimentas estos síntomas, consulta con un proveedor de atención médica para una evaluación adecuada."
```

#### Direct Language Questions
```
User: "¿Cuáles son los síntomas de la diabetes?"
AI: "Los síntomas de la diabetes incluyen sed excesiva, micción frecuente, pérdida de peso inexplicable, fatiga y visión borrosa. Si experimentas estos síntomas, consulta con un proveedor de atención médica para una evaluación adecuada."
```

### 🔮 Future Enhancements

- **Voice Input**: Support for voice input in different languages
- **More Languages**: Add support for additional languages
- **Regional Dialects**: Support for regional variations
- **Medical Terminology**: Enhanced medical term translation
- **Cultural Context**: Better cultural adaptation of medical advice

### 🐛 Troubleshooting

#### Common Issues

1. **Language Not Switching**
   - Ensure the language detection phrase is in the supported patterns
   - Check that the language code is valid

2. **Incorrect Translation**
   - The system uses the LLM's built-in multilingual capabilities
   - For medical accuracy, responses are generated rather than translated

3. **Mixed Language Responses**
   - This can happen if the language detection is unclear
   - Try using more explicit language switching phrases

### 📞 Support

For issues with multilingual functionality:
1. Check the language detection patterns in `tools/language_utils.py`
2. Verify the language code is supported
3. Test with the provided test script
4. Check the console logs for language switching events
