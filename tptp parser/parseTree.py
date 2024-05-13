# Import necessary modules
from tptpParser.treeDataStructure import Node
from tptpParser.printTree import print_tree_inorder
from tptpParser.parseTreeExtraction import getOP

# This parser uses a top-down approach to analyze TPTP expressions. It systematically breaks down input formulas, terms, and predicates according to TPTP grammar rules.
# The following rules define the grammar used to parse logical formulas:
# 1. <formula> ::= (<formul>) | <formula> => <formula> | <formula> <=> <formula> | <formula> | <formula> | <formula>&<formula> | ![<variable>, . . . , <variable>]<formula> | ?[<variable>, . . . , <variable>]<formula> | ~<formula> | <predicate> | <formula>
#    - This rule defines the structure of a logical formula. It allows for various operators and constructs such as implication, equivalence, conjunction, disjunction, quantifiers, negation, and predicates.
# 2. <predicate> ::= <atomic>(<term>, . . . , <term>) | <term>=<term> | <term>!=<term> | <atomic>
#    - This rule defines the structure of a predicate, which can consist of atomic predicates, equality, inequality, or logical terms.
# 3. <term> ::= <variable> | <function>(<term>, . . . , <term>) | <constant> 
#    - This rule defines the structure of a term, which can be a variable, a function applied to terms, or a constant.
# These rules serve as the foundation for parsing logical formulas and terms within the parser. They dictate how formulas are structured and how terms and predicates are formed within those formulas. By adhering to these grammar rules, the parser can accurately interpret and process logical expressions.

# -------------------------------------- functions to build the parse tree including an explanation -----------------------------------------

# Parsing Rule Helper Functions

# This function checks if the term contains any reserved characters.
# It iterates over a list of reserved characters and returns True if any are found in the term.
def containsReservedCharacter(term):
    reservedCharacters = ['(', ')', '!', '?', '=', '&', '|', '~', ':', ',', '[', ']', '>', '$']
    for rc in reservedCharacters:
        if(rc in term):
            return True
    return False

# This function checks if a formula contains any logical operators.
# It iterates over a list of operators and returns True if any are found in the formula.
def containsOperator(term):
    operators = ['!', '?', '&', '|', '~', '=>',  '<=>']
    for op in operators:
        if op in term:
            return True 
    return False


# This function checks whether a part of the formula specified by lower and upper indices is within parentheses.
# It counts open and closed parentheses and ensures that the specified part is enclosed in the specified number of parentheses.
def inParhentheses(formula, indexLower, indexUpper, parenthesesLevel):
    openParenthesesCounter = 0
    closedParenthesesCounter = 0

    for i in range(0, len(formula)):

        if(formula[i] == ')'):
            closedParenthesesCounter += 1

        if(i in range(indexLower, indexUpper) and openParenthesesCounter - closedParenthesesCounter < parenthesesLevel):
            return False
        
        if(formula[i] == '('):
            openParenthesesCounter += 1

    # Check if the number of open and closed parentheses match
    if openParenthesesCounter != closedParenthesesCounter:
        raise Exception('parentheses error')
    return True

# This function checks whether a part of the formula specified by lower and upper indices is not within parentheses.
# It counts open and closed parentheses and ensures that the specified part is not enclosed in more than the specified number of parentheses.
def notInParhentheses(formula, indexLower, indexUpper, parenthesesLevel):
    openParenthesesCounter = 0
    closedParenthesesCounter = 0

    for i in range(0, len(formula)):
         
        if(formula[i] == '('):
            openParenthesesCounter += 1

        if(i in range(indexLower, indexUpper) and openParenthesesCounter - closedParenthesesCounter >= parenthesesLevel):
            return False
        
        if(formula[i] == ')'):
            closedParenthesesCounter += 1

    # Check if the number of open and closed parentheses match
    if openParenthesesCounter != closedParenthesesCounter:
        raise Exception('parentheses error')
    return True

# Parsing Rule Conditions for Formulas:

# Condition to check if the formula is enclosed in parentheses
def parhentheses_ParsingRule_Condition(formula, index):
    return (formula[0] == '(' and formula[len(formula)-1] == ')' and inParhentheses(formula, 1, len(formula)-1, 1)) 

# Condition to check if the formula represents an equivalence
def equivalent_ParsingRule_Condition(formula, index):
    return (index > 1 and formula[index-2] == '<' and formula[index-1] == '=' and formula[index] == '>' and  notInParhentheses(formula, index-2, index+1, 1))

# Condition to check if the formula represents an implication
def implies_ParsingRule_Condition(formula, index):
    return (index > 0 and formula[index-1] == '=' and formula[index] == '>' and notInParhentheses(formula, index-1, index+1, 1))

