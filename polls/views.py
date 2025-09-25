
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect  
from django.urls import reverse
from django.views import generic
from django.db import connection
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import bleach

from .models import Choice, Question, Comment


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@csrf_exempt
# FIX 
#@csrf_protect
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def search_questions(request):
    q = request.GET.get("q", "")
    # SQL-injection vulnerability 
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, question_text FROM polls_question WHERE question_text LIKE '%{q}%'")
        rows = cursor.fetchall()
    results = [{"id": r[0], "question_text": r[1]} for r in rows]
    return render(request, "polls/search_results.html", {"results": results, "query": q})

# FIX for sql-injection vulnerability
"""def search_questions(request):
    q = request.GET.get("q", "").strip()    
    if q:
        results = Question.objects.filter(question_text__icontains=q)
    else:
        results = Question.objects.none()
    return render(request, "polls/search_results.html", {"results": results, "query": q})"""


def reset_votes(request):
    # FIX for broken access control: very basic "auth" check 
    """if request.GET.get("key")!="secret123":
        return HttpResponseForbidden("Forbidden")"""
    
    Choice.objects.all().update(votes=0)
    return HttpResponse("All votes have been reset!")

def crash(request):
    1 / 0

@csrf_exempt
def add_comment(request, question_id):
    if request.method == "POST":
        Comment.objects.create(
            question_id=question_id,
            text=request.POST["text"]  
        )
        return redirect("polls:detail", pk=question_id)
    
"""
# FIX for XSS-vulnerability
@csrf_exempt
def add_comment(request, question_id):
    if request.method == "POST":
        cleaned_text = bleach.clean(request.POST["text"])
        Comment.objects.create(
            question_id=question_id,
            text=cleaned_text  
        )
        return redirect("polls:detail", pk=question_id)"""


