from django.db import models
from django.utils import timezone
import random
import unidecode

def unify(text):  
    text = text.strip()
    text = unidecode.unidecode(text)
    return text.lower().replace(',','.')

class QuestionTag(models.Model):
    class Meta:
        verbose_name = 'kategória'
        verbose_name_plural = 'kategórie'
    name = models.CharField(max_length=50)
    sample = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.name

class SimpleQuestion(models.Model):
    text = models.TextField()
    answer = models.TextField()
    tag = models.ForeignKey(QuestionTag,null=True,on_delete=models.CASCADE,related_name='question_set')
    def __str__(self):
        return self.text


class Player(models.Model):
    class Meta:
        verbose_name = 'Účastník'
        verbose_name_plural = 'Účastníci'

    email = models.EmailField()
    nickname = models.CharField(max_length=50)

    def create_game(self):
        gr = GameRecord.objects.create(points=0,player=self,current_question_n=0)
        tags = QuestionTag.objects.all()
        questions=[]
        for tag in tags:
            questions+=random.sample(list(tag.question_set.all()),tag.sample)
        for i,q in enumerate(questions):
            QuestionInGame.objects.create(order=i,question=q,game=gr)
        gr.num_questions = len(questions)
        gr.save()
        return gr
    def __str__(self):
        return f'{self.nickname} ({self.email})'
        


class GameRecord(models.Model):
    class Meta:
        verbose_name = 'Záznam hry'
        verbose_name_plural = 'Záznamy hry'

    points = models.PositiveSmallIntegerField()
    time = models.FloatField(null=True)
    start_at = models.DateTimeField(default=None,null=True)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    current_question_n = models.PositiveSmallIntegerField(null=True)
    num_questions = models.PositiveSmallIntegerField(null=True)
    def __str__(self):
        return f'{self.player} - {self.start_at}'

    def current_question(self):
        if self.current_question_n>=self.num_questions:
            return None
        return self.questions.filter(order=self.current_question_n).first().question

    def answer_and_get_next(self,answer):
        q = self.questions.filter(order=self.current_question_n).first()
        q.player_answer = unidecode.unidecode(str(answer)).lower()
        q.save()
        self.current_question_n=self.current_question_n+1
        self.save()
        if self.current_question_n>=self.num_questions:
            return None
        return self.current_question()

    def evaluate(self):
        self.time = (timezone.now()-self.start_at).seconds
        points=0
        for q in self.questions.all():
            points+= 1 if q.validate() else 0
        self.points = points
        self.save()
        return self.points,self.time
        

class QuestionInGame(models.Model):
    game = models.ForeignKey(GameRecord,on_delete=models.CASCADE,related_name='questions')
    question = models.ForeignKey(SimpleQuestion,on_delete=models.CASCADE)
    player_answer = models.CharField(max_length=50,verbose_name='Odpoveď',blank=True)
    order = models.PositiveSmallIntegerField()

    def validate(self):
        return unify(self.player_answer) == unify(self.question.answer)