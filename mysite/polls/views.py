from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by("pub_date")
    return render(request,"polls/index.html",{"latest_question_list": latest_question_list})
    
def detail(request, question_id):
  try:
    question = Question.objects.get(id=question_id)
  except Question.DoesNotExist:
    raise Http404("Yo...😩😩😩..Question does not exist")
  return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request,"polls/detail.html",{"question": question,"error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
    
        return HttpResponseRedirect(reverse("results", args=(question.id,)))
