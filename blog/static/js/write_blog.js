var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        username:'',
        is_login:false
    },
    mounted(){
        this.username= Cookies.get('username')
//        this.username=getCookie('username');
        this.is_login= Cookies.get('is_login')
//        this.is_login=getCookie('is_login');
        console.log(this.username)
    },
    methods: {
        //显示下拉菜单
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        }
    }
});
