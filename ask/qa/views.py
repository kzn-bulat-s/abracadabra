from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseRedirect)
from django.shortcuts import render

from models import Question, Answer
from forms import AskForm, AnswerForm

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def _get_page_no(request):
    return request.GET.get('page', 1)

def _render_questions(request, queryset, page_no, limit=10):
    try:
        page_no = int(page_no)
    except ValueError:
        raise HttpResponseBadRequest()

    paginator = Paginator(queryset, limit)
    try:
        page = paginator.page(page_no)

        questions = page.object_list
        for question in questions:
            question.url = reverse('question', args=(question.id,))

        return render(request, 'questions.html', {
            'questions': questions
        })
    except EmptyPage:
        raise Http404()

def list_questions(request):
    page_no = _get_page_no(request)
    return _render_questions(request, Question.objects.new(), page_no)

def list_popular_questions(request):
    page_no = _get_page_no(request)
    return _render_questions(request, Question.objects.popular(), page_no)

def show_question(request, id):
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        raise Http404()
    if request.method == 'GET':
        answer_form = AnswerForm()
    elif request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        
        if answer_form.is_valid():
            answer_form.save()
        
            url = reverse('question', args=(id,))
            return HttpResponseRedirect(url)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
   
    return render(request, 'question.html', {
            'question': question,
            'answer_form': answer_form,
	})

def ask_question(request):
    if request.method == 'POST':
        ask_form = AskForm(request.POST)

        if ask_form.is_valid():
            question = ask_form.save()
            url = reverse('question', args=(question.id,))
            return HttpResponseRedirect(url)

    elif request.method == 'GET':
        ask_form = AskForm()

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
    
    return render(request, 'ask.html', {
                'ask_form': ask_form,
                'ask_url': reverse('ask') }) 
