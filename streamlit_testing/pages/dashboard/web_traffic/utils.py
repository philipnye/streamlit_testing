from st_aggrid import JsCode

apply_locale_string = JsCode("""
    function stringFormatter(params) {
        return params.value.toLocaleString();
    }
""")
