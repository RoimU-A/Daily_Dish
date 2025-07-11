# Generated by Django 4.2 on 2025-07-09 07:42

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(max_length=100)),
                ('api_key', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('last_used_at', models.DateTimeField(blank=True, null=True)),
                ('usage_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'api_keys',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=255)),
                ('recipe_url', models.URLField(blank=True, max_length=500, null=True)),
                ('ingredient_1', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_1', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_1', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_2', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_2', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_2', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_3', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_3', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_3', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_4', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_4', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_4', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_5', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_5', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_5', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_6', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_6', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_6', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_7', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_7', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_7', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_8', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_8', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_8', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_9', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_9', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_9', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_10', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_10', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_10', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_11', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_11', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_11', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_12', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_12', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_12', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_13', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_13', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_13', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_14', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_14', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_14', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_15', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_15', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_15', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_16', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_16', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_16', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_17', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_17', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_17', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_18', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_18', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_18', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_19', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_19', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_19', models.CharField(blank=True, max_length=20, null=True)),
                ('ingredient_20', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_20', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('unit_20', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='IngredientCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=1, max_digits=10)),
                ('unit', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ingredient_cache',
            },
        ),
        migrations.CreateModel(
            name='CookedDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daily_dish.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cooked_dishes',
            },
        ),
        migrations.AddIndex(
            model_name='apikey',
            index=models.Index(fields=['api_key'], name='api_keys_api_key_ce86c7_idx'),
        ),
        migrations.AddIndex(
            model_name='apikey',
            index=models.Index(fields=['is_active'], name='api_keys_is_acti_73be43_idx'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['user'], name='recipes_user_id_cc6c4b_idx'),
        ),
        migrations.AddIndex(
            model_name='ingredientcache',
            index=models.Index(fields=['user'], name='ingredient__user_id_47e501_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='ingredientcache',
            unique_together={('user', 'ingredient_name')},
        ),
        migrations.AddIndex(
            model_name='cookeddish',
            index=models.Index(fields=['user'], name='cooked_dish_user_id_d1e44a_idx'),
        ),
        migrations.AddIndex(
            model_name='cookeddish',
            index=models.Index(fields=['recipe'], name='cooked_dish_recipe__9ed29b_idx'),
        ),
        migrations.AddIndex(
            model_name='cookeddish',
            index=models.Index(fields=['created_at'], name='cooked_dish_created_369ea1_idx'),
        ),
    ]
