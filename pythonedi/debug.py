"""
Debug printer

Handles logging at different debug levels
"""

from colorama import Fore, Style, init
init()

LOOP_TEMPLATE = """
{tab_level}{HEADER_COLOR}[{id}] {name}{END_COLOR}
{tab_level} * Required? {VALUE_COLOR}{req}{END_COLOR}
{tab_level} * Max repeat: {VALUE_COLOR}{repeat}{END_COLOR}
"""

SEGMENT_TEMPLATE = """
{tab_level}{HEADER_COLOR}[{id}] {name}{END_COLOR}
{tab_level} * Required? {VALUE_COLOR}{req}{END_COLOR}
{tab_level} * Max uses: {VALUE_COLOR}{max_uses}{END_COLOR}
{tab_level} * Syntax rules: {VALUE_COLOR}{syntax_rules}{END_COLOR}
{tab_level} * Notes: {VALUE_COLOR}{notes}{END_COLOR}
"""

ELEMENT_TEMPLATE = """
{tab_level}{HEADER_COLOR}{index}{name}{END_COLOR}
{tab_level} * Required? {VALUE_COLOR}{req}{END_COLOR}
{tab_level} * Data type: {VALUE_COLOR}{data_type}{END_COLOR}
{tab_level} * Data type options: {VALUE_COLOR}{data_type_ids}{END_COLOR}
{tab_level} * Length (min: {VALUE_COLOR}{length[min]}{END_COLOR}, max: {VALUE_COLOR}{length[max]}{END_COLOR})
{tab_level} * Notes: {VALUE_COLOR}{notes}{END_COLOR}
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

    def explain_segment(self, segment, tab_level = ""):
        if self.level <= 1:
            return # Only explain if debugging level is 2+
        print(Fore.CYAN + "\n" + tab_level + "-- [Segment] --" + Fore.RESET)
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
                tab_level=tab_level,
                syntax_rules="; ".join(syntax_rules_list),
                HEADER_COLOR=Fore.CYAN+Style.BRIGHT,
                VALUE_COLOR=Fore.YELLOW+Style.BRIGHT,
                END_COLOR=Fore.RESET+Style.RESET_ALL,
                **segment))

            # Print elements section
            print(Fore.CYAN + tab_level + "    -- [Elements] --" + Fore.RESET)
            for i, element in enumerate(segment["elements"]):
                self.explain_element("{}{:02d}: ".format(segment["id"], i+1), element, tab_level + "    ")
        
        # End segment
        print(Fore.CYAN + tab_level + "--------------------" + Fore.RESET)

    def explain_element(self, index, element, tab_level = ""):
        if self.level <= 1:
            return # Only explain if debugging level is 2+
        # Print template
        print(ELEMENT_TEMPLATE.format(
            tab_level=tab_level,
            index=index,
            HEADER_COLOR=Fore.GREEN,
            VALUE_COLOR=Fore.YELLOW+Style.BRIGHT,
            END_COLOR=Fore.RESET+Style.RESET_ALL,
            **element))

    def explain_loop(self, loop, tab_level=""):
        if self.level <= 1:
            return # Only explain if debugging level is 2+
        print(Fore.RED + "-- [Loop] --" + Style.RESET_ALL)
        print(LOOP_TEMPLATE.format(
            tab_level=tab_level,
            HEADER_COLOR=Fore.RED+Style.BRIGHT,
            VALUE_COLOR=Fore.YELLOW+Style.BRIGHT,
            END_COLOR=Fore.RESET+Style.RESET_ALL,
            **loop))

        for segment in loop["segments"]:
            self.explain_segment(segment, "    ")
        
        print(Fore.RED + "------------" + Style.RESET_ALL)

Debug = DebugMaster()
