# Generated by Django 3.1.4 on 2021-01-16 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20210116_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionInGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_answer', models.CharField(max_length=50)),
                ('order', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='gamerecord',
            name='questions',
        ),
        migrations.AddField(
            model_name='gamerecord',
            name='current_question_n',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='simplequestion',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_set', to='quiz.questiontag'),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='questioningame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.gamerecord'),
        ),
        migrations.AddField(
            model_name='questioningame',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.simplequestion'),
        ),
    ]
