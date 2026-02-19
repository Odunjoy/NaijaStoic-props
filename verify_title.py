import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.script_engine import transform_script

def test_viral_title():
    print("[TEST] Verifying Viral Title Generation...")
    
    # Mock data
    test_script = "She thought the VIP table was free."
    mock_api_key = "test_key"
    
    # Patch genai
    with patch('modules.script_engine.genai') as mock_genai:
        # Mock the model and generate_content
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock response with viral_title in JSON
        mock_response = MagicMock()
        mock_response.text = '''
        {
            "viral_title": "The Price of Being a 'Free' Guest",
            "setting_description": "Luxury club in VI",
            "scenes": []
        }
        '''
        mock_model.generate_content.return_value = mock_response

        # Call function
        result = transform_script(test_script, google_api_key=mock_api_key)
        
        # Check result
        if result["viral_title"] == "The Price of Being a 'Free' Guest":
            print(f"[PASS] Extracted viral title: '{result['viral_title']}'")
        else:
            print(f"[FAIL] Expected viral title, got: '{result.get('viral_title')}'")
            
        # Verify prompt contained request for title
        call_args = mock_model.generate_content.call_args
        if call_args:
            prompt_sent = call_args[0][0]
            if "viral_title" in prompt_sent:
                 print("[PASS] Prompt requested 'viral_title'.")
            else:
                 print("[FAIL] Prompt did NOT request 'viral_title'.")

if __name__ == "__main__":
    test_viral_title()
