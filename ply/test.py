from Analizador_lexico import lexer
from Analizador_sintactico import parser  # ...nuevo import...

code = '''
/*  
* Calculo de factorial de un número  
*/  
int scanf( char *fmt, ... );  
int printf( char *fmt, ... );  
int factorial( int n );  
int main( void )  
{  
int n, fact; /*declara las variables a y fact */  
printf( "Ingrese un entero: " );  
n = scanf( "%d"); /* lea n */  
fact = factorial( n ); /* llame a factorial */  
printf( "Factorial de %d ", n );  
printf( "es %d\n", fact );  
}  
int factorial( int n )  
{  
if ( n <= 1 )  
return 1;  
else  
return n * factorial( n - 1 );  
}
'''

lexer.input(code)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{tok.type:<20} {tok.value!r:40} linea {tok.lineno}")

# Uso del analizador sintáctico
result = parser.parse(code, lexer=lexer)
print("\n--- Análisis sintáctico ---")
print(result)
