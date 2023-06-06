from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Image(models.Model):
    # يشير هذا إلى كائن المستخدم الذي وضع إشارة مرجعية على هذه الصورة
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    # تم إنشاؤه: التاريخ والوقت اللذين يشيران إلى وقت إنشاء الكائن في قاعدة البيانات. نحن
    # أضافت auto_now_add لتعيين التاريخ والوقت الحالي تلقائيًا عند إنشاء الكائن.
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
    # اجمالي عدد الاعجابات 
    total_likes = models.PositiveIntegerField(default=0) 
    
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
    