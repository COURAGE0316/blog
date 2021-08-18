var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data() {
        return {
            host,
            show_menu:false,
            is_login:true,
            username:''
        }
    },
    mounted(){
//        console.log(getCookie('username'))
        this.username= Cookies.get('username')
        this.is_login=Cookies.get('is_login');
        console.log(this.username)
//        this.is_login=true
    },
    methods: {
        //显示下拉菜单
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        },
    }
});
