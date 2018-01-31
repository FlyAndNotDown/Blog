$(document).ready(function () {
    // 初始化 tooltip
    $('.tooltipped').tooltip({
        delay: 50
    });

    // // 为 p 标签添加 flow-text 类
    // $('p').addClass('flow-text');
    // $('#post-container').show();
    // $('#footer').show();

    // 为返回按键添加响应
    $('#go-back').click(function () {
        window.history.back();
    });

    // donate modal 初始化
    $('.modal').modal();
    // 绑定捐赠按钮事件
    $('.donate-modal-trigger').click(function () {
        $('#donate-modal').modal('open')
    });
});