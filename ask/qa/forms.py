from django import forms

from django.contrib.auth.models import User

from models import Question, Answer

class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

    def save(self, commit=True):
        question = super(AskForm, self).save(commit=False)
        question.author = self.user
        if commit:
            question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField()
    question = forms.IntegerField()

    def clean(self):
        data = self.cleaned_data
        
        try:
            question = Question.objects.get(pk=data['question'])
        except (Question.DoesNotExist, KeyError):
            raise forms.ValidationError("Question doesn't exists.")
        else:
            data['question'] = question
        
        return data

    def save(self):
        data = self.cleaned_data
        answer = Answer.objects.create(text=data['text'],
                              question=data['question'],
                              author=self.user)
        return answer

class UserCreationFormWithEmail(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email',)
