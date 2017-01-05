from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from models import Question, Answer

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
    return _render_questions(request, Question.objects.all(), page_no)

def list_popular_questions(request, page):
    page_no = _get_page_no(request)
    return _render_questions(request, Question.objects.popular(), page_no)

def show_question(request, id):
    try:
        question = Question.objects.get(pk=id)
        return render(request, 'question.html', {
                'question': question
            })
    except ObjectDoesNotExist:
        raise Http404()
