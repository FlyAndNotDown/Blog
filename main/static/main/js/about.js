$(document).ready(function () {
    // parallax 初始化
    $('.parallax').parallax();

    // donate modal 初始化
    $('.modal').modal();
    // 绑定捐赠按钮事件
    $('.donate-modal-trigger').click(function () {
        $('#donate-modal').modal('open')
    });
});