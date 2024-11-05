import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from app.config import settings

genai.configure(api_key=settings.GOOGLE_AI_SECRET_KEY)


def moderation_ai_posts_comments(text_to_analyze: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Please analyze the following text for any inappropriate content, including offensive language, hate speech, violence, or profanities. Provide a response indicating whether this content violates moderation guidelines and specify which categories (if any) are flagged.\n\nText to analyze:\n\"{text_to_analyze}\""

    response = model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        },
    )

    return response.candidates[0].finish_reason.name