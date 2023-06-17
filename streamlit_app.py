import pandas as pd
import streamlit as st

# Initialise session states
if 'show_next_section' not in st.session_state:
    st.session_state['show_next_section'] = False

# Add file_uploader
uploaded_file = st.file_uploader(
    key='file_uploader',
    label='''Note: The file must be
        closed in order for you to upload it
    ''',
    type=['csv'],
)

# Add next section button, controlling session state
if st.button(
    key='button_next_section',
    label='Next section',
    type='primary'
):
    st.session_state['show_next_section'] = True

# Show next section
if st.session_state['show_next_section']:

    file_contents = pd.read_csv(uploaded_file)

    st.write(file_contents.head(5))
