from django.db import models
from django.conf import settings
# إضافة الحقل التالي للمستخدم ديناميكيًا
from django.contrib.auth import get_user_model
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
    
# شابتر 7
class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    # لتخزين الوقت الذي تم فيه إنشاء العلاقة
    created = models.DateTimeField(auto_now_add=True)
    # 
    
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
        
        def __str__(self):
            return f'{self.user_from} follows {self.user_to}'
        
# إضافة الحقل التالي للمستخدم ديناميكيًا
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))
# متماثل = خطأ لتعريف علاقة غير متناظرة (إذا تابعتك ، فذلك لا يعني أنك تتابعني تلقائيًا). symmetrical=False
