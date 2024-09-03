from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Count
# from taggit.models import Tag

from .models import Posts, Comment
from .forms import EmailShareForm, CommentForm, SearchForm


# class PostsListView(ListView):
#     template_name = 'blog/published_post.html'
#     queryset = Posts.published_objects.all()
#     paginate_by = 3
#     context_object_name = 'posts'


def post_search(request):
    query = None
    results = []
    form = SearchForm()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Add config='russian' in SearchVector|SearchQuery to enable russian search
            # search_vector = SearchVector('title', weight='A') + SearchVector('text', weight='B')
            # search_query = SearchQuery(query)
            results = Posts.published_objects.annotate(
                similarity=TrigramSimilarity('title', query)
            ).filter(similarity__gt=0.1).order_by('-similarity')

    context = {'form': form,
               'query': query,
               'results': results}

    return render(request, 'blog/post_search.html', context=context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Posts,
                             status=Posts.Status.PUBLISHED,
                             slug=post,
                             published__year=year,
                             published__month=month,
                             published__day=day)
    # Same tags list
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Posts.published_objects.filter(tags__in=post_tags_ids).exclude(id=post.id)\
    # .annotate(same_tags=Count('tags')).order_by('-same_tags', '-published')[:4]

    # List of active comments to the post
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {'post': post,
               'form': form,
               'comments': comments,
               # 'similar_posts': similar_posts,
               }
    return render(request, 'blog/post_detail.html', context=context)


def post_share(request, post_id):
    post = get_object_or_404(Posts,
                             id=post_id,
                             status=Posts.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailShareForm(request.POST)
        if form.is_valid():
            c_d = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{c_d['title']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n {c_d['title']}\'s ({c_d['email']}) comment: {c_d['comment']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [c_d['to']])
            sent = True
            print(request.build_absolute_uri())
    else:
        form = EmailShareForm()
    context = {'post': post,
               'form': form,
               'sent': sent}
    return render(request, 'blog/post_share.html', context=context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Posts, status=Posts.Status.PUBLISHED, id=post_id)
    comment = None
    # We send comment
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # We create obj of Comment, without saving in DB
        comment = form.save(commit=False)
        # Attach post to comment
        comment.post = post
        # Save comment
        comment.save()
    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'blog/comment.html', context=context)


def published_post(request, slug_tag=None):
    posts_raw = Posts.published_objects.all()

    # tag = None
    # if slug_tag:
    #     tag = get_object_or_404(Tag, slug=slug_tag)
    #     posts_raw = posts_raw.filter(tags__in=[tag])

    # Paginated pages of our blog
    paginator = Paginator(posts_raw, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts}
    return render(request, 'blog/published_post.html', context=context)
