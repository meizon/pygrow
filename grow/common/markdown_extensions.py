import re
from markdown import extensions
from markdown import preprocessors
from markdown.extensions import tables
from markdown.extensions import toc
from pygments import highlight
from pygments import formatters
from pygments import lexers


class CodeBlockPreprocessor(preprocessors.Preprocessor):
  pattern = re.compile(r'\[sourcecode:(.+?)\](.+?)\[/sourcecode\]', re.S)
  formatter = formatters.HtmlFormatter(noclasses=True)

  def run(self, lines):
    def repl(m):
      try:
        lexer = lexers.get_lexer_by_name(m.group(1))
      except ValueError:
        lexer = lexers.TextLexer()
      code = highlight(m.group(2), lexer, self.formatter)
      return '\n\n<div class="code">%s</div>\n\n' % code
    joined_lines = "\n".join(lines)
    joined_lines = self.pattern.sub(repl, joined_lines)
    return joined_lines.split("\n")


class CodeBlockExtension(extensions.Extension):

  def extendMarkdown(self, md, md_globals):
    md.preprocessors.add('CodeBlockPreprocessor', CodeBlockPreprocessor(), '_begin')


EXTENSIONS = [
    tables.TableExtension(),
    toc.TocExtension(),
    CodeBlockExtension(),
]
