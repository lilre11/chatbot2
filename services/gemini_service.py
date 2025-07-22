import google.generativeai as genai
from config import Config
import logging
from typing import List, Dict, Optional

class GeminiService:
    """Service class for handling Gemini AI interactions."""
    
    def __init__(self):
        """Initialize Gemini AI service."""
        self.api_key = Config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model - using the latest Gemini 2.0 Flash model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
    
    def generate_response(self, message: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate a response using Gemini AI.
        
        Args:
            message (str): User's message
            conversation_history (List[Dict]): Previous conversation messages
            
        Returns:
            str: Generated response from Gemini
        """
        try:
            # Prepare the prompt with context
            prompt = self._prepare_prompt(message, conversation_history)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                self.logger.warning("Empty response from Gemini AI")
                return Config.DEFAULT_RESPONSE
                
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return Config.DEFAULT_RESPONSE
    
    def _prepare_prompt(self, message: str, conversation_history: List[Dict] = None) -> str:
        """
        Prepare the prompt with conversation context.
        
        Args:
            message (str): Current user message
            conversation_history (List[Dict]): Previous messages
            
        Returns:
            str: Formatted prompt
        """
        # System prompt
        system_prompt = """You are a helpful and friendly AI assistant chatbot. 
        You should provide accurate, helpful, and engaging responses to user questions.
        Keep your responses conversational and appropriate for a chat interface.
        If you don't know something, admit it rather than making up information."""
        
        # Build conversation context
        context = [system_prompt]
        
        if conversation_history:
            # Add recent conversation history (limited by MAX_CONVERSATION_HISTORY)
            recent_history = conversation_history[-Config.MAX_CONVERSATION_HISTORY:]
            for msg in recent_history:
                if msg['sender_type'] == 'user':
                    context.append(f"User: {msg['content']}")
                elif msg['sender_type'] == 'bot':
                    context.append(f"Assistant: {msg['content']}")
        
        # Add current message
        context.append(f"User: {message}")
        context.append("Assistant:")
        
        return "\n".join(context)
    
    def check_api_status(self) -> bool:
        """
        Check if the Gemini API is accessible.
        
        Returns:
            bool: True if API is accessible, False otherwise
        """
        try:
            # Test with a simple prompt
            test_response = self.model.generate_content("Hello")
            return test_response.text is not None
        except Exception as e:
            self.logger.error(f"API status check failed: {str(e)}")
            return False
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for a given text.
        
        Args:
            text (str): Text to count tokens for
            
        Returns:
            int: Estimated token count
        """
        try:
            # Simple token estimation (roughly 4 characters per token)
            return len(text) // 4
        except Exception as e:
            self.logger.error(f"Error counting tokens: {str(e)}")
            return 0
