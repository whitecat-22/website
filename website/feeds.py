from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse

from blog.models import BlogPost


class RssLatestPostsFeed(Feed):
    title = "しろねこブログ 最新記事"
    link = "/blog/"
    description = "しろねこブログ 記事に関する最新情報。"

    def items(self):
        return BlogPost.objects.order_by('-published_at')[:5]

    def item_title(self, item):
        return item.title

    # モデルに get_absolute_url() が定義されている場合は不要
    def item_link(self, item):
        return reverse('blog:blog_detail', args=[item.pk])


class AtomLatestPostsFeed(RssLatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = RssLatestPostsFeed.description
