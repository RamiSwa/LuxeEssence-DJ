from django.shortcuts import get_object_or_404, render, redirect
from .models import BlogPost, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm


# Create your views here.




def blog_list(request):
    posts = BlogPost.published.all()  # Get all published blog posts
    paginator = Paginator(posts, 3)  # 3 posts per page
    
    page_number = request.GET.get('page', 1)  # Get page number from URL

    try:
        posts = paginator.page(page_number)  # Try fetching the correct page
    except PageNotAnInteger:
        # If the page number is not an integer (invalid input), show the first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If the page number is too high (e.g., no more pages), show the last page.
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/blog-list.html', {'posts': posts})




def blog_detail(request, year, month, day, post):
    post = get_object_or_404(
        BlogPost, 
        status=BlogPost.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    
    # Fetch all active comments and replies
    comments = post.comments.filter(active=True, parent__isnull=True)
    
    # Handle comment form submission
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog_post = post
            
            # Check if this is a reply to another comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                new_comment.parent = parent_comment
            
            new_comment.save()
            return redirect(post.get_absolute_url())  # To prevent form resubmission
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/single-blog.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


# def blog_detail(request, year, month, day, post):
#     post = get_object_or_404(
#         BlogPost, 
#         status=BlogPost.Status.PUBLISHED,
#         slug=post,
#         publish__year=year,
#         publish__month=month,
#         publish__day=day
#     )
#     return render(
#         request, 'blog/single-blog.html', {'post': post}
#     )
    
    

def post_share(request, post_id):
    # Get the post object by ID
    post = get_object_or_404(BlogPost, id=post_id, status=BlogPost.Status.PUBLISHED)
    sent = False  # Flag to check if the email has been sent

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post-share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )