from django.db.models import Count, Q

from blog.models import Category, Tag


def common(request):
    context = {
        'categories': Category.objects.annotate(
            num_posts=Count('blog_post', filter=Q(blog_post__is_public=True))),
        'tags': Tag.objects.annotate(
            num_posts=Count('blog_post', filter=Q(blog_post__is_public=True))),
    }
    return context
