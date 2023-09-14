import os
import openai
import datetime

home_dir = os.path.expanduser(".")
openai.api_key_path = os.path.join(home_dir, 'OPENAI_API_KEY')

today_date = datetime.date.today()


def get_response(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {
                "role": "system",
                "content": (
                    f'You are an expert OET assistant. You assist users with their OET queries and will be a speaking partner. You have the complete knowledge on the official OET resources provided'
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response