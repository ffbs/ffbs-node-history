function pad(n, width) {
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
}

function* getPreviousMonth() {
    var month = new Date().getMonth();
    var year = new Date().getFullYear();
    while (true) {
        yield year + pad(month+1, 2);
        month === 0 ? year-- : null;
        month = ( (month-1)+12 ) % 12;
    }
}

function url(hash, month) {
    return '/out/' + hash + month + '.csv';
}

function pollForMonths(hash, months) {
    if (months === undefined) {
        months = getPreviousMonth();
    }
    var month = months.next().value;
    $.ajax({type: 'HEAD', url: url(hash, month)}).success(function () {
        $('#months').append('<option value="'+month+'">'+month+'</option>');
        pollForMonths(hash, months);
    });
}

function showGraph(url) {
    var el = document.getElementById("outlet");
    new Dygraph(el, url, {
        digitsAfterDecimal: 3,
        labelsKMB: true,
        drawAxesAtZero: true,
        title: 'Clients auf Router',
        xlabel: 'Zeitpunkt [UTC]',
        ylabel: 'Clients',
        connectSeparatedPoints: true
    });
}

function newhash() {
    if (location.hash) {
        var hash = location.hash.substr(1);
        pollForMonths(hash);
    }
}

$(function () {
    $('form').submit(function (ev) {
        ev.preventDefault();
        var month = $('select').val();
        showGraph(url(hash, month));
    });
    window.onhashchange = newhash;
    newhash();
});
