# Release process

Signing key: https://dbrgn.ch/F2F3A5FA.asc

Used variables:

    export VERSION={VERSION}
    export GPG=F2F3A5FA

Update version numbers:

    vim -p result/__init__.py CHANGELOG.md

Update diff link in CHANGELOG.md ([see example][diff-link-update-pr-example]):

    vim CHANGELOG.md

Do a signed commit and signed tag of the release:

    git add result/__init__.py CHANGELOG.md
    git commit -S${GPG} -m "Release v${VERSION}"
    git tag -u ${GPG} -m "Release v${VERSION}" v${VERSION}

Build source and binary distributions:

    rm -rf dist/*
    python3 -m build

Sign files:

    gpg --detach-sign -u ${GPG} -a dist/result-${VERSION}.tar.gz
    gpg --detach-sign -u ${GPG} -a dist/result-${VERSION}-py3-none-any.whl

Upload package to PyPI:

    twine upload dist/result-${VERSION}*
    git push
    git push --tags

[diff-link-update-pr-example]: https://github.com/rustedpy/result/pull/77/files
