# pyhtml

[![CircleCI](https://circleci.com/gh/chingc/pyhtml.svg?style=shield)](https://circleci.com/gh/chingc/pyhtml) [![codecov](https://codecov.io/gh/chingc/pyhtml/branch/master/graph/badge.svg)](https://codecov.io/gh/chingc/pyhtml)

For those who love Python and, for reasons unknown, still like to write and format HTML manually.

## Installation

1. Add `pyhtml.py` to your project
1. `import pyhtml`

## Reference

### new

This is the first thing to call and will return a new instance of PyHTML.

```python
>>> pyhtml.new()
```

It can take the following arguments:

- `doctype: str` - doctype declaration (default: "")
  - valid doctypes: html5, html4.01s, html4.01t, html4.01f, xhtml1.1, xhtml1.0s, xhtml1.0t, xhtml1.0f
- `spaces: int` - number of spaces used for indentation (default: 4)

For html4.01 and xhtml1.0: s, t, and f stands for strict, transitional, and frameset, respectively.

### attr

Strings and tuples are stringified into HTML attribute form.

```python
>>> pyhtml.attr(("src", "simpsons.webm"), "autoplay", ("width", 800), ("height", 600))
'src="simpsons.webm" autoplay width="800" height="600"'
```

Strings are treated as boolean attributes and 2-tuples are treated as value attributes.  Tuples can take the form (str, str) or (str, int).  Multiple comma separated strings and tuples can be specified.

### append

- `string: str` -- add arbitrary text to the HTML

### indent

Add indentation.  Indentation is handled automatically by default.  This is useful during manual spacing.

### newline

Add a newline.  Newlines are handled automatically by default.  This is useful during manual spacing or when additional newlines are desired.

### vwrap

Add a void element.  These are elements that do not have a closing tag.

- `elem: str` -- an HTML void element
- `attrs: str` -- element attributes (default: "")

```python
>>> html = pyhtml.new()
>>> html.vwrap("img", pyhtml.attr(("src", "kwikemart.png"), ("width", 358), ("height", 278)))
>>> print(html)
<img src="kwikemart.png" width="358" height="278">
```

### wrap

Add an element.  The closing tag will be inserted automatically.

- `elem: str` -- an HTML element
- `attrs: str` -- element attributes (default: "")

```python
>>> html = pyhtml.new()
>>> with html.wrap("div", pyhtml.attr(("class", "big"))):
...     html.append("Embiggened!")
...
>>> print(html)
<div class="big">
    Embiggened!
</div>
```

### manual_spacing

Disable automatic indentation and newlines.  Statements within the block will not have automatic indentation or newlines.

```python
>>> html = pyhtml.new()
>>> with html.manual_spacing():
...     with html.wrap("em"):
...         html.append("Itchy")
...     html.append(" & ")
...     with html.wrap("em"):
...         html.append("Scratchy")
...
>>> print(html)
<em>Itchy</em> & <em>Scratchy</em>
```

## Examples

```python
>>> import pyhtml
>>> html = pyhtml.new()
>>> with html.wrap("html"):
...     with html.wrap("head"):
...         with html.wrap("title"):
...             html.append("Dr. Nick")
...     with html.wrap("body"):
...         with html.wrap("p"):
...             html.append("Hi, everybody!")
...
>>> print(html)
<html>
    <head>
        <title>
            Dr. Nick
        </title>
    </head>
    <body>
        <p>
            Hi, everybody!
        </p>
    </body>
</html>
```

```python
# Disable auto-spacing when you want to have
# a wrapped element on a single line.

>>> import pyhtml
>>> html = pyhtml.new()
>>> with html.wrap("html"):
...     with html.wrap("head"):
...         with html.manual_spacing():
...             html.indent()
...             with html.wrap("title"):
...                 html.append("Ned Flanders")
...             html.newline()
...     with html.wrap("body"):
...         with html.manual_spacing():
...             html.indent()
...             with html.wrap("p"):
...                 html.append("Hi diddly ho!")
...             html.newline()
...
>>> print(html)
<html>
    <head>
        <title>Ned Flanders</title>
    </head>
    <body>
        <p>Hi diddly ho!</p>
    </body>
</html>
```

```python
# Tip: Context managers can be nested.

>>> import pyhtml
>>> html = pyhtml.new()
>>> family = ["homer", "marge", "bart", "lisa", "maggie"]
>>> with html.wrap("ul"), html.manual_spacing():
...     for member in family:
...         html.indent()
...         with html.wrap("li"):
...             html.append(member)
...         html.newline()
...
>>> print(html)
<ul>
    <li>homer</li>
    <li>marge</li>
    <li>bart</li>
    <li>lisa</li>
    <li>maggie</li>
</ul>
```
