import google.generativeai as genai

from google.generativeai.types import HarmCategory, HarmBlockThreshold

from app.config import settings

genai.configure(api_key=settings.GOOGLE_AI_SECRET_KEY)


def moderation_ai_posts_comments(text_to_analyze: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt_data = f"Please analyze the following text for any inappropriate content, including offensive language, hate speech, violence, or profanities. Provide a response indicating whether this content violates moderation guidelines and specify which categories (if any) are flagged.\n\nText to analyze:\n\"{text_to_analyze}\""

    response = model.generate_content(
        prompt_data,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        },
    )

    return response.candidates[0].finish_reason.name

def get_automatic_reply_content(post_content: str, comment_content_to_reply: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt_data = f"""
    You are an assistant designed to generate thoughtful and relevant replies to comments on social media posts. Based on the context provided, craft a response that aligns with the tone and content of the original post.

    Post content: "{post_content}"

    Comment to reply to: "{comment_content_to_reply}"

    Please create a reply that is:
    1. Relevant to both the post content and comment.
    2. Friendly, engaging, and adds value to the conversation.
    3. Reflective of the original post's sentiment, whether informative, encouraging, or lighthearted.

    Reply:
    """

    response = model.generate_content(
        prompt_data,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        },
    )

    return response.text.strip()