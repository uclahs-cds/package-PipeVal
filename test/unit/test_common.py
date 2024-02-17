# pylint: disable=C0116
# pylint: disable=C0114
# pylint: disable=C0103
from pipeval.common import skippedValidation

def test__skippedValidation__properly_skips_function_call(monkeypatch, capsys):
    monkeypatch.setenv('PIPEVAL_SKIP_CHECKSUM', 'true')

    @skippedValidation('CHECKSUM')
    def to_be_decorated():
        print('Decorated function called')

    to_be_decorated()

    out, _ = capsys.readouterr()

    assert 'Skipping validation CHECKSUM' in out
    assert 'Decorated function called' not in out

def test__skippedValidation__properly_calls_function(monkeypatch, capsys):
    monkeypatch.setenv('PIPEVAL_SKIP_CHECKSUM', 'false')

    @skippedValidation('CHECKSUM')
    def to_be_decorated():
        print('Decorated function called')

    to_be_decorated()

    out, _ = capsys.readouterr()

    assert 'Skipping validation CHECKSUM' not in out
    assert 'Decorated function called' in out
