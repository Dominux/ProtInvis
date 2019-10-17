from django.db import models

from .constants import dyes_for_form

class ProtInvis_Session(models.Model):
    uniprot_id = models.CharField(max_length=1000)
    the_dye = models.CharField(max_length=50, choices=dyes_for_form) 
    use_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uniprot_id, self.the_dye}"
