# c_parser.py
import ply.yacc as yacc

# Import the token list from your lexer
from Analizador_lexico import tokens, lexer # Also import lexer for testing

# --- Operator Precedence ---
# Based on C-reducido "Precedencia de operadores y expresiones" and standard C rules
# Lowest precedence at the top, highest at the bottom.
precedence = (
    ('right', 'ASSIGN'),        # Assignment
    ('left', 'EQ', 'NEQ'),      # Equality
    ('left', 'LT', 'LE', 'GT', 'GE'), # Relational
    ('left', 'PLUS', 'MINUS'),  # Additive
    ('left', 'TIMES', 'DIVIDE'),# Multiplicative
    ('right', 'UMINUS', 'UPLUS'), # Unary minus and plus (fictitious tokens for precedence)
    # Parentheses, function calls are usually handled by grammar structure directly
)

# --- Grammar Productions ---

# The PDF uses "identificador" for IDs. Your lexer produces 'ID' token.
# The PDF uses "integer_constant", "char_constant", "string_constant". Your lexer produces these.
# The PDF uses "op_suma" for +,- and "op_mul" for *,/. We'll use PLUS, MINUS, TIMES, DIVIDE tokens.
# The PDF uses "op_igual" for ==,!= and "op_relacional" for <,<=,>,>=. We'll use the specific tokens.
# The PDF uses "..." for ellipsis. Your lexer has PUNTOS.

# Start symbol
start = 'unidad_compilacion'

def p_unidad_compilacion_single(p):
    'unidad_compilacion : declaracion_externa'
    p[0] = [p[1]] # AST: a list of external declarations

def p_unidad_compilacion_list(p):
    'unidad_compilacion : unidad_compilacion declaracion_externa'
    p[0] = p[1] + [p[2]] # AST: append to list

def p_declaracion_externa(p):
    '''declaracion_externa : definicion_funcion
                           | declaracion_global''' # Renamed 'declaracion' to be more specific
    p[0] = p[1] # AST node

# Note: The PDF's "declaracion" is ambiguous. I'm interpreting it as:
# - declaracion_global: for global variable/function prototype declarations
# - declaracion_variable_local: for local variables inside functions
# - statement: for executable statements

def p_declaracion_global(p):
    '''declaracion_global : variable_declaracion
                          | funcion_prototipo_declaracion'''
    p[0] = p[1]

def p_definicion_funcion(p):
    'definicion_funcion : encabezado_def_funcion cuerpo_funcion'
    p[0] = ('func_def', p[1], p[2]) # AST node (name, params, body)

def p_encabezado_def_funcion(p):
    'encabezado_def_funcion : tipo_retorno ID LPAREN def_parametros RPAREN'
    p[0] = ('func_header', p[1], p[2], p[4]) # AST: (return_type, name, params)

def p_tipo_retorno(p):
    '''tipo_retorno : tipo
                    | VOID'''
    p[0] = p[1] # AST: the type string or 'void'

def p_tipo(p):
    '''tipo : INT
            | CHAR'''
    p[0] = p[1] # AST: the type string 'int' or 'char'

def p_def_parametros_list(p):
    'def_parametros : lista_def_parametros'
    p[0] = p[1] # AST: list of param definitions

def p_def_parametros_void(p):
    'def_parametros : VOID'
    p[0] = [] # AST: empty list for void params

# lista_def_parametros for function definitions (not prototypes)
def p_lista_def_parametros_multi(p):
    'lista_def_parametros : lista_def_parametros COMMA tipo ID'
    p[0] = p[1] + [(p[3], p[4])] # AST: list of (type, name) tuples

def p_lista_def_parametros_single(p):
    'lista_def_parametros : tipo ID'
    p[0] = [(p[1], p[2])] # AST: list of (type, name) tuples

def p_cuerpo_funcion(p):
    'cuerpo_funcion : LBRACE opcional_declaraciones_locales opcional_lista_statements RBRACE'
    p[0] = ('block', p[2], p[3]) # AST: (local_vars, statements)

