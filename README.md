# IfG Analytics Dashboard
## Authentication
The dashboard uses Microsoft Entra authentication, following [Streamlit's guide to implementing this](https://docs.streamlit.io/develop/tutorials/authentication/microsoft).

The identity app registration that has been created has an expiry date: 3 April 2027.

## Serving the dashboard
### Web
Hosted on Streamlit Community Cloud at [https://instituteforgovernment.streamlit.app/](https://instituteforgovernment.streamlit.app/).

[Environment variables](#environment-variables) and [authentication secrets](#authentication) are held as [app secrets](https://docs.streamlit.io/develop/concepts/connections/secrets-management).

### Local development
1. Add [environment variables](#environment-variables) as system environment variables
1. Add a `secrets.toml` file in a `.streamlit` directory containing [authentication](#authentication) details
1. Create a new virtual environment using `python -m venv env`
1. Activate the virtual environment using `env\Scripts\activate`
1. Run `pip install -r requirements.txt` to install packages
1. Run `pre-commit install` to install [`pre-commit`](https://pre-commit.com/)
1. Run `streamlit run streamlit_app.py`

## Project structure
```
├── .streamlit/
│   ├── config.toml
│
├── docs/
│   ├── design_notes.md
│
├── streamlit_testing/
|   ├── config/        <<< Variables used app-wide
|   │   ├── ag_grid_theme.py
|   │   ├── colours.py
|   │
|   ├── js/     <<< JS functions used app-wide
|   │   ├── <function name>.js
|   │
|   ├── pages/
|   │   ├── dashboard/
|   │       ├── web_metrics/
|   │          ├── md/        <<< Markdown text to be rendered in pages
|   │             ├── roadmap/
|   │                ├── doing.md
|   │                ├── done.md
|   │                ├── future.md
|   │             ├── <page name>.md
|   │          ├── <page name>.py
|   │          ├── chart_annotations.py        <<< Chart annotations used across multiple pages
|   │          ├── config.py        <<< Variables used across multiple pages
|   │          ├── definitions.py     <<< Definitions to be rendered in the UI
|   │          ├── elements.py     <<< Page elements used across multiple pages
|   │          ├── notes.py     <<< Notes to be rendered in the UI
|   │          ├── utils.py     <<< (Non-page element) functions and code snippets used across multiple pages
|   │
|   ├── sql/
|   │   ├── dashboard/
|   │       ├── web_metrics/
|   │          ├── <page name>.sql
│
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── streamlit_app.py
└── requirements.txt
```

## Design decisions
Documentation of key design decisions can be found in [design_notes.md](/docs/design_notes.md).

## Environment variables
The following environment variables are used by the app:
- `ODBC_DRIVER`: ODBC driver name to be used in database connection
- `ODBC_SERVER`: Server name to be used in database connection
- `ODBC_DATABASE`: Database name to be used in database connection
- `ODBC_AUTHENTICATION`: Authentication type to be used in database connection
- `AZURE_CLIENT_ID`: Username to be used in database connection
- `AZURE_CLIENT_SECRET`: Password to be used in database connection
- `DS_CONTACT_EMAIL_ADDRESS`: Email address to be used for contacting the data science team
- `IFG_WEB_ISSUES_FILE_LINK`: Link to document where web issues are logged

## Licences
An AG Grid licence is held in order to make use of all [`streamlit-aggrid` features](https://github.com/PablocFonseca/streamlit-aggrid). The license is perpetual - i.e. no need for renewal.
