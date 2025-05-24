/*  
* progama de ejemplo No. 2  
*/  
int scanf( char *fmt, ... );  
int printf( char *fmt, ... );  
int cuenta( int n );  
int main( void )  
{  
int i, suma;  
i = scanf( "%d", &i); /* lea i */  
suma = cuenta(i); /* llama a cuenta y le pasa como parámetro el valor de i */  
printf( "%d\n", suma ); /* imprima resultados */  
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