def p_opcional_declaraciones_locales(p):
    '''opcional_declaraciones_locales : declaraciones_locales_list
                                      | empty''' # empty for no local declarations
    if len(p) == 2: p[0] = p[1] # p[1] could be [] from empty
    else: p[0] = []


def p_declaraciones_locales_list_multi(p):
    'declaraciones_locales_list : declaraciones_locales_list variable_declaracion'
    p[0] = p[1] + [p[2]]

def p_declaraciones_locales_list_single(p):
    'declaraciones_locales_list : variable_declaracion'
    p[0] = [p[1]]

def p_variable_declaracion(p): # Used for global and local vars
    'variable_declaracion : tipo lista_simple_identificadores SEMICOLON'
    p[0] = ('var_decl', p[1], p[2]) # AST: (type, list_of_ids)

def p_lista_simple_identificadores_multi(p):
    'lista_simple_identificadores : lista_simple_identificadores COMMA ID'
    p[0] = p[1] + [p[3]]

def p_lista_simple_identificadores_single(p):
    'lista_simple_identificadores : ID'
    p[0] = [p[1]]

def p_funcion_prototipo_declaracion(p): # Renamed from "declaracion_funcion" in PDF to avoid clash
    'funcion_prototipo_declaracion : tipo_retorno ID LPAREN declaracion_parametros RPAREN SEMICOLON'
    p[0] = ('func_prototype', p[1], p[2], p[4]) # AST: (return_type, name, param_types)

def p_declaracion_parametros_list(p):
    'declaracion_parametros : lista_decl_parametros'
    p[0] = p[1]

def p_declaracion_parametros_ellipsis(p):
    'declaracion_parametros : lista_decl_parametros COMMA PUNTOS' # Using PUNTOS from lexer
    p[0] = p[1] + ['...'] # AST: indicate ellipsis

def p_declaracion_parametros_void(p):
    'declaracion_parametros : VOID'
    p[0] = [] # No params

def p_lista_decl_parametros_multi(p):
    'lista_decl_parametros : lista_decl_parametros COMMA especificacion_decl_parametros'
    p[0] = p[1] + [p[3]]

def p_lista_decl_parametros_single(p):
    'lista_decl_parametros : especificacion_decl_parametros'
    p[0] = [p[1]]

def p_especificacion_decl_parametros_simple(p):
    'especificacion_decl_parametros : tipo ID'
    p[0] = ('param', p[1], p[2]) # AST: (type, name)

def p_especificacion_decl_parametros_pointer(p):
    'especificacion_decl_parametros : CHAR TIMES ID' # Specific for "char *"
    p[0] = ('param_ptr', p[1], p[3]) # AST: (base_type, name), assuming TIMES means pointer

# --- Statements ---
def p_opcional_lista_statements(p):
    '''opcional_lista_statements : statement_list
                                 | empty'''
    if len(p) == 2: p[0] = p[1]
    else: p[0] = []


def p_statement_list_multi(p):
    'statement_list : statement_list statement'
    p[0] = p[1] + [p[2]]

def p_statement_list_single(p):
    'statement_list : statement'
    p[0] = [p[1]]

def p_statement(p):
    '''statement : expression_statement
                 | return_statement
                 | while_statement
                 | if_statement
                 | block_statement'''
    p[0] = p[1] # AST node for the specific statement type

def p_expression_statement(p):
    'expression_statement : expresion SEMICOLON'
    p[0] = ('expr_stmt', p[1])

def p_return_statement_empty(p):
    'return_statement : RETURN SEMICOLON'
    p[0] = ('return_stmt', None)

def p_return_statement_expr(p):
    'return_statement : RETURN expresion SEMICOLON'
    p[0] = ('return_stmt', p[2])

def p_while_statement(p):
    'while_statement : WHILE LPAREN expresion RPAREN statement'
    p[0] = ('while_stmt', p[3], p[5])

