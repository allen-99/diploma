from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class Theme(models.Model):
    theme_id = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=100)
    theme_description = models.CharField(max_length=10000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.theme_name


class SetOfText(models.Model):
    set_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_learning = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)


class Text(models.Model):
    text_id = models.BigAutoField(primary_key=True)
    text = models.TextField(max_length=100000)
    date = models.DateTimeField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    set = models.ForeignKey(SetOfText, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.text_id) + '. ' + self.text[:100]


class Model(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.TextField(max_length=1000)
    name = models.TextField(max_length=100000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    parameters = models.TextField()


class ReviewTextBlock(models.Model):
    block_id = models.BigAutoField(primary_key=True)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    textBlock = models.TextField(max_length=255, blank=True)
    sa_value = models.FloatField()

    def __str__(self):
        return str(self.block_id) + '. ' + self.textBlock[:100] + '... sa:' + str(self.sa_value)
