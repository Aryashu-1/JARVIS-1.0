from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

groq_model =ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="meta-llama/llama-4-scout-17b-16e-instruct"
)