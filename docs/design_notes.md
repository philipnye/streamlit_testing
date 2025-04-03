# Dashboard
## Design decisions
### Data table
- `streamlit-aggrid`'s `AgGrid()` is used over `streamlit`'s `dataframe()` to display tabular data as, as of v1.43.1 at least, `streamlit`'s `dataframe()` lacks the following functionality:
    - Filterable columns
    - Pagination

### Analytics
- [`streamlit-analytics2`](https://github.com/444B/streamlit-analytics2), Google Analytics and Statcounter were all tested
- `streamlit-analytics2` had problems integrating with authentication on streamlit (`AttributeError: st.session_state has no attribute "session_data"`)
- Google Analytics and Statcounter didn't work (no traffic recorded)
