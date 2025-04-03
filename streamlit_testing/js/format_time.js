function stringFormatter(params) {
    if (!params.value) {
        return params.value;
    } else {
        return new Date(params.value * 1000).toISOString().slice(11, 19);
    }
}