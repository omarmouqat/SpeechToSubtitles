from dotenv import load_dotenv
import os

load_dotenv()
from groq import Groq


# Initialize the Groq client
client = Groq(api_key=os.getenv("TOKEN"))#put your token here for more seurity when deploying put it into an .env as TOKEN


# Specify the path to the audio file
filename = os.path.dirname(__file__) + "/audio.mp3" # Replace with your audio file!a

# Open the audio file
with open(filename, "rb") as file:
    # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
      file=file, # Required audio file
      model="whisper-large-v3-turbo", # Required model to use for transcription
      prompt="Specify context or spelling",  # Optional
      response_format="verbose_json",  # Optional
      timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
      language="en",  # Optional
      temperature=0.0  # Optional
    )
    # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)
    #print(type(transcription))
    data = transcription.to_dict()["words"]

    #output =json.dumps(transcription, indent=2, default=str)
    for word in data:
        print(word)

"""
the out put should be like this:
{'word': 'my', 'start': 0.02, 'end': 0.42}
{'word': 'thought', 'start': 0.42, 'end': 0.74}
{'word': 'i', 'start': 0.74, 'end': 0.98}
{'word': 'have', 'start': 0.98, 'end': 1.16}
{'word': 'nobody', 'start': 1.16, 'end': 1.48}
{'word': 'by', 'start': 1.48, 'end': 1.74}
{'word': 'a', 'start': 1.74, 'end': 1.86}
{'word': 'beauty', 'start': 1.86, 'end': 2.08}
{'word': 'and', 'start': 2.08, 'end': 2.28}
{'word': 'will', 'start': 2.28, 'end': 2.44}
{'word': 'as', 'start': 2.44, 'end': 2.62}
{'word': "you've", 'start': 2.62, 'end': 2.82}
{'word': 'poured', 'start': 2.82, 'end': 3.06}
{'word': 'mr', 'start': 3.06, 'end': 4.08}
{'word': 'rochester', 'start': 4.08, 'end': 4.62}
{'word': 'is', 'start': 4.62, 'end': 4.94}
{'word': 'sub', 'start': 4.94, 'end': 5.18}
{'word': 'and', 'start': 5.18, 'end': 5.36}
{'word': 'that', 'start': 5.36, 'end': 5.52}
{'word': 'so', 'start': 5.52, 'end': 5.76}
{'word': "don't", 'start': 5.76, 'end': 6.06}
{'word': 'find', 'start': 6.06, 'end': 6.3}
{'word': 'simpus', 'start': 6.3, 'end': 6.74}
{'word': 'and', 'start': 6.74, 'end': 7.48}
{'word': 'devoted', 'start': 7.48, 'end': 7.84}
{'word': 'to', 'start': 7.84, 'end': 8.06}
{'word': 'bowed', 'start': 8.06, 'end': 8.46}
{'word': 'to', 'start': 8.46, 'end': 9.2}
{'word': 'at', 'start': 9.2, 'end': 9.38}
{'word': 'might', 'start': 9.38, 'end': 9.64}
{'word': 'in', 'start': 9.64, 'end': 9.84}
{'word': 'a', 'start': 9.84, 'end': 10}
"""
