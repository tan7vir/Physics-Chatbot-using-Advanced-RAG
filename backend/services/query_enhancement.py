
import requests
from langchain.prompts import ChatPromptTemplate
import re
from config.config import GENERATE_API_URL, SECONDARY_MODEL

# Define the prompt template for generating responses
PROMPT_TEMPLATE = """
    You are creating questions for 9-10 grade students. Given the following prompt: '{prompt}', rewrite it into 5 more refined and specific questions. Provide only the questions, without any additional information or context.
    """

def query_enhncement ( question ):
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(prompt=question)

    print("/")
    print("/")
    print("/")
    print("/")
    print ( "------------prompt----------------")
    print("/")
    print("/")
    print("/")
    print ( prompt )

    payload = {
        "model": SECONDARY_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(GENERATE_API_URL, json=payload)

    if response.status_code == 200:
        response_data = response.json()

        # Correctly access the 'response' key in the response data
        if 'response' in response_data:
            questions = re.split(r'\n\d+\.\s', response_data['response'].strip())

            # Remove any empty strings from the list
            questions = [q for q in questions if q]
            print("/")
            print("/")
            print("/")
            print("/")
            print ( "------------5 Questions----------------")
            print("/")
            print("/")
            print("/")
            print ({"response": questions})
            return questions
        else:
            return question
    else:
        print ({"response": "Oops! Something went wrong in retrivel Question!"})
        return question 

if __name__ == "__main__":
    query_enhncement ("How do you solve the quadratic equation ( ax^2 + bx + c = 0 ) using the quadratic formula, and what are the steps involved in this process?")