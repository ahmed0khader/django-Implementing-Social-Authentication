from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse #DONE
from django.contrib.auth import authenticate, login, logout #DONE
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

# chapter 7
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# app actions => utils.py 308 => 334
from actions.utils import create_action 
from actions.models import Action


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else: 
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)

# register
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_user': new_user,})
    else:
        user_form = UserRegistrationForm()
        
    context = {
        'user_form': user_form,
    }
    return render(request, 'account/register.html', context)


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10] # select_related => العناصر ذات الصلة
    context = {
        'section': 'dashboard',
        'actions': actions
    }
    return render(request, 'account/dashboard.html', context)


# Edit Profile 
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
        }
    return render(request, 'account/edit.html', context)

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    
    context = {
        'users': users,
        'section': 'people',
    }
    return render(request, 'account/user/list.html', context)

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    
    context = {
        'user': user,
        'section': 'people',
    }
    return render(request, 'account/user/detail.html', context)


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create( 
                    user_from=request.user,
                    user_to=user
                    )
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                    ).delete()
                
            return JsonResponse({'status':'ok'})
        
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})
