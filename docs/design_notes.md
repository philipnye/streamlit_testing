# Dashboard
## Design decisions
- `streamlit-aggrid`'s `AgGrid()` is used over `streamlit`'s `dataframe()` to display tabular data as, as of v1.43.1 at least, `streamlit`'s `dataframe()` lacks the following functionality:
    - Filterable columns
    - Pagination
