"""Test compatibility with Sphinx themes."""

import difflib

import pytest

from sphinxcontrib.versioning.sphinx_ import build
from sphinxcontrib.versioning.versions import Versions


@pytest.mark.parametrize('theme', [
    'alabaster',
    'sphinx_rtd_theme',
    'classic',
    'sphinxdoc',
    'traditional',
    'nature',
    'pyramid',
    'bizstyle',
])
def test_supported(tmpdir, local_docs, run, theme):
    """Test with different themes. Verify not much changed between sphinx-build and sphinx-versioning.

    :param tmpdir: pytest fixture.
    :param local_docs: conftest fixture.
    :param run: conftest fixture.
    :param str theme: Theme name to use.
    """
    target_n = tmpdir.ensure_dir('target_n')
    target_y = tmpdir.ensure_dir('target_y')
    versions = Versions([
        ('', 'master', 'heads', 1),
        ('', 'feature', 'heads', 2),
        ('', 'v1.0.0', 'tags', 3),
        ('', 'v1.2.0', 'tags', 4),
        ('', 'v2.0.0', 'tags', 5),
        ('', 'v2.1.0', 'tags', 6),
        ('', 'v2.2.0', 'tags', 7),
        ('', 'v2.3.0', 'tags', 8),
        ('', 'v2.4.0', 'tags', 9),
        ('', 'v2.5.0', 'tags', 10),
        ('', 'v2.6.0', 'tags', 11),
        ('', 'v2.7.0', 'tags', 12),
        ('', 'testing_branch', 'heads', 13),
    ], sort=['semver'])

    # Build with normal sphinx-build.
    run(local_docs, ['sphinx-build', '.', str(target_n), '-D', 'html_theme=' + theme])
    contents_n = target_n.join('contents.html').read()
    assert 'master' not in contents_n

    # Build with versions.
    build(str(local_docs), str(target_y), versions, 'master', ['-D', 'html_theme=' + theme])
    contents_y = target_y.join('contents.html').read()
    assert 'master' in contents_y

    # Verify nothing removed.
    diff = list(difflib.unified_diff(contents_n.splitlines(True), contents_y.splitlines(True)))[2:]
    assert diff
    for line in diff:
        assert not line.startswith('-')

    # Verify added.
    for name, _ in versions:
        assert any(name in line for line in diff if line.startswith('+'))


def test_sphinx_rtd_theme(tmpdir, local_docs):
    """Test sphinx_rtd_theme features.

    :param tmpdir: pytest fixture.
    :param local_docs: conftest fixture.
    """
    local_docs.join('conf.py').write('html_theme="sphinx_rtd_theme"')

    # Build branches only.
    target_b = tmpdir.ensure_dir('target_b')
    versions = Versions([('', 'master', 'heads', 1), ('', 'feature', 'heads', 2)], sort=['semver'])
    build(str(local_docs), str(target_b), versions, 'master', list())
    contents = target_b.join('contents.html').read()
    assert '<dt>Branches</dt>' in contents
    assert '<dt>Tags</dt>' not in contents

    # Build tags only.
    target_t = tmpdir.ensure_dir('target_t')
    versions = Versions([('', 'v1.0.0', 'tags', 3), ('', 'v1.2.0', 'tags', 4)], sort=['semver'])
    build(str(local_docs), str(target_t), versions, 'v1.2.0', list())
    contents = target_t.join('contents.html').read()
    assert '<dt>Branches</dt>' not in contents
    assert '<dt>Tags</dt>' in contents

    # Build both.
    target_bt = tmpdir.ensure_dir('target_bt')
    versions = Versions([
        ('', 'master', 'heads', 1), ('', 'feature', 'heads', 2),
        ('', 'v1.0.0', 'tags', 3), ('', 'v1.2.0', 'tags', 4)
    ], sort=['semver'])
    build(str(local_docs), str(target_bt), versions, 'master', list())
    contents = target_bt.join('contents.html').read()
    assert '<dt>Branches</dt>' in contents
    assert '<dt>Tags</dt>' in contents