10 HOME : H$ = "0123456789ABCDEF"
20 INPUT "START (EX C100): ";S$ : INPUT "END (EX C7FF): ";E$
30 V$ = S$ : GOSUB 300 : S = V : V$ = E$ : GOSUB 300 : E = V
40 X = PEEK (49282) : HOME : N = 0
50 FOR A = S TO E STEP 8
60 V = A : D = 4 : GOSUB 200 : L$ = O$ + ":" : C = 0
70 FOR I = 0 TO 7 : B = PEEK (A + I) : C = C + B : V = B : D = 2 : GOSUB 200 : L$ = L$ + " " + O$ : NEXT I
80 V = C - INT (C / 256) * 256 : D = 2 : GOSUB 200 : PRINT L$;" ";O$
90 N = N + 1 : IF N = 20 THEN N = 0 : PRINT "-- PRESS KEY --"; : GET K$ : HOME
100 NEXT A : END
200 O$ = "" : FOR J = 1 TO D : R = V - INT (V / 16) * 16 : O$ = MID$ (H$,R + 1,1) + O$ : V = INT (V / 16) : NEXT J : RETURN
300 V = 0 : FOR J = 1 TO LEN (V$) : K = ASC ( MID$ (V$,J,1)) - 48 : IF K > 9 THEN K = K - 7
310 V = V * 16 + K : NEXT J : RETURN
