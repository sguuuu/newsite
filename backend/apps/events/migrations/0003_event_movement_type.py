from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='movement_type',
            field=models.CharField(
                choices=[
                    ('olympiad_movement', 'Подготовительно-олимпиадное движение'),
                    ('career_guidance', 'Профориентационное движение'),
                ],
                default='olympiad_movement',
                max_length=30,
                verbose_name='Направление движения',
            ),
        ),
    ]
