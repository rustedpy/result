# Release process

1) Export the necessary environment variables:
```
# Examples: '0.8.0', '0.8.0rc1', '0.8.0b1'
export VERSION={VERSION BEING RELEASED}

# See `gpg -k`
export GPG={YOUR GPG}
```

2) Update version numbers to match the version being released:
```
vim -p src/result/__init__.py CHANGELOG.md
```

3) Update diff link in CHANGELOG.md ([see example][diff-link-update-pr-example]):
```
vim CHANGELOG.md
```

4) Do a signed commit and signed tag of the release:
```
git add result/__init__.py CHANGELOG.md
git commit -S${GPG} -m "Release v${VERSION}"
git tag -u ${GPG} -m "Release v${VERSION}" v${VERSION}
```

5) Build source and binary distributions:
```
rm -rf ./dist
python3 -m build
```

6) Sign files:
```
gpg --detach-sign -u ${GPG} -a dist/result-${VERSION}.tar.gz
gpg --detach-sign -u ${GPG} -a dist/result-${VERSION}-py3-none-any.whl
```

7) Upload package to PyPI:
```
twine upload dist/result-${VERSION}*
git push
git push --tags
```

8) Optionally check the new version is published correctly
- https://github.com/rustedpy/result/tags
- https://pypi.org/project/result/#history

2) Update version number to next dev version (for example after `v0.9.0` this should be set to `0.10.0.dev0`:
```
vim -p src/result/__init__.py
```

[diff-link-update-pr-example]: https://github.com/rustedpy/result/pull/77/files
