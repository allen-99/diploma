from django.db import models


class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


class Theme(models.Model):
    theme_id = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=100)
    theme_description = models.CharField(max_length=10000, blank=True)

    def __str__(self):
        return self.theme_name


class Text(models.Model):
    text_id = models.BigAutoField(primary_key=True)
    text = models.TextField(max_length=100000)
    date = models.DateTimeField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return str(self.text_id) + '. ' + self.text[:100]


class TextBlock(models.Model):
    block_id = models.BigAutoField(primary_key=True)
    text_id = models.ForeignKey(Text, on_delete=models.CASCADE)
    theme_id = models.ForeignKey(Theme, on_delete=models.CASCADE)
    textBlock = models.TextField(max_length=255, blank=True)
    sa_value = models.FloatField()

    def __str__(self):
        return str(self.block_id) + '. ' + self.textBlock[:100] + '... sa:' + str(self.sa_value)
