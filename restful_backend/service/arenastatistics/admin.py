from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Player)
admin.site.register(QuestionTopic)
admin.site.register(QuestionVariant)
admin.site.register(Question)
admin.site.register(Session)
admin.site.register(Round)
admin.site.register(Participation)
admin.site.register(Answer)

