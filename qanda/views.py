from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Question, Answer


def question_list(request):
    questions = Question.objects.all()
    return render(request, 'qanda/question_list.html', {'questions': questions})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    
    if request.method == 'POST':
        answer_text = request.POST.get('answer_text', '').strip()
        if answer_text:
            Answer.objects.create(question=question, text=answer_text)
            messages.success(request, 'Answer submitted successfully!')
            return redirect('question_detail', pk=pk)
        else:
            messages.error(request, 'Answer cannot be empty.')
    
    return render(request, 'qanda/question_detail.html', {'question': question})


def ask_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '').strip()
        if question_text:
            Question.objects.create(text=question_text)
            messages.success(request, 'Question submitted successfully!')
            return redirect('question_list')
        else:
            messages.error(request, 'Question cannot be empty.')
    
    return render(request, 'qanda/ask_question.html')
