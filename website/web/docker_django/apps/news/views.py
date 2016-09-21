from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required

###############################################################################
# Public pages
###############################################################################
def news(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:10:1]
    return render(request, 'news/news.html', {'posts': posts})

def lab_news(request):
    posts = Post.objects.filter(category='Lab-News').filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'news/news.html', {'posts': posts})

def social_news(request):
    posts = Post.objects.filter(category='Social').filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'news/news.html', {'posts': posts})

def other_news(request):
    posts = Post.objects.filter(category='Other').filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'news/news.html', {'posts': posts})

from watson import search as watson
def news_search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            search_results = watson.filter(Post, q)
            return render(request, 'news/search_results.html', {'search_results': search_results, 'query': q})
    return redirect('news')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    domain = Site.objects.get_current().domain
    return render(request, 'news/post_detail.html', {'post': post, 'domain': domain})


###############################################################################
# Member only pages
###############################################################################
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            try:
                post.save()
            except:
                error = 'Could not save new post, contact Will.'
                return render(request, 'landing_page/error.html', {'error': error})
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'news/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'news/post_edit.html', {'form': form})
