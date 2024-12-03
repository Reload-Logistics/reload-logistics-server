from django.db import models
from django.utils import timezone

class FrequentlyAskedQuestion(models.Model):

    id = models.AutoField(primary_key=True)
    
    question = models.CharField(default = "", max_length = 1500, null=True, blank=True)
    answer = models.CharField(default = "", max_length = 2000, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"Question {self.id}"