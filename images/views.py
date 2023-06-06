from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Ajax
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Project Files
from .forms import *
from .models import *
# app actions
from actions.utils import create_action
# database Redis
import redis
from django.conf import settings
# Create your views here.

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)
# قم بإنشاء طريقة عرض جديدة لعرض ترتيب الصور الأكثر مشاهدة
@login_required
def image_ranking(request):
    # احصل على قاموس تصنيف الصور
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # احصل على معظم الصور التي يتم عرضها
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    
    context = {
        'section': 'images',
        'most_viewed': most_viewed,
    }
    return render(request, 'images/image/ranking.html', context)


# 
@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # تعيين المستخدم الحالي للعنصر
            # هذه هي الطريقة التي سنعرف بها من قام بتحميل كل صورة.
            new_image.user = request.user
            new_image.save()
            # app actions => utils.py
            create_action(request.user, 'bookmarked image', new_image)
            
            messages.success(request, 'Image added successfully')
            # إعادة التوجيه إلى عرض تفاصيل العنصر الجديد الذي تم إنشاؤه
            return redirect(new_image.get_absolute_url())
    else:
        # إنشاء نموذج بالبيانات التي يوفرها التطبيق المختصر عبر GET
        form = ImageCreateForm(request.GET)
    context = {
        'section': 'images',
        'form': form, 
        
    }
    return render(request, 'images/image/create.html', context)


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # زيادة عدد مرات مشاهدة الصورة الإجمالية بمقدار 1
    total_views = r.incr(f'image:{image.id}:views')
    # تصنيف الصور الزيادة بمقدار 1
    r.zincrby('image_ranking', 1, image.id)
    context = {
        'image': image,
        'section': 'images',
        'total_views': total_views,
    }
    return render(request, 'images/image/detail.html', context)

# AJAX
# تسجيل الدخول مطلوب
@login_required
# تتطلب POST
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                # app actions => utils.py
                create_action(request.user, 'bookmarked image', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})

        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


# إضافة ترفيم للصور لا نهائي 
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
        
    except PageNotAnInteger:
        # إذا لم تكن الصفحة عددًا صحيحًا ، فقم بتسليم الصفحة الأولى
        images = paginator.page(1)
        
    except EmptyPage:
        if images_only:
            # إذا طلب AJAX وصفحة خارج النطاق
            # إرجاع صفحة فارغة
            return HttpResponse('')
        # إذا كانت الصفحة خارج النطاق تُرجع الصفحة الأخيرة من النتائج
        images = paginator.page(paginator.num_pages)
    
    if images_only:
        return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images})
    
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})