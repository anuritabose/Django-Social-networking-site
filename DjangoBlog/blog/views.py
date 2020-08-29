from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin#if we try to create a post without being logged in, we will be redirected to the login page; we can't use decorators for this purpose because they can be used only with functions. For classes, we use mixins
from django.views.generic import (
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView
)
from .models import Post



def home(request):
    context={
    'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] #to change order of posts on home page-it now displays latest posts first

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields = ['title', 'text']

    def form_valid(self,form):
        form.instance.author=self.request.user #takes the instance and sets the author = the current logged in user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields = ['title', 'text']
    
    def form_valid(self,form):
        form.instance.author=self.request.user #takes the instance and sets the author = the current logged in user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object() #gets the post that we're currently trying to update
        if self.request.user==post.author: #check if the current logged in user=author of the post we're trying to update
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object() #gets the post that we're currently trying to update
        if self.request.user==post.author: #check if the current logged in user=author of the post we're trying to update
            return True
        return False


def about(request):
    return render(request,'blog/about.html')

#PostListView is a class based view. class based views look for a specific type of template:
#   <app>/<model>_<viewtype>.html


