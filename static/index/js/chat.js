$(document).ready(function () {
    var ws = new WebSocket("ws://10.0.142.104:8000/chat")
    var chatuser = []
    $("#helpmsg").hide()
    $("#help").click(function () {
        $("#helpmsg").toggle()
        $("#chat").toggle()
    })

    function sendmessage() {
        var msg = document.getElementById("message").value
        if (msg == "") {
            return
        }
        $("#charhistory").html($("#charhistory").html() + "<p style='text-align: right'>" + msg + "<span style='color: red'>:[我]</span>" + "</p>")
        document.getElementById("message").value = ""
        var msguser = "<span style='color:blue;'>"
        if (chatuser.length > 0) {
            msguser = "<span style='color:purple;font-weight: bolder'>"
            msguser += "."
            for (i in chatuser) {
                msguser += chatuser[i] + "."
            }
        }
        ws.send(msguser + "|" + msg)
    }

    function change() {
        $.getJSON('/flist', function (data) {
            $("#left p").remove()
            var temp = []
            for (i in data) {
                for (j in chatuser) {
                    if (data[i] == chatuser[j]) {
                        temp.push(data[i])
                        break
                    }
                }
            }
            chatuser = temp
            for (i in data) {
                var color = "<p>"
                for (j in chatuser) {
                    if (data[i] == chatuser[j]) {
                        color = "<p style='color: red'>"
                    }
                }
                $("#left").html($("#left").html() + color + data[i] + "</p>")
            }
            $("#left p").click(function () {
                if ($(this).css("color").toString() == "rgb(53, 61, 68)") {
                    $(this).css("color", "rgb(255, 0, 0)")
                    chatuser.push($(this).text().toString())
                }
                else {
                    $(this).css("color", "rgb(53, 61, 68)")
                    chatuser.pop($(this).text().toString())
                }
            })
            $("#left p").dblclick(function () {
                $("#left p").css("color", "rgb(53, 61, 68)")
                chatuser = []
                $(this).css("color", "rgb(255, 0, 0)")
                chatuser.push($(this).text().toString())
            })
        })
    }

    ws.onmessage = function (data) {
        $("#charhistory").html($("#charhistory").html() + "<p>" + data.data + "</p>")
        if (data.data.toString().match("^<span style=\'color:((green)|(yellow));")) {
            change()
        }
    }
    $("#sendmessage").click(sendmessage)
    change()
})