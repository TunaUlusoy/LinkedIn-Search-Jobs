import pandas as pd
import streamlit as st
from search import Search

st.title("Search")

tab1, tab2, tab3 = st.tabs(["Search", "Jobs", "Keywords"])


def color(string):
    st.markdown(f'<p style="color:#FFA500;font-size:19px;">{string}</p>', unsafe_allow_html=True)


def process(df, page_number):
    row = df.iloc[int(page_number) - 1]

    for i in df.columns:
        color(i)
        if type(row[i]) == str:
            st.write(str(row[i]))
        else:
            st.write(row[i])


with tab1:
    username = st.text_input("Enter your LinkedIn username:")
    password = st.text_input("Enter your LinkedIn password:", type="password")
    keywords = st.text_input("Enter job keywords:", key=11)
    location_name = st.text_input("Enter location name:", key=21)
    day = st.slider("Enter how many days passed since job posting:", 1, 60, 1)
    limit = st.slider("Enter limit job was listed:", 1, 200, 1)

    if st.button("Search", key=41):
        st.text("Searching for jobs...")
        search = Search(username, password, keywords, location_name, day, limit)
        results = search.search_results()
        rows = search.get_requirements_from_results(results)
        st.text(f"Completed, {len(rows)} jobs was found.")

upload_flag = False

with tab2:
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file.name)
        if len(df) == 0:
            st.header("**There is no job :cry:**")
        elif len(df) == 1:
            st.header("**There is one job :neutral_face:**")
            process(df, 1)
        else:
            st.header(f"**There are {len(df)} jobs :smile:**")
            page_number = st.slider("Enter job number :", 1, len(df), 1)
            process(df, page_number)

with tab3:
    pass
    # TODO
    #  Summarize the description, extract keywords


