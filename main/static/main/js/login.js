$(document).ready(function () {
    // 登录事件
    $('#login-btn').click(function () {
        Materialize.toast('登录事件发送', 3000);
        $.ajax({
            url: "",    //TODO
            async: true,
            data: "username=" + $('#username').val() + "&password=" + $('#password').val(),
            dataType: 'json',
            success: function(data) {
                //TODO
            }
        });
    });

    // 注册事件
    $('#register-btn').click(function () {
        Materialize.toast('注册事件发送', 3000);
        $.ajax({
            url: "",    //TODO
            async: true,
            data: "username=" + $('#username').val() + "&password=" + $('#password').val(),
            dataType: 'json',
            success: function(data) {
                //TODO
            }
        });
    });
});