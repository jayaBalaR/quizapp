import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection

def run():
    st.set_page_config(
        page_title="Kids quiz app",
        page_icon="",
    )

if __name__ == "__main__":
    run()

# Custom CSS for the buttons
page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://i.imgur.com/pqyk82F.png");
  background-size: cover;
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

# Set the background image using a picture's URL
# page_bg_img = '''
# <style>
#     .reportview-container {
#         background: url("https://imgur.com/pqyk82F");
#     }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session variables if they do not exist
default_values = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': None, 'answer_submitted': False, 'name':'','school':'', 's_class':'', 'age':0}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data
with open('question_answers_dict.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

def submit_answer():

    # Check if an option has been selected
    if st.session_state.selected_option is not None:
        # Mark the answer as submitted
        st.session_state.answer_submitted = True
        # Check if the selected option is correct
        if st.session_state.selected_option == quiz_data[st.session_state.current_index]['answer']:
            st.session_state.score += 10
    else:
        # If no option selected, show a message and do not mark as submitted
        st.warning("Please select an option before submitting.")

def next_question():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

def submit_details():
    # with open("scores.json", "w") as outfile:
    #     outfile.write(json_object)
    # Print results.
    for row in df.itertuples():
        st.write(f"{row.name} has a :{row.pet}:")

# Title and description
st.title("Kids Quiz App")
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

# Progress bar
progress_bar_value = (st.session_state.current_index + 1) / len(quiz_data)
st.metric(label="Score", value=f"{st.session_state.score} / {len(quiz_data) * 10}")
st.progress(progress_bar_value)

# Display the question and answer options
question_item = quiz_data[st.session_state.current_index]
st.subheader(f"Question {st.session_state.current_index + 1}")
st.title(f"**{question_item['question']}**")
st.write(question_item['information'])


st.markdown(""" ___""")

# Answer selection
options = question_item['options']
correct_answer = question_item['answer']

if st.session_state.answer_submitted:
    for i, option in enumerate(options):
        label = option
        if option == correct_answer:
            st.success(f"{label} (Correct answer)")
        elif option == st.session_state.selected_option:
            st.error(f"{label} (Incorrect answer)")
        else:
            st.write(label)
else:
    for i, option in enumerate(options):
        if st.button(option, key=i, use_container_width=True):
            st.session_state.selected_option = option

st.markdown(""" ___""")

# Submission button and response logic
if st.session_state.answer_submitted:
    if st.session_state.current_index < len(quiz_data) - 1:
        st.button('Next', on_click=next_question)
    else:
        result = f"{st.session_state.score} / {len(quiz_data) * 10}"
        st.write(f"**Quiz completed! Your score is: {st.session_state.score} / {len(quiz_data) * 10}**")
        
        name = st.text_area("Enter your name")
        school = st.text_area("Enter your school")
        s_class = st.text_area("Enter your class in Roman Numerals(I-X)")
        age = st.number_input('Enter your age in years and months')
        data = {"Name": name, "Age": age, "School": school, "Class": s_class, "score": result}
        # Serializing json
        json_object = json.dumps(data, indent=4)
        st.button('Student Submit', on_click=submit_details)
 
        # Writing to sample.json

        if st.button('Restart', on_click=restart_quiz):
            pass
else:
    if st.session_state.current_index < len(quiz_data):
        st.button('Submit', on_click=submit_answer)
