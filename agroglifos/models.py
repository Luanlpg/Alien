from django.db import models

# model de agroglifo
class Agroglifos(models.Model):
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    date = models.DateField()
    description = models.CharField(max_length=900, default='N/D')
    uuid = models.CharField(default='-- -- --', max_length=300)
    url = models.URLField(default='-- -- --', max_length=300)


    def save(self, *args, **kwargs):
        """
        Validação do campo state.
        """
        states_options = [
                "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
                "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
                "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
                ]

        if self.state not in states_options:
            raise Exception('Invalid state!')
        self.url = f'/details/{self.uuid}/'
        super(Agroglifos, self).save(*args, **kwargs)