# Condition to check if the formula contains a conjunction
def and_ParsingRule_Condition(formula, index):
    return (formula[index] == '&' and notInParhentheses(formula, index, index+1, 1))

# Condition to check if the formula contains a disjunction
def or_ParsingRule_Condition(formula, index):
    return (formula[index] == '|' and notInParhentheses(formula, index, index+1, 1))

# Condition to check if the formula represents a universal quantification
def all_ParsingRule_Condition(formula, index):
    return (index != len(formula) -1 and formula[index] == '!' and formula[index+1]=='[' and notInParhentheses(formula, index, index+1, 1))

# Condition to check if the formula represents an existential quantification
def exists_ParsingRule_Condition(formula, index):
    return (index != len(formula) -1 and formula[index] == '?' and formula[index+1]=='[' and notInParhentheses(formula, index, index+1, 1))

# Condition to check if the formula represents negation
def not_ParsingRule_Condition(formula, index):
    return (formula[0] == '~' and notInParhentheses(formula, index, index+1, 1))

# Condition to check if the formula represents inequality
def notequal_ParsingRule_Condition(formula, index):
    return (index != len(formula) - 1 and formula[index] == '!' and formula[index + 1] == '=' and notInParhentheses(formula, index, index+2, 1))

# Condition to check if the formula represents equality
def equals_ParsingRule_Condition(formula, index):
    return (formula[index] == '='  and notInParhentheses(formula, index, index+1, 1))

# Condition to check if the formula represents a predicate with arguments
def predicate_ParsingRule_Condition(formula, index):
    return ((formula[index] == '(' and not containsReservedCharacter(formula[0:index]) and formula[len(formula)-1] == ')'))

# Condition to check if the formula represents a zero-arity predicate
def zeroArityPredicate_ParsingRule_Condition(formula, index):
    return (formula[0].islower() and not containsReservedCharacter(formula) and notInParhentheses(formula, 0, len(formula), 1))

# Condition to check if the formula represents false
def false_ParsingRule_Condition(formula, index):
    return (formula == '$false')

# Condition to check if the formula represents true
def true_ParsingRule_Condition(formula, index):
    return (formula == '$true')

# Parsing Rules for Formulas:

# Rule to parse a formula enclosed in parentheses
def parhentheses_ParsingRule(formula, index):
    return {'opType':'parentheses', 'op':'()', 'formula': formula, 'term': '', 'subFormulas': [formula[1:index-1]], 'subTerms': []}

# Rule to parse an equivalence formula
def equivalent_ParsingRule(formula, index):
    return {'opType':'equivalent', 'op':'<=>', 'formula': formula, 'term': '', 'subFormulas': [formula[0:index-2], formula[index+1:len(formula)]], 'subTerms': []}

# Rule to parse an implication formula
def implies_ParsingRule(formula, index):
    return {'opType':'implies', 'op':'=>', 'formula': formula, 'term': '', 'subFormulas': [formula[0:index-1], formula[index+1:len(formula)]], 'subTerms': []}

# Rule to parse a conjunction formula
def and_ParsingRule(formula, index):
    return {'opType':'and', 'op':'&', 'formula': formula, 'term': '', 'subFormulas': [formula[0:index], formula[index+1:len(formula)]], 'subTerms': []}

# Rule to parse a disjunction formula
def or_ParsingRule(formula, index):
    return {'opType':'or', 'op':'|', 'formula': formula, 'term': '', 'subFormulas': [formula[0:index], formula[index+1:len(formula)]], 'subTerms': []}

# Rule to parse a universal quantification formula
def all_ParsingRule(formula, index):
    part = ''
    op = ''
    for q in range(index, len(formula)):
        if formula[q] == ':':
            part = formula[q+1:len(formula)]
            op = formula[index:q]
            break

    return {'opType':'all', 'op':op, 'formula': formula, 'term': '', 'subFormulas': [part], 'subTerms': []}

# Rule to parse an existential quantification formula
def exists_ParsingRule(formula, index):
    part = ''
    op = ''
    for q in range(index, len(formula)):
        if formula[q] == ':':
            part = formula[q+1:len(formula)]
            op = formula[index:q]
            break

    return {'opType':'exists', 'op':op, 'formula': formula, 'term': '', 'subFormulas': [part], 'subTerms': []}

# Rule to parse a negation formula
def not_ParsingRule(formula, index):
    return {'opType':'not', 'op':'~', 'formula': formula, 'term': '', 'subFormulas': [formula[index+1:len(formula)]], 'subTerms': []}

# Rule to parse an inequality formula
def notequal_ParsingRule(formula, index):
    return {'opType':'notEQ', 'op':'!=', 'formula': formula, 'term': '', 'subFormulas': [], 'subTerms': [formula[0: index], formula[index+2: len(formula)]]}

