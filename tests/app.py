import pandas as pd
import requests
import json, time, re

GENERATE_API_URL = 'http://127.0.0.1:5000/api/generate'

# Load the CSV file
def load_questions(filename):
    return pd.read_csv(filename)


def process_response(reply):
    """Replace \[ with $$ and \] with $$ in a string."""
    reply = reply.replace(r'\[', '$$').replace(r'\]', '$$')
    
    # Use regex to find patterns that start with (/, followed by any characters, and end with )
    modified_reply = re.sub(r'\(\s*/.*?\s*\)', r'$$\g<0>$$', reply)
    
    return modified_reply

# Call the API to get the response
def call_api(question):
    response = requests.post(GENERATE_API_URL, json={"prompt": question, "model": 'qwen2.5:3b'})
    
    if response.status_code == 200:
        data = response.json()
        assistant_reply = data.get("response", "Failed to connect.")
    else:
        assistant_reply = "Failed to connect to the server. Please try again later in generation"
    
    assistant_reply = process_response(assistant_reply)
    return assistant_reply

# Save responses to a new CSV file
def save_responses(responses):
    responses_df = pd.DataFrame(responses)
    responses_df.to_csv('responses.csv', index=False)

def main():
    start_time = time.time()
    questions_df = load_questions('../Data/Questions_Sheet1.csv')  # Ensure path is correct
    print("Questions have been loaded")
    responses = []
    number = 1
    # Iterate over the questions in the DataFrame
    for idx, row in questions_df.iterrows():  # Use iterrows() to access each row as a Series
        print(f"sending question {number}")
        response_text = call_api(row['Questions'])  # Access question from 'Questions' column
        responses.append({'Question': row['Questions'], 'Generated Response': response_text, 'Answer': row['Answers']})  # Append question, response, and answer
        print(f"Question {number}")
        number += 1
    
    # Save the collected responses
    save_responses(responses)
    end_time = time.time()
    total_time = end_time - start_time
    print("Responses have been saved to responses.csv")
    print(f"Total execution time: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()
