from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from home.models import ArticleCategory,Article,Comment
from django.http.response import HttpResponseNotFound


# Create your views here.
class IndexView(View):
    def get(self,request):
        '''
        1.获取所有分类信息
        2.接收用户点击的分类id
        3.根据分类id进行分类的查询
        4。获取分页参数
        5.根据分类信息查询文章数据
        6.创建分页器
        7.进行分页处理
        8.组织数据传递给模版
        :param request:
        :return:
        '''

        # 1.获取所有分类信息
        categories = ArticleCategory.objects.all()
        # 2.接收用户点击的分类id,默认值设置为1
        cat_id = request.GET.get('cat_id',1)
        # 3.根据分类id进行分类的查询
        try:
            category = ArticleCategory.objects.get(id = cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此类')
        # 4。获取分页参数
        page_num = request.GET.get('page_num',1) # 获取当前页数
        page_size = request.GET.get('page_size',10)
        # 5.根据分类信息查询文章数据
        articles = Article.objects.filter(category=category)
        # 6.创建分页器
        from django.core.paginator import Paginator,EmptyPage
        paginator = Paginator(articles,per_page=page_size)
        # 7.进行分页处理
        try:
            page_articles = paginator.page(page_num) # 获取当前页的数据
        except EmptyPage:
            return HttpResponseNotFound('empty page')
        # 总页数
        total_page = paginator.num_pages
        # 8.组织数据传递给模板
        context = {
            'categories':categories, # 分类信息
            'category':category, # 当前分类
            'articles':page_articles,
            'page_size':page_size,
            'total_page':total_page,
            'page_num':page_num,
        }
        return render(request,'index.html',context=context)

# 博客详情视图
class DetailView(View):

    # 在浏览器中展示会发送一个get请求
    def get(self,request):
        '''
        1.接收文章id信息
        2.根据文章id进行文章数据的查询
        3.查询分类数据

        4.获取分页请求参数
        5.根据文章信息查询评论数据
        6.创建分页器
        7.进行分页处理

        8.组织模板数据
        :param request:
        :return:
        '''
        # 1.接收文章id信息
        id = request.GET.get('id')
        # 2.根据文章id进行文章数据的查询
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request,'404.html')

        else:
            # 让浏览量加1
            article.total_views += 1
            article.save()

        # 3.查询分类数据
        categories = ArticleCategory.objects.all()

        # 查询浏览量前十的文章数据,默认是升序，前面加一个 - 表示降序
        hot_articles = Article.objects.order_by('-total_views')[:9]

        # 4.获取分页请求参数
        page_size = request.GET.get('page_size',10)
        page_num = request.GET.get('page_num',1)
        # 5.根据文章信息查询评论数据
        comments = Comment.objects.filter(article=article).order_by('-created')
        # 获取评论总数
        total_count = comments.count()
        # 6.创建分页器
        from django.core.paginator import Paginator,EmptyPage
        paginator = Paginator(comments,page_size)
        # 7.进行分页处理
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('empty page')
        # 总页数
        total_page = paginator.num_pages


        # 8.组织模板数据
        context = {
            'categories':categories, # 所有的分类信息
            'category':article.category, # 当前的分类信息
            'article':article, # 文章信息
            'hot_articles':hot_articles, # 浏览量前十的文章
            'total_count':total_count,
            'comments':page_comments,
            'page_size':page_size,
            'total_page':total_page,
            'page_num':page_num

        }
        return render(request,'detail.html',context=context)

    # 提交评论会发送post请求
    def post(self,request):
        '''
        1.接收用户信息
        2.判断用户是否登录
        3.登录用户则可以接收form数据
            3.1 接收评论数据
            3.2 验证文章是否存在
            3.3 保存评论数据
            3.4 修改文章的评论数量
        4.未登录用户则跳转到登录页面
        '''
        # 1.接收用户信息
        user = request.user
        # 2.判断用户是否登录
        if user and user.is_authenticated:
            # 3.登录用户则可以接收form数据
            #     3.1 接收评论数据
            id = request.POST.get('id')
            content = request.POST.get('content')
            #     3.2 验证文章是否存在
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                return HttpResponseNotFound('没有此文章')
            #     3.3 保存评论数据
            Comment.objects.create(
                content=content,
                article=article,
                user=user
            )
            #     3.4 修改文章的评论数量
            article.comments_count += 1
            article.save()
            # 刷新当前页面（页面重定向）
            path = reverse('home:detail')+'?id={}'.format(article.id)
            return redirect(path)

        else:
            # 4.未登录用户则跳转到登录页面
            return redirect(reverse('users:login'))
        pass

