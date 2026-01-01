from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text[:50]
    
    class Meta:
        ordering = ['-created_at']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Answer to: {self.question.text[:30]}"
    
    class Meta:
        ordering = ['created_at']
