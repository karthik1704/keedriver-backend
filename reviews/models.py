from django.db import models

from accounts.models import MyUser


# Create your models here.
class Review(models.Model):
    reviewer = models.ForeignKey(
        MyUser, related_name="reviewer_user", on_delete=models.CASCADE
    )
    review_to = models.ForeignKey(
        MyUser, related_name="review_user", on_delete=models.CASCADE
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    title = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return self.reviewer.get_full_name()
