from django.shortcuts import get_object_or_404, render, redirect
from .models import BlogPost, Comment, Category, Banner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)
from django.db import models
from django.db.models import Count

# Create your views here.



def blog_list(request, category_slug=None, tag_slug=None):
    category = None
    tag = None


    
    # Get all categories with post count
    categories = Category.objects.annotate(post_count=models.Count('posts'))

    # Get all tags
    tags = Tag.objects.all()[:5]

    # Get all published posts
    posts = BlogPost.published.all()

    # Filter by category if category_slug is provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    # Filter by tag if tag_slug is provided
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # Paginate posts
    paginator = Paginator(posts, 3)  # Show 3 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Get recent posts
    recent_posts = BlogPost.published.order_by('-publish')[:3]  # Limit to 5 recent posts

    return render(request, 'blog/blog-list.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'recent_posts': recent_posts,
        'selected_category': category,
        'selected_tag': tag,
        
    })





def blog_detail(request, year, month, day, post):
    post = get_object_or_404(
        BlogPost, 
        status=BlogPost.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    
        # Fetch active banners
    banners = Banner.objects.filter(active=True)
    
    # Fetch categories and tags for sidebar
    categories = Category.objects.all()
    tags = Tag.objects.annotate(num_posts=Count('blogpost')).order_by('-num_posts')[:8]
    
    
    # Fetch all active comments and replies
    comments = post.comments.filter(active=True, parent__isnull=True)

    # Fetch a limited number of most-used tags for the sidebar
    tags = Tag.objects.annotate(num_posts=Count('blogpost')).order_by('-num_posts')[:8]

    # Fetch similar posts, including categories
    similar_posts = post.get_similar_posts()

    

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
        'comments': post.comments.filter(active=True, parent__isnull=True),
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'categories': categories,
        'tags': tags,
        'banners': banners,
    })

    
    

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
    
    

"""Building a search view"""




def search(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        # Define a search vector with a weight for better ranking
        search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        search_query = SearchQuery(query)

        # Annotate the posts with a rank and filter for relevant results
        results = (
            BlogPost.published.annotate(rank=SearchRank(search_vector, search_query))
            .filter(rank__gte=0.1)  # Adjust this threshold based on desired relevance
            .order_by('-rank')
        )
    
    return render(request, 'blog/search_results.html', {'query': query, 'results': results})


