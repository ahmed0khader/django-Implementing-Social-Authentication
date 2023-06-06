from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Action(models.Model):
    user = models.ForeignKey('auth.User', related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    # chapter 7 || 301 => 328
    
    # • target_ct: حقل ForeignKey يشير إلى نموذج ContentType
    target_ct = models.ForeignKey(ContentType, blank=True, null=True,
                                related_name='target_obj', 
                                on_delete=models.CASCADE)
    
    # • target_id: حقل PositiveIntegerField لتخزين المفتاح الأساسي للكائن ذي الصلة
    target_id = models.PositiveIntegerField(null=True, blank=True)
    
    # • الهدف: حقل GenericForeignKey للكائن ذي الصلة بناءً على مزيج من الاثنين المجالات السابقة
    target = GenericForeignKey('target_ct', 'target_id')
    
    # تسمح لك السمة limit_choices_to بتقييد محتوى الحقول ForeignKey على مجموعة محددة من القيم.
    #  limit_choices_to => الحد_الاختيارات_إلى => 303=330
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id']),
        ]
        ordering = ['-created']
        
