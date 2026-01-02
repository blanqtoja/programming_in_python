from django.db import models


class Record(models.Model):
    continuous_feature1 = models.FloatField(default=0.0)
    continuous_feature2 = models.FloatField(default=0.0)
    categorical_feature1 = models.IntegerField(default=0)

    def __str__(self):
        return f'Continuous feature 1: {self.continuous_feature1}, Continuous feature 2: {self.continuous_feature2}, Categorical feature 1: {self.categorical_feature1}'
