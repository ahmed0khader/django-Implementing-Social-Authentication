from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils import timezone
from .models import Action

# chapter 7 page => 304 => 331

def create_action(user, verb, target=None):
    # تحقق من أي إجراء مشابه تم اتخاذه في الدقيقة الأخيرة
    # لتجنب حفظ الإجراءات المكررة وإرجاع قيمة منطقية لإخبارك ما إذا تم حفظ الإجراء.
    # هذه هي الطريقة التي تتجنب بها التكرارات
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60) #الدقيقة الأخيرة => last_minute
    similar_actions = Action.objects.filter(user_id=user.id,  #إجراءات مماثلة => similar_actions
                                            verb=verb, 
                                            created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                target_id=target.id)
    if not similar_actions:
        # لم يتم العثور على إجراءات حالية
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False