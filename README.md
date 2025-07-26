# air-markdown

![PyPI version](https://img.shields.io/pypi/v/air_markdown.svg)

Air Tags + Markdown!

* Free software: MIT License
* Documentation: https://air-markdown.readthedocs.io.

## Features

* Handy `Markdown()` Air Tag that renders markdown into HTML.

## Installation

Via pip:

```sh
pip install air-markdown
```

or uv:

```sh
uv add air-markdown
```

## Usage

```python
from air_markdown import Markdown

Markdown('# Hello, world')
```

Renders as:

```html
<h1>Hello, world.</h1>
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
