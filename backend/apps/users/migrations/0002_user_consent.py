from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='consent_given',
            field=models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных'),
        ),
        migrations.AddField(
            model_name='user',
            name='consent_given_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата согласия'),
        ),
    ]
