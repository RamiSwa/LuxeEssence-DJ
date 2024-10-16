from django.shortcuts import get_object_or_404, render
from .models import BlogPost, Category


# Create your views here.


def blog_list(request):
    posts = BlogPost.published.all()
    
    return render(request, 'blog/blog-list.html', {'posts': posts})



def blog_detail(request, id):
    post = get_object_or_404(
        BlogPost, 
        id=id,
        status=BlogPost.Status.PUBLISHED
    )
    return render(
        request, 'blog/single-blog.html', {'post': post}
    )