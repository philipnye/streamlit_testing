function compareDates(comparatorDate, cellValue) {
    const formattedDate = cellValue.toLocaleString('default');
    if (formattedDate < comparatorDate) {
    return 1;
    } else if (formattedDate > comparatorDate) {
    return -1;
    } else {
    return 0;
    }
}