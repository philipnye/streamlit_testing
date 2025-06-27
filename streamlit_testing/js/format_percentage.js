function customPercentFormatter(params) {
    let n = Number.parseFloat(params.value) * 100;

    if (!Number.isNaN(n)) {
      return n.toFixed(0)+'%';
    } else {
      return '-';
    }
}