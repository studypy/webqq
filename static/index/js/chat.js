var ws = new WebSocket("ws://10.0.142.104:8000/chat")

function sendmessage() {
    var msg = document.getElementById("message").value
    if (msg == "") {
        return
    }
    ws.send(msg)
    msg = msg + "<span style='color: red'>:[我]</span>"
    $("#charhistory").html($("#charhistory").html() + "<p style='text-align: right'>" + msg + "</p>")
    document.getElementById("message").value = ""
}

function change() {
    $.getJSON('/flist', function (data) {
        $("#left").html("")
        for (i in data) {
            $("#left").html($("#left").html() + "<p>" + data[i] + "</p>")
        }
    })
}

$(document).ready(function () {
    ws.onmessage = function (data) {
        $("#charhistory").html($("#charhistory").html() + "<p>" + data.data + "</p>")
        if (data.data.toString().match("^<span style=\'color:((green)|(yellow));")) {
            change()
        }
    }
    $("#sendmessage").click(sendmessage)
    change()
})