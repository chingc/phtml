# pyhtml [![CircleCI](https://circleci.com/gh/chingc/pyhtml.svg?style=shield)](https://circleci.com/gh/chingc/pyhtml) [![codecov](https://codecov.io/gh/chingc/pyhtml/branch/master/graph/badge.svg)](https://codecov.io/gh/chingc/pyhtml)

For those who love Python and, for reasons unknown, still like to write and format HTML by hand.

## Installation

- Add `pyhtml.py` to your project
- `from pyhtml import PyHTML`

## Reference

### Constructor

`PyHTML(auto_spacing: bool = True, spaces: int = 4)`

- `auto_spacing: bool` - Automatic indentation and newline.  Default: `True`

- `spaces: int` - The number of spaces used for indentation.  Default: `4`

Both of these arguments are instance variables that can be changed at any time.  Although changing the number of spaces used for indentation isn't very useful, disabling auto-spacing has its uses and will be covered below.

### Methods

`attr(*attr: Union[str, Tuple[str, Union[int, str]]]) -> str`

A static method that will return a string formatted as HTML attributes.  It can take multiple strings and 2-tuples.  Strings are treated as boolean attributes and 2-tuples are treated as value attributes.  Tuples take the form (str, str) or (str, int).

``` python
>>> PyHTML.attr(("src", "simpsons.webm"), "autoplay", ("width", 800), ("height", 600))
'src="simpsons.webm" autoplay width="800" height="600"'
```

`append(string: str) -> self`

Add text.

`indent() -> self`

Add indentation.  There is no need to call this if auto-spacing is enabled.

`newline() -> self`

Add a newline.  There is no need to call this if auto-spacing is enabled.

`vwrap(elem: str, attrs: str = "") -> self`

For void elements that do not have a close tag.

``` python
>>> html.vwrap("img", PyHTML.attr(("src", "kwikemart.png"), ("width", 358), ("height", 278)))
>>> print(html)
<img src="kwikemart.png" width="358" height="278">
```

`wrap(elem: str, attrs: str = "") -> Generator`

A context manager for adding an element.

``` python
>>> with html.wrap("div", PyHTML.attr(("class", "big"))):
...     html.append("Embiggened!")
...
>>> print(html)
<div class="big">
    Embiggened!
</div>
```

## Examples

``` python
>>> from pyhtml import PyHTML
>>> html = PyHTML()
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

``` python
# Setting `auto_spacing` to `False` will disable auto-spacing.
# This is useful if you want to have a wrapped element on a
# single line.  Set it to `True` to re-enable auto-spacing.

>>> from pyhtml import PyHTML
>>> html = PyHTML()
>>> html.auto_spacing = False
>>> html.append("Bart! BART! ")
>>> with html.wrap("b"):
...     html.append("BAAAART!")
...
>>> print(html)
Bart! BART! <b>BAAAART!</b>
```

``` python
>>> from pyhtml import PyHTML
>>> html = PyHTML()
>>> family = ["homer", "marge", "bart", "lisa", "maggie"]
>>> with html.wrap("ul"):
...     html.auto_spacing = False
...     for member in family:
...         html.indent()
...         with html.wrap("li"):
...             html.append(member)
...         html.newline()
...     html.auto_spacing = True
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
