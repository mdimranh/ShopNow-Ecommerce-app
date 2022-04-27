
$(function () {
    $("#print-btn").click(function () {
        var doc = new jsPDF()
        doc.addHTML($("#invoice")[0], 5, 10, {
            'background': '#fff'
        }, function () {
            doc.save('invoice.pdf');
        })
    })
})