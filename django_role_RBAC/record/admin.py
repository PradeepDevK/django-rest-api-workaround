from django.contrib import admin
from record.models import StudentAssessmentRecord

@admin.register(StudentAssessmentRecord)
class StudentAssessmentRecordAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "score",]