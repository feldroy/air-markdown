"""Main module."""

import html
from contextlib import redirect_stdout
from io import StringIO

import air
import mistletoe
from mistletoe import block_token
from mistletoe.html_renderer import HtmlRenderer


class Markdown(air.Tag):
    def __init__(self, *args, **kwargs):
        """Convert a Markdown string to HTML using mistletoe

        Args:
            *args: Should be exactly one string argument
            **kwargs: Ignored (for consistency with Tag interface)
        """
        if len(args) > 1:
            raise ValueError("Markdown tag accepts only one string argument")

        raw_string = args[0] if args else ""

        if not isinstance(raw_string, str):
            raise TypeError("Markdown tag only accepts string content")

        super().__init__(raw_string)

    @property
    def html_renderer(self) -> mistletoe.HtmlRenderer:  # type: ignore
        """Override this to change the HTML renderer.

        Example:
            import mistletoe
            from air_markdown import Markdown

            class MyCustomRenderer(mistletoe.HtmlRenderer):
                # My customizations here

            Markdown.html_renderer = MyCustomRenderer

            Markdown('# Important title Here')
        """
        return mistletoe.HtmlRenderer

    def wrapper(self, content) -> str:
        """Override this method to handle cases where CSS needs it.

        Example:
            from air_markdown import Markdown

            class TailwindTypographyMarkdown(Markdown):
                def wrapper(self):
                    return f'<article class="prose">{content}</article>'


            Markdown('# Important title Here')
        """
        return content

    def render(self) -> str:
        """Render the string with the Markdown library."""
        content = self._children[0] if self._children else ""
        return self.wrapper(mistletoe.markdown(content, self.html_renderer))


class TailwindTypographyMarkdown(Markdown):
    def wrapper(self, content) -> str:
        return f'<article class="prose">{content}</article>'


class AirHTMLRenderer(HtmlRenderer):
    def render_block_code(self, token: block_token.BlockCode) -> str:
        template = "<pre><code{attr}>{inner}</code></pre>"
        if token.language == "airtag_rendered":
            code = token.content.strip()
            f = StringIO()
            with redirect_stdout(f):
                exec(code, globals(), {})
            return f.getvalue()
        elif token.language:
            attr = ' class="{}"'.format(f"language-{html.escape(token.language)}")
        else:
            attr = ""
        inner = self.escape_html_text(token.content)
        return template.format(attr=attr, inner=inner)


class AirMarkdown(Markdown):
    html_renderer = AirHTMLRenderer

    def wrapper(self, content) -> str:
        return f'<article class="prose">{content}</article>'
