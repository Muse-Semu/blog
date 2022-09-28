from ctypes import LibraryLoader
from importlib.util import LazyLoader
from multiprocessing import context
from multiprocessing.util import is_exiting
from . import models
from re import template
from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Profile,Comment
from .forms import ProfileUpdateForm,UserUpdate,UserRegistrationForm,CommentForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
def frontpage(request):
    posts=Post.objects.all()
    return render(request,'blog/homepage.html',{'posts':posts}) 
def about(request):
    return render(request,'blog/about.html')
def PostCatagory(request,cats):
    post_catagory=Post.objects.filter(catagory=cats)
    post_count=Post.objects.filter(catagory=cats).count
    return render(request,'blog/catagory.html',{'cats':cats ,'post_catagory':post_catagory,'post_count':post_count})
def LikeView(request,pk):
   post=get_object_or_404(Post,id=request.POST.get('lk'))
   post.like.add(request.user)
   if request.user:
      model=Post    
      context_object_name='post'
   else:
        post.like.remove(request.user)   
   return HttpResponseRedirect(reverse('home'))

class HomePage(ListView):
    template_name='blog/homepage.html'
    model=Post
    context_object_name='post'
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['count']=context['post'].count()
        search=self.request.GET.get('search-area') or ''
        if search:
            context['post']=context['post'].filter(title__icontains=search)
            context['result']=context['post'].filter(title__icontains=search).count()
            context['search']=search
        return context     
class LoginUser(LoginView):
    template_name="blog/signin.html"
    fields="__all__"
    redirect_authenticated_user=False
    def get_success_url(self):
        return reverse_lazy('home')
class PostCreate(LoginRequiredMixin,CreateView):
    template_name='blog/post_form.html'
    model=Post
    fields=['title','image','discription','body','catagory']
    success_url=reverse_lazy('userpost')
    def form_valid(self,form): 
         form.instance.user=self.request.user
         return super(PostCreate,self).form_valid(form)
class UserRegister(UserRegistrationForm,FormView):
    template_name="blog/signup.html"
    form_class=UserRegistrationForm
    redirect_authenticated_user=True
    fields=('username','email','password1','password2')
    success_url=reverse_lazy('signup')
    def form_valid(self, form): 
         user = form.save()
         if user is not None:
            login(self.request,user) 
         return super(UserRegister,self).form_valid(form)   
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
             return redirect('login')     
        return super(UserRegister,self).get(*args,*kwargs)
class UserPosts(LoginRequiredMixin,ListView):
    model=Post
    context_object_name='post' 
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['post']=context['post'].filter(user=self.request.user)
        context['count']=context['post'].filter(user=self.request.user).count()
        search=self.request.GET.get('search-area') or ''
        if search:
            context['post']=context['post'].filter(title__icontains=search ) 
            context['result']=context['post'].filter(title__icontains=search).count()
            context['search']=search
        return context            
    def myPost(request):
        posts=Post.objects.filter(user=request.user)
        count=Post.objects.filter(user=request.user).count()  
        search_re=request.GET.get('search-area') or ''
        if search_re:
            posts=Post.objects.filter(title__icontains=search_re) and Post.objects.filter(title__icontains=search_re)
            count=Post.objects.filter(title__icontains=search_re).count()
            posts['search']=search_re
        return render(request,'blog/post_list.html',{'posts':posts,'count':count})     
class PostDelete(LoginRequiredMixin,DeleteView):
    model=Post
    template_name='blog/delete_post.html'
    context_object_name='post'
    success_url=reverse_lazy('home')  
class PostUpdate(LoginRequiredMixin,UpdateView):
    model=Post
    fields=('title','discription','body','image','catagory')
    success_url=reverse_lazy('userpost')
class PostDetail(DetailView):
    model=Post
    context_object_name='post'
    template_name='blog/post_detail.html'
class UserProfile(LoginRequiredMixin,ListView):
    model=Profile
    context_object_name='profile' 
    template_name='blog/profile.html'
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        return context
class AddPostComment(LoginRequiredMixin,CreateView):
    model=Comment
    context_object_name='comment' 
    form_class=CommentForm 
    template_name='blog/add_coment.html' 
    success_url=reverse_lazy('home') 
    def form_valid(self, form):
        form.instance.post_id=self.kwargs['pk']
        if self.request.user.is_authenticated:
            form.instance.user=self.request.user
        return super().form_valid(form)
class PostComment(ListView):
    model=Comment
    context_object_name='comment'  
    template_name='blog/post_comment.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['comment']=context['comment'].filter(post_id=self.kwargs['pk'])
        context['id']=self.kwargs['pk']
        cm=Comment.objects.all()
        context['user']=cm
        
        return context
@login_required
def profile(request):
    if request.method =="POST":
        u_form=UserUpdate(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,
                           request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
        else:
           u_form=UserUpdate(instance=request.user)  
           p_form=ProfileUpdateForm(instance=request.user.profile)
    u_form=UserUpdate(instance=request.user)
    p_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        "u_form":u_form,
        "p_form":p_form
        }
    pro=Profile.objects.filter(user=request.user)
    return render(request,'blog/profile.html',context)
def search(request):
    return render(request,'blog/homepage.html')
class UserView(LoginRequiredMixin,ListView):
      model=User
      context_object_name='user'
      template_name='blog/userlist.html'
      def get_context_data(self, **kwargs) :
          if self.request.user.is_superuser :
           context = super().get_context_data(**kwargs)
           context['ct']=context['user'].count()
           return context;    
class DeleteUser(LoginRequiredMixin,DeleteView): 
    model=User
    context_object_name='user'
    template_name='blog/delete_user.html'
    success_url=reverse_lazy('users')
class UpdateUserStatus(LoginRequiredMixin,UpdateView,FormView):
    model=User
    fields='__all__'
    template_name='blog/user_status.html'
    success_url=reverse_lazy('users')  
    def form_valid(self, form): 
        form.save()   
        return super(UpdateUserStatus,self).form_valid(form)   
    def get(self,*args,**kwargs):
        return super(UpdateUserStatus,self).get(*args,*kwargs)
class RegisterAdmin(LoginRequiredMixin,CreateView):
    template_name="blog/signup.html"
    form_class=UserRegistrationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('users')
    def form_valid(self, form): 
        form.save()   
        return super(RegisterAdmin,self).form_valid(form)   
    def get(self,*args,**kwargs):
        return super(RegisterAdmin,self).get(*args,*kwargs)
def about(request):
    return render(request,'blog/about.html')    