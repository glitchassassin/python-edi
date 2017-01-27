"""
Explainer produces a human-readable version of the expectation for the
formatted data.
"""

from colorama import Fore, Style, init

# Initialize colorama wrapper
init()

SEGMENT_TEMPLATE = """
{HEADER_COLOR}[{id}] {name}{END_COLOR}
 * Required? {VALUE_COLOR}{req}{END_COLOR}
 * Max uses: {VALUE_COLOR}{max_uses}{END_COLOR}
 * Syntax rules: {VALUE_COLOR}{syntax_rules}{END_COLOR}
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

def explain(structure):
    # Decide which type of structure this is
    if type(structure) is list:
        for segment in structure:
            explain_segment(segment)
    elif type(structure) is dict and "type" in structure:
        if structure["type"] == "segment":
            explain_segment(structure)
        elif structure["type"] == "element":
            explain_element("", structure)
        elif structure["type"] == "loop":
            explain_loop(structure)
    else:
        raise TypeError("Expected either a loop, a segment, an element, or a list of segments.")
    

def explain_segment(segment):
    print(Fore.CYAN + "\n-- [Segment] --" + Fore.RESET)
    if segment["type"] == "segment":
        # Parse syntax rules into human-readable format
        syntax_rules_list = []
        if "syntax" in segment:
            for rule in segment["syntax"]:
                # Troubleshooting
                if "rule" not in rule or "criteria" not in rule:
                    raise ValueError("Invalid rule definition in segment {}: {}".format(segment["id"], rule))
                if len(rule["criteria"]) < 2:
                    raise ValueError("Invalid criteria for syntax rule {} in segment {}: Expected two or more values".format(rule["rule"], segment["id"]))
                
                if rule["rule"] == "ATLEASTONE":
                    required_elements = ", ".join(["{}{:02d}".format(segment["id"], e) for e in rule["criteria"]])
                    syntax_rules_list.append("At least one of {} is required".format(required_elements))
                elif rule["rule"] == "ALLORNONE":
                    required_elements = ", ".join(["{}{:02d}".format(segment["id"], e) for e in rule["criteria"]])
                    syntax_rules_list.append("If one of {} is present, the rest are required".format(required_elements))
                elif rule["rule"] == "IFATLEASTONE":
                    first_element = "{}{:02d}".format(segment["id"], rule["criteria"][0])
                    required_elements = ", ".join(["{}{:02d}".format(segment["id"], e) for e in rule["criteria"][1:]])
                    syntax_rules_list.append("If {} is present, at least one of {} are required".format(first_element, required_elements))

        # Print template
        print(SEGMENT_TEMPLATE.format(
            syntax_rules="; ".join(syntax_rules_list),
            HEADER_COLOR=Fore.CYAN+Style.BRIGHT,
            VALUE_COLOR=Fore.YELLOW+Style.BRIGHT,
            END_COLOR=Fore.RESET+Style.RESET_ALL,
            **segment))

        # Print elements section
        print(Fore.CYAN + "    -- [Elements] --" + Fore.RESET)
        for i, element in enumerate(segment["elements"]):
            explain_element("{}{:02d}: ".format(segment["id"], i+1), element)
    
    # End segment
    print(Fore.CYAN + "--------------------" + Fore.RESET)

def explain_element(index, element):
    # Print template
    print(ELEMENT_TEMPLATE.format(
        index=index,
        HEADER_COLOR=Fore.GREEN,
        VALUE_COLOR=Fore.YELLOW+Style.BRIGHT,
        END_COLOR=Fore.RESET+Style.RESET_ALL,
        **element))

def explain_loop(loop):
    raise NotImplementedError()