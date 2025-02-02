import io
import json
import sys
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from django.conf import settings
from django.http import FileResponse
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def get_dump(request):
    python_exe = sys.executable
    manage_py = Path(settings.BASE_DIR) / 'manage.py'
    with TemporaryDirectory() as tempdirname:
        dump_filepath = f'{tempdirname}/dump.json'
        run(
            [str(python_exe),
             str(manage_py),
             'dumpdata',
             '--indent=4',
             '--exclude', 'auth.permission',
             '--exclude', 'contenttypes',
             '-o',
             dump_filepath]
        )
        with open(dump_filepath, 'rb') as dump:
            dump_in_memory = io.BytesIO(dump.read())
            return FileResponse(dump_in_memory,
                                as_attachment=True,
                                filename="dump.json")