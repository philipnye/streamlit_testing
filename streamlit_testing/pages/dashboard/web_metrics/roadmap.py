import streamlit as st

# DRAW PAGE HEADER
st.title("Roadmap")


# CREATE FUNCTION
def display_markdown_containers(text: str, delimiter: str, border: bool) -> None:
    """Displays chunked-up markdown in containers."""
    chunks = split_markdown(text, delimiter)

    for chunk in chunks:
        with st.container(border=border):
            st.markdown(chunk)


def split_markdown(text: str, delimiter: str) -> list[str]:
    """Splits the markdown text into chunks based on delimiter."""
    return [delimiter + " " + chunk.strip() for chunk in text.split(delimiter) if chunk.strip()]


# PAGE CONTENT
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Done")

    with open("streamlit_testing/pages/dashboard/web_metrics/md/roadmap/done.md", "r", encoding="utf-8") as file:
        done = file.read()

    display_markdown_containers(done, delimiter="###", border=True)

with col2:
    st.header("Doing")

    with open("streamlit_testing/pages/dashboard/web_metrics/md/roadmap/doing.md", "r", encoding="utf-8") as file:
        doing = file.read()

    display_markdown_containers(doing, delimiter="###", border=True)

with col3:
    st.header("Future (tbc)")

    with open("streamlit_testing/pages/dashboard/web_metrics/md/roadmap/future.md", "r", encoding="utf-8") as file:
        future = file.read()

    display_markdown_containers(future, delimiter="###", border=True)
