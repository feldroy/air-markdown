"""Main module."""

import ast
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
    def html_renderer(self) -> type[mistletoe.HtmlRenderer]:
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
        """Render airtag_rendered code blocks as the executed output
        of calling the Air Tag's .render() method.

        For example:
        ```airtag_rendered
        air.H2("Heading 2")
        ```
        will render as `<h2>Heading 2</h2>`
        """
        template = "<pre><code{attr}>{inner}</code></pre>"
        if token.language == "airtag_rendered":
            code = token.content.strip()
            if not code:
                return ""

            try:
                module = ast.parse(code)
                if not module.body:
                    return ""

                if isinstance(module.body[-1], ast.Expr):
                    last_expr_node = module.body.pop()
                    statements = ast.Module(body=module.body, type_ignores=[])
                    code_obj = compile(statements, "<string>", "exec")
                    local_scope = {}
                    exec(code_obj, globals(), local_scope)

                    expr_obj = compile(ast.Expression(body=last_expr_node.value), "<string>", "eval")  # type: ignore
                    result = eval(expr_obj, globals(), local_scope)

                    if isinstance(result, air.Tag):
                        return result.render()
                    return str(result)
                else:
                    # Fallback for statements without a final expression
                    f = StringIO()
                    with redirect_stdout(f):
                        exec(code, globals(), {})
                    return f.getvalue()

            except Exception as e:
                error_message = f"Error rendering airtag: {e}"
                inner = self.escape_html_text(f"{code}\n\n{error_message}")
                attr = ' class="language-airtag-error"'
                return template.format(attr=attr, inner=inner)

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
