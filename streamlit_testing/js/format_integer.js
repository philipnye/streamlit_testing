function stringFormatter(params) {
    if (!params.value) {
        return params.value;
    } else {
        return params.value.toLocaleString();
    }
}