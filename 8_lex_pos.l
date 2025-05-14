%{
/* Lexical Analyzer for Parts of Speech in English */
/* Without using Symbol Table */

#include <stdio.h>
#include <string.h>

/* Function to print the token type */
void print_token(char* token_type, char* lexeme) {
    printf("%-15s : %s\n", token_type, lexeme);
}

int line_num = 1;
%}

/* Regular Definitions */

/* Common articles */
ARTICLE         a|an|the

/* Common prepositions */
PREPOSITION     at|by|for|from|in|of|on|to|with|about|above|across|after|against|along|among|around|before|behind|below|beneath|beside|between|beyond|during|except|inside|into|near|off|over|through|toward|under|until|upon|within|without

/* Common conjunctions */
CONJUNCTION     and|but|or|nor|for|yet|so|because|although|since|unless|while|where|if|that|than

/* Common pronouns */
PRONOUN         I|me|my|mine|myself|you|your|yours|yourself|he|him|his|himself|she|her|hers|herself|it|its|itself|we|us|our|ours|ourselves|they|them|their|theirs|themselves|who|whom|whose|which|what|this|that|these|those

/* Auxiliary verbs and common regular verbs */
VERB            am|is|are|was|were|be|being|been|have|has|having|do|does|did|doing|go|goes|went|gone|going|dread|dreads|dreaded|dreading|run|runs|ran|running|arrive|arrives|arrived|arriving|thank|thanks|thanked|thanking|stop|stops|stopped|stopping|question|questions|questioned|questioning|exist|exists|existed|existing|give|gives|gave|giving|need|needs|needed|needing|kill|kills|killed|killing|come|comes|came|coming


/* Common adjectives */
ADJECTIVE       good|bad|big|small|large|little|old|new|high|low|great|nice|beautiful|ugly|happy|sad|angry|silly|smart|stupid|rich|poor|young|tall|short|fat|thin|fast|slow|early|late|hard|soft|hot|cold|warm|cool|clean|dirty|empty|full|heavy|light|strong|weak|wet|dry|sick|healthy|tired|awake|hungry|thirsty|busy|free|safe|dangerous|right|wrong|true|false|open|closed|difficult|easy|expensive|cheap|dark|bright|loud|quiet|dead|alive|same|different|important|interesting|boring|funny|serious|strange|normal|odd|necessary|possible|impossible|real|fake|best|worst|first|last|next|previous|only|favorite|better|worse

/* Common adverbs */
ADVERB          very|really|quickly|slowly|carefully|badly|well|always|never|sometimes|often|rarely|again|now|then|here|there|away|together|almost|only|just|even|still|too|also|not|so|quite|rather|somewhat|somehow|somewhere|anywhere|everywhere|nowhere|maybe|perhaps|probably|certainly|definitely|absolutely|completely|totally|entirely|fully|hardly|barely|nearly|almost|simply|merely|actually|finally|eventually|suddenly|gradually|basically|generally|usually|normally|naturally|especially|particularly|specifically|exactly|precisely|literally|anyway|however|though|instead|therefore|thus|meanwhile|otherwise|nevertheless|regardless|besides|moreover|furthermore|additionally

/* Common nouns */
NOUN            [a-zA-Z]+

/* Numbers */
NUMBER          [0-9]+(\.[0-9]+)?

/* Punctuation */
PUNCTUATION     [.,;:!?()[\]{}'""-]

/* Whitespace */
WHITESPACE      [ \t]+

/* Newline */
NEWLINE         \n

%%

{ARTICLE}       { print_token("ARTICLE", yytext); }
{PREPOSITION}   { print_token("PREPOSITION", yytext); }
{CONJUNCTION}   { print_token("CONJUNCTION", yytext); }
{PRONOUN}       { print_token("PRONOUN", yytext); }
{VERB}          { print_token("VERB", yytext); }
{ADJECTIVE}     { print_token("ADJECTIVE", yytext); }
{ADVERB}        { print_token("ADVERB", yytext); }
{NUMBER}        { print_token("NUMBER", yytext); }
{PUNCTUATION}   { print_token("PUNCTUATION", yytext); }
{NOUN}          { print_token("NOUN", yytext); }
{WHITESPACE}    { /* Ignore whitespace */ }
{NEWLINE}       { line_num++; }
.               { printf("UNKNOWN: %s at line %d\n", yytext, line_num); }

%%

int yywrap() {
    return 1;
}

int main(int argc, char** argv) {
    if (argc > 1) {
        FILE* file = fopen(argv[1], "r");
        if (!file) {
            printf("Could not open file %s\n", argv[1]);
            return 1;
        }
        yyin = file;
    } else {
        printf("Reading from standard input (type input text and press Ctrl+D when finished):\n");
        yyin = stdin;
    }
    
    printf("%-15s : %s\n", "PART_OF_SPEECH", "WORD");
    printf("----------------------------------------\n");
    
    yylex();
    
    printf("\nLexical analysis completed.\n");
    
    if (argc > 1) {
        fclose(yyin);
    }
    
    return 0;
}

/* 

create program.txt

flex -l program.l
gcc lex.yy.c
./a.out program.txt

*/
