import itertools
import json
import os
import shutil
import sys
from collections import defaultdict

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def add_initial_media(fixtures_dir, verbosity):
    initial_media_path = os.path.join(fixtures_dir, 'media')
    if not os.path.isdir(initial_media_path):
        return

    target_dir = os.path.join(settings.MEDIA_ROOT, 'default')
    if verbosity > 0:
        print(f"Copying default media from {initial_media_path} to {target_dir}:")

    no_media_to_copy = True
    for media_name in os.listdir(initial_media_path):
        media_path = os.path.join(initial_media_path, media_name)
        target_path = os.path.join(target_dir, media_name)
        os.makedirs(target_dir, exist_ok=True)

        if not os.path.exists(target_path):
            shutil.copy(media_path, target_path)
            no_media_to_copy = False

            if verbosity > 0:
                print(f"  {media_path}... OK")

    if no_media_to_copy:
        print(f"  No files to copy.")


def add_initial_data(fixtures_dir, app_config, apps, verbosity):
    initial_data_path = os.path.join(fixtures_dir, 'initial_data.json')
    try:
        initial_data = json.load(open(initial_data_path))
    except IOError:
        return

    if verbosity > 0:
        print("Applying initial data from " + initial_data_path + ":", file=sys.stdout)

    created_counts = defaultdict(int)

    for idx, item in enumerate(initial_data):
        model_name = item['model'].lower()  # type: str
        if model_name.startswith(app_config.name.lower() + '.'):
            model_name = model_name.split('.', 1)[1]
            model = apps.get_model(app_config.name, model_name)
            allowed_fields = set(itertools.chain(*((f.name, f.attname) for f in model._meta.fields)))

            fields = item['fields']
            fields = {k: v for k, v in fields.items() if k in allowed_fields}
            if 'slug' in fields:
                query_kwargs = {'slug': fields['slug']}
            elif item.get('pk', None):
                query_kwargs = {'pk': item['pk']}
            else:
                print(f"  Object #{idx} needs either a pk or a slug!")
                continue
            obj, created = model.objects.get_or_create(**query_kwargs, defaults=fields)
            created_counts[model._meta.verbose_name_plural.title()] += int(created)

    if verbosity > 0:
        created_counts = [(k, v) for k, v in created_counts.items() if v]
        for model_name, count in created_counts:
            print(f"  Created {count} {model_name}...")

        if not created_counts:
            print(f"  No objects to create.")


def add_seed_data(app_config, apps, verbosity, **kwargs):
    fixtures_dir = os.path.join(app_config.path, 'fixtures')
    add_initial_data(fixtures_dir, app_config, apps, verbosity)
    add_initial_media(fixtures_dir, verbosity)


class BaseAppConfig(AppConfig):
    def ready(self):
        post_migrate.connect(add_seed_data, sender=self)
