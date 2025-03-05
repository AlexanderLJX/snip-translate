# translation.py
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

def get_gpt_translation(input, length="medium", timeout=7):
    import os
    import asyncio
    from google import genai
    from google.genai import types
    
    # Set up event loop for the thread
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set"
    
    try:
        # Initialize the client
        client = genai.Client(
            api_key=api_key,
        )
        
        # Set the model
        model = "gemini-2.0-flash"
        
        # Create the prompt with examples for few-shot learning
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text="translate the following to English:\"さっきからこいつの思考が全く読めない\" \n Reply with only the translation, followed by a full in depth explanation starting with \"Full explanation:\"."
                    ),
                ],
            ),
            types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text="I haven't been able to read this person's thoughts at all since a while ago. \nFull explanation: \n1. さっきから (sakki kara): \"since a while ago\" or \"for some time now\"\n2. こいつ (koitsu): \"this guy\" or \"this person\" (informal and somewhat rude)\n3. の (no): possessive particle, similar to \"'s\" or \"of\" in English\n4. 思考 (shikō): \"thought\" or \"thinking\"\n5. が (ga): subject particle\n6. 全く (mattaku): \"completely\" or \"entirely\"\n7. 読めない (yomenai): negative potential form of the verb 読む (yomu, \"to read\"), meaning \"can't read\"\nThe speaker is expressing their inability to understand or predict what the other person is thinking."
                    ),
                ],
            ),
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text="translate the following to English:\"これは僕が己の過ちに対して支払った代償であり\" \n Reply with only the translation, followed by a full in depth explanation starting with \"Full explanation:\"."
                    ),
                ],
            ),
            types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text="This is the price I paid for my own mistakes. \nFull explanation: \n1. これは (Kore wa): This means \"this is\" and is used to refer to something that has been mentioned or is being discussed.\n2. 僕が (boku ga): \"僕\" (boku) is a first-person pronoun meaning \"I\" or \"me,\" and \"が\" (ga) is a subject marker. Together, they mean \"I\" as the subject of the sentence.\n3. 己の過ちに対して (onore no ayamachi ni taishite): \"己\" (onore) is a pronoun meaning \"oneself\" or \"myself.\" \"過ち\" (ayamachi) means \"mistake\" or \"error.\" \"に対して\" (ni taishite) is a preposition meaning \"toward\" or \"in relation to.\" So, this phrase means \"toward my own mistakes.\"\n4. 支払った代償であり (shiharatta daishou de ari): \"支払った\" (shiharatta) is the past tense of the verb \"支払う\" (shiharau), which means \"to pay\" or \"to compensate.\" \"代償\" (daishou) means \"price\" or \"compensation.\" \"であり\" (de ari) is a formal way to say \"is\" or \"to be.\" This phrase means \"the price I paid.\"\nThe speaker is acknowledging that the situation they are facing is a consequence or payment they have to bear for their own errors or wrongdoings. It suggests a sense of personal accountability and responsibility for the negative outcome they are experiencing."
                    ),
                ],
            ),
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=f"translate the following to English:\"{input}\" \n Reply with only the translation, followed by a full in depth explanation starting with \"Full explanation:\"."
                    ),
                ],
            ),
        ]
        
        # Configure the generation parameters
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=64,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )
        
        # Generate the response
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        # Return the response text
        return response.text
        
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        return f"Error using Gemini API: {str(e)}\n{trace}"