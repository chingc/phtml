# simplemarkup

A simple little pretty print markup generator.

This is something I created to help generate HTML for one of my other projects.  I wrote this because many of the tools already available were too complex or too big for my needs.  This will not check markup for validity, it simply creates pretty output for the input its given.


## Sample Output

DJRivals source  \[[index.html][1]\]<br />


## Requirements

- Python

Note: simplemarkup was written and tested under Python 3.3.0.  It should be able to run under Python 2.6.x, 2.7.x, and 3.x with little to no modifications.


## Installation and Usage

- Simply place the `simplemarkup.py` module into your project folder and import the module.

#### Constructor

`SimpleMarkup(width)` Creates a simplemarkup object.

- width: (Optional) An integer to specify the number of spaces used for indentation.  Defaults to 4.

#### Methods

`output()` Returns the raw output.

`raw(string)` Add a string exactly as given.

- string: A string.

`empty(tag, attr)` Add an empty element.

- tag: An empty element tag as a string.
- attr: (Optional) A list of 2-tuples strings.  Defaults to an empty list.

`begin(tag, attr, value)` Add the opening tag of an element.

- tag: An element tag as a string.
- attr: (Optional) A list of 2-tuples strings.  Defaults to an empty list.
- value: (Optional) The value that goes between an opening and closing element tag as a string.  Defaults to an empty string.

`end()` Add the closing tag of an element.

Additional methods `rawln`, `emptyln`, `beginln`, and `endln` are available and are equivalent to the previously mentioned versions except these will append a newline.


## Examples

    >>> sm = SimpleMarkup()
    >>> sm.raw("Hello, world!")
    >>> print(sm.output())
    Hello, world!
    >>>

    >>> sm = SimpleMarkup()
    >>> sm.empty("img", [("src", "http://www.example.com/example.png"), ("width", "640"), ("height", "480")])
    >>> print(sm.output())
    <img src="http://www.example.com/example.png" width="640" height="480" />
    >>>

    >>> sm = SimpleMarkup()
    >>> sm.begin("p", [("style", "font-variant: small-caps;")], "SimpleMarkup!")
    >>> sm.end()
    >>> print(sm.output())
    <p style="font-variant: small-caps;">SimpleMarkup!</p>
    >>>

This example gives a taste of what makes simplemarkup really powerful.

    >>> fruits = ["apple", "banana", "cherry", "mango", "orange", "pear", "watermelon"]
    >>> sm.beginln("ul")
    >>> for fruit in fruits:
    ...     sm.begin("li", value=fruit)
    ...     sm.endln()
    >>> sm.end()
    >>> print(sm.output())
    <ul>
        <li>apple</li>
        <li>banana</li>
        <li>cherry</li>
        <li>mango</li>
        <li>orange</li>
        <li>pear</li>
        <li>watermelon</li>
    </ul>
    >>>

Note: simplemarkup allows function chaining.  The contents of the loop can be reduced to `sm.begin("li", value=fruit).endln()`.


## License

simplemarkup is distributed under the Simplified BSD license.  See [LICENSE][2] for more details.




[1]: https://raw.github.com/smwst/smwst.github.com/master/DJRivals/index.html
[2]: https://github.com/smwst/simplemarkup/blob/master/LICENSE "License"
