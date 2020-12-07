from django.urls import path

from blog.views import (
    IndexView,
    BlogListView,
    SearchPostView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    BlogDetailView,
    ContactView,
    CategoryListView,
    TagListView,
    CategoryPostView,
    TagPostView,
    CommentFormView,
#    comment_approve,
    comment_remove,
#    ReplyFormView,
#    reply_approve,
#    reply_remove,
)


app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(),name="index"),
    path('blog/', BlogListView.as_view(),name="blog"),
    path('search/', SearchPostView.as_view(), name='search_post'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(),name="blog_detail"),
    path('blog_create/', BlogCreateView.as_view(),name="blog_create"),
    path('blog_update/<int:pk>/', BlogUpdateView.as_view(),name="blog_update"),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(),name="blog_delete"),
    path('contact/', ContactView.as_view(),name="contact"),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('category/<str:category_slug>/',
         CategoryPostView.as_view(), name='category_post'),
    path('tag/<str:tag_slug>/', TagPostView.as_view(), name='tag_post'),
    path('comment/<int:pk>/', CommentFormView.as_view(), name='comment_form'),
##    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
##    path('reply/<int:pk>/', ReplyFormView.as_view(), name='reply_form'),
##    path('reply/<int:pk>/approve/', reply_approve, name='reply_approve'),
##    path('reply/<int:pk>/remove/', reply_remove, name='reply_remove'),
]
