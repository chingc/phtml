# pxml

A simple tool to help you write markup.


## Requirements

Python 3.x


## Usage

``` python
from pxml import PXML  # import the module
pxml = PXML()          # create the object
```


#### Constructor

`PXML(width)` Creates a pxml object.
- width: (Optional) The number of spaces used for indentation.  Default is 4.


#### Methods

`attributes(attr)` Return the attribute list as a string.
- attr: A list of 2-tuple strings.

``` python
>>> pxml.attributes([("id", "skinner"), ("class", "principal")])
' id="skinner" class="principal"'
```

`indent()` Add indentation.

``` python
>>> print(pxml.indent().insert("Bart!"))  # assuming the current indentation depth is 1
    Bart!
```

`insert(string)` Add a string.

``` python
>>> print(pxml.insert("Lisa"))
Lisa
```

`newline()` Add a newline.

``` python
>>> print(pxml.insert('10 print "D\'oh!"').newline().insert("20 GOTO 10"))
10 print "D'oh!"
20 GOTO 10
```


#### Context Managers

`tag(name, attr)` Add tagged content.
- name: Name of the tag.
- attr: (Optional) A list of 2-tuple strings.

``` python
>>> with pxml.tag("div", [("class", "big")]):
...     pxml.indent().insert("pxml!").newline()
...
>>> print(pxml)
<div class="big">
    Embiggened!
</div>
```

`itag(name, attr)` Add inline tagged content.
- name: Name of the tag.
- attr: (Optional) A list of 2-tuple strings.

``` python
>>> with pxml.itag("beer"):
...     pxml.insert("Duff!")
...
>>> print(pxml)
<beer>Duff!</beer>
```


## Additional Example

``` python
>>> pxml = PXML()
>>> family = ["homer", "marge", "bart", "lisa", "maggie"]
>>> with pxml.tag("ul"):
...     for member in family:
...         pxml.indent()
...         with pxml.itag("li"):
...             pxml.insert(member)
...         pxml.newline()
...
>>> print(pxml)
<ul>
    <li>homer</li>
    <li>marge</li>
    <li>bart</li>
    <li>lisa</li>
    <li>maggie</li>
</ul>
```


## License

Simplified BSD license.

See the included `LICENSE` for more details.
