from st_aggrid import JsCode

apply_locale_string = JsCode("""
    function stringFormatter(params) {
        return params.value.toLocaleString();
    }
""")
format_date = JsCode("""
    function stringFormatter(params) {
        const date = new Date(params.value);
        const formattedDate = date.toLocaleString('default', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
        });
        return formattedDate;
    }
""")
format_date_comparator = JsCode("""
    function(comparatorDate, cellValue) {
        const formattedDate = cellValue.toLocaleString('default');
        if (formattedDate < comparatorDate) {
        return 1;
        } else if (formattedDate > comparatorDate) {
        return -1;
        } else {
        return 0;
        }
    }
""")
