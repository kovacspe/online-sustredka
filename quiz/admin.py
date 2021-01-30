from django.contrib import admin
from quiz import models
# Register your models here.

@admin.register(models.SimpleQuestion)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

@admin.register(models.GameRecord)
class GameRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(models.QuestionInGame)
class QuestionInGameAdmin(admin.ModelAdmin):
    pass

@admin.register(models.QuestionTag)
class QuestionTagAdmin(admin.ModelAdmin):
    pass