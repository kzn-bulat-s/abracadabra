from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseRedirect)
from django.shortcuts import render

from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from models import Question, Answer
from forms import AskForm, AnswerForm, UserCreationFormWithEmail

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
            answer_form.user = request.user
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
            ask_form.user = request.user
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

def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationFormWithEmail(request.POST)
        if signup_form.is_valid():
            try:
                user = signup_form.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login_user(request, user)
            except Exception as e:
                print e
            else:
                return HttpResponseRedirect('/')

    elif request.method == 'GET':
        signup_form = UserCreationFormWithEmail()
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    return render(request, 'signup.html', {
            'signup_form': signup_form
        })

def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            try:
                data = login_form.cleaned_data
		print data
                user = authenticate(username=data['username'],
                                    password=data['password'])
		print user
                if user is not None and user.is_active:
                    login_user(request, user)
                    return HttpResponseRedirect('/')
            except:
                pass
            else:
                return HttpResponseRedirect('/')
	print login_form.cleaned_data
	print login_form.errors

    elif request.method == 'GET':
        login_form = AuthenticationForm()
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    return render(request, 'login.html', {
            'login_form': login_form
        })
