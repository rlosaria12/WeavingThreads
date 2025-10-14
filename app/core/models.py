from django.db import models

class Program(models.Model):
    program_number = models.IntegerField(max_length=5, unique=True, blank=False)
    program = models.CharField(max_length=255, blank=False, verbose_name="Program Name")

    def save(self, *args, **kwargs):
        # Auto-generate program_number only if empty
        if not self.pk and not self.program_number:  # only on creation
            last = Program.objects.order_by('-id').first()
            next_number = (last.id + 1) if last else 1
            self.program_number = str(next_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Program {self.program_number}: {self.program}"

    class Meta:
        ordering = ['program_number']


class SubProgram(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name='subprograms',
        verbose_name="Program Name"
    )
    
    subprogram_number = models.IntegerField(max_length=5, blank=False, verbose_name="Sub-Program Number")
    subprogram = models.CharField(max_length=255, blank=False, verbose_name="Sub-Program Name")

    def save(self, *args, **kwargs):
        # Auto-generate subprogram_number per program only if empty
        if not self.subprogram_number:
            last = SubProgram.objects.filter(program=self.program).order_by('-id').first()
            if last and last.subprogram_number.isdigit():
                next_number = int(last.subprogram_number) + 1
            else:
                next_number = 1
            self.subprogram_number = str(next_number)
        super().save(*args, **kwargs)

    def __str__(self):
        # single-line representation for admin
        return f"{self.program.program_number}.{self.subprogram_number} {self.subprogram}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['program', 'subprogram_number'],
                name='unique_subprogram_per_program'
            )
        ]

        ordering = ['program__program_number', 'subprogram_number']

class Activity(models.Model):
    subprogram = models.ForeignKey(
        SubProgram,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name="Sub-Program Name"
    )
    activity_number = models.IntegerField(max_length=5, blank=False)
    activity = models.CharField(max_length=255, blank=False, verbose_name="Activity Name")

    def __str__(self):
        return f"{self.subprogram.program.program_number}.{self.subprogram.subprogram_number}.{self.activity_number} {self.activity}"

    class Meta:
        verbose_name_plural = "Activities"
        constraints = [
            models.UniqueConstraint(
                fields=['subprogram', 'activity_number'],
                name='unique_activity_per_subprogram'
            )
        ]
    ordering = ['activity_number']

class SubActivity(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='subactivities',
        verbose_name="Activity"
    )
    subactivity_number = models.CharField(max_length=5, blank=False, verbose_name="Sub-Activity Number")
    subactivity = models.CharField(max_length=255, blank=False, verbose_name="Sub-Activity Name")

    def __str__(self):
        return f"{self.activity.subprogram.program.program_number}." \
               f"{self.activity.subprogram.subprogram_number}." \
               f"{self.activity.activity_number}." \
               f"{self.subactivity_number} {self.subactivity}"

    class Meta:
        verbose_name_plural = "Sub-Activities"
        constraints = [
            models.UniqueConstraint(
                fields=['activity', 'subactivity_number'],
                name='unique_subactivity_per_activity'
            )
        ]
        ordering = [
            'activity__subprogram__program__program_number',
            'activity__subprogram__subprogram_number',
            'activity__activity_number',
            'subactivity_number'
        ]



