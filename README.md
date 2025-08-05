# air-markdown

![PyPI version](https://img.shields.io/pypi/v/air_markdown.svg)

Markdown = Air Tags + Mistletoe

* Free software: MIT License
* Documentation: https://air-markdown.readthedocs.io.

## Features

* Handy `Markdown()` Air Tag that renders Markdown into HTML.
* Powerful `AirMarkdown()` Air Tag that renders Markdown into HTML, including rendering of Air Tags inside ````air-live``` blocks. For example, if you have:

```air-live
air.H2("Heading 2")
```

it will render as `<h2>Heading 2</h2>`.


## Installation

Via uv:

```sh
uv add air-markdown
```

Or pip:

```sh
pip install air-markdown
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

## Customizing the rendered HTML

Mistletoe allows for customization of the renderer through overloading of the `Markdown.html_renderer` property. 

```python
from air_markdown import Markdown
import mistletoe

class SupermanRenderer(mistletoe.HtmlRenderer):
    def render_strong(self, token: mistletoe.span_token.Strong) -> str:
        template = '<strong class="superman">{}</strong>'
        return template.format(self.render_inner(token))  

Markdown.html_renderer = SupermanRenderer
```

Now `Markdown("**Look in the sky!**")` renders

```html
<p><strong class="superman">Look in the sky!</strong></p>\n
```

## Wrapping Markdown output

If you need to wrap Markdown output, just override the `Markdown.wrapper`. So if you need all content to be wrapped by a `section` tag:

```python
Markdown.wrapper = lambda self, x: f'<section>{x}</section>'   

assert Markdown('# Big').render() == '<section><h1>Big</h1>\n</section>'
```

## TailwindTypographyMarkdown()

Useful for when using Tailwind Typography, it wraps content in an `<article class="prose">` tag.

```python
html = TailwindTypographyMarkdown('# Tailwind support').render()
assert html == '<article class="prose"><h1>Tailwind support</h1>\n</article>'
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.

