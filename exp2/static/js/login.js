$(function() {

    //点击“去注册”的链接
    $("#link_reg").on('click',function(event){
        event.preventDefault(); // 阻止默认行为
        $('.login-box').hide()
        $('.reg-box').show()
    })
    //点击“登录”的链接
    $("#link_login").on('click',function(){
        $('.login-box').show()
        $('.reg-box').hide()
    })
   
    //从layui 中获取form 对象
    var form =layui.form 
    var layer = layui.layer;


})



