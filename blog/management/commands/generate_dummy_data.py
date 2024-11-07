from django.contrib.auth import get_user_model
from django.utils.text import slugify
from blog.models import BlogPost, Category, Comment, Banner
from taggit.models import Tag
from random import choice, randint
from faker import Faker
import datetime

fake = Faker()
User = get_user_model()

# Create or get a test user
author, created = User.objects.get_or_create(username='testuser', defaults={'password': 'testpassword'})

# Create categories
categories = [
    Category.objects.get_or_create(name=name, slug=slugify(name))[0]
    for name in ["Skincare", "Makeup", "Wellness", "Haircare", "Beauty Tips"]
]

# Create tags
tags = [
    Tag.objects.get_or_create(name=name)[0]
    for name in ["hydration", "anti-aging", "organic", "natural", "trending"]
]

# Create blog posts
for i in range(20):
    title = fake.sentence(nb_words=6)
    slug = slugify(title)
    body = fake.paragraph(nb_sentences=10)
    publish_date = datetime.datetime.now() - datetime.timedelta(days=randint(0, 30))

    # Randomly assign a category and tags
    category = choice(categories)
    selected_tags = [choice(tags) for _ in range(randint(1, 3))]

    # Create the post
    post = BlogPost.objects.create(
        title=title,
        slug=slug,
        author=author,
        category=category,
        body=body,
        publish=publish_date,
        status=BlogPost.Status.PUBLISHED,
        meta_title=fake.sentence(nb_words=4),
        meta_description=fake.text(max_nb_chars=150),
        excerpt=fake.text(max_nb_chars=100),
    )
    post.tags.set(selected_tags)
    post.save()

    # Print for feedback
    print(f"Created post: {title} with category {category.name}")

# Create comments for blog posts
posts = BlogPost.objects.all()
for post in posts:
    for _ in range(randint(1, 5)):
        comment = Comment.objects.create(
            blog_post=post,
            author=fake.name(),
            email=fake.email(),
            body=fake.paragraph(nb_sentences=3),
            active=True,
        )
        print(f"Created comment by {comment.author} on post '{post.title}'")

# Create banners
for i in range(5):
    Banner.objects.create(
        name=f"Banner {i + 1}",
        image='banners/default.jpg',  # Adjust to match a default image
        link=fake.url(),
        active=True,
        position=i,
    )
    print(f"Created banner {i + 1}")
