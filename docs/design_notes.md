# Dashboard
## Design decisions
### Data table
- `streamlit-aggrid`'s `AgGrid()` is used over `streamlit`'s `dataframe()` to display tabular data as, as of v1.43.1 at least, `streamlit`'s `dataframe()` lacks the following functionality:
    - Filterable columns
    - Pagination

#### Filtering
- An option to make filtering more visible is to use [AG Grid floating filters](https://www.ag-grid.com/javascript-data-grid/floating-filters/):
```python
grid_options["defaultColDef"] = {
    "filter": True,
    "filterParams": {
        "excelMode": "windows",
    },
    "floatingFilter": True,     # <<< This is the line that's been added
}
```
- This works, but is very visually intrusive in the UI. Think this is best handle via user guidance rather than the UI

### Analytics
- [`streamlit-analytics2`](https://github.com/444B/streamlit-analytics2), Google Analytics and Statcounter were all tested
- `streamlit-analytics2` had problems integrating with authentication on streamlit (`AttributeError: st.session_state has no attribute "session_data"`)
- Google Analytics and Statcounter didn't work (no traffic recorded)
