import json
import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client with the API key
gpt_api_key = "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"
client = OpenAI(api_key=gpt_api_key)

# Function to interact with the LLM
def chat_with_llm(chat_history):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history,
        max_tokens=1500,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Function to save the responses as a JSON file
def save_responses_to_json(responses, filename):
    with open(filename, 'w') as json_file:
        json.dump(responses, json_file, indent=4)

# Main Streamlit app
def main():
    st.set_page_config(page_title="Credit Form 2 Assistant", layout="wide")

    # Layout setup
    col1, col2 = st.columns([1, 2])  # Adjust ratios for better alignment

    with col1:
        st.title("Credit Form 2 Assistant")
        st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line for visual separation

        # Initialize session state
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = [
                {"role": "system", "content": '''You are a virtual assistant guiding the user through a credit form creation process. 
You should ask each question in sequence, validate the answers, and store the responses. 
You will also need to recall previous answers to provide context for subsequent questions.
Here is the credit form flow:

1.**What kind of housing do you want to buy?**: "There are three types of housing for Users to buy:- 1. 1st housing, 2. 2nd housing, 3. Investment property"
     - Ask the user whether they want to buy 1st housing, 2nd housing, or an Investment property.
     - Validation: Only proceed to the next question if the user answers this question correctly by selecting one of the provided options.
     - Storage: `registration_data["kind_of_housing"] = f"{user_input}"`
                 
2.**Do you already have a project?**: "Ask the user whether they already have a project. The options are Yes or No. give this option in bullet points always" 
     - Storage: registration_data["already_have_project"] = f"{user_input}" 
     - Validation: 
             1. If Yes, you need to ask him the following 3 questions(3rd, 4th and 5th questions):-
                     3. **Please select the constructor from the list**: "Ask the user to select a constructor from the following options provide the options in bullet points:
                            (a) DemoConstructor1 
                            (b) DemoConstructor2 
                            (c) DemoConstructor3" 

                        - Validation: The user must choose one of the listed constructors. If the user enters any other response, re-ask the question until a valid option is selected.
                        - Storage: registration_data["selected_constructor"] = f"{user_input}"

                    4. **Can you select the project you decided on?** "Ask the user to choose a project from the following options provide the options in bullet points:
                           (a) ProjectDemo1
                           (b) ProjectDemo2
                           (c) ProjectDemo3"
                 
                        - Validation: The user must select one of the listed projects. If the user enters any other response, re-ask the question until a valid option is selected.
                        - Storage: registration_data["selected_project"] = f"{user_input}"

                    5. **In which department is the project located?** "Ask the user to choose the department where the project is located from the following options, provide the options in bullet points:

                         (a) BOGOTA1
                         (b) BOGOTA2
                         (c) BOGOTA3"

                        - Validation: The user must select one of the listed departments. If the user enters any other response, re-ask the question until a valid option is selected.
                        - Storage: registration_data["project_department"] = f"{user_input}"
            2. If the answer is No: Skip the following questions (3, 4, and 5). In this case Move to question 6. 

6.**Would you like to add an additional Buyer?**: "Display the list of available additional buyers and ask the user to select one. 
               (a) Buyer 1 - Status: Not Registered
               (b) Buyer 2 - Status: Not Registered
               (c) Buyer 3 - Status: Not Registered 
               (d) Add New Buyer 
        - Storage: `registration_data["selected_buyer"] = f"{user_input}"`
                 
                If they want to add a new buyer, they need to provide the following details one by one:
                    Details Required for New Buyer:

                        (a) **Identification Number**: Ask for what is the montly income
                        - Validation: Ensure the input is in the correct format (e.g., alphanumeric, specific length).
                        - Storage: `registration_data["additional_buyer_identification_number"] = f"{user_input}"`
                        
                        (b) Additional Buyer Email: Ask for additional buyer email
                        - Validation: Check for valid email format (e.g., user@example.com).
                        - Storage: `registration_data["additional_buyer_email"] = f"{user_input}"`
                        
                        (c) Full Name: Ask for what is the full name of buyer
                        - Validation: Ensure the name is entered correctly (e.g., no numbers or special characters).
                        - Storage: `registration_data["additional_buyer_full_name"] = f"{user_input}"`
                 
                        (d) Phone Number: Ask for what is the phone number of buyer
                        - Validation: Ensure the phone number is in the correct format in 10 digits.
                        - Storage: `registration_data["additional_buyer_phone_number"] = f"{user_input}"`
                 
                        (e) Kinship: Ask the user for Choosing from the following options: 
                                    (i) Spouse
                                    (ii) Mother
                                    (iii) Dad
                                    (iv) Son/Daughter
                                    (v) Brother/Sister
                                    (vi) Grandfather/Grandmother
                                - Validation: Only accept one of the listed kinship options. Re-ask if an invalid option is entered.
                                - Storage: `registration_data["additional_buyer_kinship"] = f"{user_input}"`
                 
                        (f) **Monthly Income**: Ask for what is the montly income of the buyer
                                - Validation: Ensure the value is numerical. Convert text entries to numbers for calculations.
                                - Storage: `registration_data["additional_buyer_monthly_income"] = f"{user_input}"`
                 
                        (g) Monthly Payment by Additional Buyer: Ask for what is the Monthly Payment by Additional Buyer
                                - Validation: Ensure the value is numerical. Convert text entries to numbers for calculations.
                                - Storage: registration_data["additional_buyer_monthly_payment"] = f"{user_input}"

                Ask again If they want to add another new buyer, they need to provide the above details one by one: and you can start the flow from (a) to (g) again.

                                        

For each step, ensure you:
        - Collect the user’s input.
        - Validate the input according to the rules specified
        - If the input is invalid, politely ask the user to provide the correct information by being the same flow.
        - don't show storage information on each question
                 
At the end of the process, return all collected information in format Specified above. Be sure to maintain a conversational tone and provide appropriate guidance based on previous answers.
'''}
            ]
        if 'responses' not in st.session_state:
            st.session_state['responses'] = {}
        if 'current_question_index' not in st.session_state:
            st.session_state['current_question_index'] = -1  # Start before the first question

        # Load questions from file
        questions_file = "/upart2.txt"
        try:
            with open(questions_file, 'r') as file:
                questions = file.readlines()
            questions = [q.strip() for q in questions if q.strip()]
        except Exception as e:
            st.error(f"Error loading questions file: {e}")
            return

        # User input
        user_input = st.text_input("Type your message:", key="user_input")

        if user_input:
            st.session_state['chat_history'].append({"role": "user", "content": user_input})

            if st.session_state['current_question_index'] == -1:
                st.session_state['current_question_index'] = 0
                st.session_state['responses'] = {}

            if st.session_state['current_question_index'] >= 0:
                current_question = questions[st.session_state['current_question_index']]
                llm_response = chat_with_llm(st.session_state['chat_history'])
                
                st.session_state['latest_llm_response'] = llm_response  # Store the response
                st.write(f"Assistant: {llm_response}")

                if "invalid" in llm_response.lower():
                    st.session_state['chat_history'].append({"role": "assistant", "content": current_question})
                else:
                    st.session_state['chat_history'].append({"role": "assistant", "content": llm_response})
                    st.session_state['responses'][current_question] = user_input
                    st.session_state['current_question_index'] += 1

                    if st.session_state['current_question_index'] < len(questions):
                        next_question = questions[st.session_state['current_question_index']]
                    else:
                        save_responses_to_json(st.session_state['responses'], 'responsessection2.json')
                        st.success("All questions answered. Thank you! Your responses have been saved.")
                        st.session_state['current_question_index'] = -1

    with col2:
        st.subheader("Chat History")
        st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line for visual separation
        # Create a container for chat history with proper height and no extra space
        container = st.container()
        with container:
            for message in st.session_state['chat_history']:
                if message['role'] == 'assistant':
                    st.write(f"Assistant: {message['content']}")
                elif message['role'] == 'user':
                    st.write(f"You: {message['content']}")

if __name__ == "__main__":
    main()
