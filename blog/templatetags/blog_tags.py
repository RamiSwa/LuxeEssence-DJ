from django import template
from django.db.models import Count
from blog.models import BlogPost

register = template.Library()

@register.filter(name='truncate_words')
def truncate_words(value, word_limit=10):
    """Truncates text to a certain number of words."""
    words = value.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return value



@register.simple_tag
def get_popular_posts(count=5):
    """Fetch the top posts with the most comments."""
    return BlogPost.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = BlogPost.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.filter(name='format_date')
def format_date(value, date_format='%B %d, %Y'):
    """
    Formats a date in the specified format.
    """
    return value.strftime(date_format) if value else ''
