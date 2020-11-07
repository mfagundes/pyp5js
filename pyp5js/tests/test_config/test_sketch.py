import json
import os
from pytest import fixture
from pathlib import Path
from tempfile import NamedTemporaryFile

from pyp5js.fs import LibFiles
from pyp5js.config import TRANSCRYPT_INTERPRETER, PYODIDE_INTERPRETER
from pyp5js.config.sketch import SketchConfig


@fixture
def transcrypt_json_file():
    try:
        fd = NamedTemporaryFile(mode='w', delete=False)
        data = {"interpreter": "transcrypt"}
        json.dump(data, fd)
        filename = fd.name
        fd.seek(0)
        fd.close()
        yield filename
    finally:
        os.remove(filename)

@fixture
def pyodide_json_file():
    try:
        fd = NamedTemporaryFile(mode='w', delete=False)
        data = {"interpreter": "pyodide"}
        json.dump(data, fd)
        filename = fd.name
        fd.seek(0)
        fd.close()
        yield filename
    finally:
        os.remove(filename)

@fixture
def transcrypt_config():
    return SketchConfig(interpreter=TRANSCRYPT_INTERPRETER)

@fixture
def pyodide_config():
    return SketchConfig(interpreter=PYODIDE_INTERPRETER)


def test_init_transcrypt_sketch_config_from_json(transcrypt_json_file):
    config = SketchConfig.from_json(transcrypt_json_file)
    assert config.interpreter == TRANSCRYPT_INTERPRETER


def test_init_pyodide_sketch_config_from_json(pyodide_json_file):
    config = SketchConfig.from_json(pyodide_json_file)
    assert config.interpreter == PYODIDE_INTERPRETER


def test_write_sketch_interpreter_config(transcrypt_config):
    config = transcrypt_config
    fd = NamedTemporaryFile(mode="w", delete=False)
    config.write(fd.name)
    fd.close()
    with open(fd.name) as fd:
        data = json.load(fd)

    assert data["interpreter"] == TRANSCRYPT_INTERPRETER
    os.remove(fd.name)

def test_get_transcrypt_index_template(transcrypt_config):
    template = transcrypt_config.get_index_template()
    pyp5js_files = LibFiles()
    assert pyp5js_files.transcrypt_index_html == template
    assert template.exists()

def test_get_pyodide_index_template(pyodide_config):
    template = pyodide_config.get_index_template()
    pyp5js_files = LibFiles()
    assert pyp5js_files.pyodide_index_html == template
    assert template.exists()
