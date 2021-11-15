#from libraryshop.models import UserOwnBook, Book, User
from django.conf import settings
import libraryshop.models
from django.db import migrations, models
import django.db.models.deletion
#from django.db.models
hello=migrations.CreateModel(name='UserOwnBook', fields=[ ('id', models.BigAutoField(auto_created=True,
    primary_key=True, serialize=False, verbose_name='ID')), ('book_id',
    models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='libraryshop.book')), ('user_id',
        models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
    ],
),
