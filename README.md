# python-edi
EDI message generator in Python. Creates &amp; validates messages according to specific formats


## EDI Format Definitions
EDI messages consist of a set of Segments (usually lines) comprised of Elements. Some segments can be part of a Loop. These formats are defined in JSON. See the provided format(s) for examples.

A loop has certain expected properties:

* `id` (Loop ID)
* `repeat` (Max times the loop can repeat)

Each segment has certain expected properties:

* `id` (Segment ID)
* `name` (Human-readable segment name)
* `req` (Whether segment is required: [M]andatory, [O]ptional)
* `max_uses` (Some segments can be included more than once)
* `notes` (Optional details for hinting documentation)
* `syntax` (An optional list of syntax rules, defined below)
* `elements` (List of included elements)

Each element has certain expected features: 

* `id` (Element ID)
* `name` (Human-readable element name)
* `req` (Whether segment is required: [M]andatory, [O]ptional)
* `data_type` (Type of segment data, defined below)
* `data_type_ids` (If `data_type` is `ID`, this is a dict of valid IDs with descriptions)
* `length` (Dict specifying field length)
    * `min` (Min length of field)
    * `max` (Max length of field)

Valid data types include:

* `AN` (Any data type)
* `DT` (Date, must be provided as Python DATE or DATETIME object)
* `ID` (Alphanumeric ID. List of valid IDs provided as dict with descriptions)
* `R`  (Percentage)
* `Nx` (Number with `x` decimal points)
* `TM` (Time, must be provided as Python TIME or DATETIME object)

Syntax rules are specified as a dict with a `rule` and a list of `criteria`. Valid syntax rules include:

* `ATLEASTONE` (where at least one of the element IDs in the `criteria` list is included and is not empty)
* `ALLORNONE` (where either all of the element IDs in the `criteria` list are included, or none are)
* `IFATLEASTONE` (if the first element in `criteria` is included, then at least one of the other elements must be included)