# Rule to parse an equality formula
def equals_ParsingRule(formula, index):
    return {'opType':'equal', 'op':'=', 'formula': formula, 'term': '', 'subFormulas': [], 'subTerms': [formula[0: index], formula[index+1: len(formula)]]}

# Rule to parse a predicate with arguments
def predicate_ParsingRule(formula, index):
    return {'opType':'predicate', 'op': formula.split('(')[0] + '()', 'formula': formula, 'term': '', 'subFormulas': [], 'subTerms': [formula[index+1: len(formula)-1]]}

# Rule to parse a zero-arity predicate
def zeroArityPredicate_ParsingRule(formula, index):
    return {'opType':'predicate', 'op': formula, 'formula': formula, 'term': '', 'subFormulas': [], 'subTerms': []}

# Rule to parse false
def false_ParsingRule(formula, index):
    return {'opType':'false', 'op': '$false', 'formula': formula, 'term': '', 'subFormulas': [], 'subTerms': []}

# Rule to parse true
def true_ParsingRule(formula, index):
    return {'opType':'true', 'op': '$true', 'formula': formula, 'term': '', 'subFormulas': [], 'subTerms': []}

# Parsing Rule Conditions for Terms:

# Condition to check if a term contains parameters
def parameters_ParsingRule_Condition(term, index):
    return (term[index] == ',' and notInParhentheses(term, index, index+1, 1))

# Condition to check if a term represents a function
def function_ParsingRule_Condition(term, index):
    return (term[index] == '(' and notInParhentheses(term, index, index+1, 2) and not containsReservedCharacter(term[0:index]) and term[len(term)-1] == ')')

# Condition to check if a term represents a variable
def variable_ParsingRule_Condition(term, index):
    return not term[0].islower() and not containsReservedCharacter(term) and notInParhentheses(term, 0, len(term), 1)

# Condition to check if a term represents a constant
def constant_ParsingRule_Condition(term, index):
    return term[0].islower() and not containsReservedCharacter(term) and notInParhentheses(term, 0, len(term), 1)

# Parsing Rules for Terms:

# Rule to parse parameters of a function
def parameters_ParsingRule(term, index):
    openParenthesesCounter = 0
    closedParenthesesCounter = 0

    subTerms = []
    paramStart = 0

    for j in range(paramStart, len(term)):
        if(term[j] == '('):
            openParenthesesCounter += 1
        elif(term[j] == ')'):
            closedParenthesesCounter += 1

        if(term[j] == ',' and openParenthesesCounter - closedParenthesesCounter == 0):
            subTerms.append(term[paramStart:j])
            paramStart = j + 1
    subTerms.append(term[paramStart:len(term)])

    return {'opType':'parameters', 'op':',', 'formula': '', 'term': term, 'subFormulas': [], 'subTerms': subTerms}

# Rule to parse a function
def function_ParsingRule(term, index):
    return {'opType':'function', 'op': term.split('(')[0] + '()', 'formula': '', 'term': term, 'subFormulas': [], 'subTerms': [term[index+1:len(term)-1]]}

# Rule to parse a variable
def variable_ParsingRule(term, index):
    return {'opType':'variable', 'op': term, 'formula': '', 'term': term, 'subFormulas': [], 'subTerms': []}

# Rule to parse a constant
def constant_ParsingRule(term, index):
    return {'opType':'constant', 'op': term, 'formula': '', 'term': term, 'subFormulas': [], 'subTerms': []}

# Define the evaluation order for parsing formulas. Each sublist represents a level of evaluation,
# evaluated from top to bottom. Within each sublist, parsing rules are evaluated from left to right.
parsingRulesFormulas = [
    # Level 1: Evaluation of parentheses
    [
        {
            'condition': parhentheses_ParsingRule_Condition,
            'rule': parhentheses_ParsingRule
        }
    ],
    # Level 2: Evaluation of equivalence and implication
    [
        {
            'condition': equivalent_ParsingRule_Condition,
            'rule': equivalent_ParsingRule

        },
        {
            'condition': implies_ParsingRule_Condition,
            'rule': implies_ParsingRule
        }
    ],
    # Level 3: Evaluation of conjunction and disjunction
    [
        {
            'condition': and_ParsingRule_Condition,
            'rule': and_ParsingRule
        },
        {
            'condition': or_ParsingRule_Condition,
            'rule': or_ParsingRule
        }
    ],
    # Level 4: Evaluation of universal and existential quantification
    [
        {
            'condition': all_ParsingRule_Condition,
            'rule': all_ParsingRule
        },
        {
            'condition': exists_ParsingRule_Condition,
            'rule': exists_ParsingRule
        }
    ],
    # Level 5: Evaluation of negation
    [
        {
            'condition': not_ParsingRule_Condition,
            'rule': not_ParsingRule
        }
    ],
    # Level 6: Evaluation of inequality and equality
    [
        {
            'condition': notequal_ParsingRule_Condition,
            'rule': notequal_ParsingRule
        },
        {
            'condition': equals_ParsingRule_Condition,
            'rule': equals_ParsingRule
        }
    ],
    # Level 7: Evaluation of predicates
    [
        {
            'condition': predicate_ParsingRule_Condition,
            'rule': predicate_ParsingRule
        },
        {
            'condition': zeroArityPredicate_ParsingRule_Condition,
            'rule': zeroArityPredicate_ParsingRule
        }
    ],
    # Level 8: Evaluation of true and false
    [
        {
            'condition': false_ParsingRule_Condition,
            'rule': false_ParsingRule
        },
        {
            'condition': true_ParsingRule_Condition,
            'rule': true_ParsingRule
        }
    ]
]

