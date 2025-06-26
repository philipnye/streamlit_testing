function compareDates(date1, date2) {
    if (!date1 && !date2) return 0;
    if (!date1) return 1;
    if (!date2) return -1;

    const d1 = date1 instanceof Date ? date1 : new Date(date1);
    const d2 = date2 instanceof Date ? date2 : new Date(date2);

    const d1Valid = !isNaN(d1.getTime());
    const d2Valid = !isNaN(d2.getTime());

    if (!d1Valid && !d2Valid) return 0;
    if (!d1Valid) return 1;
    if (!d2Valid) return -1;

    // Compare dates
    if (d1.getTime() < d2.getTime()) return -1;
    if (d1.getTime() > d2.getTime()) return 1;
    return 0;
}