def p_if_statement_then(p):
    'if_statement : IF LPAREN expresion RPAREN statement'
    p[0] = ('if_stmt', p[3], p[5], None) # Condition, then_branch, else_branch (None)

def p_if_statement_else(p):
    'if_statement : IF LPAREN expresion RPAREN statement ELSE statement'
    p[0] = ('if_stmt', p[3], p[5], p[7]) # Condition, then_branch, else_branch

def p_block_statement(p):
    'block_statement : LBRACE opcional_declaraciones_locales opcional_lista_statements RBRACE'
    # This is same as cuerpo_funcion structure, but represents a compound statement
    p[0] = ('block', p[2], p[3])


# --- Expressions ---
# The PDF: expresion -> expresion_igualdad "=" expresion_igualdad | expresion_igualdad
# This is unusual for assignment. Assuming it means assignment has lowest precedence and right-associativity
# And that the LHS of '=' must be an l-value (e.g., ID).
# For C-reducido, let's assume assignment is "ID = expression"
def p_expresion_assign(p):
    'expresion : ID ASSIGN expresion'
    p[0] = ('assign', p[1], p[3]) # AST: (target_id, value_expr)

def p_expresion_passthrough_equality(p):
    'expresion : expresion_igualdad'
    p[0] = p[1]

def p_expresion_igualdad_op(p):
    '''expresion_igualdad : expresion_relacional EQ expresion_relacional
                          | expresion_relacional NEQ expresion_relacional'''
    p[0] = ('binary_op', p[2], p[1], p[3]) # AST: (op_token, left_expr, right_expr)

def p_expresion_igualdad_passthrough(p):
    'expresion_igualdad : expresion_relacional'
    p[0] = p[1]

def p_expresion_relacional_op(p):
    '''expresion_relacional : expresion_simple LT expresion_simple
                            | expresion_simple LE expresion_simple
                            | expresion_simple GT expresion_simple
                            | expresion_simple GE expresion_simple'''
    p[0] = ('binary_op', p[2], p[1], p[3])

def p_expresion_relacional_passthrough(p):
    'expresion_relacional : expresion_simple'
    p[0] = p[1]

def p_expresion_simple_op(p):
    '''expresion_simple : expresion_simple PLUS term
                        | expresion_simple MINUS term'''
    p[0] = ('binary_op', p[2], p[1], p[3])

def p_expresion_simple_passthrough(p):
    'expresion_simple : term'
    p[0] = p[1]

