function stringFormatter(params) {
    const date = new Date(params.value);
    const formattedDate = date.toLocaleString('default', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    });
    return formattedDate;
}