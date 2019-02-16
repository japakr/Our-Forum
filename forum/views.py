from django.shortcuts import render, redirect, get_object_or_404
from forum.models import Topic, Post
from forum.forms import TopicForm, PostForm
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.decorators import login_required

def index(request):
    topics = Topic.objects.order_by('-last_update')
    return render(request, 'forum/index.html', {'topics': topics})

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.author = request.user
            new_topic.last_poster = new_topic.author
            new_topic.save()
            return redirect('../')

    return render(request, 'forum/new_topic.html', {'form': form})

def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.post_set.order_by('date_added')
    return render(request, 'forum/topic.html', {'topic': topic, 'posts': posts})

@login_required
def new_post(request, topic_id, post_id=''):
    topic = get_object_or_404(Topic, id=topic_id)
    if post_id != '':
        post = get_object_or_404(Post, id=post_id)
    else:
        post = None
    posts = topic.post_set.order_by('date_added')
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.topic = topic
            new_post.father = post
            new_post.author = request.user
            new_post.save()
            topic = Topic.objects.get(id=topic_id)
            topic.last_update = timezone.now()
            topic.last_poster = new_post.author
            topic.save()
            return redirect('../')

    return render(request, 'forum/new_post.html', {'topic': topic, 'posts': posts, 'form': form, 'post': post})

@login_required
def edit_post(request, post_id, topic_id):
    post = get_object_or_404(Post, id=post_id)
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.post_set.order_by('date_added')
    if post.author != request.user:
        raise Http404

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, instance=post)
        new_post = form.save(commit=False)
        new_post.edit_date = timezone.now()
        new_post.save()
        return redirect('../')

    return render(request, 'forum/edit_post.html', {'form': form, 'selected_post': post, 'topic': topic, 'posts': posts})

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.post_set.order_by('date_added')
    if topic.author != request.user:
        raise Http404

    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.edit_date = timezone.now()
            new_topic.save()
            return redirect('../')

    return render(request, 'forum/edit_topic.html', {'topic': topic, 'posts': posts, 'form': form})
