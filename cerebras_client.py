import requests
import json
import re
from config import CEREBRAS_API_KEY, CEREBRAS_API_URL, CEREBRAS_MODELS_URL

class CerebrasClient:
    def __init__(self):
        self.api_key = CEREBRAS_API_KEY
        self.api_url = CEREBRAS_API_URL
        self.models_url = CEREBRAS_MODELS_URL
        self.current_model = "cerebras-1.3b-chat"  # Default model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # Track recent responses to avoid repetition
        self.recent_responses = []
    
    def _format_for_telegram(self, text: str) -> str:
        """
        Format text for Telegram messages, handling special characters and formatting
        """
        if not text:
            return text
        
        # Remove any existing markdown that might cause issues
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Convert **bold** to <b>bold</b>
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Convert *italic* to <i>italic</i>
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)  # Convert `code` to <code>code</code>
        text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)      # Convert __underline__ to <u>underline</u>
        
        # Clean up extra whitespace and newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove multiple empty lines
        text = text.strip()
        
        # Ensure proper line breaks
        text = text.replace('\n', '\n')
        
        # Escape HTML special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Re-apply our HTML formatting
        text = text.replace('&lt;b&gt;', '<b>')
        text = text.replace('&lt;/b&gt;', '</b>')
        text = text.replace('&lt;i&gt;', '<i>')
        text = text.replace('&lt;/i&gt;', '</i>')
        text = text.replace('&lt;code&gt;', '<code>')
        text = text.replace('&lt;/code&gt;', '</code>')
        text = text.replace('&lt;u&gt;', '<u>')
        text = text.replace('&lt;/u&gt;', '</u>')
        
        return text
    
    def _add_to_recent_responses(self, response):
        """Add response to recent responses to avoid repetition"""
        self.recent_responses.append(response)
        # Keep only last 5 responses
        if len(self.recent_responses) > 5:
            self.recent_responses.pop(0)
    
    def _is_recent_response(self, response):
        """Check if response was recently used"""
        return response in self.recent_responses
    
    def _get_unique_response(self, responses):
        """Get a response that hasn't been used recently"""
        # Filter out recently used responses
        available_responses = [r for r in responses if not self._is_recent_response(r)]
        
        # If all responses were used recently, reset the list and use any
        if not available_responses:
            self.recent_responses.clear()
            available_responses = responses
        
        return available_responses[0] if available_responses else responses[0]
    
    def get_available_models(self):
        """Fetch available models from Cerebras API"""
        try:
            response = requests.get(
                self.models_url,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                models_data = response.json()
                if "data" in models_data:
                    models = [model["id"] for model in models_data["data"]]
                    return models
                else:
                    print("⚠️ No models found in API response")
                    return []
            else:
                print(f"❌ Failed to fetch models: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching models: {e}")
            return []
    
    def set_model(self, model_name):
        """Set the current model to use"""
        available_models = self.get_available_models()
        if model_name in available_models:
            self.current_model = model_name
            print(f"✅ Model set to: {model_name}")
            return True
        else:
            print(f"❌ Model '{model_name}' not found. Available models: {available_models}")
            return False
    
    def get_current_model(self):
        """Get the current model being used"""
        return self.current_model
    
    def generate_response(self, messages, role_system_prompt):
        """
        Generate a response using Cerebras API
        
        Args:
            messages (list): List of conversation messages
            role_system_prompt (str): System prompt for the selected role
            
        Returns:
            str: Generated response from the API or fallback response
        """
        try:
            response = self._try_api_call(messages, role_system_prompt)
            if response:
                print(f"✅ API call successful with model: {self.current_model}")
                # Format the response for Telegram
                formatted_response = self._format_for_telegram(response)
                return formatted_response
        except Exception as e:
            print(f"❌ API call failed: {e}")
        
        # If API call fails, return a fallback response
        print("⚠️ API call failed, using fallback response")
        fallback_response = self._generate_fallback_response(role_system_prompt, messages)
        return self._format_for_telegram(fallback_response)
    
    def _try_api_call(self, messages, role_system_prompt):
        """Try to make an API call to Cerebras API"""
        try:
            # Prepare the messages with system prompt
            api_messages = [
                {"role": "system", "content": role_system_prompt}
            ]
            
            # Add conversation messages
            for msg in messages:
                api_messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant",
                    "content": msg["content"]
                })
            
            payload = {
                "model": self.current_model,
                "messages": api_messages,
                "max_tokens": 1000,
                "temperature": 0.7,
                "stream": False
            }
            
            print(f"🔗 Making API call to: {self.api_url}")
            print(f"🤖 Using model: {self.current_model}")
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    print(f"✅ API response received: {content[:100]}...")
                    return content
                else:
                    print("⚠️ API response missing choices")
                    return None
            elif response.status_code == 404:
                print(f"❌ Endpoint not found: {self.api_url}")
                return None
            elif response.status_code == 401:
                print(f"❌ Unauthorized - check your API key")
                return None
            elif response.status_code == 400:
                print(f"⚠️ 400 Bad Request - API endpoint exists but request format may be wrong")
                print(f"   Response: {response.text[:200]}")
                return None
            else:
                print(f"❌ Error {response.status_code}: {response.text[:200]}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def _generate_fallback_response(self, role_system_prompt, messages):
        """Generate a fallback response when API is unavailable"""
        if not messages:
            return "I'm here to help! What would you like to talk about?"
        
        # Get the last user message
        last_message = messages[-1]["content"].lower()
        
        # Context-aware responses based on user input
        if "hi" in last_message or "hello" in last_message or "hey" in last_message:
            greetings = [
                "Hi there! 👋 How are you doing today?",
                "Hello! 😊 Nice to meet you! How can I help?",
                "Hey! 👋 What's on your mind?",
                "Hi! 😄 Great to see you! What would you like to talk about?"
            ]
            response = self._get_unique_response(greetings)
            self._add_to_recent_responses(response)
            return response
        
        elif "how are you" in last_message or "how r u" in last_message:
            status_responses = [
                "I'm doing well, thank you for asking! 😊 How about you?",
                "I'm here and ready to help! How are you feeling today?",
                "I'm functioning well and excited to chat with you! How are you?",
                "I'm doing great! Thanks for checking in. How are you doing?"
            ]
            response = self._get_unique_response(status_responses)
            self._add_to_recent_responses(response)
            return response
        
        elif "?" in last_message:
            question_responses = [
                "That's a great question! I'd love to help you with that.",
                "Interesting question! Let me think about that for you.",
                "That's something I'd be happy to discuss with you!",
                "Great question! I'm here to help you explore that topic."
            ]
            response = self._get_unique_response(question_responses)
            self._add_to_recent_responses(response)
            return response
        
        # Simple role-based fallback responses with variety
        if "coder" in role_system_prompt.lower() or "programming" in role_system_prompt.lower():
            responses = [
                "I'd love to help you with programming! However, I'm currently experiencing some technical difficulties with my AI service. Please try again in a few minutes, or feel free to ask me anything else!",
                "Hello! I'm your coding assistant, made by Glitch Artist I'm currently having some technical issues, but I'm here to help with programming questions when I'm back online!",
                "As your programming expert, I'm ready to help with code questions! I'm experiencing some AI service issues right now, but I'll be back to assist you soon!",
                "Hey there! I'm your coding buddy. I'm having some technical difficulties at the moment, but I'm excited to help you with programming when I'm back online!"
            ]
        elif "analyst" in role_system_prompt.lower() or "data" in role_system_prompt.lower():
            responses = [
                "I'd be happy to help with data analysis! I'm experiencing some technical difficulties right now, but I'll be back to assist you with data insights soon!",
                "Hi there! I'm your data analysis expert. I'm currently having some technical issues, but I'm ready to help with data questions when I'm back online!",
                "As your data analyst, I'm here to help interpret data and provide insights! I'm having some AI service issues, but I'll be back to help you analyze data soon!",
                "Hello! I'm your data expert. I'm currently experiencing some technical difficulties, but I'm ready to dive into data analysis with you when I'm back online!"
            ]
        elif "partner" in role_system_prompt.lower() or "supportive" in role_system_prompt.lower():
            responses = [
                "I'm here to support you! I'm currently experiencing some technical difficulties, but I want you to know that I care and I'm listening. What's on your mind?",
                "Hey there! I'm your supportive companion. I'm having some technical issues right now, but I'm here to listen and support you through whatever you're going through.",
                "I'm here for you! I'm experiencing some AI service difficulties, but I want you to know that your feelings matter and I'm here to listen. How are you doing?",
                "Hello! I'm your supportive friend. I'm having some technical issues, but I care about you and I'm here to listen. What would you like to talk about?"
            ]
        elif "therapist" in role_system_prompt.lower() or "therapeutic" in role_system_prompt.lower():
            responses = [
                "I'm here to provide therapeutic support. I'm currently having some technical issues, but I want you to know that your feelings are valid and important. How are you feeling right now?",
                "As your therapeutic support, I'm here to help you explore your feelings and develop coping strategies. I'm experiencing some AI service issues, but I'm listening. What's on your mind?",
                "I'm here to provide emotional guidance and support. I'm having some technical difficulties, but I want you to know that your emotions matter. How are you doing today?",
                "Hello! I'm your therapeutic companion. I'm experiencing some technical issues, but I'm here to support your emotional well-being. What would you like to discuss?"
            ]
        else:
            # Default assistant responses
            responses = [
                "I'm here to help! I'm currently experiencing some technical difficulties with my AI service, but I'm ready to assist you with anything you need. What can I help you with today?",
                "Hello! I'm your AI assistant. I'm having some technical issues at the moment, but I'm here to help you with whatever you need. What would you like to talk about?",
                "Hi there! I'm here to assist you! I'm experiencing some AI service difficulties, but I'm ready to help. What can I do for you today?",
                "Hey! I'm your helpful assistant. I'm having some technical issues right now, but I'm here to support you. What would you like to discuss?"
            ]
        
        response = self._get_unique_response(responses)
        self._add_to_recent_responses(response)
        return response
    
    def is_api_key_valid(self):
        """Check if the API key is configured"""
        return bool(self.api_key and self.api_key != "your_cerebras_api_key_here") 