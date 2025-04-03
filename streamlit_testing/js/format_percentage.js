function customPercentFormatter(params) {
    let n = Number.parseFloat(params.value) * 100;

    if (!Number.isNaN(n)) {
      return n.toFixed(1).replace(/\B(?=(\d{3})+(?!\d))/g, ',')+'%';
    } else {
      return '-';
    }
}