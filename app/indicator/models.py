from django.db import models
from core.models import Program, SubProgram, Activity  # ✅ import Activity

class Indicator(models.Model):
    year = models.PositiveIntegerField(verbose_name="Fiscal Year")
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    subprogram = models.ForeignKey(SubProgram, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)  # ✅ new field
    output_indicator = models.CharField(max_length=255, blank=True)
    target_indicator = models.CharField(max_length=255, blank=True)

    def __str__(self):
        parts = [str(self.program)]
        if self.subprogram:
            parts.append(str(self.subprogram))
        if self.activity:
            parts.append(str(self.activity))
        return " - ".join(parts)
