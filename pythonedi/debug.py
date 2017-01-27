"""
Debug printer

Handles logging at different debug levels
"""

from colorama import Fore, Style, init
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

class DebugMaster(object):
    """ Auto-instantiated as Debug to provide a single point of contact """
    def __init__(self):
        self.level = 3
        self.tags = {
            "ERROR":   "{}[ ERROR ]{} ".format(Fore.RED+Style.BRIGHT, Style.RESET_ALL),
            "WARNING": "{}[WARNING]{} ".format(Fore.YELLOW+Style.BRIGHT, Style.RESET_ALL),
            "MESSAGE": "{}[MESSAGE]{} ".format(Fore.CYAN+Style.BRIGHT, Style.RESET_ALL)
        }

    def log(self, message, level=1):
        """ Creates a custom message at the specified level """
        if level <= self.level:
            print("\n" + message)

    def log_error(self, message):
        """ Creates an error-level log messsage """
        self.log(self.tags["ERROR"] + message, 1)

    def log_warning(self, message):
        """ Creates a warning-level log messsage """
        self.log(self.tags["WARNING"] + message, 2)

    def log_message(self, message):
        """ Creates a message-level log messsage """
        self.log(self.tags["MESSAGE"] + message, 3)

    def explain(self, structure):
        print(self.level)
        if self.level <= 1:
            return # Only explain if debugging level is 2+
        # Decide which type of structure this is
        if type(structure) is list:
            for segment in structure:
                self.explain_segment(segment)
        elif type(structure) is dict and "type" in structure:
            if structure["type"] == "segment":
                self.explain_segment(structure)
            elif structure["type"] == "element":
                self.explain_element("", structure)
            elif structure["type"] == "loop":
                self.explain_loop(structure)
        else:
            raise TypeError("Expected either a loop, a segment, an element, or a list of segments.")

    def explain_segment(self, segment):
        if self.level <= 1:
            return # Only explain if debugging level is 2+
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
                self.explain_element("{}{:02d}: ".format(segment["id"], i+1), element)
        
        # End segment
        print(Fore.CYAN + "--------------------" + Fore.RESET)

    def explain_element(self, index, element):
        if self.level <= 1:
            return # Only explain if debugging level is 2+
        # Print template
        print(ELEMENT_TEMPLATE.format(
            index=index,
            HEADER_COLOR=Fore.GREEN,
            VALUE_COLOR=Fore.YELLOW+Style.BRIGHT,
            END_COLOR=Fore.RESET+Style.RESET_ALL,
            **element))

    def explain_loop(self, loop):
        if self.level <= 1:
            return # Only explain if debugging level is 2+
        raise NotImplementedError()

Debug = DebugMaster()
