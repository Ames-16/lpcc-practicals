%{
/* C Language Lexical Analyzer without Symbol Table
   This lexer identifies tokens in C language and prints them
*/

#include <stdio.h>
#include <string.h>

/* Token counts */
int total_tokens = 0;
int keywords = 0;
int identifiers = 0;
int operators = 0;
int numbers = 0;
int strings = 0;
int preprocessor = 0;
int comments = 0;
int special_chars = 0;

/* For better output formatting */
#define PRINT_TOKEN(type, value) printf("%-20s %s\n", type, value)
%}

/* Regular expression definitions */

/* Keywords */
KEYWORD         auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while

/* Identifiers */
IDENTIFIER      [a-zA-Z_][a-zA-Z0-9_]*

/* Numbers */
INTEGER         [0-9]+
FLOAT           [0-9]+\.[0-9]+([eE][+-]?[0-9]+)?|[0-9]+[eE][+-]?[0-9]+
HEX             0[xX][0-9a-fA-F]+
OCTAL           0[0-7]+

/* Strings and Characters */
STRING          \"([^\"\\\n]|\\.)*\"
CHAR            \'([^\'\\\n]|\\.)*\'

/* Operators */
ARITHMETIC_OP   [+\-*/%]
RELATIONAL_OP   [<>]=?|==|!=
LOGICAL_OP      &&|\|\||!
BITWISE_OP      [&|^~]|<<|>>
ASSIGNMENT_OP   [+\-*/%&|^]?=
INCREMENT_OP    \+\+|--
MISC_OP         [?:.]

/* Preprocessor directives */
PREPROCESSOR    ^[ \t]*#[a-zA-Z]+.*$

/* Comments */
C_COMMENT       \/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+\/
CPP_COMMENT     \/\/.*\n

/* Special characters */
SPECIAL_CHAR    [;,(){}\[\]]

/* Whitespace */
WHITESPACE      [ \t\n]+

%%

{KEYWORD}       { PRINT_TOKEN("KEYWORD", yytext); keywords++; total_tokens++; }
{IDENTIFIER}    { PRINT_TOKEN("IDENTIFIER", yytext); identifiers++; total_tokens++; }
{INTEGER}       { PRINT_TOKEN("INTEGER", yytext); numbers++; total_tokens++; }
{FLOAT}         { PRINT_TOKEN("FLOAT", yytext); numbers++; total_tokens++; }
{HEX}           { PRINT_TOKEN("HEX", yytext); numbers++; total_tokens++; }
{OCTAL}         { PRINT_TOKEN("OCTAL", yytext); numbers++; total_tokens++; }
{STRING}        { PRINT_TOKEN("STRING", yytext); strings++; total_tokens++; }
{CHAR}          { PRINT_TOKEN("CHAR", yytext); strings++; total_tokens++; }
{ARITHMETIC_OP} { PRINT_TOKEN("ARITHMETIC_OP", yytext); operators++; total_tokens++; }
{RELATIONAL_OP} { PRINT_TOKEN("RELATIONAL_OP", yytext); operators++; total_tokens++; }
{LOGICAL_OP}    { PRINT_TOKEN("LOGICAL_OP", yytext); operators++; total_tokens++; }
{BITWISE_OP}    { PRINT_TOKEN("BITWISE_OP", yytext); operators++; total_tokens++; }
{ASSIGNMENT_OP} { PRINT_TOKEN("ASSIGNMENT_OP", yytext); operators++; total_tokens++; }
{INCREMENT_OP}  { PRINT_TOKEN("INCREMENT_OP", yytext); operators++; total_tokens++; }
{MISC_OP}       { PRINT_TOKEN("MISC_OP", yytext); operators++; total_tokens++; }
{PREPROCESSOR}  { PRINT_TOKEN("PREPROCESSOR", yytext); preprocessor++; total_tokens++; }
{C_COMMENT}     { PRINT_TOKEN("C_COMMENT", yytext); comments++; total_tokens++; }
{CPP_COMMENT}   { PRINT_TOKEN("CPP_COMMENT", yytext); comments++; total_tokens++; }
{SPECIAL_CHAR}  { PRINT_TOKEN("SPECIAL_CHAR", yytext); special_chars++; total_tokens++; }
{WHITESPACE}    { /* Ignore whitespace */ }
.               { PRINT_TOKEN("UNRECOGNIZED", yytext); total_tokens++; }

%%

int yywrap() {
    return 1;
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            fprintf(stderr, "Error: Could not open file %s\n", argv[1]);
            return 1;
        }
        yyin = file;
    } else {
        printf("Reading from standard input (type ctrl-D to end):\n");
        yyin = stdin;
    }
    
    /* Print header for token output */
    printf("\n");
    printf("%-20s %s\n", "TOKEN TYPE", "VALUE");
    printf("------------------------------------------\n");
    
    yylex();
    
    /* Print token statistics with better formatting */
    /* printf("\n");
    printf("           TOKEN STATISTICS               \n");
    printf("------------------------------------------\n");
    printf("%-25s %5d\n", "Total tokens", total_tokens);
    printf("------------------------------------------\n");
    printf("%-25s %5d\n", "Keywords", keywords);
    printf("%-25s %5d\n", "Identifiers", identifiers);
    printf("%-25s %5d\n", "Operators", operators);
    printf("%-25s %5d\n", "Numbers", numbers);
    printf("%-25s %5d\n", "Strings & Characters", strings);
    printf("%-25s %5d\n", "Preprocessor directives", preprocessor);
    printf("%-25s %5d\n", "Comments", comments);
    printf("%-25s %5d\n", "Special characters", special_chars); */
    
    if (argc > 1) {
        fclose(yyin);
    }
    
    return 0;
}

/* 
create program.C

lex -l program.l
gcc lex.yy.c
./a.out program.c
*/