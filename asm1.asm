    START 200
    READ X 
    MOVER AREG, ='10' 
    MOVEM AREG, Y 
    MOVER BREG, ='60'
    ADD AREG, BREG
    COMP AREG, X 
    BC GT, LAST 
    LTORG
NEXT SUB AREG, ='10'
    MOVER CREG, Y 
    ADD CREG, ='80'
    MOVEM CREG, Y 
    PRINT Y 
    STOP
X DS 1
Y DS 1
    END