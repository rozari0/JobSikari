from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_careers_skill_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="cv_text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