# Define the evaluation order for parsing terms. Each sublist represents a level of evaluation,
# evaluated from top to bottom. Within each sublist, parsing rules are evaluated from left to right.
parsingRulesTerms = [
    # Level 1: Evaluation of function parameters
    [
        {
            'condition': parameters_ParsingRule_Condition,
            'rule': parameters_ParsingRule
        }
    ],
    # Level 2: Evaluation of functions
    [
        {
            'condition': function_ParsingRule_Condition,
            'rule': function_ParsingRule
        }
    ],
    # Level 3: Evaluation of variables
    [
        {
            'condition': variable_ParsingRule_Condition,
            'rule': variable_ParsingRule
        }
    ],
    # Level 4: Evaluation of constants
    [
        {
            'condition': constant_ParsingRule_Condition,
            'rule': constant_ParsingRule
        }
    ]
]

# This function checks the parsing rule condition on each character in the formula.
# It iterates over the parsing rules defined in the specified evaluation order and checks
# if any rule can be applied to the current position in the formula string.

def checkParsingRules(formula_term, parsingRules):
    # Variables to track parentheses counts
    openParenthesesCounter = 0
    closedParenthesesCounter = 0

    # Iterate over each priority level in the parsing rules
    for prio in parsingRules:
        # Iterate over each character in the formula to evaluate from left to right
        for i in range(0, len(formula_term)):
            # Iterate over the rules within the current priority level
            for parsingRule in prio:
                # Extract the condition and rule functions for the current rule
                condition = parsingRule['condition']
            
                # Check if the condition for applying the rule is met at the current position
                if(condition(formula_term, i)):
                    # If condition is met, apply the rule and return the result
                    rule = parsingRule['rule']
                    res = rule(formula_term, i)
                    return res # Return the result of applying the rule
    
    # If no rule can be applied, raise an exception     
    raise Exception('no rule could be applied')       

# This function builds a parse tree for a term based on the specified parsing rules for terms.
# It recursively applies parsing rules to the term string to construct a parse tree.
def buildTermParseTree(term, parsingRulesTerms):
    # Generate the current node
    node = Node()

    # Apply parsing rules to the term to determine its structure
    res = checkParsingRules(term, parsingRulesTerms)
    subTerms = res['subTerms']

    # Recursively build parse trees for sub-terms and append them as children of the current node
    for subt in subTerms:
        newNode = buildTermParseTree(subt, parsingRulesTerms)
        node.nodes.append(newNode)
    
    # Assign the result of parsing as the value of the current node
    node.value = res
    return node

# This function builds a parse tree for a logic formula based on the specified parsing rules for formulas and terms.
# It recursively applies parsing rules to the formula string to construct a parse tree.
def buildParseTree(formula, parsingRulesFormulas, parsingRulesTerms):
    # Generate the current node
    node = Node()

    # Apply parsing rules to the formula to determine its structure
    res = checkParsingRules(formula, parsingRulesFormulas)
    subFormulas = res['subFormulas']

    # Recursively build parse trees for sub-formulas and append them as children of the current node
    for subf in subFormulas:
        newNode = buildParseTree(subf, parsingRulesFormulas, parsingRulesTerms)
        node.nodes.append(newNode)

    # If the current node corresponds to a predicate, equality, or inequality operation,
    # recursively build parse trees for sub-terms and append them as children of the current node
    if(res['opType'] == 'predicate' or res['opType'] == 'equal' or res['opType'] == 'notEQ'):
        for subt in res['subTerms']:
            newNode = buildTermParseTree(subt, parsingRulesTerms)
            node.nodes.append(newNode)

    # Assign the result of parsing as the value of the current node
    node.value = res
    return node

# Function to generate a parse tree from a formula
def generateParseTree(formula):
    return buildParseTree(formula, parsingRulesFormulas, parsingRulesTerms)

