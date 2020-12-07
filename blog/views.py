import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy
from django.views import generic

from blog.forms import ContactForm , CommentForm, BlogCreateForm  # ReplyForm

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Count, Q
from django.http import Http404
#from django.views.generic.detail import DetailView
#from django.views.generic.list import ListView
#from django.views.generic.edit import CreateView

from blog.models import Category, Tag, BlogPost, Comment  # Reply


logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class BlogListView(generic.ListView):
    model = BlogPost
    template_name = 'blog.html'
    paginate_by = 3

    def get_queryset(self):
        blogs = BlogPost.objects.order_by('-created_at')
        return blogs


class SearchPostView(generic.ListView):
    model = BlogPost
    template_name = 'search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


class BlogDetailView(generic.DetailView):
    model = BlogPost
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'blog_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class CategoryListView(generic.ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('blog_post', filter=Q(blog_post__is_public=True)))


class TagListView(generic.ListView):
    queryset = Tag.objects.annotate(num_posts=Count(
        'blog_post', filter=Q(blog_post__is_public=True)))


class CategoryPostView(generic.ListView):
    model = BlogPost
    template_name = 'category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostView(generic.ListView):
    model = BlogPost
    template_name = 'tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context



class CommentFormView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(BlogPost, pk=post_pk)
        comment.save()
        return redirect('blog:blog_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['blog_post'] = get_object_or_404(BlogPost, pk=post_pk)
        return context


#@login_required
#def comment_approve(request, pk):
#    comment = get_object_or_404(Comment, pk=pk)
#    comment.approve()
#    return redirect('blog:blog_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:blog_detail', pk=comment.post.pk)


#class ReplyFormView(CreateView):
#    model = Reply
#    form_class = ReplyForm
#
#    def form_valid(self, form):
#        reply = form.save(commit=False)
#        comment_pk = self.kwargs['pk']
#        reply.comment = get_object_or_404(Comment, pk=comment_pk)
#        reply.save()
#        return redirect('blog:blog_detail', pk=reply.comment.post.pk)
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        comment_pk = self.kwargs['pk']
#        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
#        return context
#
#
#@login_required
#def reply_approve(request, pk):
#    reply = get_object_or_404(Reply, pk=pk)
#    reply.approve()
#    return redirect('blog:blog_detail', pk=reply.comment.post.pk)
#
#
#@login_required
#def reply_remove(request, pk):
#    reply = get_object_or_404(Reply, pk=pk)
#    reply.delete()
#    return redirect('blog:blog_detail', pk=reply.comment.post.pk)


class ContactView(generic.FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('blog:contact')

    def form_valid(self, form):
        form.send_mail()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = BlogPost
    template_name = 'blog_create.html'
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.user = self.request.user
        blog.save()
        messages.success(self.request, 'ブログを投稿しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ブログの投稿に失敗しました。')
        return super().form_invalid(form)


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = BlogPost
    template_name = 'blog_update.html'
    form_class = BlogCreateForm

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'ブログを更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ブログの更新に失敗しました。')
        return super().form_invalid(form)


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = BlogPost
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('blog:blog')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'ブログを削除しました。')
        return super().delete(request, *args, **kwargs)
