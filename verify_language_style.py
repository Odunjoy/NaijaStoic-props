import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.script_engine import transform_script

def test_language_styles():
    print("[TEST] Verifying Language Style Prompt Construction...")
    
    # Mock data
    test_script = "Hello world"
    mock_api_key = "test_key"
    
    styles = {
        "pidgin": "Authentic Nigerian Pidgin English",
        "mixed": "Urban Lagos Mix",
        "english": "Standard Nigerian English"
    }

    # Patch genai
    with patch('modules.script_engine.genai') as mock_genai:
        # Mock the model and generate_content
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock response to avoid JSON parse errors in the function
        mock_response = MagicMock()
        mock_response.text = '{"scenes": [], "setting_description": "test"}'
        mock_model.generate_content.return_value = mock_response

        for style, keyword in styles.items():
            print(f"\n--- Testing Style: {style} ---")
            
            # Call function
            transform_script(test_script, language_style=style, google_api_key=mock_api_key)
            
            # Get the argument passed to generate_content
            call_args = mock_model.generate_content.call_args
            if call_args:
                prompt_sent = call_args[0][0]
                
                # Check if keyword is in the prompt
                if keyword in prompt_sent:
                    print(f"[PASS] Prompt contains expected keyword: '{keyword}'")
                else:
                    print(f"[FAIL] Prompt MISSING keyword: '{keyword}'")
                    print(f"Prompt snippet: {prompt_sent[:500]}...")
            else:
                print("[FAIL] generate_content was not called.")

if __name__ == "__main__":
    test_language_styles()