def p_term_op(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = ('binary_op', p[2], p[1], p[3])

def p_term_passthrough(p):
    'term : factor'
    p[0] = p[1]

def p_factor_constant(p):
    'factor : constant'
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = ('id_ref', p[1]) # AST: reference to an identifier

def p_factor_paren_expr(p):
    'factor : LPAREN expresion RPAREN'
    p[0] = p[2] # The value of the inner expression

def p_factor_unary_op(p):
    '''factor : PLUS factor %prec UPLUS
              | MINUS factor %prec UMINUS'''
    p[0] = ('unary_op', p[1], p[2]) # AST: (op_token, expression)

def p_factor_func_call_with_args(p):
    'factor : callable_name LPAREN lista_expresiones RPAREN'
    p[0] = ('func_call', p[1], p[3]) # AST: (func_name_node, arg_list)

def p_factor_func_call_no_args(p):
    'factor : callable_name LPAREN RPAREN'
    p[0] = ('func_call', p[1], []) # AST: (func_name_node, empty_arg_list)

def p_callable_name(p):
    '''callable_name : ID
                     | PRINTF
                     | SCANF'''
    p[0] = ('callable', p[1]) # Node indicating what is being called (ID or specific keyword)


def p_constant(p):
    '''constant : STRING_CONSTANT
                | INTEGER_CONSTANT
                | CHAR_CONSTANT'''
    # The lexer already converts INTEGER_CONSTANT to int.
    # STRING_CONSTANT and CHAR_CONSTANT from lexer might need unescaping if not done there.
    # Your lexer's t_STRING_CONSTANT and t_CHAR_CONSTANT return the raw string including quotes.
    # This needs to be processed here or in the lexer to get the actual content.
    # For now, assume lexer gives actual value. If it gives raw, unescape here.
    # Example for string: if p[1] is '"abc"', then actual_value = p[1][1:-1] and unescape.
    # Your provided lexer for t_STRING_CONSTANT and t_CHAR_CONSTANT:
    # t_CHAR_CONSTANT(t): r"\'([^\\\n]|(\\.))\'"; return t -> t.value is raw, e.g. "'a'" or "'\\''"
    # t_STRING_CONSTANT(t): r'\"([^\\\n]|(\\[n"\\]))*\"'; return t -> t.value is raw, e.g. "\"abc\""

    if isinstance(p[1], str):
        if p.slice[1].type == 'STRING_CONSTANT':
            # Basic unescaping for strings, assuming lexer doesn't do it fully
            val = p[1][1:-1] # Remove outer quotes
            val = val.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
            p[0] = ('string_literal', val)
        elif p.slice[1].type == 'CHAR_CONSTANT':
            val = p[1][1:-1] # Remove outer quotes
            if val == "\\'": val = "'"
            elif val == "\\\\": val = "\\"
            # Else it's a single char
            p[0] = ('char_literal', val)
        else: # Should not happen if types are correct
            p[0] = p[1]
    else: # INTEGER_CONSTANT
        p[0] = ('int_literal', p[1])


def p_lista_expresiones_multi(p):
    'lista_expresiones : lista_expresiones COMMA expresion'
    p[0] = p[1] + [p[3]]

def p_lista_expresiones_single(p):
    'lista_expresiones : expresion'
    p[0] = [p[1]]

# --- Empty production ---
def p_empty(p):
    'empty :'
    p[0] = [] # Or None, depending on how you want to represent empty lists/optional parts

# --- Error rule for syntax errors ---
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}') on line {p.lineno}")
        # You might want to add more sophisticated error recovery here
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# --- Main function for testing ---
if __name__ == '__main__':
    source_code_example = """
    int global_var;
    char another_global;

    int sum(int a, int b); /* Prototype */

    void main(void) {
        int x, y, z;
        char c;
        x = 10;
        y = 20 + (5 * 2);
        global_var = x + y;
        c = 'a';
        
        if (x > 5) {
            printf("x is greater than 5\\n");
        } else {
            x = x + 1;
        }

        while (x < 15) {
            x = x + 1;
            printf("x in while: %d\\n", x);
        }
        z = sum(x,y);
        return;
    }

    int sum(int a, int b) {
        return a + b;
    }
    """
    
    error_example = """
    int main(void) {
        x = 10 + ; /* Syntax error here */
        return 0
    }
    """

    print("\n--- Parsing Correct Example ---")
    # Provide the lexer to the parser
    result = parser.parse(source_code_example, lexer=lexer)
    if result:
        print("Parsing Successful!")
        # print("AST:", result) # Uncomment to see the basic AST
    else:
        print("Parsing Failed or no input returned result.")

    # Reset lexer for next parse (important if lexer has state like lineno)
    lexer.lineno = 1 
    # If your lexer has other state that needs resetting, do it here.
    # Or, create a new lexer instance: 
    # from Analizador_lexico import lexer as new_lexer_instance
    # For simple tests, resetting lineno might be enough.
    # A cleaner way for multiple parses is to re-initialize the lexer or ensure parse() gets a fresh one.
    # lexer.input('') # Clear previous input if necessary and supported by your lexer's design

    print("\n--- Parsing Error Example ---")
    # Re-initialize lexer for a clean state (PLY lexers maintain state)
    from Analizador_lexico import lexer as fresh_lexer
    error_result = parser.parse(error_example, lexer=fresh_lexer)
    if error_result:
        print("Error example parsed (unexpected, should have failed or reported errors).")
    else:
        print("Error example processing finished (check for syntax error messages above).")