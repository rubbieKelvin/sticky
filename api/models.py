from uuid import uuid4
from nanoid import generate
from django.db import models

def generate_pid():
    return generate(size=9)

# Create your models here.
class Clipboard(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    text = models.TextField(max_length=100_000)
    public_id = models.CharField(default=generate_pid, max_length=9)
    date_created = models.DateTimeField(auto_now_add=True)
    view_once = models.BooleanField(default=True)
    