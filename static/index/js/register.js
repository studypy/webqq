$(document).ready(function () {
    $("#userId,#username").focus(function () {
        var attr = $(this).attr("name")
        $("." + attr).remove()
        $("#submit").attr("disabled", "disabled")
    })
    $("#userId,#username").blur(function () {
        var value = $(this).val()
        if (value) {
            var attr = $(this).attr("name")
            var t = this
            var data = ""
            if (attr == "username") {
                data = "username=" + value
            }
            else {
                data = "userId=" + value
            }
            $.getJSON("/check?" + data, function (data) {
                if (data.length) {
                    $("." + attr).remove()
                    $(t).after("<p class= \'" + attr + "\' " + "style='color: red'>已被占用！</p>")
                }
                else {
                    $("#submit").attr("disabled", "none")
                }
            })
        }
    })
})