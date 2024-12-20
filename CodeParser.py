from typing import Tuple

class Code:
    def __init__(self):
        self.classes = []
        self.procs = []

class Class:
    def __init__(self):
        self.name = ""
        self.superclass_name = ""
        self.properties = {}
        self.methods = []

class Method:
    def __init__(self):
        self.name = ""
        self.code = ""

class StateInfo:
    def __init__(self):
        self.current_class = Class()
        self.code = ""
        self.index = 0
        self.bol = True
        self.current_token = ""
        self.isMethod = False
        self.isInParaList = False
        self.propertyname = ""
        self.propertyvalue = ""
        self.isLinebreakInString = False
        self.state_before_comment = None        
        self.classes = []
        self.procs = []
        self.isInList = False

class ByondParser:
    def parse(self, code):              
        current_state = DefaultState.instance()
        previous_state = None
        state_info = StateInfo()
        state_info.code = code + '\n' #hack
        
        
        while state_info.index < len(state_info.code):
            #if previous_state == None or type(previous_state) != type(current_state):
            #    print(f"State: {type(current_state).__name__}, {state_info.current_class.name}")
                
            new_state_info, new_state = current_state.parse(state_info, previous_state)
            state_info = new_state_info
                
            previous_state = current_state
            current_state = new_state            
        
        if state_info.current_class != None and state_info.current_class.name != "":
            state_info.classes.append(state_info.current_class)

        ret = Code()
        ret.classes = state_info.classes
        ret.procs = state_info.procs
        return ret

class ParserState:
    def parse(self, state_info: "StateInfo", previous_state: "ParserState") -> Tuple["StateInfo", "ParserState"]:
        return state_info, previous_state

