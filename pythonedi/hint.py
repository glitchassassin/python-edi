"""
Explainer produces a human-readable version of the expectation for the
formatted data.
"""

from colorama import Fore, Style, init

SEGMENT_TEMPLATE = """
{HEADER_COLOR}[{id}] {name}{END_COLOR}
 * Required? {VALUE_COLOR}{req}{END_COLOR}
 * Max uses: {VALUE_COLOR}{max_uses}{END_COLOR}
 * Notes: {VALUE_COLOR}{notes}{END_COLOR}
"""

ELEMENT_TEMPLATE = """
    {HEADER_COLOR}{index}{name}{END_COLOR}
      * Required? {VALUE_COLOR}{req}{END_COLOR}
      * Data type: {VALUE_COLOR}{data_type}{END_COLOR}
      * Data type options: {VALUE_COLOR}{data_type_ids}{END_COLOR}
      * Length (min: {VALUE_COLOR}{length[min]}{END_COLOR}, max: {VALUE_COLOR}{length[max]}{END_COLOR})
      * Notes: {VALUE_COLOR}{notes}{END_COLOR}
"""
init()

def explain(structure):
    if type(structure) is list:
        for segment in structure:
            explain_segment(segment)
    elif type(structure) is dict and "type" in dict:
        if structure["type"] == "segment":
            explain_segment(structure)
        elif structure["type"] == "element":
            explain_element("", structure)
        elif structure["type"] == "loop":
            explain_loop(structure)
    else:
        raise TypeError("Expected either a loop, a segment, an element, or a list of segments.")
    

def explain_segment(segment):
    print(Fore.CYAN + "-- [Segment] --" + Fore.RESET)
    if segment["type"] == "segment":
        print(SEGMENT_TEMPLATE.format(
            HEADER_COLOR=Fore.CYAN+Style.BRIGHT,
            VALUE_COLOR=Fore.YELLOW+Style.BRIGHT,
            END_COLOR=Fore.RESET+Style.RESET_ALL,
            **segment))
        print(Fore.CYAN + "    -- [Elements] --" + Fore.RESET)
        for i, element in enumerate(segment["elements"]):
            explain_element("{}{:02d}: ".format(segment["id"], i+1), element)
    print(Fore.CYAN + "--------------------" + Fore.RESET)

def explain_element(index, element):
    print(ELEMENT_TEMPLATE.format(
        index=index,
        HEADER_COLOR=Fore.GREEN,
        VALUE_COLOR=Fore.YELLOW+Style.BRIGHT,
        END_COLOR=Fore.RESET+Style.RESET_ALL,
        **element))

def explain_loop(loop):
    raise NotImplementedError()