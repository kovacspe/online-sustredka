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
    model = models.QuestionInGame
    
    list_display = [
        'pk',
        'player',
        'player_answer',
        'question',
        
    ]
    list_filter = (
        'question',
    )
    def player(self,obj):
        return obj.game.player
    player.admin_order_field  = 'game__player'
    player.short_description= 'Hrac'

@admin.register(models.QuestionTag)
class QuestionTagAdmin(admin.ModelAdmin):
    pass