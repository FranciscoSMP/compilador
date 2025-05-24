from lexer import lexer

code = '''
/* programa de ejemplo No. 1 */
int scanf( char *fmt, ... );
int printf( char *fmt, ... );
int main( void )
{
  int i, j;
  i = scanf("%d"); /* lea i */
  j = 9 + i * 8;    /* evalue j */
  printf("Resultado es %d\\n", j); /* imprima j */
}

/* programa de ejemplo No. 2 */
int scanf( char *fmt, ... );
int printf( char *fmt, ... );
int cuenta( int n );
int main( void )
{
  int i, suma;
  i = scanf("%d", &i); /* lea i */
  suma = cuenta(i);    /* llama a cuenta y le pasa como parámetro el valor de i */
  printf("%d\\n", suma); /* imprima resultados */
}

int cuenta( int n )
{
  int i, suma;
  i = 1;
  suma = 0;
  while ( i <= n ) {
    suma = suma + i;
    i = i + 1;
  }
  return suma;
}
'''

lexer.input(code)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{tok.type:<20} {tok.value!r:40} linea {tok.lineno}")