class MultilineCommentState(ParserState):
    _instance = None  # Singleton instance    

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MultilineCommentState, cls).__new__(cls)
        return cls._instance

    def parse(self, state_info, previous_state):
        char = state_info.code[state_info.index]
        new_state = self
        
        if char == "*":
            if state_info.index + 1 < len(state_info.code) and state_info.code[state_info.index+1] == "/":
                new_state = state_info.state_before_comment
        else:
            new_state = self

        state_info.index += 1
        return state_info, new_state

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class InPropertyValueState(ParserState):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InPropertyValueState, cls).__new__(cls)
        return cls._instance

    def parse(self, state_info, previous_state):
        new_state = self
        char = state_info.code[state_info.index]

        if char == "\n":
            if state_info.isInList == False:
                if state_info.isLinebreakInString == False:
                    #print(f"property value: {propertyvalue}")
                    state_info.propertyname = state_info.propertyname.strip()
                    state_info.propertyvalue = state_info.propertyvalue.strip().strip('"')
                    state_info.current_class.properties[state_info.propertyname] = state_info.propertyvalue.strip("\"")
                    state_info.current_token = ""
                    new_state = InBodyState.instance()
                else:
                    state_info.isLinebreakInString = False
            state_info.bol = True                    
        elif char == "/" and state_info.index + 1 < len(state_info.code) and state_info.code[state_info.index+1] == "/":
            #print(f"property value: {state_info.propertyvalue}")
            state_info.propertyname = state_info.propertyname.strip()
            state_info.propertyvalue = state_info.propertyvalue.strip().strip('"')
            state_info.current_class.properties[state_info.propertyname] = state_info.propertyvalue
            state_info.state_before_comment = InBodyState.instance()
            new_state = InCommentState.instance()
            state_info.current_token = ""
        elif char == "\\":
            state_info.isLinebreakInString = True
        elif char == "(":
            state_info.isInList = True
        elif char == ")":
            state_info.isInList = False

        else:
            state_info.propertyvalue += char
        state_info.index += 1
        return state_info, new_state

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
class InBodyState(ParserState):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InBodyState, cls).__new__(cls)
        return cls._instance

    def parse(self, state_info, previous_state):
        char = state_info.code[state_info.index]
        new_state = self

        if state_info.bol:
            state_info.bol = False
            if char == "\n":
                state_info.bol = True
            if char != "\t":
                # Check if the next line with text is still part of this method
                stillInMethod = False
                index = state_info.index
                while index < len(state_info.code) - 1:
                    index += 1
                    if state_info.code[index] == " " or state_info.code[index] == "\n":
                        continue

                    if state_info.code[index] == "\t":
                        stillInMethod = True
                        break
                    else:                        
                        break

                if stillInMethod == False:
                    new_state = DefaultState.instance()
                    if state_info.isMethod:
                        if state_info.current_class.name != "":
                            state_info.current_class.methods[-1].code = state_info.current_token
                        else:
                            state_info.procs[-1].code = state_info.current_token
                    state_info.current_token = ""
        elif state_info.isMethod == False:
                new_state = InPropertyNameState.instance()
                state_info.current_token = ""
                state_info.propertyname = char
        else:
            if char == "\n":
                state_info.bol = True

        state_info.current_token += char

        state_info.index += 1
        return state_info, new_state

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class InPropertyNameState(ParserState):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InPropertyNameState, cls).__new__(cls)
        return cls._instance

    def parse(self, state_info, previous_state):
        char = state_info.code[state_info.index]
        new_state = self
        if char == "=":
            new_state = InPropertyValueState.instance()
            #print(f"property name:{propertyname}")
            state_info.propertyvalue = ""
            state_info.index += 1
            state_info.current_token = ""
        else:
            state_info.propertyname += char
            state_info.index += 1
        return state_info, new_state

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class DefaultState(ParserState):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DefaultState, cls).__new__(cls)
        return cls._instance

    def parse(self, state_info, previous_state):
        char = state_info.code[state_info.index]
        new_state = self
        # detect start of single-line comment
        if state_info.bol and char == "/":
            if state_info.index + 1 < len(state_info.code) and state_info.code[state_info.index+1] == "/": # //
                state_info.state_before_comment = self
                new_state = InCommentState.instance()
                state_info.bol = False
            elif state_info.index + 1 < len(state_info.code) and state_info.code[state_info.index+1] == "*": # /*
                state_info.state_before_comment = self
                new_state = MultilineCommentState.instance()
                state_info.bol = False
                state_info.current_token = ""
            elif state_info.bol:
                new_state = InClassOrMethodNameState.instance()
                state_info.isMethod = False
                state_info.bol = False
                state_info.current_token = ""
        elif char == "\n":
            state_info.bol = True
        elif state_info.bol:
            state_info.bol = False
        state_info.index += 1
        return state_info, new_state

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class InClassOrMethodNameState(ParserState):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InClassOrMethodNameState, cls).__new__(cls)
        return cls._instance

    def parse(self, state_info, previous_state):
        char = state_info.code[state_info.index]
        new_state = self
        if char == "\n":
            new_state = InBodyState.instance()
            state_info.index += 1
            state_info.bol = True
            if state_info.isMethod:
                newMethod = Method()                
                if state_info.current_class.name == "":
                    newMethod.name = state_info.current_token
                    state_info.procs.append(newMethod)
                else:
                    newMethod.name = state_info.current_token[len(state_info.current_class.name)+1:].rstrip(')')
                    state_info.current_class.methods.append(newMethod)
            else:
                if state_info.current_class.name != "":
                    state_info.classes.append(state_info.current_class)
                state_info.current_class = Class()               
                state_info.current_class.name = state_info.current_token
                #print(f"Set current class name to {state_info.current_token}")                        
            state_info.current_token = ""                    
        elif char == "(":
            state_info.isMethod = True
            state_info.isInParaList = True
            state_info.index += 1
        elif char == ")":
            state_info.index += 1
            state_info.isInParaList = False
        elif char == "/" and state_info.index + 1 < len(state_info.code) and state_info.code[state_info.index+1] == "/":
            new_state = InCommentState.instance()
            state_info.state_before_comment = InBodyState.instance()
            if state_info.isMethod:
                newMethod = Method()
                newMethod.name = state_info.current_token[len(state_info.current_class.name)+1:].rstrip().rstrip(')')
                state_info.current_class.methods.append(newMethod)
            else:
                if state_info.current_class.name != "":
                    state_info.classes.append(state_info.current_class)
                state_info.current_class = Class()               
                state_info.current_class.name = state_info.current_token          
            state_info.current_token = ""
            state_info.index += 1
            
        else:
            if state_info.isInParaList == False:
                state_info.current_token += char
            state_info.index += 1

        return state_info, new_state
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class InCommentState(ParserState):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InCommentState, cls).__new__(cls)
        return cls._instance

    def parse(self, state_info, previous_state):
        new_state = self
        char = state_info.code[state_info.index]
        if char == "\n":
            new_state = state_info.state_before_comment
            state_info.index += 1
            state_info.bol = True
        else:
            state_info.index += 1
            state_info.bol = False

        return state_info, new_state

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
