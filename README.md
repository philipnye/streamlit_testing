# IfG Analytics Dashboard
## Serving the dashboard
### Web
Hosted on Streamlit Community Cloud at [https://instituteforgovernment.streamlit.app/](https://instituteforgovernment.streamlit.app/)

### Local development
1. Create a new virtual environment using `python -m venv env`
1. Activate the virtual environment using `env\Scripts\activate`
1. Run `pip install -r requirements.txt` to install packages
1. Run `pre-commit install` to install [`pre-commit`](https://pre-commit.com/)
1. Run `streamlit run streamlit_app.py`

## Project structure
```
streamlit_testing/
├── docs/
│   ├── design_notes.md
│
├── js/
│   ├── <function name>.js
│
├── pages/
│   ├── dashboard/
│       ├── web_metrics/
│          ├── <page name>.py
│          ├── config.py        <<< Variables used across multiple pages
│          ├── elements.py     <<< Page elements used across multiple pages
│          ├── utils.py     <<< (Non-page element) functions and code snippets used across multiple pages
│
├── sql/
│   ├── dashboard/
│       ├── web_metrics/
│          ├── <page name>.sql
│
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── streamlit_app.py
└── requirements.txt
```