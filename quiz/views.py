from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from quiz.forms import StartForm
from quiz import models
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.utils import timezone
from functools import cmp_to_key

class ContactList(ListView):
    paginate_by = 2
    model = models.SimpleQuestion

def question(request):
    contact_list = models.SimpleQuestion.objects.all()
    paginator = Paginator(contact_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quiz/list.html', {'page_obj': page_obj})

def start(request):
    if request.method == 'POST':
        form = StartForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Create quiz session object and start it
            try:
                player = models.Player.objects.get(email=form.cleaned_data['email'])
            except models.Player.DoesNotExist:
               return render(request, 'quiz/wrong_player.html', {'email': form.cleaned_data['email']})
            g = player.create_game()
            return redirect(f'start-game/{g.pk}/')
    else:
        form = StartForm()

    return render(request, 'quiz/start.html', {'form': form})

def game(request,pk):
    gr = get_object_or_404(models.GameRecord,pk=pk)
    if request.method == 'POST':
        answer = request.POST['answer']
        q  = gr.answer_and_get_next(answer)
    else:
        q = gr.current_question()
    if q is None:
        if gr.time is None:
            gr.evaluate()
        return render(request,'quiz/game_results.html',{'player': gr.player,'time':gr.time,'points':gr.points,'max_points':gr.num_questions})
    return render(request,'quiz/question.html',{'question_text':q.text,'pk':pk})
        


def start_game(request,pk):
    gr = get_object_or_404(models.GameRecord,pk=pk)
    if request.method == 'POST':
        
        if gr.start_at is not None:
            return redirect(f'/quiz/game/{pk}/')
        gr.start_at = timezone.now()
        gr.current_question_n = 0
        gr.save()
        return redirect(f'/quiz/game/{pk}/')
    else:
        return render(request, 'quiz/instructions.html', {'player': gr.player,'pk':pk})


def results(request):
    # Sort by player
    records = models.GameRecord.objects.order_by('player','-points','time','start_at')
    
    # Get best for every player
    result_board = []
    current_player = None
    for rec in records:
        print(rec.player,',',rec.points,',',rec.time)
        if rec.player!=current_player: 
            result_board.append(rec)
            current_player = rec.player

    # Sort
    def comp_rec(it1,it2):
        if it1.points>it2.points:
            return -1
        elif it1.points<it2.points:
            return 1
        else:
            if it1.time>it2.time:
                return 1
            elif it1.time<it2.time:
                return -1
            else:
                return 0
    result_board = sorted(result_board,key=cmp_to_key(comp_rec))

    # Render
    return render(request, 'quiz/results.html', {'results': result_board})

