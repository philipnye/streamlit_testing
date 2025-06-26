function stringFormatter(params) {
    if (!params.value || params.value === null || params.value === undefined) {
        return '';
    }

    let date;

    if (typeof params.value === 'string') {
        date = new Date(params.value);
    } else if (params.value instanceof Date) {
        date = params.value;
    } else {
        date = new Date(params.value);
    }

    if (isNaN(date.getTime())) {
        return '';
    }

    const formattedDate = date.toLocaleString('en-GB', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    });
    return formattedDate;
}