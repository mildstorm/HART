; ======================================================================
; 정원 HART U65 (2764, 8KB) U64 두 번째 6502 실행 펌웨어
;   독립 로컬 버스에서 동작하는 보조 6502의 전용 제어 프로그램
;   화면 초기화, 비디오 제어, 한글 변환, 80컬럼 제어 루틴
;   오프셋 0x1300-0x14FF: 화면 하단 기능키(F1-F12) 라벨 테이블
;     - Apple BASIC 모드 1, 2, 3 기능키 세트
;     - CP/M 모드 기능키 세트 (DIR, ERA, REN, SAVE, TYPE, STAT, WORKING 등)
; Base Address: $E000 - $FFFF (8192 bytes)
; ======================================================================

$E000:  D8        CLD
$E001:  A2 00     LDX #$00
$E003:  8A        TXA
$E004:  85 02     STA $02
$E006:  9D 00 40  STA $4000,X
$E009:  9D 00 50  STA $5000,X
$E00C:  9D 00 41  STA $4100,X
$E00F:  9D 00 51  STA $5100,X
$E012:  9D 00 42  STA $4200,X
$E015:  9D 00 52  STA $5200,X
$E018:  9D 00 43  STA $4300,X
$E01B:  9D 00 53  STA $5300,X
$E01E:  E8        INX
$E01F:  D0 E5     BNE $E006
$E021:  4C 6E D1  JMP $D16E
$E024:  53        .BYTE $53
$E025:  45 41     EOR $41
$E027:  86 28     STX $28
$E029:  C9 00     CMP #$00
$E02B:  C9 00     CMP #$00
$E02D:  C9 00     CMP #$00
$E02F:  C9 00     CMP #$00
$E031:  C9 00     CMP #$00
$E033:  C9 00     CMP #$00
$E035:  C9 00     CMP #$00
$E037:  C9 00     CMP #$00
$E039:  C9 00     CMP #$00
$E03B:  C9 00     CMP #$00
$E03D:  C9 00     CMP #$00
$E03F:  C9 00     CMP #$00
$E041:  C9 00     CMP #$00
$E043:  C9 00     CMP #$00
$E045:  C9 00     CMP #$00
$E047:  C9 FF     CMP #$FF
$E049:  E9 00     SBC #$00
$E04B:  C9 40     CMP #$40 ('@')
$E04D:  8E 02 00  STX $0002
$E050:  D0 02     BNE $E054
$E052:  F0 59     BEQ $E0AD
$E054:  EA        NOP
$E055:  38        SEC
$E056:  86 03     STX $03
$E058:  8C 02 00  STY $0002
$E05B:  8E 02 00  STX $0002
$E05E:  B0 C7     BCS $E027
$E060:  EA        NOP
$E061:  38        SEC
$E062:  86 03     STX $03
$E064:  8C 02 00  STY $0002
$E067:  8E 02 00  STX $0002
$E06A:  B0 13     BCS $E07F
$E06C:  87        .BYTE $87
$E06D:  01 0B     ORA ($0B,X)
$E06F:  7B        .BYTE $7B
$E070:  E6 07     INC $07
$E072:  C2        .BYTE $C2
$E073:  7A        .BYTE $7A
$E074:  EA        NOP
$E075:  8E 03 00  STX $0003
$E078:  8C 06 00  STY $0006
$E07B:  86 02     STX $02
$E07D:  EA        NOP
$E07E:  EA        NOP
$E07F:  86 00     STX $00
$E081:  C9 00     CMP #$00
$E083:  C9 00     CMP #$00
$E085:  C9 00     CMP #$00
$E087:  C9 00     CMP #$00
$E089:  C9 00     CMP #$00
$E08B:  C9 00     CMP #$00
$E08D:  C9 00     CMP #$00
$E08F:  C9 00     CMP #$00
$E091:  C9 00     CMP #$00
$E093:  C9 00     CMP #$00
$E095:  C9 00     CMP #$00
$E097:  C9 00     CMP #$00
$E099:  C9 00     CMP #$00
$E09B:  C9 00     CMP #$00
$E09D:  C9 00     CMP #$00
$E09F:  C9 FF     CMP #$FF
$E0A1:  E9 00     SBC #$00
$E0A3:  C9 80     CMP #$80
$E0A5:  8E 02 00  STX $0002
$E0A8:  D0 B6     BNE $E060
$E0AA:  F0 A9     BEQ $E055
$E0AC:  EA        NOP
$E0AD:  38        SEC
$E0AE:  86 03     STX $03
$E0B0:  8C 02 00  STY $0002
$E0B3:  8E 02 00  STX $0002
$E0B6:  B0 17     BCS $E0CF
$E0B8:  5A        .BYTE $5A
$E0B9:  6C 6A A6  JMP ($A66A)
$E0BC:  9E        .BYTE $9E
$E0BD:  98        TYA
$E0BE:  96 A4     STX $A4,Y
$E0C0:  82        .BYTE $82
$E0C1:  00        BRK
$E0C2:  C9 BA     CMP #$BA (':')
$E0C4:  86 03     STX $03
$E0C6:  8E 02 00  STX $0002
$E0C9:  8C 00 0C  STY $0C00
$E0CC:  4C CF C0  JMP $C0CF
$E0CF:  86 50     STX $50
$E0D1:  C9 00     CMP #$00
$E0D3:  C9 00     CMP #$00
$E0D5:  C9 00     CMP #$00
$E0D7:  C9 00     CMP #$00
$E0D9:  C9 00     CMP #$00
$E0DB:  C9 00     CMP #$00
$E0DD:  C9 00     CMP #$00
$E0DF:  C9 00     CMP #$00
$E0E1:  C9 00     CMP #$00
$E0E3:  C9 00     CMP #$00
$E0E5:  C9 00     CMP #$00
$E0E7:  C9 00     CMP #$00
$E0E9:  C9 00     CMP #$00
$E0EB:  C9 00     CMP #$00
$E0ED:  C9 00     CMP #$00
$E0EF:  C9 FF     CMP #$FF
$E0F1:  E9 00     SBC #$00
$E0F3:  C9 00     CMP #$00
$E0F5:  8E 02 00  STX $0002
$E0F8:  D0 B2     BNE $E0AC
$E0FA:  EA        NOP
$E0FB:  9A        TXS
$E0FC:  8E 03 00  STX $0003
$E0FF:  8E 02 00  STX $0002
$E102:  4C B1 C9  JMP $C9B1
$E105:  00        BRK
$E106:  C3        .BYTE $C3
$E107:  B8        CLV
$E108:  EA        NOP
$E109:  EA        NOP
$E10A:  EA        NOP
$E10B:  EA        NOP
$E10C:  EA        NOP
$E10D:  EA        NOP
$E10E:  4C EB C2  JMP $C2EB
$E111:  BA        TSX
$E112:  8E 03 00  STX $0003
$E115:  8C 02 00  STY $0002
$E118:  86 02     STX $02
$E11A:  A2 09     LDX #$09
$E11C:  CA        DEX
$E11D:  D0 FD     BNE $E11C
$E11F:  BA        TSX
$E120:  EA        NOP
$E121:  4C F2 CA  JMP $CAF2
$E124:  C8        INY
$E125:  FE 27 86  INC $8627,X
$E128:  28        PLP
$E129:  C9 00     CMP #$00
$E12B:  C9 00     CMP #$00
$E12D:  C9 00     CMP #$00
$E12F:  C9 00     CMP #$00
$E131:  C9 00     CMP #$00
$E133:  C9 00     CMP #$00
$E135:  C9 00     CMP #$00
$E137:  C9 00     CMP #$00
$E139:  C9 00     CMP #$00
$E13B:  C9 00     CMP #$00
$E13D:  C9 00     CMP #$00
$E13F:  C9 00     CMP #$00
$E141:  C9 00     CMP #$00
$E143:  C9 00     CMP #$00
$E145:  C9 00     CMP #$00
$E147:  C9 FF     CMP #$FF
$E149:  E9 00     SBC #$00
$E14B:  C9 40     CMP #$40 ('@')
$E14D:  8E 02 00  STX $0002
$E150:  D0 02     BNE $E154
$E152:  F0 70     BEQ $E1C4
$E154:  EA        NOP
$E155:  38        SEC
$E156:  86 03     STX $03
$E158:  8C 02 00  STY $0002
$E15B:  8E 02 00  STX $0002
$E15E:  B0 C7     BCS $E127
$E160:  EA        NOP
$E161:  38        SEC
$E162:  86 03     STX $03
$E164:  8C 02 00  STY $0002
$E167:  8E 02 00  STX $0002
$E16A:  B0 13     BCS $E17F
$E16C:  0E 04 21  ASL $2104
$E16F:  0B        .BYTE $0B
$E170:  0E 36 20  ASL $2036
$E173:  23        .BYTE $23
$E174:  EA        NOP
$E175:  8E 03 00  STX $0003
$E178:  8C 06 00  STY $0006
$E17B:  86 02     STX $02
$E17D:  EA        NOP
$E17E:  EA        NOP
$E17F:  86 00     STX $00
$E181:  C9 00     CMP #$00
$E183:  C9 00     CMP #$00
$E185:  C9 00     CMP #$00
$E187:  C9 00     CMP #$00
$E189:  C9 00     CMP #$00
$E18B:  C9 00     CMP #$00
$E18D:  C9 00     CMP #$00
$E18F:  C9 00     CMP #$00
$E191:  C9 00     CMP #$00
$E193:  C9 00     CMP #$00
$E195:  C9 00     CMP #$00
$E197:  C9 00     CMP #$00
$E199:  C9 00     CMP #$00
$E19B:  C9 00     CMP #$00
$E19D:  C9 00     CMP #$00
$E19F:  C9 FF     CMP #$FF
$E1A1:  E9 00     SBC #$00
$E1A3:  C9 80     CMP #$80
$E1A5:  8E 02 00  STX $0002
$E1A8:  D0 B6     BNE $E160
$E1AA:  F0 A9     BEQ $E155
$E1AC:  4C 5E D1  JMP $D15E
$E1AF:  BD 9E C2  LDA $C29E,X
$E1B2:  9D 8B 42  STA $428B,X
$E1B5:  E8        INX
$E1B6:  E0 0A     CPX #$0A
$E1B8:  90 F2     BCC $E1AC
$E1BA:  AC F6 43  LDY $43F6
$E1BD:  4C AE D2  JMP $D2AE
$E1C0:  47        .BYTE $47
$E1C1:  AF        .BYTE $AF
$E1C2:  2A        ROL
$E1C3:  EA        NOP
$E1C4:  38        SEC
$E1C5:  86 03     STX $03
$E1C7:  8C 02 00  STY $0002
$E1CA:  8E 02 00  STX $0002
$E1CD:  B0 00     BCS $E1CF
$E1CF:  86 50     STX $50
$E1D1:  C9 00     CMP #$00
$E1D3:  C9 00     CMP #$00
$E1D5:  C9 00     CMP #$00
$E1D7:  C9 00     CMP #$00
$E1D9:  C9 00     CMP #$00
$E1DB:  C9 00     CMP #$00
$E1DD:  C9 00     CMP #$00
$E1DF:  C9 00     CMP #$00
$E1E1:  C9 00     CMP #$00
$E1E3:  C9 00     CMP #$00
$E1E5:  C9 00     CMP #$00
$E1E7:  C9 00     CMP #$00
$E1E9:  C9 00     CMP #$00
$E1EB:  C9 00     CMP #$00
$E1ED:  C9 00     CMP #$00
$E1EF:  C9 FF     CMP #$FF
$E1F1:  E9 00     SBC #$00
$E1F3:  C9 20     CMP #$20 (' ')
$E1F5:  8E 02 00  STX $0002
$E1F8:  D0 C9     BNE $E1C3
$E1FA:  4C C3 C0  JMP $C0C3
$E1FD:  04        .BYTE $04
$E1FE:  D5 11     CMP $11,X
$E200:  4C F4 D6  JMP $D6F4
$E203:  AD FD 43  LDA $43FD
$E206:  0A        ASL
$E207:  0A        ASL
$E208:  10 F6     BPL $E200
$E20A:  AD FD 43  LDA $43FD
$E20D:  10 07     BPL $E216
$E20F:  A2 04     LDX #$04
$E211:  A9 07     LDA #$07
$E213:  EA        NOP
$E214:  D0 0B     BNE $E221
$E216:  A2 03     LDX #$03
$E218:  A9 06     LDA #$06
$E21A:  EA        NOP
$E21B:  EA        NOP
$E21C:  EA        NOP
$E21D:  D0 02     BNE $E221
$E21F:  A2 03     LDX #$03
$E221:  CA        DEX
$E222:  D0 FD     BNE $E221
$E224:  BA        TSX
$E225:  8E 03 00  STX $0003
$E228:  86 02     STX $02
$E22A:  38        SEC
$E22B:  E9 01     SBC #$01
$E22D:  D0 F0     BNE $E21F
$E22F:  EA        NOP
$E230:  EA        NOP
$E231:  EA        NOP
$E232:  EA        NOP
$E233:  EA        NOP
$E234:  EA        NOP
$E235:  EA        NOP
$E236:  A9 06     LDA #$06
$E238:  D0 02     BNE $E23C
$E23A:  86 02     STX $02
$E23C:  8E 03 00  STX $0003
$E23F:  38        SEC
$E240:  E9 01     SBC #$01
$E242:  F0 07     BEQ $E24B
$E244:  A2 03     LDX #$03
$E246:  CA        DEX
$E247:  D0 FD     BNE $E246
$E249:  F0 EF     BEQ $E23A
$E24B:  A2 03     LDX #$03
$E24D:  CA        DEX
$E24E:  D0 FD     BNE $E24D
$E250:  A9 04     LDA #$04
$E252:  86 02     STX $02
$E254:  8E 03 00  STX $0003
$E257:  86 02     STX $02
$E259:  D0 00     BNE $E25B
$E25B:  A2 04     LDX #$04
$E25D:  CA        DEX
$E25E:  D0 FD     BNE $E25D
$E260:  E9 01     SBC #$01
$E262:  86 03     STX $03
$E264:  86 02     STX $02
$E266:  D0 F3     BNE $E25B
$E268:  AD FD 43  LDA $43FD
$E26B:  49 80     EOR #$80
$E26D:  8D FD 43  STA $43FD
$E270:  30 06     BMI $E278
$E272:  A9 0C     LDA #$0C
$E274:  EA        NOP
$E275:  38        SEC
$E276:  B0 16     BCS $E28E
$E278:  EA        NOP
$E279:  EA        NOP
$E27A:  EA        NOP
$E27B:  EA        NOP
$E27C:  EA        NOP
$E27D:  8E 03 00  STX $0003
$E280:  86 02     STX $02
$E282:  A9 0B     LDA #$0B
$E284:  A2 03     LDX #$03
$E286:  38        SEC
$E287:  D0 02     BNE $E28B
$E289:  A2 09     LDX #$09
$E28B:  CA        DEX
$E28C:  D0 FD     BNE $E28B
$E28E:  BA        TSX
$E28F:  8E 03 00  STX $0003
$E292:  8C 02 00  STY $0002
$E295:  86 02     STX $02
$E297:  E9 01     SBC #$01
$E299:  D0 EE     BNE $E289
$E29B:  4C 49 CB  JMP $CB49
$E29E:  F5 E7     SBC $E7,X
$E2A0:  D7        .BYTE $D7
$E2A1:  EE C3 AE  INC $AEC3
$E2A4:  CC E4 A0  CPY $A0E4
$E2A7:  B4 AA     LDY $AA,X
$E2A9:  EA        NOP
$E2AA:  EA        NOP
$E2AB:  EA        NOP
$E2AC:  EA        NOP
$E2AD:  4C C5 CA  JMP $CAC5
$E2B0:  A9 8C     LDA #$8C
$E2B2:  EA        NOP
$E2B3:  EA        NOP
$E2B4:  EA        NOP
$E2B5:  EA        NOP
$E2B6:  EA        NOP
$E2B7:  EA        NOP
$E2B8:  EA        NOP
$E2B9:  AA        TAX
$E2BA:  A8        TAY
$E2BB:  C8        INY
$E2BC:  A9 C0     LDA #$C0 ('@')
$E2BE:  D0 00     BNE $E2C0
$E2C0:  4C 74 C0  JMP $C074
$E2C3:  EA        NOP
$E2C4:  EA        NOP
$E2C5:  EA        NOP
$E2C6:  4D E8 43  EOR $43E8
$E2C9:  AA        TAX
$E2CA:  9A        TXS
$E2CB:  A9 6D     LDA #$6D ('m')
$E2CD:  A8        TAY
$E2CE:  49 81     EOR #$81
$E2D0:  AA        TAX
$E2D1:  A9 C0     LDA #$C0 ('@')
$E2D3:  D0 00     BNE $E2D5
$E2D5:  4C 74 C1  JMP $C174
$E2D8:  A9 88     LDA #$88
$E2DA:  30 00     BMI $E2DC
$E2DC:  EA        NOP
$E2DD:  EA        NOP
$E2DE:  EA        NOP
$E2DF:  EA        NOP
$E2E0:  EA        NOP
$E2E1:  EA        NOP
$E2E2:  EA        NOP
$E2E3:  AA        TAX
$E2E4:  A8        TAY
$E2E5:  C8        INY
$E2E6:  A9 C0     LDA #$C0 ('@')
$E2E8:  4C 74 C0  JMP $C074
$E2EB:  BA        TSX
$E2EC:  86 03     STX $03
$E2EE:  8C 02 00  STY $0002
$E2F1:  86 02     STX $02
$E2F3:  A2 09     LDX #$09
$E2F5:  CA        DEX
$E2F6:  D0 FD     BNE $E2F5
$E2F8:  EA        NOP
$E2F9:  4C 11 C1  JMP $C111
$E2FC:  C9 CD     CMP #$CD ('M')
$E2FE:  8C 0E 8E  STY $8E0E
$E301:  E8        INX
$E302:  43        .BYTE $43
$E303:  4D E8 43  EOR $43E8
$E306:  2D F3 43  AND $43F3
$E309:  10 19     BPL $E324
$E30B:  09 80     ORA #$80
$E30D:  29 F6     AND #$F6 ('v')
$E30F:  AA        TAX
$E310:  EA        NOP
$E311:  A9 40     LDA #$40 ('@')
$E313:  8D 00 0C  STA $0C00
$E316:  AC F4 43  LDY $43F4
$E319:  8E 03 00  STX $0003
$E31C:  8E 02 00  STX $0002
$E31F:  A9 08     LDA #$08
$E321:  6C F7 53  JMP ($53F7)
$E324:  09 88     ORA #$88
$E326:  29 FE     AND #$FE ('~')
$E328:  AA        TAX
$E329:  A8        TAY
$E32A:  A9 C0     LDA #$C0 ('@')
$E32C:  EA        NOP
$E32D:  4C 74 C0  JMP $C074
$E330:  8E 03 00  STX $0003
$E333:  8C 02 00  STY $0002
$E336:  86 02     STX $02
$E338:  2C F6 53  BIT $53F6
$E33B:  70 05     BVS $E342
$E33D:  EA        NOP
$E33E:  A2 08     LDX #$08
$E340:  D0 1B     BNE $E35D
$E342:  AD FE 53  LDA $53FE
$E345:  F0 04     BEQ $E34B
$E347:  A2 07     LDX #$07
$E349:  D0 12     BNE $E35D
$E34B:  A9 FF     LDA #$FF
$E34D:  8D FE 53  STA $53FE
$E350:  AD F6 53  LDA $53F6
$E353:  29 BF     AND #$BF ('?')
$E355:  8D F6 53  STA $53F6
$E358:  EA        NOP
$E359:  EA        NOP
$E35A:  EA        NOP
$E35B:  A2 03     LDX #$03
$E35D:  CA        DEX
$E35E:  D0 FD     BNE $E35D
$E360:  BA        TSX
$E361:  86 03     STX $03
$E363:  8C 02 00  STY $0002
$E366:  86 02     STX $02
$E368:  4C 17 CA  JMP $CA17
$E36B:  EA        NOP
$E36C:  EA        NOP
$E36D:  EA        NOP
$E36E:  A2 03     LDX #$03
$E370:  A9 08     LDA #$08
$E372:  CE F8 53  DEC $53F8
$E375:  D0 02     BNE $E379
$E377:  A2 08     LDX #$08
$E379:  CA        DEX
$E37A:  D0 FD     BNE $E379
$E37C:  F0 00     BEQ $E37E
$E37E:  18        CLC
$E37F:  BA        TSX
$E380:  8E 03 00  STX $0003
$E383:  8C 02 00  STY $0002
$E386:  86 02     STX $02
$E388:  E9 00     SBC #$00
$E38A:  D0 EB     BNE $E377
$E38C:  4C 03 C2  JMP $C203
$E38F:  2E D6 7C  ROL $7CD6
$E392:  D6 00     DEC $00,X
$E394:  DF        .BYTE $DF
$E395:  87        .BYTE $87
$E396:  D6 B2     DEC $B2,X
$E398:  D6 00     DEC $00,X
$E39A:  D6 1A     DEC $1A,X
$E39C:  D6 71     DEC $71,X
$E39E:  D6 AD     DEC $AD,X
$E3A0:  F8        SED
$E3A1:  43        .BYTE $43
$E3A2:  0A        ASL
$E3A3:  0A        ASL
$E3A4:  8D F2 43  STA $43F2
$E3A7:  EE FA 43  INC $43FA
$E3AA:  4C 0C D0  JMP $D00C
$E3AD:  00        BRK
$E3AE:  06 0D     ASL $0D
$E3B0:  14        .BYTE $14
$E3B1:  16 18     ASL $18,X
$E3B3:  1E 20 22  ASL $2220,X
$E3B6:  24 80     BIT $80
$E3B8:  06 0C     ASL $0C
$E3BA:  0E 14 1A  ASL $1A14
$E3BD:  21 80     AND ($80,X)
$E3BF:  02        .BYTE $02
$E3C0:  04        .BYTE $04
$E3C1:  06 0A     ASL $0A
$E3C3:  10 14     BPL $E3D9
$E3C5:  1A        .BYTE $1A
$E3C6:  21 80     AND ($80,X)
$E3C8:  06 0A     ASL $0A
$E3CA:  0C        .BYTE $0C
$E3CB:  0E 10 14  ASL $1410
$E3CE:  16 18     ASL $18,X
$E3D0:  21 80     AND ($80,X)
$E3D2:  06 0A     ASL $0A
$E3D4:  10 14     BPL $E3EA
$E3D6:  19 21 80  ORA $8021,Y
$E3D9:  06 0A     ASL $0A
$E3DB:  10 14     BPL $E3F1
$E3DD:  1A        .BYTE $1A
$E3DE:  21 9A     AND ($9A,X)
$E3E0:  AD DF C3  LDA $C3DF
$E3E3:  AE AD C3  LDX $C3AD
$E3E6:  0A        ASL
$E3E7:  7D B6 C3  ADC $C3B6,X
$E3EA:  E8        INX
$E3EB:  E0 03     CPX #$03
$E3ED:  90 F8     BCC $E3E7
$E3EF:  ED BA C3  SBC $C3BA
$E3F2:  BA        TSX
$E3F3:  4C D6 D5  JMP $D5D6
$E3F6:  F4        .BYTE $F4
$E3F7:  01 C5     ORA ($C5,X)
$E3F9:  CD BD 00  CMP $00BD
$E3FC:  C1 C3     CMP ($C3,X)
$E3FE:  99 02 EA  STA $EA02,Y
$E401:  EA        NOP
$E402:  EA        NOP
$E403:  4D E8 43  EOR $43E8
$E406:  AA        TAX
$E407:  9A        TXS
$E408:  A9 EB     LDA #$EB ('k')
$E40A:  A8        TAY
$E40B:  49 01     EOR #$01
$E40D:  AA        TAX
$E40E:  A9 C0     LDA #$C0 ('@')
$E410:  D0 00     BNE $E412
$E412:  4C 74 C1  JMP $C174
$E415:  20 01 79  JSR $7901
$E418:  EA        NOP
$E419:  8E 03 00  STX $0003
$E41C:  8E 02 00  STX $0002
$E41F:  EA        NOP
$E420:  88        DEY
$E421:  D0 03     BNE $E426
$E423:  4C B8 C9  JMP $C9B8
$E426:  86 00     STX $00
$E428:  C9 00     CMP #$00
$E42A:  C9 00     CMP #$00
$E42C:  C9 00     CMP #$00
$E42E:  C9 00     CMP #$00
$E430:  C9 00     CMP #$00
$E432:  C9 00     CMP #$00
$E434:  C9 00     CMP #$00
$E436:  C9 00     CMP #$00
$E438:  C9 00     CMP #$00
$E43A:  C9 00     CMP #$00
$E43C:  C9 00     CMP #$00
$E43E:  C9 00     CMP #$00
$E440:  C9 00     CMP #$00
$E442:  C9 00     CMP #$00
$E444:  C9 00     CMP #$00
$E446:  C9 00     CMP #$00
$E448:  C9 FF     CMP #$FF
$E44A:  E9 00     SBC #$00
$E44C:  C9 00     CMP #$00
$E44E:  86 02     STX $02
$E450:  D0 C6     BNE $E418
$E452:  A9 08     LDA #$08
$E454:  88        DEY
$E455:  86 03     STX $03
$E457:  8E 02 00  STX $0002
$E45A:  F0 04     BEQ $E460
$E45C:  EA        NOP
$E45D:  4C 4E CC  JMP $CC4E
$E460:  4C B5 C9  JMP $C9B5
$E463:  66 03     ROR $03
$E465:  AF        .BYTE $AF
$E466:  F6 42     INC $42,X
$E468:  EA        NOP
$E469:  8E 03 00  STX $0003
$E46C:  8E 02 00  STX $0002
$E46F:  EA        NOP
$E470:  88        DEY
$E471:  D0 03     BNE $E476
$E473:  4C B8 C9  JMP $C9B8
$E476:  86 00     STX $00
$E478:  C9 00     CMP #$00
$E47A:  C9 00     CMP #$00
$E47C:  C9 00     CMP #$00
$E47E:  C9 00     CMP #$00
$E480:  C9 00     CMP #$00
$E482:  C9 00     CMP #$00
$E484:  C9 00     CMP #$00
$E486:  C9 00     CMP #$00
$E488:  C9 00     CMP #$00
$E48A:  C9 00     CMP #$00
$E48C:  C9 00     CMP #$00
$E48E:  C9 00     CMP #$00
$E490:  C9 00     CMP #$00
$E492:  C9 00     CMP #$00
$E494:  C9 00     CMP #$00
$E496:  C9 00     CMP #$00
$E498:  C9 FF     CMP #$FF
$E49A:  E9 00     SBC #$00
$E49C:  C9 00     CMP #$00
$E49E:  86 02     STX $02
$E4A0:  D0 C6     BNE $E468
$E4A2:  A9 08     LDA #$08
$E4A4:  88        DEY
$E4A5:  86 03     STX $03
$E4A7:  8E 02 00  STX $0002
$E4AA:  F0 04     BEQ $E4B0
$E4AC:  EA        NOP
$E4AD:  4C 9E CC  JMP $CC9E
$E4B0:  4C B5 C9  JMP $C9B5
$E4B3:  FE 08 DA  INC $DA08,X
$E4B6:  DD 03 EA  CMP $EA03,X
$E4B9:  8E 03 00  STX $0003
$E4BC:  8E 02 00  STX $0002
$E4BF:  88        DEY
$E4C0:  EA        NOP
$E4C1:  D0 03     BNE $E4C6
$E4C3:  4C B8 C9  JMP $C9B8
$E4C6:  86 00     STX $00
$E4C8:  C9 00     CMP #$00
$E4CA:  C9 00     CMP #$00
$E4CC:  C9 00     CMP #$00
$E4CE:  C9 00     CMP #$00
$E4D0:  C9 00     CMP #$00
$E4D2:  C9 00     CMP #$00
$E4D4:  C9 00     CMP #$00
$E4D6:  C9 00     CMP #$00
$E4D8:  C9 00     CMP #$00
$E4DA:  C9 00     CMP #$00
$E4DC:  C9 00     CMP #$00
$E4DE:  C9 00     CMP #$00
$E4E0:  C9 00     CMP #$00
$E4E2:  C9 00     CMP #$00
$E4E4:  C9 00     CMP #$00
$E4E6:  C9 00     CMP #$00
$E4E8:  C9 FF     CMP #$FF
$E4EA:  E9 00     SBC #$00
$E4EC:  C9 00     CMP #$00
$E4EE:  86 02     STX $02
$E4F0:  D0 C6     BNE $E4B8
$E4F2:  A9 08     LDA #$08
$E4F4:  88        DEY
$E4F5:  86 03     STX $03
$E4F7:  8E 02 00  STX $0002
$E4FA:  F0 04     BEQ $E500
$E4FC:  EA        NOP
$E4FD:  4C EE CC  JMP $CCEE
$E500:  4C B7 C9  JMP $C9B7
$E503:  56 01     LSR $01,X
$E505:  CA        DEX
$E506:  16 04     ASL $04,X
$E508:  EA        NOP
$E509:  8E 03 00  STX $0003
$E50C:  8E 02 00  STX $0002
$E50F:  EA        NOP
$E510:  88        DEY
$E511:  D0 03     BNE $E516
$E513:  4C B8 C9  JMP $C9B8
$E516:  86 00     STX $00
$E518:  C9 00     CMP #$00
$E51A:  C9 00     CMP #$00
$E51C:  C9 00     CMP #$00
$E51E:  C9 00     CMP #$00
$E520:  C9 00     CMP #$00
$E522:  C9 00     CMP #$00
$E524:  C9 00     CMP #$00
$E526:  C9 00     CMP #$00
$E528:  C9 00     CMP #$00
$E52A:  C9 00     CMP #$00
$E52C:  C9 00     CMP #$00
$E52E:  C9 00     CMP #$00
$E530:  C9 00     CMP #$00
$E532:  C9 00     CMP #$00
$E534:  C9 00     CMP #$00
$E536:  C9 00     CMP #$00
$E538:  C9 FF     CMP #$FF
$E53A:  E9 00     SBC #$00
$E53C:  C9 00     CMP #$00
$E53E:  86 02     STX $02
$E540:  D0 C6     BNE $E508
$E542:  A9 08     LDA #$08
$E544:  88        DEY
$E545:  86 03     STX $03
$E547:  8E 02 00  STX $0002
$E54A:  F0 04     BEQ $E550
$E54C:  EA        NOP
$E54D:  4C 3E CD  JMP $CD3E
$E550:  4C B5 C9  JMP $C9B5
$E553:  3A        .BYTE $3A
$E554:  0C        .BYTE $0C
$E555:  0E 4F 7A  ASL $7A4F
$E558:  EA        NOP
$E559:  8E 03 00  STX $0003
$E55C:  8E 02 00  STX $0002
$E55F:  EA        NOP
$E560:  88        DEY
$E561:  D0 03     BNE $E566
$E563:  4C B8 C9  JMP $C9B8
$E566:  86 00     STX $00
$E568:  C9 00     CMP #$00
$E56A:  C9 00     CMP #$00
$E56C:  C9 00     CMP #$00
$E56E:  C9 00     CMP #$00
$E570:  C9 00     CMP #$00
$E572:  C9 00     CMP #$00
$E574:  C9 00     CMP #$00
$E576:  C9 00     CMP #$00
$E578:  C9 00     CMP #$00
$E57A:  C9 00     CMP #$00
$E57C:  C9 00     CMP #$00
$E57E:  C9 00     CMP #$00
$E580:  C9 00     CMP #$00
$E582:  C9 00     CMP #$00
$E584:  C9 00     CMP #$00
$E586:  C9 00     CMP #$00
$E588:  C9 FF     CMP #$FF
$E58A:  E9 00     SBC #$00
$E58C:  C9 00     CMP #$00
$E58E:  86 02     STX $02
$E590:  D0 C6     BNE $E558
$E592:  A9 08     LDA #$08
$E594:  88        DEY
$E595:  86 03     STX $03
$E597:  8E 02 00  STX $0002
$E59A:  F0 04     BEQ $E5A0
$E59C:  EA        NOP
$E59D:  4C 8E CD  JMP $CD8E
$E5A0:  4C B5 C9  JMP $C9B5
$E5A3:  4F        .BYTE $4F
$E5A4:  78        SEI
$E5A5:  FE 02 C2  INC $C202,X
$E5A8:  EA        NOP
$E5A9:  8E 03 00  STX $0003
$E5AC:  8E 02 00  STX $0002
$E5AF:  EA        NOP
$E5B0:  88        DEY
$E5B1:  D0 03     BNE $E5B6
$E5B3:  4C B8 C9  JMP $C9B8
$E5B6:  86 00     STX $00
$E5B8:  C9 00     CMP #$00
$E5BA:  C9 00     CMP #$00
$E5BC:  C9 00     CMP #$00
$E5BE:  C9 00     CMP #$00
$E5C0:  C9 00     CMP #$00
$E5C2:  C9 00     CMP #$00
$E5C4:  C9 00     CMP #$00
$E5C6:  C9 00     CMP #$00
$E5C8:  C9 00     CMP #$00
$E5CA:  C9 00     CMP #$00
$E5CC:  C9 00     CMP #$00
$E5CE:  C9 00     CMP #$00
$E5D0:  C9 00     CMP #$00
$E5D2:  C9 00     CMP #$00
$E5D4:  C9 00     CMP #$00
$E5D6:  C9 00     CMP #$00
$E5D8:  C9 FF     CMP #$FF
$E5DA:  E9 00     SBC #$00
$E5DC:  C9 00     CMP #$00
$E5DE:  86 02     STX $02
$E5E0:  D0 C6     BNE $E5A8
$E5E2:  A9 08     LDA #$08
$E5E4:  88        DEY
$E5E5:  86 03     STX $03
$E5E7:  8E 02 00  STX $0002
$E5EA:  F0 04     BEQ $E5F0
$E5EC:  EA        NOP
$E5ED:  4C DE CD  JMP $CDDE
$E5F0:  4C B5 C9  JMP $C9B5
$E5F3:  02        .BYTE $02
$E5F4:  CA        DEX
$E5F5:  FD 04 CD  SBC $CD04,X
$E5F8:  27        .BYTE $27
$E5F9:  EA        NOP
$E5FA:  86 03     STX $03
$E5FC:  8E 02 00  STX $0002
$E5FF:  EA        NOP
$E600:  88        DEY
$E601:  D0 03     BNE $E606
$E603:  4C B8 C9  JMP $C9B8
$E606:  86 00     STX $00
$E608:  C9 00     CMP #$00
$E60A:  C9 00     CMP #$00
$E60C:  C9 00     CMP #$00
$E60E:  C9 00     CMP #$00
$E610:  C9 00     CMP #$00
$E612:  C9 00     CMP #$00
$E614:  C9 00     CMP #$00
$E616:  C9 00     CMP #$00
$E618:  C9 00     CMP #$00
$E61A:  C9 00     CMP #$00
$E61C:  C9 00     CMP #$00
$E61E:  C9 00     CMP #$00
$E620:  C9 00     CMP #$00
$E622:  C9 00     CMP #$00
$E624:  C9 00     CMP #$00
$E626:  C9 00     CMP #$00
$E628:  C9 FF     CMP #$FF
$E62A:  E9 00     SBC #$00
$E62C:  C9 00     CMP #$00
$E62E:  86 02     STX $02
$E630:  D0 C7     BNE $E5F9
$E632:  A9 08     LDA #$08
$E634:  88        DEY
$E635:  86 03     STX $03
$E637:  8E 02 00  STX $0002
$E63A:  F0 04     BEQ $E640
$E63C:  EA        NOP
$E63D:  4C 2E CE  JMP $CE2E
$E640:  4C B5 C9  JMP $C9B5
$E643:  99 02 0E  STA $0E02,Y
$E646:  01 21     ORA ($21,X)
$E648:  EA        NOP
$E649:  8E 03 00  STX $0003
$E64C:  8E 02 00  STX $0002
$E64F:  88        DEY
$E650:  EA        NOP
$E651:  D0 03     BNE $E656
$E653:  4C B8 C9  JMP $C9B8
$E656:  86 00     STX $00
$E658:  C9 00     CMP #$00
$E65A:  C9 00     CMP #$00
$E65C:  C9 00     CMP #$00
$E65E:  C9 00     CMP #$00
$E660:  C9 00     CMP #$00
$E662:  C9 00     CMP #$00
$E664:  C9 00     CMP #$00
$E666:  C9 00     CMP #$00
$E668:  C9 00     CMP #$00
$E66A:  C9 00     CMP #$00
$E66C:  C9 00     CMP #$00
$E66E:  C9 00     CMP #$00
$E670:  C9 00     CMP #$00
$E672:  C9 00     CMP #$00
$E674:  C9 00     CMP #$00
$E676:  C9 00     CMP #$00
$E678:  C9 FF     CMP #$FF
$E67A:  E9 00     SBC #$00
$E67C:  C9 00     CMP #$00
$E67E:  86 02     STX $02
$E680:  D0 C6     BNE $E648
$E682:  A9 08     LDA #$08
$E684:  88        DEY
$E685:  86 03     STX $03
$E687:  8E 02 00  STX $0002
$E68A:  F0 04     BEQ $E690
$E68C:  EA        NOP
$E68D:  4C 7E CE  JMP $CE7E
$E690:  4C B5 C9  JMP $C9B5
$E693:  05 0D     ORA $0D
$E695:  51 CD     EOR ($CD),Y
$E697:  1C        .BYTE $1C
$E698:  EA        NOP
$E699:  8E 03 00  STX $0003
$E69C:  8E 02 00  STX $0002
$E69F:  88        DEY
$E6A0:  EA        NOP
$E6A1:  D0 03     BNE $E6A6
$E6A3:  4C B8 C9  JMP $C9B8
$E6A6:  86 00     STX $00
$E6A8:  C9 00     CMP #$00
$E6AA:  C9 00     CMP #$00
$E6AC:  C9 00     CMP #$00
$E6AE:  C9 00     CMP #$00
$E6B0:  C9 00     CMP #$00
$E6B2:  C9 00     CMP #$00
$E6B4:  C9 00     CMP #$00
$E6B6:  C9 00     CMP #$00
$E6B8:  C9 00     CMP #$00
$E6BA:  C9 00     CMP #$00
$E6BC:  C9 00     CMP #$00
$E6BE:  C9 00     CMP #$00
$E6C0:  C9 00     CMP #$00
$E6C2:  C9 00     CMP #$00
$E6C4:  C9 00     CMP #$00
$E6C6:  C9 00     CMP #$00
$E6C8:  C9 FF     CMP #$FF
$E6CA:  E9 00     SBC #$00
$E6CC:  C9 00     CMP #$00
$E6CE:  86 02     STX $02
$E6D0:  D0 C6     BNE $E698
$E6D2:  A9 08     LDA #$08
$E6D4:  88        DEY
$E6D5:  86 03     STX $03
$E6D7:  8E 02 00  STX $0002
$E6DA:  F0 04     BEQ $E6E0
$E6DC:  EA        NOP
$E6DD:  4C CE CE  JMP $CECE
$E6E0:  4C B5 C9  JMP $C9B5
$E6E3:  CD D2 01  CMP $01D2
$E6E6:  F6 C0     INC $C0,X
$E6E8:  C3        .BYTE $C3
$E6E9:  EA        NOP
$E6EA:  86 03     STX $03
$E6EC:  8E 02 00  STX $0002
$E6EF:  88        DEY
$E6F0:  EA        NOP
$E6F1:  D0 03     BNE $E6F6
$E6F3:  4C B8 C9  JMP $C9B8
$E6F6:  86 00     STX $00
$E6F8:  C9 00     CMP #$00
$E6FA:  C9 00     CMP #$00
$E6FC:  C9 00     CMP #$00
$E6FE:  C9 00     CMP #$00
$E700:  C9 00     CMP #$00
$E702:  C9 00     CMP #$00
$E704:  C9 00     CMP #$00
$E706:  C9 00     CMP #$00
$E708:  C9 00     CMP #$00
$E70A:  C9 00     CMP #$00
$E70C:  C9 00     CMP #$00
$E70E:  C9 00     CMP #$00
$E710:  C9 00     CMP #$00
$E712:  C9 00     CMP #$00
$E714:  C9 00     CMP #$00
$E716:  C9 00     CMP #$00
$E718:  C9 FF     CMP #$FF
$E71A:  E9 00     SBC #$00
$E71C:  C9 00     CMP #$00
$E71E:  86 02     STX $02
$E720:  D0 C7     BNE $E6E9
$E722:  A9 08     LDA #$08
$E724:  88        DEY
$E725:  86 03     STX $03
$E727:  8E 02 00  STX $0002
$E72A:  F0 04     BEQ $E730
$E72C:  EA        NOP
$E72D:  4C 1E CF  JMP $CF1E
$E730:  4C B5 C9  JMP $C9B5
$E733:  ED CD F4  SBC $F4CD
$E736:  01 7B     ORA ($7B,X)
$E738:  EA        NOP
$E739:  8E 03 00  STX $0003
$E73C:  8E 02 00  STX $0002
$E73F:  88        DEY
$E740:  EA        NOP
$E741:  D0 03     BNE $E746
$E743:  4C B8 C9  JMP $C9B8
$E746:  86 00     STX $00
$E748:  C9 00     CMP #$00
$E74A:  C9 00     CMP #$00
$E74C:  C9 00     CMP #$00
$E74E:  C9 00     CMP #$00
$E750:  C9 00     CMP #$00
$E752:  C9 00     CMP #$00
$E754:  C9 00     CMP #$00
$E756:  C9 00     CMP #$00
$E758:  C9 00     CMP #$00
$E75A:  C9 00     CMP #$00
$E75C:  C9 00     CMP #$00
$E75E:  C9 00     CMP #$00
$E760:  C9 00     CMP #$00
$E762:  C9 00     CMP #$00
$E764:  C9 00     CMP #$00
$E766:  C9 00     CMP #$00
$E768:  C9 FF     CMP #$FF
$E76A:  E9 00     SBC #$00
$E76C:  C9 00     CMP #$00
$E76E:  86 02     STX $02
$E770:  D0 C6     BNE $E738
$E772:  A9 08     LDA #$08
$E774:  88        DEY
$E775:  86 03     STX $03
$E777:  8E 02 00  STX $0002
$E77A:  F0 04     BEQ $E780
$E77C:  EA        NOP
$E77D:  4C 6E CF  JMP $CF6E
$E780:  4C B5 C9  JMP $C9B5
$E783:  0B        .BYTE $0B
$E784:  3E EB C3  ROL $C3EB,X
$E787:  F4        .BYTE $F4
$E788:  EA        NOP
$E789:  8E 03 00  STX $0003
$E78C:  8E 02 00  STX $0002
$E78F:  88        DEY
$E790:  EA        NOP
$E791:  D0 03     BNE $E796
$E793:  4C B8 C9  JMP $C9B8
$E796:  86 00     STX $00
$E798:  C9 00     CMP #$00
$E79A:  C9 00     CMP #$00
$E79C:  C9 00     CMP #$00
$E79E:  C9 00     CMP #$00
$E7A0:  C9 00     CMP #$00
$E7A2:  C9 00     CMP #$00
$E7A4:  C9 00     CMP #$00
$E7A6:  C9 00     CMP #$00
$E7A8:  C9 00     CMP #$00
$E7AA:  C9 00     CMP #$00
$E7AC:  C9 00     CMP #$00
$E7AE:  C9 00     CMP #$00
$E7B0:  C9 00     CMP #$00
$E7B2:  C9 00     CMP #$00
$E7B4:  C9 00     CMP #$00
$E7B6:  C9 00     CMP #$00
$E7B8:  C9 FF     CMP #$FF
$E7BA:  E9 00     SBC #$00
$E7BC:  C9 00     CMP #$00
$E7BE:  86 02     STX $02
$E7C0:  D0 C6     BNE $E788
$E7C2:  A9 08     LDA #$08
$E7C4:  88        DEY
$E7C5:  86 03     STX $03
$E7C7:  8E 02 00  STX $0002
$E7CA:  F0 04     BEQ $E7D0
$E7CC:  EA        NOP
$E7CD:  4C FE CB  JMP $CBFE
$E7D0:  4C B5 C9  JMP $C9B5
$E7D3:  EA        NOP
$E7D4:  EA        NOP
$E7D5:  EA        NOP
$E7D6:  38        SEC
$E7D7:  A9 03     LDA #$03
$E7D9:  BA        TSX
$E7DA:  8E 03 00  STX $0003
$E7DD:  8C 02 00  STY $0002
$E7E0:  86 02     STX $02
$E7E2:  A2 08     LDX #$08
$E7E4:  CA        DEX
$E7E5:  D0 FD     BNE $E7E4
$E7E7:  F0 00     BEQ $E7E9
$E7E9:  BA        TSX
$E7EA:  E9 01     SBC #$01
$E7EC:  D0 EB     BNE $E7D9
$E7EE:  4C 97 D5  JMP $D597
$E7F1:  A2 03     LDX #$03
$E7F3:  CA        DEX
$E7F4:  D0 FD     BNE $E7F3
$E7F6:  EA        NOP
$E7F7:  EA        NOP
$E7F8:  EA        NOP
$E7F9:  4C 11 C1  JMP $C111
$E7FC:  64        .BYTE $64
$E7FD:  66 6E     ROR $6E
$E7FF:  40        RTI
$E800:  8A        TXA
$E801:  AA        TAX
$E802:  40        RTI
$E803:  9E        .BYTE $9E
$E804:  8A        TXA
$E805:  4C CA 15  JMP $15CA
$E808:  00        BRK
$E809:  4C D8 C2  JMP $C2D8
$E80C:  4C 7D D3  JMP $D37D
$E80F:  4C B0 C2  JMP $C2B0
$E812:  4C C3 C2  JMP $C2C3
$E815:  4C D8 C2  JMP $C2D8
$E818:  4C 00 C4  JMP $C400
$E81B:  4C CF C9  JMP $C9CF
$E81E:  4C E2 C9  JMP $C9E2
$E821:  4C 00 C3  JMP $C300 ; VIDEX_80COL_ENTRY
$E824:  4C 00 C3  JMP $C300 ; VIDEX_80COL_ENTRY
$E827:  4A        LSR
$E828:  90 4B     BCC $E875
$E82A:  AD EC 43  LDA $43EC
$E82D:  29 FD     AND #$FD ('}')
$E82F:  8D EC 43  STA $43EC
$E832:  AD F6 53  LDA $53F6
$E835:  30 47     BMI $E87E
$E837:  2C E9 43  BIT $43E9
$E83A:  50 3E     BVC $E87A
$E83C:  AE F7 43  LDX $43F7
$E83F:  BD E8 53  LDA $53E8,X
$E842:  4A        LSR
$E843:  8D FB 53  STA $53FB
$E846:  AD FD 43  LDA $43FD
$E849:  EA        NOP
$E84A:  BA        TSX
$E84B:  86 03     STX $03
$E84D:  8E 02 00  STX $0002
$E850:  B0 04     BCS $E856
$E852:  29 FE     AND #$FE ('~')
$E854:  90 03     BCC $E859
$E856:  09 01     ORA #$01
$E858:  18        CLC
$E859:  8D FD 43  STA $43FD
$E85C:  AE F7 43  LDX $43F7
$E85F:  BD E9 53  LDA $53E9,X
$E862:  F0 58     BEQ $E8BC
$E864:  FD E8 53  SBC $53E8,X
$E867:  F0 57     BEQ $E8C0
$E869:  8D ED 43  STA $43ED
$E86C:  A9 00     LDA #$00
$E86E:  8D FB 43  STA $43FB
$E871:  EA        NOP
$E872:  4C 23 C9  JMP $C923
$E875:  A2 07     LDX #$07
$E877:  EA        NOP
$E878:  D0 08     BNE $E882
$E87A:  A2 03     LDX #$03
$E87C:  D0 04     BNE $E882
$E87E:  A2 04     LDX #$04
$E880:  EA        NOP
$E881:  EA        NOP
$E882:  CA        DEX
$E883:  D0 FD     BNE $E882
$E885:  BA        TSX
$E886:  86 03     STX $03
$E888:  8E 02 00  STX $0002
$E88B:  A2 07     LDX #$07
$E88D:  D0 33     BNE $E8C2
$E88F:  86 03     STX $03
$E891:  8E 02 00  STX $0002
$E894:  AD EC 43  LDA $43EC
$E897:  4A        LSR
$E898:  90 8D     BCC $E827
$E89A:  18        CLC
$E89B:  2A        ROL
$E89C:  8D EC 43  STA $43EC
$E89F:  AD F7 43  LDA $43F7
$E8A2:  C9 17     CMP #$17
$E8A4:  F0 40     BEQ $E8E6
$E8A6:  C9 19     CMP #$19
$E8A8:  F0 2A     BEQ $E8D4
$E8AA:  C9 1A     CMP #$1A
$E8AC:  F0 1A     BEQ $E8C8
$E8AE:  AD FE 43  LDA $43FE
$E8B1:  49 80     EOR #$80
$E8B3:  8D FE 43  STA $43FE
$E8B6:  EA        NOP
$E8B7:  EA        NOP
$E8B8:  A2 01     LDX #$01
$E8BA:  D0 C6     BNE $E882
$E8BC:  A2 02     LDX #$02
$E8BE:  D0 03     BNE $E8C3
$E8C0:  A2 02     LDX #$02
$E8C2:  CA        DEX
$E8C3:  D0 FD     BNE $E8C2
$E8C5:  4C 23 C9  JMP $C923
$E8C8:  AD F3 43  LDA $43F3
$E8CB:  49 80     EOR #$80
$E8CD:  8D F3 43  STA $43F3
$E8D0:  A2 01     LDX #$01
$E8D2:  D0 0C     BNE $E8E0
$E8D4:  AD E9 43  LDA $43E9
$E8D7:  29 40     AND #$40 ('@')
$E8D9:  D0 07     BNE $E8E2
$E8DB:  8D 00 08  STA $0800
$E8DE:  A2 02     LDX #$02
$E8E0:  D0 A0     BNE $E882
$E8E2:  A2 02     LDX #$02
$E8E4:  D0 FA     BNE $E8E0
$E8E6:  AD EC 43  LDA $43EC
$E8E9:  69 03     ADC #$03
$E8EB:  29 EF     AND #$EF ('o')
$E8ED:  8D EC 43  STA $43EC
$E8F0:  A9 00     LDA #$00
$E8F2:  8D FA 53  STA $53FA
$E8F5:  8D E8 53  STA $53E8
$E8F8:  8D E9 53  STA $53E9
$E8FB:  8D EA 53  STA $53EA
$E8FE:  BA        TSX
$E8FF:  86 03     STX $03
$E901:  8C 02 00  STY $0002
$E904:  8D EB 53  STA $53EB
$E907:  8D EC 53  STA $53EC
$E90A:  8D ED 53  STA $53ED
$E90D:  8D EE 53  STA $53EE
$E910:  8D EF 53  STA $53EF
$E913:  8D F0 53  STA $53F0
$E916:  8D F1 53  STA $53F1
$E919:  8D F2 53  STA $53F2
$E91C:  8D F3 53  STA $53F3
$E91F:  8D F4 53  STA $53F4
$E922:  EA        NOP
$E923:  A9 40     LDA #$40 ('@')
$E925:  8D 00 0C  STA $0C00
$E928:  BA        TSX
$E929:  8A        TXA
$E92A:  29 F7     AND #$F7 ('w')
$E92C:  AA        TAX
$E92D:  8E 07 00  STX $0007
$E930:  8E 02 00  STX $0002
$E933:  EA        NOP
$E934:  A9 08     LDA #$08
$E936:  4C BE CF  JMP $CFBE
$E939:  37        .BYTE $37
$E93A:  34        .BYTE $34
$E93B:  2C 31 35  BIT $3531
$E93E:  38        SEC
$E93F:  32        .BYTE $32
$E940:  30 39     BMI $E97B
$E942:  36 2E     ROL $2E,X
$E944:  33        .BYTE $33
$E945:  2D 2B 2A  AND $2A2B
$E948:  2F        .BYTE $2F
$E949:  DC        .BYTE $DC
$E94A:  DD 20 DA  CMP $DA20,X
$E94D:  8D 1A 18  STA $181A
$E950:  19 D0 C0  ORA $C0D0,Y
$E953:  AF        .BYTE $AF
$E954:  C1 BA     CMP ($BA,X)
$E956:  AD BB B0  LDA $B0BB
$E959:  D9 D5 CE  CMP $CED5,Y
$E95C:  CD CA B7  CMP $B7CA
$E95F:  C8        INY
$E960:  B6 D2     LDX $D2,Y
$E962:  D4        .BYTE $D4
$E963:  D6 C2     DEC $C2,X
$E965:  C7        .BYTE $C7
$E966:  B5 C6     LDA $C6,X
$E968:  B4 D7     LDY $D7,X
$E96A:  C5 D8     CMP $D8
$E96C:  C3        .BYTE $C3
$E96D:  C4 B3     CPY $B3
$E96F:  D3        .BYTE $D3
$E970:  B2        .BYTE $B2
$E971:  DB        .BYTE $DB
$E972:  88        DEY
$E973:  7F        .BYTE $7F
$E974:  17        .BYTE $17
$E975:  88        DEY
$E976:  95 8D     STA $8D,X
$E978:  DE 93 85  DEC $8593,X
$E97B:  08        PHP
$E97C:  0A        ASL
$E97D:  0B        .BYTE $0B
$E97E:  98        TYA
$E97F:  09 84     ORA #$84
$E981:  03        .BYTE $03
$E982:  01 07     ORA ($07,X)
$E984:  05 04     ORA $04
$E986:  02        .BYTE $02
$E987:  06 00     ASL $00
$E989:  89        .BYTE $89
$E98A:  D1 1F     CMP ($1F),Y
$E98C:  1F        .BYTE $1F
$E98D:  1F        .BYTE $1F
$E98E:  B1 1F     LDA ($1F),Y
$E990:  9B        .BYTE $9B
$E991:  00        BRK
$E992:  30 60     BMI $E9F4
$E994:  60        RTS
$E995:  80        .BYTE $80
$E996:  B0 E0     BCS $E978
$E998:  E0 C9     CPX #$C9 ('I')
$E99A:  CF        .BYTE $CF
$E99B:  AC AE CC  LDY $CCAE
$E99E:  B9 CB B8  LDA $B8CB,Y
$E9A1:  09 0C     ORA #$0C
$E9A3:  0F        .BYTE $0F
$E9A4:  12        .BYTE $12
$E9A5:  21 21     AND ($21,X)
$E9A7:  21 21     AND ($21,X)
$E9A9:  15 18     ORA $18,X
$E9AB:  1B        .BYTE $1B
$E9AC:  1E 24 24  ASL $2424,X
$E9AF:  24 24     BIT $24
$E9B1:  A2 08     LDX #$08
$E9B3:  D0 0B     BNE $E9C0
$E9B5:  F0 01     BEQ $E9B8
$E9B7:  EA        NOP
$E9B8:  EA        NOP
$E9B9:  9A        TXS
$E9BA:  8A        TXA
$E9BB:  A8        TAY
$E9BC:  A2 06     LDX #$06
$E9BE:  EA        NOP
$E9BF:  CA        DEX
$E9C0:  D0 FD     BNE $E9BF
$E9C2:  BA        TSX
$E9C3:  EA        NOP
$E9C4:  4C 8F C8  JMP $C88F
$E9C7:  38        SEC
$E9C8:  6A        ROR
$E9C9:  9D 8B 42  STA $428B,X
$E9CC:  4C BA D2  JMP $D2BA
$E9CF:  A9 8E     LDA #$8E
$E9D1:  EA        NOP
$E9D2:  EA        NOP
$E9D3:  EA        NOP
$E9D4:  EA        NOP
$E9D5:  EA        NOP
$E9D6:  EA        NOP
$E9D7:  EA        NOP
$E9D8:  AA        TAX
$E9D9:  A8        TAY
$E9DA:  C8        INY
$E9DB:  A9 C0     LDA #$C0 ('@')
$E9DD:  D0 00     BNE $E9DF
$E9DF:  4C 74 C0  JMP $C074
$E9E2:  EA        NOP
$E9E3:  EA        NOP
$E9E4:  EA        NOP
$E9E5:  4D E8 43  EOR $43E8
$E9E8:  AA        TAX
$E9E9:  9A        TXS
$E9EA:  A9 EF     LDA #$EF ('o')
$E9EC:  A8        TAY
$E9ED:  29 FE     AND #$FE ('~')
$E9EF:  AA        TAX
$E9F0:  A9 C0     LDA #$C0 ('@')
$E9F2:  D0 00     BNE $E9F4
$E9F4:  4C 74 C1  JMP $C174
$E9F7:  CA        DEX
$E9F8:  06 09     ASL $09
$E9FA:  21 2B     AND ($2B,X)
$E9FC:  09 CD     ORA #$CD ('M')
$E9FE:  A4 0E     LDY $0E
$EA00:  AD FD 43  LDA $43FD
$EA03:  30 06     BMI $EA0B
$EA05:  CE FB 43  DEC $43FB
$EA08:  4C E1 D0  JMP $D0E1
$EA0B:  A2 04     LDX #$04
$EA0D:  CA        DEX
$EA0E:  D0 FD     BNE $EA0D
$EA10:  EA        NOP
$EA11:  4C 0B C1  JMP $C10B
$EA14:  4C A0 D1  JMP $D1A0
$EA17:  AD FB 43  LDA $43FB
$EA1A:  D0 E4     BNE $EA00
$EA1C:  AE F5 43  LDX $43F5
$EA1F:  BD 00 80  LDA $8000,X
$EA22:  49 FF     EOR #$FF
$EA24:  2D F6 43  AND $43F6
$EA27:  D0 EB     BNE $EA14
$EA29:  8D F6 43  STA $43F6
$EA2C:  A2 0C     LDX #$0C
$EA2E:  AD 00 80  LDA $8000
$EA31:  C9 FF     CMP #$FF
$EA33:  D0 6C     BNE $EAA1
$EA35:  AD 01 80  LDA $8001
$EA38:  C9 FF     CMP #$FF
$EA3A:  D0 69     BNE $EAA5
$EA3C:  8A        TXA
$EA3D:  EA        NOP
$EA3E:  BA        TSX
$EA3F:  8E 03 00  STX $0003
$EA42:  8C 02 00  STY $0002
$EA45:  86 02     STX $02
$EA47:  AA        TAX
$EA48:  AD 02 80  LDA $8002
$EA4B:  C9 FF     CMP #$FF
$EA4D:  D0 66     BNE $EAB5
$EA4F:  AD 03 80  LDA $8003
$EA52:  C9 FF     CMP #$FF
$EA54:  D0 63     BNE $EAB9
$EA56:  AD 04 80  LDA $8004
$EA59:  C9 FF     CMP #$FF
$EA5B:  D0 60     BNE $EABD
$EA5D:  AD 05 80  LDA $8005
$EA60:  C9 FF     CMP #$FF
$EA62:  D0 5D     BNE $EAC1
$EA64:  AD 06 80  LDA $8006
$EA67:  C9 FF     CMP #$FF
$EA69:  D0 5A     BNE $EAC5
$EA6B:  AD 07 80  LDA $8007
$EA6E:  C9 FF     CMP #$FF
$EA70:  8A        TXA
$EA71:  EA        NOP
$EA72:  BA        TSX
$EA73:  86 03     STX $03
$EA75:  8C 02 00  STY $0002
$EA78:  86 02     STX $02
$EA7A:  AA        TAX
$EA7B:  90 58     BCC $EAD5
$EA7D:  AD 08 80  LDA $8008
$EA80:  C9 FF     CMP #$FF
$EA82:  D0 55     BNE $EAD9
$EA84:  AD 09 80  LDA $8009
$EA87:  C9 FF     CMP #$FF
$EA89:  D0 52     BNE $EADD
$EA8B:  AD 0A 80  LDA $800A
$EA8E:  09 5C     ORA #$5C ('\')
$EA90:  C9 FF     CMP #$FF
$EA92:  D0 4E     BNE $EAE2
$EA94:  AD 0C 80  LDA $800C
$EA97:  C9 FF     CMP #$FF
$EA99:  D0 4D     BNE $EAE8
$EA9B:  A2 80     LDX #$80
$EA9D:  EA        NOP
$EA9E:  EA        NOP
$EA9F:  30 4D     BMI $EAEE
$EAA1:  CA        DEX
$EAA2:  EA        NOP
$EAA3:  EA        NOP
$EAA4:  EA        NOP
$EAA5:  EA        NOP
$EAA6:  8A        TXA
$EAA7:  BA        TSX
$EAA8:  86 03     STX $03
$EAAA:  8C 02 00  STY $0002
$EAAD:  86 02     STX $02
$EAAF:  AA        TAX
$EAB0:  CA        DEX
$EAB1:  EA        NOP
$EAB2:  EA        NOP
$EAB3:  D0 00     BNE $EAB5
$EAB5:  CA        DEX
$EAB6:  EA        NOP
$EAB7:  EA        NOP
$EAB8:  EA        NOP
$EAB9:  CA        DEX
$EABA:  EA        NOP
$EABB:  EA        NOP
$EABC:  EA        NOP
$EABD:  CA        DEX
$EABE:  EA        NOP
$EABF:  EA        NOP
$EAC0:  EA        NOP
$EAC1:  CA        DEX
$EAC2:  EA        NOP
$EAC3:  EA        NOP
$EAC4:  EA        NOP
$EAC5:  CA        DEX
$EAC6:  EA        NOP
$EAC7:  EA        NOP
$EAC8:  8A        TXA
$EAC9:  BA        TSX
$EACA:  8E 03 00  STX $0003
$EACD:  8C 02 00  STY $0002
$EAD0:  86 02     STX $02
$EAD2:  AA        TAX
$EAD3:  D0 00     BNE $EAD5
$EAD5:  CA        DEX
$EAD6:  EA        NOP
$EAD7:  EA        NOP
$EAD8:  EA        NOP
$EAD9:  CA        DEX
$EADA:  EA        NOP
$EADB:  EA        NOP
$EADC:  EA        NOP
$EADD:  CA        DEX
$EADE:  EA        NOP
$EADF:  EA        NOP
$EAE0:  EA        NOP
$EAE1:  EA        NOP
$EAE2:  CA        DEX
$EAE3:  CA        DEX
$EAE4:  E0 0A     CPX #$0A
$EAE6:  F0 15     BEQ $EAFD
$EAE8:  BD 00 80  LDA $8000,X
$EAEB:  8D EA 43  STA $43EA
$EAEE:  8E F5 43  STX $43F5
$EAF1:  BA        TSX
$EAF2:  8E 03 00  STX $0003
$EAF5:  8C 02 00  STY $0002
$EAF8:  86 02     STX $02
$EAFA:  4C E0 C3  JMP $C3E0
$EAFD:  F0 EC     BEQ $EAEB
$EAFF:  F1 AD     SBC ($AD),Y
$EB01:  FD 43 30  SBC $3043,X
$EB04:  32        .BYTE $32
$EB05:  AE FB 53  LDX $53FB
$EB08:  4A        LSR
$EB09:  90 23     BCC $EB2E
$EB0B:  CE FD 43  DEC $43FD
$EB0E:  BD C0 43  LDA $43C0,X
$EB11:  EE FB 53  INC $53FB
$EB14:  8D 00 04  STA $0400
$EB17:  8D EE 43  STA $43EE
$EB1A:  BA        TSX
$EB1B:  86 03     STX $03
$EB1D:  8C 02 00  STY $0002
$EB20:  86 02     STX $02
$EB22:  CE ED 43  DEC $43ED
$EB25:  EA        NOP
$EB26:  A2 05     LDX #$05
$EB28:  A9 03     LDA #$03
$EB2A:  38        SEC
$EB2B:  4C E4 C7  JMP $C7E4
$EB2E:  EE FD 43  INC $43FD
$EB31:  BD C0 53  LDA $53C0,X
$EB34:  18        CLC
$EB35:  90 DD     BCC $EB14
$EB37:  A2 06     LDX #$06
$EB39:  CA        DEX
$EB3A:  D0 FD     BNE $EB39
$EB3C:  BA        TSX
$EB3D:  86 03     STX $03
$EB3F:  8C 02 00  STY $0002
$EB42:  86 02     STX $02
$EB44:  D0 00     BNE $EB46
$EB46:  4C 25 CB  JMP $CB25
$EB49:  AD ED 43  LDA $43ED
$EB4C:  D0 B2     BNE $EB00
$EB4E:  AE F5 43  LDX $43F5
$EB51:  30 40     BMI $EB93
$EB53:  BD 00 80  LDA $8000,X
$EB56:  4D EA 43  EOR $43EA
$EB59:  D0 3D     BNE $EB98
$EB5B:  8A        TXA
$EB5C:  09 80     ORA #$80
$EB5E:  8D F5 43  STA $43F5
$EB61:  EA        NOP
$EB62:  0A        ASL
$EB63:  0A        ASL
$EB64:  0A        ASL
$EB65:  A2 55     LDX #$55 ('U')
$EB67:  8E EB 43  STX $43EB
$EB6A:  BA        TSX
$EB6B:  8E 03 00  STX $0003
$EB6E:  8C 02 00  STY $0002
$EB71:  86 02     STX $02
$EB73:  AA        TAX
$EB74:  AD EA 43  LDA $43EA
$EB77:  49 FF     EOR #$FF
$EB79:  8D F6 43  STA $43F6
$EB7C:  2A        ROL
$EB7D:  B0 3A     BCS $EBB9
$EB7F:  2A        ROL
$EB80:  B0 39     BCS $EBBB
$EB82:  2A        ROL
$EB83:  B0 38     BCS $EBBD
$EB85:  2A        ROL
$EB86:  B0 37     BCS $EBBF
$EB88:  2A        ROL
$EB89:  B0 36     BCS $EBC1
$EB8B:  2A        ROL
$EB8C:  B0 35     BCS $EBC3
$EB8E:  2A        ROL
$EB8F:  B0 34     BCS $EBC5
$EB91:  90 33     BCC $EBC6
$EB93:  EA        NOP
$EB94:  EA        NOP
$EB95:  EA        NOP
$EB96:  EA        NOP
$EB97:  EA        NOP
$EB98:  E0 0A     CPX #$0A
$EB9A:  D0 07     BNE $EBA3
$EB9C:  29 A3     AND #$A3 ('#')
$EB9E:  F0 05     BEQ $EBA5
$EBA0:  4C D3 C7  JMP $C7D3
$EBA3:  D0 FB     BNE $EBA0
$EBA5:  A9 8A     LDA #$8A
$EBA7:  8D F5 43  STA $43F5
$EBAA:  A9 50     LDA #$50 ('P')
$EBAC:  8D EB 43  STA $43EB
$EBAF:  BA        TSX
$EBB0:  8E 03 00  STX $0003
$EBB3:  8E 02 00  STX $0002
$EBB6:  4C 73 CB  JMP $CB73
$EBB9:  E8        INX
$EBBA:  EA        NOP
$EBBB:  E8        INX
$EBBC:  EA        NOP
$EBBD:  E8        INX
$EBBE:  EA        NOP
$EBBF:  E8        INX
$EBC0:  EA        NOP
$EBC1:  E8        INX
$EBC2:  EA        NOP
$EBC3:  E8        INX
$EBC4:  EA        NOP
$EBC5:  E8        INX
$EBC6:  BD 39 C9  LDA $C939,X
$EBC9:  4C 19 D0  JMP $D019
$EBCC:  A2 03     LDX #$03
$EBCE:  CA        DEX
$EBCF:  D0 FD     BNE $EBCE
$EBD1:  BA        TSX
$EBD2:  86 03     STX $03
$EBD4:  8C 02 00  STY $0002
$EBD7:  86 02     STX $02
$EBD9:  A2 0A     LDX #$0A
$EBDB:  CA        DEX
$EBDC:  D0 FD     BNE $EBDB
$EBDE:  BA        TSX
$EBDF:  8E 03 00  STX $0003
$EBE2:  8C 02 00  STY $0002
$EBE5:  86 02     STX $02
$EBE7:  EA        NOP
$EBE8:  EA        NOP
$EBE9:  EA        NOP
$EBEA:  EA        NOP
$EBEB:  EA        NOP
$EBEC:  4C 6B C3  JMP $C36B
$EBEF:  FE ED EA  INC $EAED,X
$EBF2:  86 03     STX $03
$EBF4:  8E 02 00  STX $0002
$EBF7:  88        DEY
$EBF8:  EA        NOP
$EBF9:  D0 03     BNE $EBFE
$EBFB:  4C B8 C9  JMP $C9B8
$EBFE:  86 00     STX $00
$EC00:  C9 00     CMP #$00
$EC02:  C9 00     CMP #$00
$EC04:  C9 00     CMP #$00
$EC06:  C9 00     CMP #$00
$EC08:  C9 00     CMP #$00
$EC0A:  C9 00     CMP #$00
$EC0C:  C9 00     CMP #$00
$EC0E:  C9 00     CMP #$00
$EC10:  C9 00     CMP #$00
$EC12:  C9 00     CMP #$00
$EC14:  C9 00     CMP #$00
$EC16:  C9 00     CMP #$00
$EC18:  C9 00     CMP #$00
$EC1A:  C9 00     CMP #$00
$EC1C:  C9 00     CMP #$00
$EC1E:  C9 00     CMP #$00
$EC20:  C9 FF     CMP #$FF
$EC22:  E9 00     SBC #$00
$EC24:  C9 00     CMP #$00
$EC26:  86 02     STX $02
$EC28:  D0 C7     BNE $EBF1
$EC2A:  A9 08     LDA #$08
$EC2C:  88        DEY
$EC2D:  86 03     STX $03
$EC2F:  8E 02 00  STX $0002
$EC32:  F0 04     BEQ $EC38
$EC34:  EA        NOP
$EC35:  4C 26 C4  JMP $C426
$EC38:  4C B5 C9  JMP $C9B5
$EC3B:  FE 0C E6  INC $E60C,X
$EC3E:  10 CA     BPL $EC0A
$EC40:  EA        NOP
$EC41:  8E 03 00  STX $0003
$EC44:  8E 02 00  STX $0002
$EC47:  88        DEY
$EC48:  EA        NOP
$EC49:  D0 03     BNE $EC4E
$EC4B:  4C B8 C9  JMP $C9B8
$EC4E:  86 00     STX $00
$EC50:  C9 00     CMP #$00
$EC52:  C9 00     CMP #$00
$EC54:  C9 00     CMP #$00
$EC56:  C9 00     CMP #$00
$EC58:  C9 00     CMP #$00
$EC5A:  C9 00     CMP #$00
$EC5C:  C9 00     CMP #$00
$EC5E:  C9 00     CMP #$00
$EC60:  C9 00     CMP #$00
$EC62:  C9 00     CMP #$00
$EC64:  C9 00     CMP #$00
$EC66:  C9 00     CMP #$00
$EC68:  C9 00     CMP #$00
$EC6A:  C9 00     CMP #$00
$EC6C:  C9 00     CMP #$00
$EC6E:  C9 00     CMP #$00
$EC70:  C9 FF     CMP #$FF
$EC72:  E9 00     SBC #$00
$EC74:  C9 00     CMP #$00
$EC76:  86 02     STX $02
$EC78:  D0 C6     BNE $EC40
$EC7A:  A9 08     LDA #$08
$EC7C:  88        DEY
$EC7D:  86 03     STX $03
$EC7F:  8E 02 00  STX $0002
$EC82:  F0 04     BEQ $EC88
$EC84:  EA        NOP
$EC85:  4C 76 C4  JMP $C476
$EC88:  4C B5 C9  JMP $C9B5
$EC8B:  A5 09     LDA $09
$EC8D:  C3        .BYTE $C3
$EC8E:  23        .BYTE $23
$EC8F:  0B        .BYTE $0B
$EC90:  EA        NOP
$EC91:  8E 03 00  STX $0003
$EC94:  8E 02 00  STX $0002
$EC97:  88        DEY
$EC98:  EA        NOP
$EC99:  D0 03     BNE $EC9E
$EC9B:  4C B8 C9  JMP $C9B8
$EC9E:  86 00     STX $00
$ECA0:  C9 00     CMP #$00
$ECA2:  C9 00     CMP #$00
$ECA4:  C9 00     CMP #$00
$ECA6:  C9 00     CMP #$00
$ECA8:  C9 00     CMP #$00
$ECAA:  C9 00     CMP #$00
$ECAC:  C9 00     CMP #$00
$ECAE:  C9 00     CMP #$00
$ECB0:  C9 00     CMP #$00
$ECB2:  C9 00     CMP #$00
$ECB4:  C9 00     CMP #$00
$ECB6:  C9 00     CMP #$00
$ECB8:  C9 00     CMP #$00
$ECBA:  C9 00     CMP #$00
$ECBC:  C9 00     CMP #$00
$ECBE:  C9 00     CMP #$00
$ECC0:  C9 FF     CMP #$FF
$ECC2:  E9 00     SBC #$00
$ECC4:  C9 00     CMP #$00
$ECC6:  86 02     STX $02
$ECC8:  D0 C6     BNE $EC90
$ECCA:  A9 08     LDA #$08
$ECCC:  88        DEY
$ECCD:  86 03     STX $03
$ECCF:  8E 02 00  STX $0002
$ECD2:  F0 04     BEQ $ECD8
$ECD4:  EA        NOP
$ECD5:  4C C6 C4  JMP $C4C6
$ECD8:  4C B5 C9  JMP $C9B5
$ECDB:  21 00     AND ($00,X)
$ECDD:  00        BRK
$ECDE:  39 22 13  AND $1322,Y
$ECE1:  EA        NOP
$ECE2:  86 03     STX $03
$ECE4:  8E 02 00  STX $0002
$ECE7:  88        DEY
$ECE8:  EA        NOP
$ECE9:  D0 03     BNE $ECEE
$ECEB:  4C B8 C9  JMP $C9B8
$ECEE:  86 00     STX $00
$ECF0:  C9 00     CMP #$00
$ECF2:  C9 00     CMP #$00
$ECF4:  C9 00     CMP #$00
$ECF6:  C9 00     CMP #$00
$ECF8:  C9 00     CMP #$00
$ECFA:  C9 00     CMP #$00
$ECFC:  C9 00     CMP #$00
$ECFE:  C9 00     CMP #$00
$ED00:  C9 00     CMP #$00
$ED02:  C9 00     CMP #$00
$ED04:  C9 00     CMP #$00
$ED06:  C9 00     CMP #$00
$ED08:  C9 00     CMP #$00
$ED0A:  C9 00     CMP #$00
$ED0C:  C9 00     CMP #$00
$ED0E:  C9 00     CMP #$00
$ED10:  C9 FF     CMP #$FF
$ED12:  E9 00     SBC #$00
$ED14:  C9 00     CMP #$00
$ED16:  86 02     STX $02
$ED18:  D0 C7     BNE $ECE1
$ED1A:  A9 08     LDA #$08
$ED1C:  88        DEY
$ED1D:  86 03     STX $03
$ED1F:  8E 02 00  STX $0002
$ED22:  F0 04     BEQ $ED28
$ED24:  EA        NOP
$ED25:  4C 16 C5  JMP $C516
$ED28:  4C B5 C9  JMP $C9B5
$ED2B:  44        .BYTE $44
$ED2C:  45 46     EOR $46
$ED2E:  4D 56 EA  EOR $EA56
$ED31:  8E 03 00  STX $0003
$ED34:  8E 02 00  STX $0002
$ED37:  88        DEY
$ED38:  EA        NOP
$ED39:  D0 03     BNE $ED3E
$ED3B:  4C B8 C9  JMP $C9B8
$ED3E:  86 00     STX $00
$ED40:  C9 00     CMP #$00
$ED42:  C9 00     CMP #$00
$ED44:  C9 00     CMP #$00
$ED46:  C9 00     CMP #$00
$ED48:  C9 00     CMP #$00
$ED4A:  C9 00     CMP #$00
$ED4C:  C9 00     CMP #$00
$ED4E:  C9 00     CMP #$00
$ED50:  C9 00     CMP #$00
$ED52:  C9 00     CMP #$00
$ED54:  C9 00     CMP #$00
$ED56:  C9 00     CMP #$00
$ED58:  C9 00     CMP #$00
$ED5A:  C9 00     CMP #$00
$ED5C:  C9 00     CMP #$00
$ED5E:  C9 00     CMP #$00
$ED60:  C9 FF     CMP #$FF
$ED62:  E9 00     SBC #$00
$ED64:  C9 00     CMP #$00
$ED66:  86 02     STX $02
$ED68:  D0 C6     BNE $ED30
$ED6A:  A9 08     LDA #$08
$ED6C:  88        DEY
$ED6D:  86 03     STX $03
$ED6F:  8E 02 00  STX $0002
$ED72:  F0 04     BEQ $ED78
$ED74:  EA        NOP
$ED75:  4C 66 C5  JMP $C566
$ED78:  4C B5 C9  JMP $C9B5
$ED7B:  66 6E     ROR $6E
$ED7D:  70 71     BVS $EDF0
$ED7F:  72        .BYTE $72
$ED80:  EA        NOP
$ED81:  8E 03 00  STX $0003
$ED84:  8E 02 00  STX $0002
$ED87:  88        DEY
$ED88:  EA        NOP
$ED89:  D0 03     BNE $ED8E
$ED8B:  4C B8 C9  JMP $C9B8
$ED8E:  86 00     STX $00
$ED90:  C9 00     CMP #$00
$ED92:  C9 00     CMP #$00
$ED94:  C9 00     CMP #$00
$ED96:  C9 00     CMP #$00
$ED98:  C9 00     CMP #$00
$ED9A:  C9 00     CMP #$00
$ED9C:  C9 00     CMP #$00
$ED9E:  C9 00     CMP #$00
$EDA0:  C9 00     CMP #$00
$EDA2:  C9 00     CMP #$00
$EDA4:  C9 00     CMP #$00
$EDA6:  C9 00     CMP #$00
$EDA8:  C9 00     CMP #$00
$EDAA:  C9 00     CMP #$00
$EDAC:  C9 00     CMP #$00
$EDAE:  C9 00     CMP #$00
$EDB0:  C9 FF     CMP #$FF
$EDB2:  E9 00     SBC #$00
$EDB4:  C9 00     CMP #$00
$EDB6:  86 02     STX $02
$EDB8:  D0 C6     BNE $ED80
$EDBA:  A9 08     LDA #$08
$EDBC:  88        DEY
$EDBD:  86 03     STX $03
$EDBF:  8E 02 00  STX $0002
$EDC2:  F0 04     BEQ $EDC8
$EDC4:  EA        NOP
$EDC5:  4C B6 C5  JMP $C5B6
$EDC8:  4C B5 C9  JMP $C9B5
$EDCB:  52        .BYTE $52
$EDCC:  20 20 43  JSR $4320
$EDCF:  50 20     BVC $EDF1
$EDD1:  EA        NOP
$EDD2:  86 03     STX $03
$EDD4:  8E 02 00  STX $0002
$EDD7:  88        DEY
$EDD8:  EA        NOP
$EDD9:  D0 03     BNE $EDDE
$EDDB:  4C B8 C9  JMP $C9B8
$EDDE:  86 00     STX $00
$EDE0:  C9 00     CMP #$00
$EDE2:  C9 00     CMP #$00
$EDE4:  C9 00     CMP #$00
$EDE6:  C9 00     CMP #$00
$EDE8:  C9 00     CMP #$00
$EDEA:  C9 00     CMP #$00
$EDEC:  C9 00     CMP #$00
$EDEE:  C9 00     CMP #$00
$EDF0:  C9 00     CMP #$00
$EDF2:  C9 00     CMP #$00
$EDF4:  C9 00     CMP #$00
$EDF6:  C9 00     CMP #$00
$EDF8:  C9 00     CMP #$00
$EDFA:  C9 00     CMP #$00
$EDFC:  C9 00     CMP #$00
$EDFE:  C9 00     CMP #$00
$EE00:  C9 FF     CMP #$FF
$EE02:  E9 00     SBC #$00
$EE04:  C9 00     CMP #$00
$EE06:  86 02     STX $02
$EE08:  D0 C7     BNE $EDD1
$EE0A:  A9 08     LDA #$08
$EE0C:  88        DEY
$EE0D:  86 03     STX $03
$EE0F:  8E 02 00  STX $0002
$EE12:  F0 04     BEQ $EE18
$EE14:  EA        NOP
$EE15:  4C 06 C6  JMP $C606
$EE18:  4C B5 C9  JMP $C9B5
$EE1B:  4D 20 30  EOR $3020
$EE1E:  52        .BYTE $52
$EE1F:  45 EA     EOR $EA
$EE21:  8E 03 00  STX $0003
$EE24:  8E 02 00  STX $0002
$EE27:  88        DEY
$EE28:  EA        NOP
$EE29:  D0 03     BNE $EE2E
$EE2B:  4C B8 C9  JMP $C9B8
$EE2E:  86 00     STX $00
$EE30:  C9 00     CMP #$00
$EE32:  C9 00     CMP #$00
$EE34:  C9 00     CMP #$00
$EE36:  C9 00     CMP #$00
$EE38:  C9 00     CMP #$00
$EE3A:  C9 00     CMP #$00
$EE3C:  C9 00     CMP #$00
$EE3E:  C9 00     CMP #$00
$EE40:  C9 00     CMP #$00
$EE42:  C9 00     CMP #$00
$EE44:  C9 00     CMP #$00
$EE46:  C9 00     CMP #$00
$EE48:  C9 00     CMP #$00
$EE4A:  C9 00     CMP #$00
$EE4C:  C9 00     CMP #$00
$EE4E:  C9 00     CMP #$00
$EE50:  C9 FF     CMP #$FF
$EE52:  E9 00     SBC #$00
$EE54:  C9 00     CMP #$00
$EE56:  86 02     STX $02
$EE58:  D0 C6     BNE $EE20
$EE5A:  A9 08     LDA #$08
$EE5C:  88        DEY
$EE5D:  86 03     STX $03
$EE5F:  8E 02 00  STX $0002
$EE62:  F0 04     BEQ $EE68
$EE64:  EA        NOP
$EE65:  4C 56 C6  JMP $C656
$EE68:  4C B5 C9  JMP $C9B5
$EE6B:  44        .BYTE $44
$EE6C:  43        .BYTE $43
$EE6D:  20 52 4C  JSR $4C52
$EE70:  EA        NOP
$EE71:  8E 03 00  STX $0003
$EE74:  8E 02 00  STX $0002
$EE77:  88        DEY
$EE78:  EA        NOP
$EE79:  D0 03     BNE $EE7E
$EE7B:  4C B8 C9  JMP $C9B8
$EE7E:  86 00     STX $00
$EE80:  C9 00     CMP #$00
$EE82:  C9 00     CMP #$00
$EE84:  C9 00     CMP #$00
$EE86:  C9 00     CMP #$00
$EE88:  C9 00     CMP #$00
$EE8A:  C9 00     CMP #$00
$EE8C:  C9 00     CMP #$00
$EE8E:  C9 00     CMP #$00
$EE90:  C9 00     CMP #$00
$EE92:  C9 00     CMP #$00
$EE94:  C9 00     CMP #$00
$EE96:  C9 00     CMP #$00
$EE98:  C9 00     CMP #$00
$EE9A:  C9 00     CMP #$00
$EE9C:  C9 00     CMP #$00
$EE9E:  C9 00     CMP #$00
$EEA0:  C9 FF     CMP #$FF
$EEA2:  E9 00     SBC #$00
$EEA4:  C9 00     CMP #$00
$EEA6:  86 02     STX $02
$EEA8:  D0 C6     BNE $EE70
$EEAA:  A9 08     LDA #$08
$EEAC:  88        DEY
$EEAD:  86 03     STX $03
$EEAF:  8E 02 00  STX $0002
$EEB2:  F0 04     BEQ $EEB8
$EEB4:  EA        NOP
$EEB5:  4C A6 C6  JMP $C6A6
$EEB8:  4C B5 C9  JMP $C9B5
$EEBB:  44        .BYTE $44
$EEBC:  20 20 20  JSR $2020
$EEBF:  45 EA     EOR $EA
$EEC1:  8E 03 00  STX $0003
$EEC4:  8E 02 00  STX $0002
$EEC7:  88        DEY
$EEC8:  EA        NOP
$EEC9:  D0 03     BNE $EECE
$EECB:  4C B8 C9  JMP $C9B8
$EECE:  86 00     STX $00
$EED0:  C9 00     CMP #$00
$EED2:  C9 00     CMP #$00
$EED4:  C9 00     CMP #$00
$EED6:  C9 00     CMP #$00
$EED8:  C9 00     CMP #$00
$EEDA:  C9 00     CMP #$00
$EEDC:  C9 00     CMP #$00
$EEDE:  C9 00     CMP #$00
$EEE0:  C9 00     CMP #$00
$EEE2:  C9 00     CMP #$00
$EEE4:  C9 00     CMP #$00
$EEE6:  C9 00     CMP #$00
$EEE8:  C9 00     CMP #$00
$EEEA:  C9 00     CMP #$00
$EEEC:  C9 00     CMP #$00
$EEEE:  C9 00     CMP #$00
$EEF0:  C9 FF     CMP #$FF
$EEF2:  E9 00     SBC #$00
$EEF4:  C9 00     CMP #$00
$EEF6:  86 02     STX $02
$EEF8:  D0 C6     BNE $EEC0
$EEFA:  A9 08     LDA #$08
$EEFC:  88        DEY
$EEFD:  86 03     STX $03
$EEFF:  8E 02 00  STX $0002
$EF02:  F0 04     BEQ $EF08
$EF04:  EA        NOP
$EF05:  4C F6 C6  JMP $C6F6
$EF08:  4C B5 C9  JMP $C9B5
$EF0B:  00        BRK
$EF0C:  00        BRK
$EF0D:  00        BRK
$EF0E:  00        BRK
$EF0F:  00        BRK
$EF10:  EA        NOP
$EF11:  8E 03 00  STX $0003
$EF14:  8E 02 00  STX $0002
$EF17:  88        DEY
$EF18:  EA        NOP
$EF19:  D0 03     BNE $EF1E
$EF1B:  4C B8 C9  JMP $C9B8
$EF1E:  86 00     STX $00
$EF20:  C9 00     CMP #$00
$EF22:  C9 00     CMP #$00
$EF24:  C9 00     CMP #$00
$EF26:  C9 00     CMP #$00
$EF28:  C9 00     CMP #$00
$EF2A:  C9 00     CMP #$00
$EF2C:  C9 00     CMP #$00
$EF2E:  C9 00     CMP #$00
$EF30:  C9 00     CMP #$00
$EF32:  C9 00     CMP #$00
$EF34:  C9 00     CMP #$00
$EF36:  C9 00     CMP #$00
$EF38:  C9 00     CMP #$00
$EF3A:  C9 00     CMP #$00
$EF3C:  C9 00     CMP #$00
$EF3E:  C9 00     CMP #$00
$EF40:  C9 FF     CMP #$FF
$EF42:  E9 00     SBC #$00
$EF44:  C9 00     CMP #$00
$EF46:  86 02     STX $02
$EF48:  D0 C6     BNE $EF10
$EF4A:  A9 08     LDA #$08
$EF4C:  88        DEY
$EF4D:  86 03     STX $03
$EF4F:  8E 02 00  STX $0002
$EF52:  F0 04     BEQ $EF58
$EF54:  EA        NOP
$EF55:  4C 46 C7  JMP $C746
$EF58:  4C B5 C9  JMP $C9B5
$EF5B:  00        BRK
$EF5C:  00        BRK
$EF5D:  00        BRK
$EF5E:  00        BRK
$EF5F:  00        BRK
$EF60:  EA        NOP
$EF61:  8E 03 00  STX $0003
$EF64:  8E 02 00  STX $0002
$EF67:  88        DEY
$EF68:  EA        NOP
$EF69:  D0 03     BNE $EF6E
$EF6B:  4C B8 C9  JMP $C9B8
$EF6E:  86 00     STX $00
$EF70:  C9 00     CMP #$00
$EF72:  C9 00     CMP #$00
$EF74:  C9 00     CMP #$00
$EF76:  C9 00     CMP #$00
$EF78:  C9 00     CMP #$00
$EF7A:  C9 00     CMP #$00
$EF7C:  C9 00     CMP #$00
$EF7E:  C9 00     CMP #$00
$EF80:  C9 00     CMP #$00
$EF82:  C9 00     CMP #$00
$EF84:  C9 00     CMP #$00
$EF86:  C9 00     CMP #$00
$EF88:  C9 00     CMP #$00
$EF8A:  C9 00     CMP #$00
$EF8C:  C9 00     CMP #$00
$EF8E:  C9 00     CMP #$00
$EF90:  C9 FF     CMP #$FF
$EF92:  E9 00     SBC #$00
$EF94:  C9 00     CMP #$00
$EF96:  86 02     STX $02
$EF98:  D0 C6     BNE $EF60
$EF9A:  A9 08     LDA #$08
$EF9C:  88        DEY
$EF9D:  86 03     STX $03
$EF9F:  8E 02 00  STX $0002
$EFA2:  F0 04     BEQ $EFA8
$EFA4:  EA        NOP
$EFA5:  4C 96 C7  JMP $C796
$EFA8:  4C B5 C9  JMP $C9B5
$EFAB:  D0 0A     BNE $EFB7
$EFAD:  A9 0A     LDA #$0A
$EFAF:  8D F2 43  STA $43F2
$EFB2:  A9 04     LDA #$04
$EFB4:  6C F0 43  JMP ($43F0)
$EFB7:  A9 00     LDA #$00
$EFB9:  EA        NOP
$EFBA:  F0 F8     BEQ $EFB4
$EFBC:  0E 21 86  ASL $8621
$EFBF:  00        BRK
$EFC0:  C9 00     CMP #$00
$EFC2:  C9 00     CMP #$00
$EFC4:  C9 00     CMP #$00
$EFC6:  C9 00     CMP #$00
$EFC8:  C9 00     CMP #$00
$EFCA:  C9 00     CMP #$00
$EFCC:  C9 00     CMP #$00
$EFCE:  C9 00     CMP #$00
$EFD0:  C9 00     CMP #$00
$EFD2:  C9 00     CMP #$00
$EFD4:  C9 00     CMP #$00
$EFD6:  C9 00     CMP #$00
$EFD8:  C9 00     CMP #$00
$EFDA:  C9 00     CMP #$00
$EFDC:  C9 00     CMP #$00
$EFDE:  C9 00     CMP #$00
$EFE0:  C9 FF     CMP #$FF
$EFE2:  E9 00     SBC #$00
$EFE4:  C9 00     CMP #$00
$EFE6:  86 02     STX $02
$EFE8:  D0 03     BNE $EFED
$EFEA:  4C 30 C3  JMP $C330
$EFED:  EA        NOP
$EFEE:  8E 03 00  STX $0003
$EFF1:  8E 02 00  STX $0002
$EFF4:  EA        NOP
$EFF5:  EA        NOP
$EFF6:  4C BE CF  JMP $CFBE
$EFF9:  E5 22     SBC $22
$EFFB:  4F        .BYTE $4F
$EFFC:  21 3E     AND ($3E,X)
$EFFE:  C3        .BYTE $C3
$EFFF:  32        .BYTE $32
$F000:  4C 68 D3  JMP $D368
$F003:  4C 23 D2  JMP $D223
$F006:  4C 38 D2  JMP $D238
$F009:  4C 4D D2  JMP $D24D
$F00C:  A9 82     LDA #$82
$F00E:  AA        TAX
$F00F:  A8        TAY
$F010:  8E 00 08  STX $0800
$F013:  CE FA 53  DEC $53FA
$F016:  4C 30 C3  JMP $C330
$F019:  BA        TSX
$F01A:  EA        NOP
$F01B:  86 03     STX $03
$F01D:  8C 02 00  STY $0002
$F020:  86 02     STX $02
$F022:  AA        TAX
$F023:  AD 0A 80  LDA $800A
$F026:  8D E9 43  STA $43E9
$F029:  E0 A1     CPX #$A1 ('!')
$F02B:  90 5C     BCC $F089
$F02D:  49 FF     EOR #$FF
$F02F:  29 4C     AND #$4C ('L')
$F031:  F0 42     BEQ $F075
$F033:  C9 40     CMP #$40 ('@')
$F035:  90 0D     BCC $F044
$F037:  F0 31     BEQ $F06A
$F039:  EA        NOP
$F03A:  8A        TXA
$F03B:  C9 C0     CMP #$C0 ('@')
$F03D:  90 5A     BCC $F099
$F03F:  49 40     EOR #$40 ('@')
$F041:  EA        NOP
$F042:  D0 5B     BNE $F09F
$F044:  8A        TXA
$F045:  C9 B0     CMP #$B0 ('0')
$F047:  F0 0A     BEQ $F053
$F049:  C9 C0     CMP #$C0 ('@')
$F04B:  F0 0B     BEQ $F058
$F04D:  B0 0D     BCS $F05C
$F04F:  49 10     EOR #$10
$F051:  D0 56     BNE $F0A9
$F053:  A9 DF     LDA #$DF ('_')
$F055:  EA        NOP
$F056:  D0 F9     BNE $F051
$F058:  49 20     EOR #$20 (' ')
$F05A:  D0 43     BNE $F09F
$F05C:  C9 DB     CMP #$DB ('[')
$F05E:  B0 02     BCS $F062
$F060:  90 02     BCC $F064
$F062:  49 20     EOR #$20 (' ')
$F064:  8D F7 43  STA $43F7
$F067:  4C B0 D0  JMP $D0B0
$F06A:  EA        NOP
$F06B:  8A        TXA
$F06C:  C9 C0     CMP #$C0 ('@')
$F06E:  90 35     BCC $F0A5
$F070:  49 40     EOR #$40 ('@')
$F072:  EA        NOP
$F073:  D0 34     BNE $F0A9
$F075:  E0 C1     CPX #$C1 ('A')
$F077:  90 16     BCC $F08F
$F079:  AD E9 43  LDA $43E9
$F07C:  29 10     AND #$10
$F07E:  F0 13     BEQ $F093
$F080:  8A        TXA
$F081:  C9 DB     CMP #$DB ('[')
$F083:  B0 11     BCS $F096
$F085:  49 20     EOR #$20 (' ')
$F087:  D0 21     BNE $F0AA
$F089:  EA        NOP
$F08A:  EA        NOP
$F08B:  EA        NOP
$F08C:  38        SEC
$F08D:  B0 00     BCS $F08F
$F08F:  EA        NOP
$F090:  EA        NOP
$F091:  EA        NOP
$F092:  EA        NOP
$F093:  EA        NOP
$F094:  8A        TXA
$F095:  EA        NOP
$F096:  38        SEC
$F097:  B0 CB     BCS $F064
$F099:  C9 B0     CMP #$B0 ('0')
$F09B:  D0 0A     BNE $F0A7
$F09D:  A9 9F     LDA #$9F
$F09F:  8D F7 43  STA $43F7
$F0A2:  4C AD D0  JMP $D0AD
$F0A5:  EA        NOP
$F0A6:  EA        NOP
$F0A7:  A9 1F     LDA #$1F
$F0A9:  EA        NOP
$F0AA:  8D F7 43  STA $43F7
$F0AD:  AD F7 43  LDA $43F7
$F0B0:  BA        TSX
$F0B1:  86 03     STX $03
$F0B3:  8C 02 00  STY $0002
$F0B6:  86 02     STX $02
$F0B8:  C9 0C     CMP #$0C
$F0BA:  B0 0C     BCS $F0C8
$F0BC:  AA        TAX
$F0BD:  AD EC 43  LDA $43EC
$F0C0:  09 02     ORA #$02
$F0C2:  8D EC 43  STA $43EC
$F0C5:  6C F7 53  JMP ($53F7)
$F0C8:  C9 20     CMP #$20 (' ')
$F0CA:  B0 0D     BCS $F0D9
$F0CC:  AD EC 43  LDA $43EC
$F0CF:  09 01     ORA #$01
$F0D1:  8D EC 43  STA $43EC
$F0D4:  A2 05     LDX #$05
$F0D6:  4C EB D1  JMP $D1EB
$F0D9:  29 7F     AND #$7F
$F0DB:  0D FE 43  ORA $43FE
$F0DE:  4C E3 D1  JMP $D1E3
$F0E1:  AE FC 43  LDX $43FC
$F0E4:  38        SEC
$F0E5:  B0 00     BCS $F0E7
$F0E7:  AD EC 43  LDA $43EC
$F0EA:  29 0C     AND #$0C
$F0EC:  F0 05     BEQ $F0F3
$F0EE:  BD 00 D4  LDA $D400,X
$F0F1:  D0 04     BNE $F0F7
$F0F3:  BD 00 D3  LDA $D300,X
$F0F6:  EA        NOP
$F0F7:  4C 33 D1  JMP $D133
$F0FA:  C3        .BYTE $C3
$F0FB:  FF        .BYTE $FF
$F0FC:  0F        .BYTE $0F
$F0FD:  3E 0C 32  ROL $320C,X
$F100:  4C 50 D3  JMP $D350
$F103:  4C 00 D2  JMP $D200
$F106:  4C 0B D2  JMP $D20B
$F109:  4C 17 D2  JMP $D217
$F10C:  AC FA 53  LDY $53FA
$F10F:  BD 00 D4  LDA $D400,X
$F112:  99 C0 53  STA $53C0,Y
$F115:  E8        INX
$F116:  BD 00 D4  LDA $D400,X
$F119:  99 C0 43  STA $43C0,Y
$F11C:  EE FA 53  INC $53FA
$F11F:  E8        INX
$F120:  8A        TXA
$F121:  BA        TSX
$F122:  86 03     STX $03
$F124:  8E 02 00  STX $0002
$F127:  86 02     STX $02
$F129:  AA        TAX
$F12A:  8E F9 53  STX $53F9
$F12D:  AC FC 53  LDY $53FC
$F130:  4C 6B C3  JMP $C36B
$F133:  BA        TSX
$F134:  86 03     STX $03
$F136:  8C 02 00  STY $0002
$F139:  86 02     STX $02
$F13B:  8D 00 04  STA $0400
$F13E:  8D EE 43  STA $43EE
$F141:  EE FC 43  INC $43FC
$F144:  A2 05     LDX #$05
$F146:  D0 00     BNE $F148
$F148:  4C F5 C2  JMP $C2F5
$F14B:  A9 05     LDA #$05
$F14D:  8D F8 43  STA $43F8
$F150:  AD F7 43  LDA $43F7
$F153:  EA        NOP
$F154:  10 06     BPL $F15C
$F156:  8D 00 04  STA $0400
$F159:  4C F1 C7  JMP $C7F1
$F15C:  10 FB     BPL $F159
$F15E:  BD F2 D1  LDA $D1F2,X
$F161:  7D A7 C9  ADC $C9A7,X
$F164:  9D 8B 52  STA $528B,X
$F167:  4C AF C1  JMP $C1AF
$F16A:  00        BRK
$F16B:  03        .BYTE $03
$F16C:  06 09     ASL $09
$F16E:  CE F3 43  DEC $43F3
$F171:  BD AD C3  LDA $C3AD,X
$F174:  8D FF 43  STA $43FF
$F177:  30 06     BMI $F17F
$F179:  4C 62 D2  JMP $D262
$F17C:  E8        INX
$F17D:  D0 F2     BNE $F171
$F17F:  29 7F     AND #$7F
$F181:  8D FF 43  STA $43FF
$F184:  EE F8 43  INC $43F8
$F187:  AD F8 43  LDA $43F8
$F18A:  C9 06     CMP #$06
$F18C:  90 EB     BCC $F179
$F18E:  4C 94 D2  JMP $D294
$F191:  EA        NOP
$F192:  EA        NOP
$F193:  EA        NOP
$F194:  BA        TSX
$F195:  8E 03 00  STX $0003
$F198:  8C 02 00  STY $0002
$F19B:  86 02     STX $02
$F19D:  4C 4B D1  JMP $D14B
$F1A0:  AD 0B 80  LDA $800B
$F1A3:  AE EB 43  LDX $43EB
$F1A6:  F0 08     BEQ $F1B0
$F1A8:  CE EB 43  DEC $43EB
$F1AB:  EA        NOP
$F1AC:  EA        NOP
$F1AD:  4C EB C2  JMP $C2EB
$F1B0:  CD E9 43  CMP $43E9
$F1B3:  D0 F7     BNE $F1AC
$F1B5:  BA        TSX
$F1B6:  EA        NOP
$F1B7:  AD F8 43  LDA $43F8
$F1BA:  86 03     STX $03
$F1BC:  8C 02 00  STY $0002
$F1BF:  86 02     STX $02
$F1C1:  D0 19     BNE $F1DC
$F1C3:  A9 05     LDA #$05
$F1C5:  8D F8 43  STA $43F8
$F1C8:  AD F7 43  LDA $43F7
$F1CB:  C9 20     CMP #$20 (' ')
$F1CD:  B0 03     BCS $F1D2
$F1CF:  EA        NOP
$F1D0:  90 03     BCC $F1D5
$F1D2:  8D 00 04  STA $0400
$F1D5:  A2 04     LDX #$04
$F1D7:  D0 00     BNE $F1D9
$F1D9:  4C F5 C2  JMP $C2F5
$F1DC:  CE F8 43  DEC $43F8
$F1DF:  A2 06     LDX #$06
$F1E1:  D0 F6     BNE $F1D9
$F1E3:  8D 00 04  STA $0400
$F1E6:  8D EE 43  STA $43EE
$F1E9:  A2 04     LDX #$04
$F1EB:  CA        DEX
$F1EC:  D0 FD     BNE $F1EB
$F1EE:  BA        TSX
$F1EF:  4C 97 D5  JMP $D597
$F1F2:  B9 CD 8B  LDA $8BCD,Y
$F1F5:  D7        .BYTE $D7
$F1F6:  85 D1     STA $D1
$F1F8:  88        DEY
$F1F9:  D0 8A     BNE $F185
$F1FB:  91 16     STA ($16),Y
$F1FD:  0F        .BYTE $0F
$F1FE:  C3        .BYTE $C3
$F1FF:  65 AE     ADC $AE
$F201:  F9 53 F0  SBC $F053,Y
$F204:  02        .BYTE $02
$F205:  D0 01     BNE $F208
$F207:  EA        NOP
$F208:  4C 0C D1  JMP $D10C
$F20B:  AE F9 53  LDX $53F9
$F20E:  F0 02     BEQ $F212
$F210:  D0 02     BNE $F214
$F212:  A2 50     LDX #$50 ('P')
$F214:  4C 0C D1  JMP $D10C
$F217:  AE F9 53  LDX $53F9
$F21A:  F0 02     BEQ $F21E
$F21C:  D0 02     BNE $F220
$F21E:  A2 A0     LDX #$A0 (' ')
$F220:  4C 0C D1  JMP $D10C
$F223:  EA        NOP
$F224:  EA        NOP
$F225:  BD D0 D2  LDA $D2D0,X
$F228:  8D FC 43  STA $43FC
$F22B:  38        SEC
$F22C:  FD D1 D2  SBC $D2D1,X
$F22F:  49 FF     EOR #$FF
$F231:  8D FB 43  STA $43FB
$F234:  BA        TSX
$F235:  4C 97 D5  JMP $D597
$F238:  EA        NOP
$F239:  EA        NOP
$F23A:  BD DC D2  LDA $D2DC,X
$F23D:  8D FC 43  STA $43FC
$F240:  38        SEC
$F241:  FD DD D2  SBC $D2DD,X
$F244:  49 FF     EOR #$FF
$F246:  8D FB 43  STA $43FB
$F249:  BA        TSX
$F24A:  4C 97 D5  JMP $D597
$F24D:  EA        NOP
$F24E:  EA        NOP
$F24F:  BD E8 D2  LDA $D2E8,X
$F252:  8D FC 43  STA $43FC
$F255:  38        SEC
$F256:  FD E9 D2  SBC $D2E9,X
$F259:  49 FF     EOR #$FF
$F25B:  8D FB 43  STA $43FB
$F25E:  BA        TSX
$F25F:  4C 97 D5  JMP $D597
$F262:  AD F8 43  LDA $43F8
$F265:  0A        ASL
$F266:  0A        ASL
$F267:  0A        ASL
$F268:  8D F4 43  STA $43F4
$F26B:  0A        ASL
$F26C:  0A        ASL
$F26D:  6D F4 43  ADC $43F4
$F270:  4E FF 43  LSR $43FF
$F273:  B0 11     BCS $F286
$F275:  6D FF 43  ADC $43FF
$F278:  A8        TAY
$F279:  A9 DA     LDA #$DA ('Z')
$F27B:  99 4B 51  STA $514B,Y
$F27E:  E9 02     SBC #$02
$F280:  99 4B 41  STA $414B,Y
$F283:  4C 7C D1  JMP $D17C
$F286:  6D FF 43  ADC $43FF
$F289:  A8        TAY
$F28A:  A9 D7     LDA #$D7 ('W')
$F28C:  99 4B 51  STA $514B,Y
$F28F:  88        DEY
$F290:  69 03     ADC #$03
$F292:  90 EC     BCC $F280
$F294:  8A        TXA
$F295:  0A        ASL
$F296:  0A        ASL
$F297:  8D F1 43  STA $43F1
$F29A:  8D FA 43  STA $43FA
$F29D:  CE F8 43  DEC $43F8
$F2A0:  AE FD 43  LDX $43FD
$F2A3:  4C AC C1  JMP $C1AC
$F2A6:  38        SEC
$F2A7:  6A        ROR
$F2A8:  9D 8B 52  STA $528B,X
$F2AB:  4C B4 D2  JMP $D2B4
$F2AE:  B9 FC C7  LDA $C7FC,Y
$F2B1:  4C A6 D2  JMP $D2A6
$F2B4:  B9 B8 C0  LDA $C0B8,Y
$F2B7:  4C C7 C9  JMP $C9C7
$F2BA:  E8        INX
$F2BB:  C8        INY
$F2BC:  C0 09     CPY #$09
$F2BE:  90 EE     BCC $F2AE
$F2C0:  4C 9F C3  JMP $C39F
$F2C3:  01 06     ORA ($06,X)
$F2C5:  0F        .BYTE $0F
$F2C6:  16 1B     ASL $1B,X
$F2C8:  21 27     AND ($27,X)
$F2CA:  2D 33 3A  AND $3A33
$F2CD:  40        RTI
$F2CE:  46 4D     LSR $4D
$F2D0:  01 08     ORA ($08,X)
$F2D2:  0E 1A 20  ASL $201A
$F2D5:  26 2E     ROL $2E
$F2D7:  34        .BYTE $34
$F2D8:  3A        .BYTE $3A
$F2D9:  41 47     EOR ($47,X)
$F2DB:  4C 51 58  JMP $5851
$F2DE:  5F        .BYTE $5F
$F2DF:  66 6C     ROR $6C
$F2E1:  72        .BYTE $72
$F2E2:  78        SEI
$F2E3:  7F        .BYTE $7F
$F2E4:  87        .BYTE $87
$F2E5:  90 97     BCC $F27E
$F2E7:  9C        .BYTE $9C
$F2E8:  A1 A5     LDA ($A5,X)
$F2EA:  AA        TAX
$F2EB:  AF        .BYTE $AF
$F2EC:  B5 BB     LDA $BB,X
$F2EE:  C1 C9     CMP ($C9,X)
$F2F0:  CE D3 D8  DEC $D8D3
$F2F3:  DE E6 12  DEC $12E6,X
$F2F6:  23        .BYTE $23
$F2F7:  73        .BYTE $73
$F2F8:  23        .BYTE $23
$F2F9:  72        .BYTE $72
$F2FA:  23        .BYTE $23
$F2FB:  1A        .BYTE $1A
$F2FC:  77        .BYTE $77
$F2FD:  3E FF 12  ROL $12FF,X
$F300:  31 D0     AND ($D0),Y
$F302:  D2        .BYTE $D2
$F303:  A3        .BYTE $A3
$F304:  A0 32     LDY #$32 ('2')
$F306:  C3        .BYTE $C3
$F307:  C1 D4     CMP ($D4,X)
$F309:  C1 CC     CMP ($CC,X)
$F30B:  CF        .BYTE $CF
$F30C:  C7        .BYTE $C7
$F30D:  A0 33     LDY #$33 ('3')
$F30F:  D0 D2     BNE $F2E3
$F311:  C9 CE     CMP #$CE ('N')
$F313:  D4        .BYTE $D4
$F314:  A0 34     LDY #$34 ('4')
$F316:  D2        .BYTE $D2
$F317:  D5 CE     CMP $CE,X
$F319:  A0 35     LDY #$35 ('5')
$F31B:  CC C9 D3  CPY $D3C9
$F31E:  D4        .BYTE $D4
$F31F:  A0 36     LDY #$36 ('6')
$F321:  CC CF C1  CPY $C1CF
$F324:  C4 A0     CPY $A0
$F326:  37        .BYTE $37
$F327:  D3        .BYTE $D3
$F328:  C1 D6     CMP ($D6,X)
$F32A:  C5 A0     CMP $A0
$F32C:  38        SEC
$F32D:  D2        .BYTE $D2
$F32E:  C5 C1     CMP $C1
$F330:  C4 A0     CPY $A0
$F332:  39 C9 CE  AND $CEC9,Y
$F335:  D0 D5     BNE $F30C
$F337:  D4        .BYTE $D4
$F338:  A0 01     LDY #$01
$F33A:  C4 C1     CPY $C1
$F33C:  D4        .BYTE $D4
$F33D:  C1 A0     CMP ($A0,X)
$F33F:  02        .BYTE $02
$F340:  CF        .BYTE $CF
$F341:  D0 C5     BNE $F308
$F343:  CE A0 03  DEC $03A0
$F346:  C3        .BYTE $C3
$F347:  CC CF D3  CPY $D3CF
$F34A:  C5 A0     CMP $A0
$F34C:  A0 A0     LDY #$A0 (' ')
$F34E:  A0 A0     LDY #$A0 (' ')
$F350:  AE F9 53  LDX $53F9
$F353:  F0 02     BEQ $F357
$F355:  D0 01     BNE $F358
$F357:  EA        NOP
$F358:  AC FA 53  LDY $53FA
$F35B:  BD 00 D3  LDA $D300,X
$F35E:  99 C0 53  STA $53C0,Y
$F361:  E8        INX
$F362:  BD 00 D3  LDA $D300,X
$F365:  4C 19 D1  JMP $D119
$F368:  EA        NOP
$F369:  EA        NOP
$F36A:  BD C3 D2  LDA $D2C3,X
$F36D:  8D FC 43  STA $43FC
$F370:  38        SEC
$F371:  FD C4 D2  SBC $D2C4,X
$F374:  49 FF     EOR #$FF
$F376:  8D FB 43  STA $43FB
$F379:  BA        TSX
$F37A:  4C 97 D5  JMP $D597
$F37D:  EA        NOP
$F37E:  EA        NOP
$F37F:  EA        NOP
$F380:  4D E8 43  EOR $43E8
$F383:  AA        TAX
$F384:  9A        TXS
$F385:  A9 69     LDA #$69 ('i')
$F387:  A8        TAY
$F388:  49 81     EOR #$81
$F38A:  AA        TAX
$F38B:  A9 C0     LDA #$C0 ('@')
$F38D:  D0 00     BNE $F38F
$F38F:  4C 74 C1  JMP $C174
$F392:  A9 00     LDA #$00
$F394:  10 00     BPL $F396
$F396:  10 04     BPL $F39C
$F398:  E8        INX
$F399:  E8        INX
$F39A:  A9 10     LDA #$10
$F39C:  8D F4 43  STA $43F4
$F39F:  10 15     BPL $F3B6
$F3A1:  AD EF 43  LDA $43EF
$F3A4:  0A        ASL
$F3A5:  AA        TAX
$F3A6:  AD F4 43  LDA $43F4
$F3A9:  30 E7     BMI $F392
$F3AB:  F0 EB     BEQ $F398
$F3AD:  69 10     ADC #$10
$F3AF:  8D F4 43  STA $43F4
$F3B2:  E8        INX
$F3B3:  E8        INX
$F3B4:  E8        INX
$F3B5:  E8        INX
$F3B6:  BD A2 D5  LDA $D5A2,X
$F3B9:  8D F7 53  STA $53F7
$F3BC:  BD A3 D5  LDA $D5A3,X
$F3BF:  8D F8 53  STA $53F8
$F3C2:  BA        TSX
$F3C3:  86 03     STX $03
$F3C5:  8E 02 00  STX $0002
$F3C8:  86 02     STX $02
$F3CA:  4E F4 43  LSR $43F4
$F3CD:  A9 C1     LDA #$C1 ('A')
$F3CF:  ED F4 43  SBC $43F4
$F3D2:  AA        TAX
$F3D3:  AD F4 43  LDA $43F4
$F3D6:  8E F4 43  STX $43F4
$F3D9:  A2 05     LDX #$05
$F3DB:  CA        DEX
$F3DC:  D0 FD     BNE $F3DB
$F3DE:  38        SEC
$F3DF:  BA        TSX
$F3E0:  E9 00     SBC #$00
$F3E2:  86 03     STX $03
$F3E4:  8E 02 00  STX $0002
$F3E7:  F0 08     BEQ $F3F1
$F3E9:  A2 09     LDX #$09
$F3EB:  CA        DEX
$F3EC:  D0 FD     BNE $F3EB
$F3EE:  18        CLC
$F3EF:  90 EE     BCC $F3DF
$F3F1:  4C 87 DF  JMP $DF87
$F3F4:  06 00     ASL $00
$F3F6:  B7        .BYTE $B7
$F3F7:  C0 C3     CPY #$C3 ('C')
$F3F9:  90 18     BCC $F413
$F3FB:  FE 2E C8  INC $C82E,X
$F3FE:  FE 0D 31  INC $310D,X
$F401:  C7        .BYTE $C7
$F402:  CF        .BYTE $CF
$F403:  D3        .BYTE $D3
$F404:  D5 C2     CMP $C2,X
$F406:  A0 32     LDY #$32 ('2')
$F408:  C7        .BYTE $C7
$F409:  CF        .BYTE $CF
$F40A:  D4        .BYTE $D4
$F40B:  CF        .BYTE $CF
$F40C:  A0 33     LDY #$33 ('3')
$F40E:  CF        .BYTE $CF
$F40F:  CE C5 D2  DEC $D2C5
$F412:  D2        .BYTE $D2
$F413:  A0 C7     LDY #$C7 ('G')
$F415:  CF        .BYTE $CF
$F416:  D4        .BYTE $D4
$F417:  CF        .BYTE $CF
$F418:  A0 34     LDY #$34 ('4')
$F41A:  D4        .BYTE $D4
$F41B:  C8        INY
$F41C:  C5 CE     CMP $CE
$F41E:  A0 35     LDY #$35 ('5')
$F420:  CE C5 D8  DEC $D8C5
$F423:  D4        .BYTE $D4
$F424:  A0 36     LDY #$36 ('6')
$F426:  C4 C5     CPY $C5
$F428:  CC C5 D4  CPY $D4C5
$F42B:  C5 A0     CMP $A0
$F42D:  37        .BYTE $37
$F42E:  C3        .BYTE $C3
$F42F:  C8        INY
$F430:  D2        .BYTE $D2
$F431:  A4 A8     LDY $A8
$F433:  38        SEC
$F434:  CD C9 C4  CMP $C4C9
$F437:  A4 A0     LDY $A0
$F439:  39 D2 C9  AND $C9D2,Y
$F43C:  C7        .BYTE $C7
$F43D:  C8        INY
$F43E:  D4        .BYTE $D4
$F43F:  A4 01     LDY $01
$F441:  CC C5 C6  CPY $C6C5
$F444:  D4        .BYTE $D4
$F445:  A4 02     LDY $02
$F447:  C8        INY
$F448:  CF        .BYTE $CF
$F449:  CD C5 03  CMP $03C5
$F44C:  D3        .BYTE $D3
$F44D:  D4        .BYTE $D4
$F44E:  C5 D0     CMP $D0
$F450:  31 C3     AND ($C3),Y
$F452:  CF        .BYTE $CF
$F453:  CC CF D2  CPY $D2CF
$F456:  BD 32 C8  LDA $C832,X
$F459:  C9 CD     CMP #$CD ('M')
$F45B:  C5 CD     CMP $CD
$F45D:  BA        TSX
$F45E:  33        .BYTE $33
$F45F:  CC CF CD  CPY $CDCF
$F462:  C5 CD     CMP $CD
$F464:  BA        TSX
$F465:  34        .BYTE $34
$F466:  D0 C5     BNE $F42D
$F468:  C5 CB     CMP $CB
$F46A:  A0 35     LDY #$35 ('5')
$F46C:  D0 CF     BNE $F43D
$F46E:  CB        .BYTE $CB
$F46F:  C5 A0     CMP $A0
$F471:  36 D0     ROL $D0,X
$F473:  CC CF D4  CPY $D4CF
$F476:  A0 37     LDY #$37 ('7')
$F478:  C6 CC     DEC $CC
$F47A:  C1 D3     CMP ($D3,X)
$F47C:  C8        INY
$F47D:  A0 38     LDY #$38 ('8')
$F47F:  CE CF D2  DEC $D2CF
$F482:  CD C1 CC  CMP $CCC1
$F485:  A0 39     LDY #$39 ('9')
$F487:  C9 CE     CMP #$CE ('N')
$F489:  D6 C5     DEC $C5,X
$F48B:  D2        .BYTE $D2
$F48C:  D3        .BYTE $D3
$F48D:  C5 A0     CMP $A0
$F48F:  01 D3     ORA ($D3,X)
$F491:  D0 C5     BNE $F458
$F493:  C5 C4     CMP $C4
$F495:  BD 02 D4  LDA $D402,X
$F498:  C1 C2     CMP ($C2,X)
$F49A:  A0 03     LDY #$03
$F49C:  D4        .BYTE $D4
$F49D:  C5 D8     CMP $D8
$F49F:  D4        .BYTE $D4
$F4A0:  31 C4     AND ($C4),Y
$F4A2:  C9 D2     CMP #$D2 ('R')
$F4A4:  32        .BYTE $32
$F4A5:  C5 D2     CMP $D2
$F4A7:  C1 A0     CMP ($A0,X)
$F4A9:  33        .BYTE $33
$F4AA:  D2        .BYTE $D2
$F4AB:  C5 CE     CMP $CE
$F4AD:  A0 34     LDY #$34 ('4')
$F4AF:  D3        .BYTE $D3
$F4B0:  C1 D6     CMP ($D6,X)
$F4B2:  C5 A0     CMP $A0
$F4B4:  35 D4     AND $D4,X
$F4B6:  D9 D0 C5  CMP $C5D0,Y
$F4B9:  A0 36     LDY #$36 ('6')
$F4BB:  D3        .BYTE $D3
$F4BC:  D4        .BYTE $D4
$F4BD:  C1 D4     CMP ($D4,X)
$F4BF:  A0 37     LDY #$37 ('7')
$F4C1:  D7        .BYTE $D7
$F4C2:  CF        .BYTE $CF
$F4C3:  D2        .BYTE $D2
$F4C4:  CB        .BYTE $CB
$F4C5:  C9 CE     CMP #$CE ('N')
$F4C7:  C7        .BYTE $C7
$F4C8:  38        SEC
$F4C9:  AE CD C1  LDX $C1CD
$F4CC:  C3        .BYTE $C3
$F4CD:  39 AE C3  AND $C3AE,Y
$F4D0:  CF        .BYTE $CF
$F4D1:  CD 01 C4  CMP $C401
$F4D4:  C4 D4     CPY $D4
$F4D6:  A0 02     LDY #$02
$F4D8:  C3        .BYTE $C3
$F4D9:  CF        .BYTE $CF
$F4DA:  D0 D9     BNE $F4B5
$F4DC:  A0 03     LDY #$03
$F4DE:  C6 CF     DEC $CF
$F4E0:  D2        .BYTE $D2
$F4E1:  CD C1 D4  CMP $D4C1
$F4E4:  A0 A0     LDY #$A0 (' ')
$F4E6:  A0 A0     LDY #$A0 (' ')
$F4E8:  A0 A0     LDY #$A0 (' ')
$F4EA:  A0 A0     LDY #$A0 (' ')
$F4EC:  A0 A0     LDY #$A0 (' ')
$F4EE:  A0 A0     LDY #$A0 (' ')
$F4F0:  19 E5 21  ORA $21E5,Y
$F4F3:  01 00     ORA ($00,X)
$F4F5:  3D 3A 4A  AND $4A3A,X
$F4F8:  21 CA     AND ($CA,X)
$F4FA:  06 14     ASL $14
$F4FC:  B7        .BYTE $B7
$F4FD:  C2        .BYTE $C2
$F4FE:  5D 18 AD  EOR $AD18,X
$F501:  FD 43 09  SBC $0943,X
$F504:  10 8D     BPL $F493
$F506:  FD 43 8C  SBC $8C43,X
$F509:  F4        .BYTE $F4
$F50A:  43        .BYTE $43
$F50B:  A2 2F     LDX #$2F ('/')
$F50D:  A0 00     LDY #$00
$F50F:  B9 1C D5  LDA $D51C,Y
$F512:  99 00 50  STA $5000,Y
$F515:  C8        INY
$F516:  CA        DEX
$F517:  D0 F6     BNE $F50F
$F519:  4C 00 50  JMP $5000
$F51C:  A2 40     LDX #$40 ('@')
$F51E:  A0 00     LDY #$00
$F520:  B9 00 D8  LDA $D800,Y
$F523:  9D 00 50  STA $5000,X
$F526:  C8        INY
$F527:  B9 00 D8  LDA $D800,Y
$F52A:  9D 00 40  STA $4000,X
$F52D:  E8        INX
$F52E:  F0 13     BEQ $F543
$F530:  C8        INY
$F531:  D0 ED     BNE $F520
$F533:  EE 06 50  INC $5006
$F536:  EE 0D 50  INC $500D
$F539:  AD 06 50  LDA $5006
$F53C:  C9 DF     CMP #$DF ('_')
$F53E:  90 E0     BCC $F520
$F540:  4C 4B D5  JMP $D54B
$F543:  EE 09 50  INC $5009
$F546:  EE 10 50  INC $5010
$F549:  D0 E5     BNE $F530
$F54B:  A2 00     LDX #$00
$F54D:  A0 00     LDY #$00
$F54F:  B9 80 D7  LDA $D780,Y
$F552:  9D 00 50  STA $5000,X
$F555:  C8        INY
$F556:  B9 80 D7  LDA $D780,Y
$F559:  9D 00 40  STA $4000,X
$F55C:  E8        INX
$F55D:  C8        INY
$F55E:  10 EF     BPL $F54F
$F560:  BA        TSX
$F561:  AC F4 43  LDY $43F4
$F564:  4C 30 C3  JMP $C330
$F567:  AD FD 43  LDA $43FD
$F56A:  29 EF     AND #$EF ('o')
$F56C:  8D FD 43  STA $43FD
$F56F:  A9 A0     LDA #$A0 (' ')
$F571:  A2 00     LDX #$00
$F573:  9D 00 40  STA $4000,X
$F576:  9D 00 50  STA $5000,X
$F579:  9D 00 41  STA $4100,X
$F57C:  9D 00 51  STA $5100,X
$F57F:  9D 00 42  STA $4200,X
$F582:  9D 00 52  STA $5200,X
$F585:  E8        INX
$F586:  D0 EB     BNE $F573
$F588:  9D 00 43  STA $4300,X
$F58B:  9D 00 53  STA $5300,X
$F58E:  E8        INX
$F58F:  E0 C0     CPX #$C0 ('@')
$F591:  90 F5     BCC $F588
$F593:  BA        TSX
$F594:  4C 30 C3  JMP $C330
$F597:  8E 03 00  STX $0003
$F59A:  8C 02 00  STY $0002
$F59D:  86 02     STX $02
$F59F:  4C 0C DF  JMP $DF0C
$F5A2:  FE CB 26  INC $26CB,X
$F5A5:  C4 4E     CPY $4E
$F5A7:  CC 76 C4  CPY $C476
$F5AA:  9E        .BYTE $9E
$F5AB:  CC C6 C4  CPY $C4C6
$F5AE:  EE CC 16  INC $16CC
$F5B1:  C5 3E     CMP $3E
$F5B3:  CD 66 C5  CMP $C566
$F5B6:  8E CD B6  STX $B6CD
$F5B9:  C5 DE     CMP $DE
$F5BB:  CD 06 C6  CMP $C606
$F5BE:  2E CE 56  ROL $56CE
$F5C1:  C6 7E     DEC $7E
$F5C3:  CE A6 C6  DEC $C6A6
$F5C6:  CE CE F6  DEC $F6CE
$F5C9:  C6 1E     DEC $1E
$F5CB:  CF        .BYTE $CF
$F5CC:  46 C7     LSR $C7
$F5CE:  6E CF 96  ROR $96CF
$F5D1:  C7        .BYTE $C7
$F5D2:  FE CB 26  INC $26CB,X
$F5D5:  C4 86     CPY $86
$F5D7:  03        .BYTE $03
$F5D8:  8C 02 00  STY $0002
$F5DB:  86 02     STX $02
$F5DD:  8D F8 53  STA $53F8
$F5E0:  AD EC 43  LDA $43EC
$F5E3:  29 0C     AND #$0C
$F5E5:  4A        LSR
$F5E6:  4A        LSR
$F5E7:  AA        TAX
$F5E8:  BD 6A D1  LDA $D16A,X
$F5EB:  8D F7 53  STA $53F7
$F5EE:  AD FA 53  LDA $53FA
$F5F1:  C9 28     CMP #$28 ('(')
$F5F3:  B0 03     BCS $F5F8
$F5F5:  4C 62 D7  JMP $D762
$F5F8:  4C CC CB  JMP $CBCC
$F5FB:  15 11     ORA $11,X
$F5FD:  80        .BYTE $80
$F5FE:  00        BRK
$F5FF:  0E A2 04  ASL $04A2
$F602:  A9 06     LDA #$06
$F604:  D0 04     BNE $F60A
$F606:  A2 09     LDX #$09
$F608:  EA        NOP
$F609:  CA        DEX
$F60A:  D0 FD     BNE $F609
$F60C:  BA        TSX
$F60D:  86 03     STX $03
$F60F:  8E 02 00  STX $0002
$F612:  38        SEC
$F613:  E9 01     SBC #$01
$F615:  D0 EF     BNE $F606
$F617:  4C A1 D3  JMP $D3A1
$F61A:  A9 05     LDA #$05
$F61C:  A2 05     LDX #$05
$F61E:  CA        DEX
$F61F:  D0 FD     BNE $F61E
$F621:  BA        TSX
$F622:  8E 03 00  STX $0003
$F625:  8E 06 00  STX $0006
$F628:  8E 02 00  STX $0002
$F62B:  4C 06 D6  JMP $D606
$F62E:  AD EF 43  LDA $43EF
$F631:  69 00     ADC #$00
$F633:  C9 18     CMP #$18
$F635:  90 1F     BCC $F656
$F637:  A9 00     LDA #$00
$F639:  EA        NOP
$F63A:  8D EF 43  STA $43EF
$F63D:  EA        NOP
$F63E:  EA        NOP
$F63F:  A9 00     LDA #$00
$F641:  8D FE 53  STA $53FE
$F644:  BA        TSX
$F645:  8E 03 00  STX $0003
$F648:  8E 02 00  STX $0002
$F64B:  A9 03     LDA #$03
$F64D:  8D E8 43  STA $43E8
$F650:  A9 01     LDA #$01
$F652:  A2 08     LDX #$08
$F654:  D0 06     BNE $F65C
$F656:  90 E2     BCC $F63A
$F658:  A2 09     LDX #$09
$F65A:  EA        NOP
$F65B:  CA        DEX
$F65C:  D0 FD     BNE $F65B
$F65E:  BA        TSX
$F65F:  86 03     STX $03
$F661:  8E 02 00  STX $0002
$F664:  38        SEC
$F665:  E9 01     SBC #$01
$F667:  D0 EF     BNE $F658
$F669:  EA        NOP
$F66A:  AD E8 43  LDA $43E8
$F66D:  A2 07     LDX #$07
$F66F:  D0 AE     BNE $F61F
$F671:  A9 04     LDA #$04
$F673:  8D E8 43  STA $43E8
$F676:  A9 01     LDA #$01
$F678:  A2 03     LDX #$03
$F67A:  D0 DE     BNE $F65A
$F67C:  A9 02     LDA #$02
$F67E:  8D E8 43  STA $43E8
$F681:  A9 03     LDA #$03
$F683:  A2 03     LDX #$03
$F685:  D0 D3     BNE $F65A
$F687:  A9 05     LDA #$05
$F689:  A2 04     LDX #$04
$F68B:  D0 04     BNE $F691
$F68D:  A2 09     LDX #$09
$F68F:  EA        NOP
$F690:  CA        DEX
$F691:  D0 FD     BNE $F690
$F693:  BA        TSX
$F694:  86 03     STX $03
$F696:  8E 02 00  STX $0002
$F699:  38        SEC
$F69A:  E9 01     SBC #$01
$F69C:  D0 EF     BNE $F68D
$F69E:  A2 09     LDX #$09
$F6A0:  CA        DEX
$F6A1:  D0 FD     BNE $F6A0
$F6A3:  BA        TSX
$F6A4:  EA        NOP
$F6A5:  8E 03 00  STX $0003
$F6A8:  8E 06 00  STX $0006
$F6AB:  8E 02 00  STX $0002
$F6AE:  EA        NOP
$F6AF:  4C A1 D3  JMP $D3A1
$F6B2:  A9 06     LDA #$06
$F6B4:  A2 04     LDX #$04
$F6B6:  D0 04     BNE $F6BC
$F6B8:  A2 09     LDX #$09
$F6BA:  EA        NOP
$F6BB:  CA        DEX
$F6BC:  D0 FD     BNE $F6BB
$F6BE:  BA        TSX
$F6BF:  86 03     STX $03
$F6C1:  8E 02 00  STX $0002
$F6C4:  38        SEC
$F6C5:  E9 01     SBC #$01
$F6C7:  D0 EF     BNE $F6B8
$F6C9:  AD EF 43  LDA $43EF
$F6CC:  0A        ASL
$F6CD:  69 04     ADC #$04
$F6CF:  AA        TAX
$F6D0:  EA        NOP
$F6D1:  AD F4 43  LDA $43F4
$F6D4:  69 10     ADC #$10
$F6D6:  8D F4 43  STA $43F4
$F6D9:  BD A2 D5  LDA $D5A2,X
$F6DC:  8D F7 53  STA $53F7
$F6DF:  BD A3 D5  LDA $D5A3,X
$F6E2:  8D F8 53  STA $53F8
$F6E5:  A2 02     LDX #$02
$F6E7:  CA        DEX
$F6E8:  D0 FD     BNE $F6E7
$F6EA:  BA        TSX
$F6EB:  86 07     STX $07
$F6ED:  8E 02 00  STX $0002
$F6F0:  4C CA D3  JMP $D3CA
$F6F3:  EA        NOP
$F6F4:  AD FD 43  LDA $43FD
$F6F7:  49 80     EOR #$80
$F6F9:  8D FD 43  STA $43FD
$F6FC:  A9 03     LDA #$03
$F6FE:  A2 03     LDX #$03
$F700:  D0 04     BNE $F706
$F702:  A2 08     LDX #$08
$F704:  EA        NOP
$F705:  EA        NOP
$F706:  CA        DEX
$F707:  D0 FD     BNE $F706
$F709:  BA        TSX
$F70A:  86 03     STX $03
$F70C:  8C 02 00  STY $0002
$F70F:  86 02     STX $02
$F711:  38        SEC
$F712:  E9 01     SBC #$01
$F714:  D0 EC     BNE $F702
$F716:  A9 03     LDA #$03
$F718:  A2 07     LDX #$07
$F71A:  EA        NOP
$F71B:  38        SEC
$F71C:  CA        DEX
$F71D:  D0 FD     BNE $F71C
$F71F:  BA        TSX
$F720:  B0 09     BCS $F72B
$F722:  A2 09     LDX #$09
$F724:  CA        DEX
$F725:  D0 FD     BNE $F724
$F727:  EA        NOP
$F728:  BA        TSX
$F729:  86 02     STX $02
$F72B:  8E 03 00  STX $0003
$F72E:  38        SEC
$F72F:  E9 01     SBC #$01
$F731:  D0 EF     BNE $F722
$F733:  A2 09     LDX #$09
$F735:  CA        DEX
$F736:  D0 FD     BNE $F735
$F738:  BA        TSX
$F739:  A9 03     LDA #$03
$F73B:  8E 02 00  STX $0002
$F73E:  8E 03 00  STX $0003
$F741:  8C 02 00  STY $0002
$F744:  86 02     STX $02
$F746:  38        SEC
$F747:  E9 01     SBC #$01
$F749:  F0 0C     BEQ $F757
$F74B:  A2 07     LDX #$07
$F74D:  CA        DEX
$F74E:  D0 FD     BNE $F74D
$F750:  EA        NOP
$F751:  EA        NOP
$F752:  EA        NOP
$F753:  BA        TSX
$F754:  4C 3E D7  JMP $D73E
$F757:  38        SEC
$F758:  A9 0B     LDA #$0B
$F75A:  A2 06     LDX #$06
$F75C:  EA        NOP
$F75D:  EA        NOP
$F75E:  EA        NOP
$F75F:  4C 8B C2  JMP $C28B
$F762:  AA        TAX
$F763:  D0 14     BNE $F779
$F765:  8D F9 53  STA $53F9
$F768:  8C FC 53  STY $53FC
$F76B:  EA        NOP
$F76C:  EA        NOP
$F76D:  BA        TSX
$F76E:  8E 03 00  STX $0003
$F771:  8C 02 00  STY $0002
$F774:  86 02     STX $02
$F776:  6C F7 53  JMP ($53F7)
$F779:  D0 ED     BNE $F768
$F77B:  42        .BYTE $42
$F77C:  4F        .BYTE $4F
$F77D:  4C 53 00  JMP $0053
$F780:  68        PLA
$F781:  9D 00 5C  STA $5C00,X
$F784:  68        PLA
$F785:  9D 00 58  STA $5800,X
$F788:  68        PLA
$F789:  9D 00 54  STA $5400,X
$F78C:  68        PLA
$F78D:  9D 00 50  STA $5000,X
$F790:  68        PLA
$F791:  9D 00 4C  STA $4C00,X
$F794:  68        PLA
$F795:  9D 00 48  STA $4800,X
$F798:  68        PLA
$F799:  9D 00 44  STA $4400,X
$F79C:  68        PLA
$F79D:  9D 00 40  STA $4000,X
$F7A0:  68        PLA
$F7A1:  9D 00 3C  STA $3C00,X
$F7A4:  68        PLA
$F7A5:  9D 00 38  STA $3800,X
$F7A8:  68        PLA
$F7A9:  9D 00 34  STA $3400,X
$F7AC:  68        PLA
$F7AD:  9D 00 30  STA $3000,X
$F7B0:  68        PLA
$F7B1:  9D 00 2C  STA $2C00,X
$F7B4:  68        PLA
$F7B5:  9D 00 28  STA $2800,X
$F7B8:  68        PLA
$F7B9:  9D 00 24  STA $2400,X
$F7BC:  68        PLA
$F7BD:  9D 00 20  STA $2000,X
$F7C0:  4C C0 DF  JMP $DFC0
$F7C3:  00        BRK
$F7C4:  08        PHP
$F7C5:  10 18     BPL $F7DF
$F7C7:  20 28 00  JSR $0028
$F7CA:  00        BRK
$F7CB:  30 38     BMI $F805
$F7CD:  40        RTI
$F7CE:  48        PHA
$F7CF:  50 58     BVC $F829
$F7D1:  00        BRK
$F7D2:  00        BRK
$F7D3:  60        RTS
$F7D4:  68        PLA
$F7D5:  70 78     BVS $F84F
$F7D7:  80        .BYTE $80
$F7D8:  88        DEY
$F7D9:  00        BRK
$F7DA:  00        BRK
$F7DB:  90 98     BCC $F775
$F7DD:  A0 FF     LDY #$FF
$F7DF:  FF        .BYTE $FF
$F7E0:  FF        .BYTE $FF
$F7E1:  FF        .BYTE $FF
$F7E2:  FF        .BYTE $FF
$F7E3:  FF        .BYTE $FF
$F7E4:  FF        .BYTE $FF
$F7E5:  FF        .BYTE $FF
$F7E6:  FF        .BYTE $FF
$F7E7:  FF        .BYTE $FF
$F7E8:  FF        .BYTE $FF
$F7E9:  FF        .BYTE $FF
$F7EA:  FF        .BYTE $FF
$F7EB:  FF        .BYTE $FF
$F7EC:  FF        .BYTE $FF
$F7ED:  FF        .BYTE $FF
$F7EE:  FF        .BYTE $FF
$F7EF:  FF        .BYTE $FF
$F7F0:  FF        .BYTE $FF
$F7F1:  FF        .BYTE $FF
$F7F2:  FF        .BYTE $FF
$F7F3:  FF        .BYTE $FF
$F7F4:  FF        .BYTE $FF
$F7F5:  FF        .BYTE $FF
$F7F6:  FF        .BYTE $FF
$F7F7:  FF        .BYTE $FF
$F7F8:  FF        .BYTE $FF
$F7F9:  FF        .BYTE $FF
$F7FA:  FF        .BYTE $FF
$F7FB:  FF        .BYTE $FF
$F7FC:  FF        .BYTE $FF
$F7FD:  FF        .BYTE $FF
$F7FE:  FF        .BYTE $FF
$F7FF:  FF        .BYTE $FF
$F800:  00        BRK ; [PLOT]
$F801:  00        BRK
$F802:  00        BRK
$F803:  00        BRK
$F804:  00        BRK
$F805:  00        BRK
$F806:  00        BRK
$F807:  00        BRK
$F808:  00        BRK
$F809:  00        BRK
$F80A:  00        BRK
$F80B:  00        BRK
$F80C:  00        BRK
$F80D:  00        BRK
$F80E:  00        BRK
$F80F:  FF        .BYTE $FF
$F810:  FF        .BYTE $FF
$F811:  FF        .BYTE $FF
$F812:  FF        .BYTE $FF
$F813:  FF        .BYTE $FF
$F814:  FF        .BYTE $FF
$F815:  FF        .BYTE $FF
$F816:  FF        .BYTE $FF
$F817:  FF        .BYTE $FF
$F818:  FF        .BYTE $FF
$F819:  FF        .BYTE $FF ; [HLINE]
$F81A:  FF        .BYTE $FF
$F81B:  FF        .BYTE $FF
$F81C:  FF        .BYTE $FF
$F81D:  FF        .BYTE $FF
$F81E:  FF        .BYTE $FF
$F81F:  FF        .BYTE $FF
$F820:  FF        .BYTE $FF
$F821:  FF        .BYTE $FF
$F822:  FF        .BYTE $FF
$F823:  FF        .BYTE $FF
$F824:  FF        .BYTE $FF
$F825:  FF        .BYTE $FF
$F826:  FF        .BYTE $FF
$F827:  FF        .BYTE $FF
$F828:  FF        .BYTE $FF ; [VLINE]
$F829:  FF        .BYTE $FF
$F82A:  FF        .BYTE $FF
$F82B:  FF        .BYTE $FF
$F82C:  FF        .BYTE $FF
$F82D:  FF        .BYTE $FF
$F82E:  FF        .BYTE $FF
$F82F:  FF        .BYTE $FF
$F830:  FF        .BYTE $FF
$F831:  FF        .BYTE $FF
$F832:  FF        .BYTE $FF ; [CLRSCR]
$F833:  FF        .BYTE $FF
$F834:  FF        .BYTE $FF
$F835:  FF        .BYTE $FF
$F836:  FF        .BYTE $FF ; [CLRTOP]
$F837:  FF        .BYTE $FF
$F838:  FF        .BYTE $FF
$F839:  FF        .BYTE $FF
$F83A:  FF        .BYTE $FF
$F83B:  FF        .BYTE $FF
$F83C:  FF        .BYTE $FF
$F83D:  FF        .BYTE $FF
$F83E:  FF        .BYTE $FF
$F83F:  FF        .BYTE $FF
$F840:  00        BRK
$F841:  01 42     ORA ($42,X)
$F843:  63        .BYTE $63
$F844:  04        .BYTE $04
$F845:  65 66     ADC $66
$F847:  07        .BYTE $07
$F848:  48        PHA
$F849:  09 6A     ORA #$6A ('j')
$F84B:  6B        .BYTE $6B
$F84C:  6C 6D 6E  JMP ($6E6D)
$F84F:  6F        .BYTE $6F
$F850:  70 11     BVS $F863
$F852:  12        .BYTE $12
$F853:  53        .BYTE $53
$F854:  74        .BYTE $74
$F855:  15 56     ORA $56,X
$F857:  17        .BYTE $17
$F858:  18        CLC
$F859:  59 1A 1B  EOR $1B1A,Y
$F85C:  1C        .BYTE $1C
$F85D:  1D 1E 00  ORA $001E,X
$F860:  00        BRK
$F861:  00        BRK
$F862:  C2        .BYTE $C2
$F863:  E3        .BYTE $E3
$F864:  C4 E5     CPY $E5
$F866:  C6 E7     DEC $E7
$F868:  00        BRK
$F869:  00        BRK
$F86A:  CA        DEX
$F86B:  EB        .BYTE $EB
$F86C:  8C AD AE  STY $AEAD
$F86F:  AF        .BYTE $AF
$F870:  00        BRK
$F871:  00        BRK
$F872:  92        .BYTE $92
$F873:  93        .BYTE $93
$F874:  B4 B5     LDY $B5,X
$F876:  B6 97     LDX $97,Y
$F878:  00        BRK
$F879:  00        BRK
$F87A:  9A        TXS
$F87B:  BB        .BYTE $BB
$F87C:  DC        .BYTE $DC
$F87D:  00        BRK
$F87E:  00        BRK
$F87F:  00        BRK
$F880:  80        .BYTE $80
$F881:  80        .BYTE $80
$F882:  80        .BYTE $80
$F883:  80        .BYTE $80
$F884:  80        .BYTE $80
$F885:  80        .BYTE $80
$F886:  80        .BYTE $80
$F887:  80        .BYTE $80
$F888:  88        DEY
$F889:  88        DEY
$F88A:  88        DEY
$F88B:  88        DEY
$F88C:  88        DEY
$F88D:  88        DEY
$F88E:  80        .BYTE $80
$F88F:  88        DEY
$F890:  B6 A4     LDX $A4,Y
$F892:  92        .BYTE $92
$F893:  80        .BYTE $80
$F894:  80        .BYTE $80
$F895:  80        .BYTE $80
$F896:  80        .BYTE $80
$F897:  80        .BYTE $80
$F898:  94 94     STY $94,X
$F89A:  BE 94 94  LDX $9494,Y
$F89D:  BE 94 94  LDX $9494,Y
$F8A0:  80        .BYTE $80
$F8A1:  88        DEY
$F8A2:  BC 8A 9C  LDY $9C8A,X
$F8A5:  A8        TAY
$F8A6:  9E        .BYTE $9E
$F8A7:  88        DEY
$F8A8:  80        .BYTE $80
$F8A9:  A3        .BYTE $A3
$F8AA:  93        .BYTE $93
$F8AB:  88        DEY
$F8AC:  84 B2     STY $B2
$F8AE:  B1 80     LDA ($80),Y
$F8B0:  84 8A     STY $8A
$F8B2:  8A        TXA
$F8B3:  A4 AA     LDY $AA
$F8B5:  A9 91     LDA #$91
$F8B7:  AE 98 90  LDX $9098
$F8BA:  88        DEY
$F8BB:  80        .BYTE $80
$F8BC:  80        .BYTE $80
$F8BD:  80        .BYTE $80
$F8BE:  80        .BYTE $80
$F8BF:  80        .BYTE $80
$F8C0:  98        TYA
$F8C1:  84 82     STY $82
$F8C3:  82        .BYTE $82
$F8C4:  82        .BYTE $82
$F8C5:  82        .BYTE $82
$F8C6:  84 98     STY $98
$F8C8:  8C 90 A0  STY $A090
$F8CB:  A0 A0     LDY #$A0 (' ')
$F8CD:  A0 90     LDY #$90
$F8CF:  8C 80 88  STY $8880
$F8D2:  AA        TAX
$F8D3:  9C        .BYTE $9C
$F8D4:  88        DEY
$F8D5:  9C        .BYTE $9C
$F8D6:  AA        TAX
$F8D7:  88        DEY
$F8D8:  80        .BYTE $80
$F8D9:  88        DEY
$F8DA:  88        DEY
$F8DB:  88        DEY
$F8DC:  BE 88 88  LDX $8888,Y
$F8DF:  88        DEY
$F8E0:  00        BRK
$F8E1:  80        .BYTE $80
$F8E2:  80        .BYTE $80
$F8E3:  80        .BYTE $80
$F8E4:  80        .BYTE $80
$F8E5:  8C 88 84  STY $8488
$F8E8:  80        .BYTE $80
$F8E9:  80        .BYTE $80
$F8EA:  80        .BYTE $80
$F8EB:  80        .BYTE $80
$F8EC:  BE 80 80  LDX $8080,Y
$F8EF:  80        .BYTE $80
$F8F0:  80        .BYTE $80
$F8F1:  80        .BYTE $80
$F8F2:  80        .BYTE $80
$F8F3:  80        .BYTE $80
$F8F4:  80        .BYTE $80
$F8F5:  80        .BYTE $80
$F8F6:  88        DEY
$F8F7:  88        DEY
$F8F8:  80        .BYTE $80
$F8F9:  A0 90     LDY #$90
$F8FB:  88        DEY
$F8FC:  84 82     STY $82
$F8FE:  81 80     STA ($80,X)
$F900:  9C        .BYTE $9C
$F901:  A2 B2     LDX #$B2 ('2')
$F903:  AA        TAX
$F904:  A6 A2     LDX $A2
$F906:  A2 9C     LDX #$9C
$F908:  88        DEY
$F909:  8C 88 88  STY $8888
$F90C:  88        DEY
$F90D:  88        DEY
$F90E:  88        DEY
$F90F:  9C        .BYTE $9C
$F910:  9C        .BYTE $9C
$F911:  A2 A0     LDX #$A0 (' ')
$F913:  A0 9C     LDY #$9C
$F915:  82        .BYTE $82
$F916:  82        .BYTE $82
$F917:  BE BE 90  LDX $90BE,Y
$F91A:  88        DEY
$F91B:  9C        .BYTE $9C
$F91C:  A0 A0     LDY #$A0 (' ')
$F91E:  A2 9C     LDX #$9C
$F920:  B0 88     BCS $F8AA
$F922:  84 92     STY $92
$F924:  92        .BYTE $92
$F925:  BE 90 90  LDX $9090,Y
$F928:  BE 82 82  LDX $8282,Y
$F92B:  9E        .BYTE $9E
$F92C:  A0 A0     LDY #$A0 (' ')
$F92E:  A2 9C     LDX #$9C
$F930:  B8        CLV
$F931:  84 82     STY $82
$F933:  9E        .BYTE $9E
$F934:  A2 A2     LDX #$A2 ('"')
$F936:  A2 9C     LDX #$9C
$F938:  BE A0 A0  LDX $A0A0,Y
$F93B:  A0 90     LDY #$90
$F93D:  88        DEY
$F93E:  84 84     STY $84
$F940:  9C        .BYTE $9C
$F941:  A2 A2     LDX #$A2 ('"')
$F943:  9C        .BYTE $9C
$F944:  A2 A2     LDX #$A2 ('"')
$F946:  A2 9C     LDX #$9C
$F948:  9C        .BYTE $9C
$F949:  A2 A2     LDX #$A2 ('"')
$F94B:  A2 BC     LDX #$BC ('<')
$F94D:  A0 A2     LDY #$A2 ('"')
$F94F:  9C        .BYTE $9C
$F950:  80        .BYTE $80
$F951:  88        DEY
$F952:  88        DEY
$F953:  80        .BYTE $80
$F954:  80        .BYTE $80
$F955:  88        DEY
$F956:  88        DEY
$F957:  80        .BYTE $80
$F958:  80        .BYTE $80
$F959:  88        DEY
$F95A:  88        DEY
$F95B:  80        .BYTE $80
$F95C:  80        .BYTE $80
$F95D:  88        DEY
$F95E:  88        DEY
$F95F:  84 80     STY $80
$F961:  90 88     BCC $F8EB
$F963:  84 82     STY $82
$F965:  84 88     STY $88
$F967:  90 80     BCC $F8E9
$F969:  80        .BYTE $80
$F96A:  80        .BYTE $80
$F96B:  BE 80 BE  LDX $BE80,Y
$F96E:  80        .BYTE $80
$F96F:  80        .BYTE $80
$F970:  80        .BYTE $80
$F971:  82        .BYTE $82
$F972:  84 88     STY $88
$F974:  90 88     BCC $F8FE
$F976:  84 82     STY $82
$F978:  9C        .BYTE $9C
$F979:  A2 A0     LDX #$A0 (' ')
$F97B:  98        TYA
$F97C:  88        DEY
$F97D:  80        .BYTE $80
$F97E:  88        DEY
$F97F:  88        DEY
$F980:  9C        .BYTE $9C
$F981:  A2 B2     LDX #$B2 ('2')
$F983:  AA        TAX
$F984:  AA        TAX
$F985:  9A        TXS
$F986:  82        .BYTE $82
$F987:  BC 88 94  LDY $9488,X
$F98A:  A2 A2     LDX #$A2 ('"')
$F98C:  BE A2 A2  LDX $A2A2,Y
$F98F:  A2 9E     LDX #$9E
$F991:  A2 A2     LDX #$A2 ('"')
$F993:  9E        .BYTE $9E
$F994:  A2 A2     LDX #$A2 ('"')
$F996:  A2 9E     LDX #$9E
$F998:  9C        .BYTE $9C
$F999:  A2 82     LDX #$82
$F99B:  82        .BYTE $82
$F99C:  82        .BYTE $82
$F99D:  82        .BYTE $82
$F99E:  A2 9C     LDX #$9C
$F9A0:  8E 92 A2  STX $A292
$F9A3:  A2 A2     LDX #$A2 ('"')
$F9A5:  A2 92     LDX #$92
$F9A7:  8E BE 82  STX $82BE
$F9AA:  82        .BYTE $82
$F9AB:  9E        .BYTE $9E
$F9AC:  82        .BYTE $82
$F9AD:  82        .BYTE $82
$F9AE:  82        .BYTE $82
$F9AF:  BE BE 82  LDX $82BE,Y
$F9B2:  82        .BYTE $82
$F9B3:  9E        .BYTE $9E
$F9B4:  82        .BYTE $82
$F9B5:  82        .BYTE $82
$F9B6:  82        .BYTE $82
$F9B7:  82        .BYTE $82
$F9B8:  9C        .BYTE $9C
$F9B9:  A2 82     LDX #$82
$F9BB:  82        .BYTE $82
$F9BC:  BA        TSX
$F9BD:  A2 A2     LDX #$A2 ('"')
$F9BF:  9C        .BYTE $9C
$F9C0:  A2 A2     LDX #$A2 ('"')
$F9C2:  A2 BE     LDX #$BE ('>')
$F9C4:  A2 A2     LDX #$A2 ('"')
$F9C6:  A2 A2     LDX #$A2 ('"')
$F9C8:  9C        .BYTE $9C
$F9C9:  88        DEY
$F9CA:  88        DEY
$F9CB:  88        DEY
$F9CC:  88        DEY
$F9CD:  88        DEY
$F9CE:  88        DEY
$F9CF:  9C        .BYTE $9C
$F9D0:  B8        CLV
$F9D1:  90 90     BCC $F963
$F9D3:  90 90     BCC $F965
$F9D5:  90 92     BCC $F969
$F9D7:  8C A2 92  STY $92A2
$F9DA:  8A        TXA
$F9DB:  86 86     STX $86
$F9DD:  8A        TXA
$F9DE:  92        .BYTE $92
$F9DF:  A2 82     LDX #$82
$F9E1:  82        .BYTE $82
$F9E2:  82        .BYTE $82
$F9E3:  82        .BYTE $82
$F9E4:  82        .BYTE $82
$F9E5:  82        .BYTE $82
$F9E6:  82        .BYTE $82
$F9E7:  BE A2 B6  LDX $B6A2,Y
$F9EA:  AA        TAX
$F9EB:  A2 A2     LDX #$A2 ('"')
$F9ED:  A2 A2     LDX #$A2 ('"')
$F9EF:  A2 A2     LDX #$A2 ('"')
$F9F1:  A2 A6     LDX #$A6 ('&')
$F9F3:  AA        TAX
$F9F4:  B2        .BYTE $B2
$F9F5:  A2 A2     LDX #$A2 ('"')
$F9F7:  A2 9C     LDX #$9C
$F9F9:  A2 A2     LDX #$A2 ('"')
$F9FB:  A2 A2     LDX #$A2 ('"')
$F9FD:  A2 A2     LDX #$A2 ('"')
$F9FF:  9C        .BYTE $9C
$FA00:  9E        .BYTE $9E
$FA01:  A2 A2     LDX #$A2 ('"')
$FA03:  A2 9E     LDX #$9E
$FA05:  82        .BYTE $82
$FA06:  82        .BYTE $82
$FA07:  82        .BYTE $82
$FA08:  9C        .BYTE $9C
$FA09:  A2 A2     LDX #$A2 ('"')
$FA0B:  A2 AA     LDX #$AA ('*')
$FA0D:  B6 92     LDX $92,Y
$FA0F:  AC 9E A2  LDY $A29E
$FA12:  A2 A2     LDX #$A2 ('"')
$FA14:  9E        .BYTE $9E
$FA15:  92        .BYTE $92
$FA16:  A2 A2     LDX #$A2 ('"')
$FA18:  9C        .BYTE $9C
$FA19:  A2 82     LDX #$82
$FA1B:  9C        .BYTE $9C
$FA1C:  A0 A0     LDY #$A0 (' ')
$FA1E:  A2 9C     LDX #$9C
$FA20:  BE 88 88  LDX $8888,Y
$FA23:  88        DEY
$FA24:  88        DEY
$FA25:  88        DEY
$FA26:  88        DEY
$FA27:  88        DEY
$FA28:  A2 A2     LDX #$A2 ('"')
$FA2A:  A2 A2     LDX #$A2 ('"')
$FA2C:  A2 A2     LDX #$A2 ('"')
$FA2E:  A2 9C     LDX #$9C
$FA30:  A2 A2     LDX #$A2 ('"')
$FA32:  A2 A2     LDX #$A2 ('"')
$FA34:  A2 A2     LDX #$A2 ('"')
$FA36:  94 88     STY $88,X
$FA38:  A2 A2     LDX #$A2 ('"')
$FA3A:  A2 A2     LDX #$A2 ('"')
$FA3C:  AA        TAX
$FA3D:  AA        TAX
$FA3E:  B6 A2     LDX $A2,Y
$FA40:  A2 A2     LDX #$A2 ('"')
$FA42:  94 88     STY $88,X
$FA44:  94 A2     STY $A2,X
$FA46:  A2 A2     LDX #$A2 ('"')
$FA48:  A2 A2     LDX #$A2 ('"')
$FA4A:  94 88     STY $88,X
$FA4C:  88        DEY
$FA4D:  88        DEY
$FA4E:  88        DEY
$FA4F:  88        DEY
$FA50:  BE A0 90  LDX $90A0,Y
$FA53:  88        DEY
$FA54:  88        DEY
$FA55:  84 82     STY $82
$FA57:  BE 9C 84  LDX $849C,Y
$FA5A:  84 84     STY $84
$FA5C:  84 84     STY $84
$FA5E:  84 9C     STY $9C
$FA60:  80        .BYTE $80
$FA61:  81 82     STA ($82,X)
$FA63:  84 88     STY $88
$FA65:  90 A0     BCC $FA07
$FA67:  80        .BYTE $80
$FA68:  9C        .BYTE $9C
$FA69:  90 90     BCC $F9FB
$FA6B:  90 90     BCC $F9FD
$FA6D:  90 90     BCC $F9FF
$FA6F:  9C        .BYTE $9C
$FA70:  80        .BYTE $80
$FA71:  80        .BYTE $80
$FA72:  88        DEY
$FA73:  94 A2     STY $A2,X
$FA75:  80        .BYTE $80
$FA76:  80        .BYTE $80
$FA77:  80        .BYTE $80
$FA78:  80        .BYTE $80
$FA79:  80        .BYTE $80
$FA7A:  80        .BYTE $80
$FA7B:  80        .BYTE $80
$FA7C:  80        .BYTE $80
$FA7D:  80        .BYTE $80
$FA7E:  80        .BYTE $80
$FA7F:  BF        .BYTE $BF
$FA80:  8C 84 88  STY $8884
$FA83:  80        .BYTE $80
$FA84:  80        .BYTE $80
$FA85:  80        .BYTE $80
$FA86:  80        .BYTE $80
$FA87:  80        .BYTE $80
$FA88:  80        .BYTE $80
$FA89:  80        .BYTE $80
$FA8A:  9E        .BYTE $9E
$FA8B:  A0 9C     LDY #$9C
$FA8D:  A2 A2     LDX #$A2 ('"')
$FA8F:  DC        .BYTE $DC
$FA90:  82        .BYTE $82
$FA91:  82        .BYTE $82
$FA92:  9A        TXS
$FA93:  A6 A2     LDX $A2
$FA95:  A2 A2     LDX #$A2 ('"')
$FA97:  9E        .BYTE $9E
$FA98:  80        .BYTE $80
$FA99:  80        .BYTE $80
$FA9A:  BC 82 82  LDY $8282,X
$FA9D:  82        .BYTE $82
$FA9E:  82        .BYTE $82
$FA9F:  BC A0 A0  LDY $A0A0,X
$FAA2:  AC B2 A2  LDY $A2B2
$FAA5:  A2 A2     LDX #$A2 ('"')
$FAA7:  BC 80 80  LDY $8080,X
$FAAA:  9C        .BYTE $9C
$FAAB:  A2 92     LDX #$92
$FAAD:  8E A2 9C  STX $9CA2
$FAB0:  98        TYA
$FAB1:  A4 84     LDY $84
$FAB3:  8E 84 84  STX $8484
$FAB6:  84 84     STY $84
$FAB8:  20 9C A2  JSR $A29C
$FABB:  A2 BC     LDX #$BC ('<')
$FABD:  A0 A0     LDY #$A0 (' ')
$FABF:  9E        .BYTE $9E
$FAC0:  82        .BYTE $82
$FAC1:  82        .BYTE $82
$FAC2:  82        .BYTE $82
$FAC3:  9E        .BYTE $9E
$FAC4:  A2 A2     LDX #$A2 ('"')
$FAC6:  A2 A2     LDX #$A2 ('"')
$FAC8:  88        DEY
$FAC9:  80        .BYTE $80
$FACA:  88        DEY
$FACB:  88        DEY
$FACC:  88        DEY
$FACD:  88        DEY
$FACE:  88        DEY
$FACF:  88        DEY
$FAD0:  08        PHP
$FAD1:  80        .BYTE $80
$FAD2:  88        DEY
$FAD3:  88        DEY
$FAD4:  88        DEY
$FAD5:  88        DEY
$FAD6:  88        DEY
$FAD7:  86 82     STX $82
$FAD9:  82        .BYTE $82
$FADA:  A2 92     LDX #$92
$FADC:  8A        TXA
$FADD:  8E 92 A2  STX $A292
$FAE0:  8C 88 88  STY $8888
$FAE3:  88        DEY
$FAE4:  88        DEY
$FAE5:  88        DEY
$FAE6:  88        DEY
$FAE7:  90 80     BCC $FA69
$FAE9:  80        .BYTE $80
$FAEA:  94 AA     STY $AA,X
$FAEC:  AA        TAX
$FAED:  AA        TAX
$FAEE:  AA        TAX
$FAEF:  AA        TAX
$FAF0:  80        .BYTE $80
$FAF1:  80        .BYTE $80
$FAF2:  9A        TXS
$FAF3:  A4 A4     LDY $A4
$FAF5:  A4 A4     LDY $A4
$FAF7:  A4 80     LDY $80
$FAF9:  80        .BYTE $80
$FAFA:  9C        .BYTE $9C
$FAFB:  A2 A2     LDX #$A2 ('"')
$FAFD:  A2 A2     LDX #$A2 ('"')
$FAFF:  9C        .BYTE $9C
$FB00:  1E A2 A2  ASL $A2A2,X
$FB03:  A2 9E     LDX #$9E
$FB05:  82        .BYTE $82
$FB06:  82        .BYTE $82
$FB07:  82        .BYTE $82
$FB08:  3C        .BYTE $3C
$FB09:  A2 A2     LDX #$A2 ('"')
$FB0B:  A2 BC     LDX #$BC ('<')
$FB0D:  A0 A0     LDY #$A0 (' ')
$FB0F:  A0 80     LDY #$80
$FB11:  80        .BYTE $80
$FB12:  BA        TSX
$FB13:  86 82     STX $82
$FB15:  82        .BYTE $82
$FB16:  82        .BYTE $82
$FB17:  82        .BYTE $82
$FB18:  80        .BYTE $80
$FB19:  80        .BYTE $80
$FB1A:  BC 82 9C  LDY $9C82,X
$FB1D:  A0 A0     LDY #$A0 (' ')
$FB1F:  9E        .BYTE $9E
$FB20:  88        DEY
$FB21:  88        DEY
$FB22:  BE 88 88  LDX $8888,Y
$FB25:  88        DEY
$FB26:  88        DEY
$FB27:  B0 80     BCS $FAA9
$FB29:  80        .BYTE $80
$FB2A:  A2 A2     LDX #$A2 ('"')
$FB2C:  A2 A2     LDX #$A2 ('"')
$FB2E:  A2 9C     LDX #$9C
$FB30:  80        .BYTE $80
$FB31:  80        .BYTE $80
$FB32:  A2 A2     LDX #$A2 ('"')
$FB34:  A2 A2     LDX #$A2 ('"')
$FB36:  94 88     STY $88,X
$FB38:  80        .BYTE $80
$FB39:  80        .BYTE $80 ; [SETGR]
$FB3A:  A2 A2     LDX #$A2 ('"')
$FB3C:  A2 AA     LDX #$AA ('*')
$FB3E:  AA        TAX
$FB3F:  94 80     STY $80,X
$FB41:  80        .BYTE $80
$FB42:  A2 94     LDX #$94
$FB44:  88        DEY
$FB45:  94 A2     STY $A2,X
$FB47:  A2 22     LDX #$22 ('"')
$FB49:  A2 A2     LDX #$A2 ('"')
$FB4B:  A2 BC     LDX #$BC ('<')
$FB4D:  A0 A0     LDY #$A0 (' ')
$FB4F:  9E        .BYTE $9E
$FB50:  80        .BYTE $80
$FB51:  80        .BYTE $80
$FB52:  BE 90 88  LDX $8890,Y
$FB55:  84 82     STY $82
$FB57:  BE 80 98  LDX $9880,Y
$FB5A:  84 88     STY $88
$FB5C:  86 88     STX $88
$FB5E:  84 98     STY $98
$FB60:  80        .BYTE $80
$FB61:  88        DEY
$FB62:  88        DEY
$FB63:  88        DEY
$FB64:  80        .BYTE $80
$FB65:  88        DEY
$FB66:  88        DEY
$FB67:  88        DEY
$FB68:  80        .BYTE $80
$FB69:  8C 90 88  STY $8890
$FB6C:  B0 88     BCS $FAF6
$FB6E:  90 8C     BCC $FAFC
$FB70:  80        .BYTE $80
$FB71:  80        .BYTE $80
$FB72:  80        .BYTE $80
$FB73:  84 AA     STY $AA
$FB75:  90 80     BCC $FAF7
$FB77:  80        .BYTE $80
$FB78:  A2 A2     LDX #$A2 ('"')
$FB7A:  FF        .BYTE $FF
$FB7B:  A2 FF     LDX #$FF
$FB7D:  AA        TAX
$FB7E:  B6 A2     LDX $A2,Y
$FB80:  87        .BYTE $87
$FB81:  84 84     STY $84
$FB83:  84 84     STY $84
$FB85:  82        .BYTE $82
$FB86:  81 80     STA ($80,X)
$FB88:  87        .BYTE $87
$FB89:  86 86     STX $86
$FB8B:  86 86     STX $86
$FB8D:  83        .BYTE $83
$FB8E:  83        .BYTE $83
$FB8F:  80        .BYTE $80
$FB90:  80        .BYTE $80
$FB91:  80        .BYTE $80
$FB92:  80        .BYTE $80
$FB93:  80        .BYTE $80
$FB94:  80        .BYTE $80
$FB95:  80        .BYTE $80
$FB96:  80        .BYTE $80
$FB97:  80        .BYTE $80
$FB98:  80        .BYTE $80
$FB99:  81 81     STA ($81,X)
$FB9B:  81 81     STA ($81,X)
$FB9D:  81 8F     STA ($8F,X)
$FB9F:  80        .BYTE $80
$FBA0:  80        .BYTE $80
$FBA1:  87        .BYTE $87
$FBA2:  81 81     STA ($81,X)
$FBA4:  81 81     STA ($81,X)
$FBA6:  8F        .BYTE $8F
$FBA7:  80        .BYTE $80
$FBA8:  80        .BYTE $80
$FBA9:  87        .BYTE $87
$FBAA:  83        .BYTE $83
$FBAB:  83        .BYTE $83
$FBAC:  83        .BYTE $83
$FBAD:  83        .BYTE $83
$FBAE:  8F        .BYTE $8F
$FBAF:  80        .BYTE $80
$FBB0:  87        .BYTE $87
$FBB1:  84 84     STY $84
$FBB3:  87        .BYTE $87
$FBB4:  81 81     STA ($81,X)
$FBB6:  8F        .BYTE $8F
$FBB7:  80        .BYTE $80
$FBB8:  87        .BYTE $87
$FBB9:  85 85     STA $85
$FBBB:  85 85     STA $85
$FBBD:  85 87     STA $87
$FBBF:  80        .BYTE $80
$FBC0:  85 85     STA $85
$FBC2:  85 87     STA $87
$FBC4:  85 85     STA $85
$FBC6:  87        .BYTE $87
$FBC7:  80        .BYTE $80
$FBC8:  85 85     STA $85
$FBCA:  87        .BYTE $87
$FBCB:  87        .BYTE $87
$FBCC:  87        .BYTE $87
$FBCD:  87        .BYTE $87
$FBCE:  87        .BYTE $87
$FBCF:  80        .BYTE $80
$FBD0:  B0 B0     BCS $FB82
$FBD2:  B1 B0     LDA ($B0),Y
$FBD4:  B1 B0     LDA ($B0),Y
$FBD6:  B0 8D     BCS $FB65
$FBD8:  82        .BYTE $82
$FBD9:  82        .BYTE $82
$FBDA:  82        .BYTE $82
$FBDB:  82        .BYTE $82
$FBDC:  85 85     STA $85
$FBDE:  85 85     STA $85
$FBE0:  86 86     STX $86
$FBE2:  86 86     STX $86
$FBE4:  85 85     STA $85
$FBE6:  85 85     STA $85
$FBE8:  82        .BYTE $82
$FBE9:  85 85     STA $85
$FBEB:  85 85     STA $85
$FBED:  85 82     STA $82
$FBEF:  80        .BYTE $80
$FBF0:  87        .BYTE $87
$FBF1:  82        .BYTE $82
$FBF2:  82        .BYTE $82
$FBF3:  82        .BYTE $82
$FBF4:  85 85     STA $85
$FBF6:  85 80     STA $80
$FBF8:  8F        .BYTE $8F
$FBF9:  86 86     STX $86
$FBFB:  86 85     STX $85
$FBFD:  85 85     STA $85
$FBFF:  80        .BYTE $80
$FC00:  82        .BYTE $82
$FC01:  87        .BYTE $87
$FC02:  82        .BYTE $82
$FC03:  82        .BYTE $82
$FC04:  82        .BYTE $82
$FC05:  85 85     STA $85
$FC07:  85 87     STA $87
$FC09:  84 84     STY $84
$FC0B:  87        .BYTE $87
$FC0C:  84 84     STY $84
$FC0E:  82        .BYTE $82
$FC0F:  81 87     STA ($87,X)
$FC11:  81 81     STA ($81,X)
$FC13:  87        .BYTE $87
$FC14:  81 81     STA ($81,X)
$FC16:  87        .BYTE $87
$FC17:  80        .BYTE $80
$FC18:  8F        .BYTE $8F
$FC19:  86 86     STX $86
$FC1B:  86 86     STX $86
$FC1D:  86 8F     STX $8F
$FC1F:  80        .BYTE $80
$FC20:  82        .BYTE $82
$FC21:  87        .BYTE $87
$FC22:  80        .BYTE $80
$FC23:  82        .BYTE $82
$FC24:  85 85     STA $85
$FC26:  85 82     STA $82
$FC28:  87        .BYTE $87
$FC29:  84 84     STY $84
$FC2B:  84 84     STY $84
$FC2D:  84 82     STY $82
$FC2F:  81 87     STA ($87,X)
$FC31:  86 86     STX $86
$FC33:  86 86     STX $86
$FC35:  86 83     STX $83
$FC37:  83        .BYTE $83
$FC38:  B1 B1     LDA ($B1),Y
$FC3A:  B1 B1     LDA ($B1),Y
$FC3C:  8D 8A 89  STA $898A
$FC3F:  C4 81     CPY $81
$FC41:  81 81     STA ($81,X)
$FC43:  81 87     STA ($87,X)
$FC45:  81 81     STA ($81,X)
$FC47:  87        .BYTE $87
$FC48:  80        .BYTE $80
$FC49:  87        .BYTE $87
$FC4A:  81 81     STA ($81,X)
$FC4C:  87        .BYTE $87
$FC4D:  81 81     STA ($81,X)
$FC4F:  87        .BYTE $87
$FC50:  87        .BYTE $87
$FC51:  83        .BYTE $83
$FC52:  83        .BYTE $83
$FC53:  83        .BYTE $83
$FC54:  87        .BYTE $87
$FC55:  83        .BYTE $83
$FC56:  83        .BYTE $83
$FC57:  87        .BYTE $87
$FC58:  87        .BYTE $87 ; [HOME]
$FC59:  84 87     STY $87
$FC5B:  81 87     STA ($87,X)
$FC5D:  87        .BYTE $87
$FC5E:  81 87     STA ($87,X)
$FC60:  87        .BYTE $87
$FC61:  85 85     STA $85
$FC63:  85 87     STA $87
$FC65:  85 85     STA $85
$FC67:  87        .BYTE $87
$FC68:  85 85     STA $85
$FC6A:  87        .BYTE $87
$FC6B:  85 87     STA $87
$FC6D:  87        .BYTE $87
$FC6E:  85 87     STA $87
$FC70:  85 87     STA $87
$FC72:  87        .BYTE $87
$FC73:  87        .BYTE $87
$FC74:  87        .BYTE $87
$FC75:  87        .BYTE $87
$FC76:  87        .BYTE $87
$FC77:  87        .BYTE $87
$FC78:  89        .BYTE $89
$FC79:  B0 B0     BCS $FC2B
$FC7B:  B1 B0     LDA ($B0),Y
$FC7D:  B0 B0     BCS $FC2F
$FC7F:  B0 82     BCS $FC03
$FC81:  82        .BYTE $82
$FC82:  82        .BYTE $82
$FC83:  85 85     STA $85
$FC85:  82        .BYTE $82
$FC86:  85 85     STA $85
$FC88:  8A        TXA
$FC89:  8A        TXA
$FC8A:  8A        TXA
$FC8B:  95 95     STA $95,X
$FC8D:  8A        TXA
$FC8E:  95 95     STA $95,X
$FC90:  82        .BYTE $82
$FC91:  85 85     STA $85
$FC93:  85 82     STA $82
$FC95:  85 85     STA $85
$FC97:  82        .BYTE $82
$FC98:  87        .BYTE $87
$FC99:  82        .BYTE $82
$FC9A:  82        .BYTE $82
$FC9B:  85 85     STA $85
$FC9D:  82        .BYTE $82
$FC9E:  85 85     STA $85
$FCA0:  9F        .BYTE $9F
$FCA1:  84 8E     STY $8E
$FCA3:  95 95     STA $95,X
$FCA5:  8E 95 95  STX $9595
$FCA8:  82        .BYTE $82
$FCA9:  87        .BYTE $87
$FCAA:  82        .BYTE $82
$FCAB:  85 85     STA $85
$FCAD:  82        .BYTE $82
$FCAE:  85 85     STA $85
$FCB0:  87        .BYTE $87
$FCB1:  84 87     STY $87
$FCB3:  84 84     STY $84
$FCB5:  87        .BYTE $87
$FCB6:  84 82     STY $82
$FCB8:  87        .BYTE $87
$FCB9:  81 87     STA ($87,X)
$FCBB:  81 87     STA ($87,X)
$FCBD:  87        .BYTE $87
$FCBE:  81 87     STA ($87,X)
$FCC0:  8F        .BYTE $8F
$FCC1:  86 86     STX $86
$FCC3:  86 8F     STX $8F
$FCC5:  86 86     STX $86
$FCC7:  8F        .BYTE $8F
$FCC8:  82        .BYTE $82
$FCC9:  87        .BYTE $87
$FCCA:  82        .BYTE $82
$FCCB:  85 82     STA $82
$FCCD:  82        .BYTE $82
$FCCE:  85 82     STA $82
$FCD0:  90 90     BCC $FC62
$FCD2:  90 90     BCC $FC64
$FCD4:  B0 90     BCS $FC66
$FCD6:  90 90     BCC $FC68
$FCD8:  C0 D0     CPY #$D0 ('P')
$FCDA:  D0 D0     BNE $FCAC
$FCDC:  F0 D0     BEQ $FCAE
$FCDE:  D0 C0     BNE $FCA0
$FCE0:  90 90     BCC $FC72
$FCE2:  90 B0     BCC $FC94
$FCE4:  90 B0     BCC $FC96
$FCE6:  90 90     BCC $FC78
$FCE8:  C0 D0     CPY #$D0 ('P')
$FCEA:  D0 F0     BNE $FCDC
$FCEC:  D0 F0     BNE $FCDE
$FCEE:  D0 C0     BNE $FCB0
$FCF0:  90 90     BCC $FC82
$FCF2:  90 98     BCC $FC8C
$FCF4:  90 90     BCC $FC86
$FCF6:  90 90     BCC $FC88
$FCF8:  A0 B0     LDY #$B0 ('0')
$FCFA:  B0 B8     BCS $FCB4
$FCFC:  B0 B0     BCS $FCAE
$FCFE:  B0 A0     BCS $FCA0
$FD00:  90 90     BCC $FC92
$FD02:  90 98     BCC $FC9C
$FD04:  90 98     BCC $FC9E
$FD06:  90 90     BCC $FC98
$FD08:  A0 B0     LDY #$B0 ('0')
$FD0A:  B0 B8     BCS $FCC4
$FD0C:  B0 B8     BCS $FCC6 ; [RDKEY]
$FD0E:  B0 A0     BCS $FCB0
$FD10:  88        DEY
$FD11:  88        DEY
$FD12:  88        DEY
$FD13:  88        DEY
$FD14:  BF        .BYTE $BF
$FD15:  80        .BYTE $80
$FD16:  80        .BYTE $80
$FD17:  80        .BYTE $80
$FD18:  90 90     BCC $FCAA
$FD1A:  90 90     BCC $FCAC
$FD1C:  B2        .BYTE $B2
$FD1D:  92        .BYTE $92
$FD1E:  9F        .BYTE $9F
$FD1F:  90 D0     BCC $FCF1
$FD21:  D0 D0     BNE $FCF3
$FD23:  D0 F2     BNE $FD17
$FD25:  D2        .BYTE $D2
$FD26:  DF        .BYTE $DF
$FD27:  D0 90     BNE $FCB9
$FD29:  90 90     BCC $FCBB
$FD2B:  90 92     BCC $FCBF
$FD2D:  92        .BYTE $92
$FD2E:  9F        .BYTE $9F
$FD2F:  90 94     BCC $FCC5
$FD31:  94 94     STY $94,X
$FD33:  94 BF     STY $BF,X
$FD35:  80        .BYTE $80 ; [RDCHAR]
$FD36:  80        .BYTE $80
$FD37:  80        .BYTE $80
$FD38:  80        .BYTE $80
$FD39:  80        .BYTE $80
$FD3A:  BF        .BYTE $BF
$FD3B:  88        DEY
$FD3C:  88        DEY
$FD3D:  88        DEY
$FD3E:  88        DEY
$FD3F:  80        .BYTE $80
$FD40:  A0 A0     LDY #$A0 (' ')
$FD42:  A0 B0     LDY #$B0 ('0')
$FD44:  A0 AF     LDY #$AF ('/')
$FD46:  A4 A4     LDY $A4
$FD48:  A0 B0     LDY #$B0 ('0')
$FD4A:  B0 B8     BCS $FD04
$FD4C:  B0 BF     BCS $FD0D
$FD4E:  B4 A4     LDY $A4,X
$FD50:  90 90     BCC $FCE2
$FD52:  90 90     BCC $FCE4
$FD54:  90 9F     BCC $FCF5
$FD56:  94 94     STY $94,X
$FD58:  80        .BYTE $80
$FD59:  80        .BYTE $80
$FD5A:  BF        .BYTE $BF
$FD5B:  94 94     STY $94,X
$FD5D:  94 94     STY $94,X
$FD5F:  80        .BYTE $80
$FD60:  80        .BYTE $80
$FD61:  80        .BYTE $80
$FD62:  80        .BYTE $80
$FD63:  BF        .BYTE $BF
$FD64:  80        .BYTE $80
$FD65:  80        .BYTE $80
$FD66:  80        .BYTE $80
$FD67:  80        .BYTE $80 ; [GETLNZ]
$FD68:  90 90     BCC $FCFA
$FD6A:  90 90     BCC $FCFC ; [GETLN]
$FD6C:  90 90     BCC $FCFE
$FD6E:  9F        .BYTE $9F
$FD6F:  90 90     BCC $FD01
$FD71:  90 90     BCC $FD03
$FD73:  90 90     BCC $FD05
$FD75:  90 90     BCC $FD07
$FD77:  90 BA     BCC $FD33
$FD79:  BA        TSX
$FD7A:  BA        TSX
$FD7B:  BA        TSX
$FD7C:  BA        TSX
$FD7D:  BA        TSX
$FD7E:  BA        TSX
$FD7F:  80        .BYTE $80
$FD80:  9E        .BYTE $9E
$FD81:  90 90     BCC $FD13
$FD83:  90 80     BCC $FD05
$FD85:  80        .BYTE $80
$FD86:  80        .BYTE $80
$FD87:  80        .BYTE $80
$FD88:  BE A8 A8  LDX $A8A8,Y
$FD8B:  A4 A4     LDY $A4
$FD8D:  80        .BYTE $80
$FD8E:  80        .BYTE $80 ; [CROUT]
$FD8F:  80        .BYTE $80
$FD90:  97        .BYTE $97
$FD91:  94 94     STY $94,X
$FD93:  AC AC 80  LDY $80AC
$FD96:  80        .BYTE $80
$FD97:  80        .BYTE $80
$FD98:  82        .BYTE $82
$FD99:  82        .BYTE $82
$FD9A:  82        .BYTE $82
$FD9B:  9E        .BYTE $9E
$FD9C:  80        .BYTE $80
$FD9D:  80        .BYTE $80
$FD9E:  80        .BYTE $80
$FD9F:  80        .BYTE $80
$FDA0:  B9 91 91  LDA $9191,Y
$FDA3:  A9 AF     LDA #$AF ('/') ; [PRA1]
$FDA5:  80        .BYTE $80
$FDA6:  80        .BYTE $80
$FDA7:  80        .BYTE $80
$FDA8:  91 B9     STA ($B9),Y
$FDAA:  91 A9     STA ($A9),Y
$FDAC:  97        .BYTE $97
$FDAD:  80        .BYTE $80
$FDAE:  80        .BYTE $80
$FDAF:  80        .BYTE $80
$FDB0:  9E        .BYTE $9E
$FDB1:  82        .BYTE $82
$FDB2:  82        .BYTE $82
$FDB3:  9E        .BYTE $9E
$FDB4:  80        .BYTE $80
$FDB5:  80        .BYTE $80
$FDB6:  80        .BYTE $80
$FDB7:  80        .BYTE $80
$FDB8:  BE 8A 8A  LDX $8A8A,Y
$FDBB:  BE 80 80  LDX $8080,Y
$FDBE:  80        .BYTE $80
$FDBF:  80        .BYTE $80
$FDC0:  9E        .BYTE $9E
$FDC1:  90 9E     BCC $FD61
$FDC3:  82        .BYTE $82
$FDC4:  9E        .BYTE $9E
$FDC5:  80        .BYTE $80
$FDC6:  80        .BYTE $80
$FDC7:  80        .BYTE $80
$FDC8:  BB        .BYTE $BB
$FDC9:  A2 A3     LDX #$A3 ('#')
$FDCB:  A1 A7     LDA ($A7,X)
$FDCD:  80        .BYTE $80
$FDCE:  80        .BYTE $80
$FDCF:  80        .BYTE $80
$FDD0:  BB        .BYTE $BB
$FDD1:  AA        TAX
$FDD2:  AB        .BYTE $AB
$FDD3:  A9 BF     LDA #$BF ('?')
$FDD5:  80        .BYTE $80
$FDD6:  80        .BYTE $80
$FDD7:  80        .BYTE $80
$FDD8:  AB        .BYTE $AB
$FDD9:  AA        TAX
$FDDA:  BB        .BYTE $BB ; [PRBYTE]
$FDDB:  A9 BF     LDA #$BF ('?')
$FDDD:  80        .BYTE $80
$FDDE:  80        .BYTE $80
$FDDF:  80        .BYTE $80
$FDE0:  93        .BYTE $93
$FDE1:  92        .BYTE $92
$FDE2:  93        .BYTE $93
$FDE3:  A9 AF     LDA #$AF ('/')
$FDE5:  80        .BYTE $80
$FDE6:  80        .BYTE $80
$FDE7:  80        .BYTE $80
$FDE8:  BB        .BYTE $BB
$FDE9:  8A        TXA
$FDEA:  BB        .BYTE $BB
$FDEB:  89        .BYTE $89
$FDEC:  BF        .BYTE $BF
$FDED:  80        .BYTE $80 ; [COUT]
$FDEE:  80        .BYTE $80
$FDEF:  80        .BYTE $80
$FDF0:  FF        .BYTE $FF
$FDF1:  B4 B7     LDY $B7,X
$FDF3:  B1 FF     LDA ($FF),Y
$FDF5:  80        .BYTE $80
$FDF6:  80        .BYTE $80
$FDF7:  80        .BYTE $80
$FDF8:  93        .BYTE $93
$FDF9:  BA        TSX
$FDFA:  93        .BYTE $93
$FDFB:  A9 97     LDA #$97
$FDFD:  80        .BYTE $80
$FDFE:  80        .BYTE $80
$FDFF:  80        .BYTE $80
$FE00:  9E        .BYTE $9E
$FE01:  92        .BYTE $92
$FE02:  92        .BYTE $92
$FE03:  9E        .BYTE $9E
$FE04:  80        .BYTE $80
$FE05:  80        .BYTE $80
$FE06:  80        .BYTE $80
$FE07:  80        .BYTE $80
$FE08:  92        .BYTE $92
$FE09:  9E        .BYTE $9E
$FE0A:  92        .BYTE $92
$FE0B:  9E        .BYTE $9E
$FE0C:  80        .BYTE $80
$FE0D:  80        .BYTE $80
$FE0E:  80        .BYTE $80
$FE0F:  80        .BYTE $80
$FE10:  AA        TAX
$FE11:  AA        TAX
$FE12:  BE AA BE  LDX $BEAA,Y
$FE15:  80        .BYTE $80
$FE16:  80        .BYTE $80
$FE17:  80        .BYTE $80
$FE18:  95 95     STA $95,X
$FE1A:  97        .BYTE $97
$FE1B:  AD AF 80  LDA $80AF
$FE1E:  80        .BYTE $80
$FE1F:  80        .BYTE $80
$FE20:  88        DEY
$FE21:  84 8A     STY $8A
$FE23:  92        .BYTE $92
$FE24:  A2 80     LDX #$80
$FE26:  80        .BYTE $80
$FE27:  80        .BYTE $80
$FE28:  A8        TAY
$FE29:  A8        TAY
$FE2A:  94 AA     STY $AA,X
$FE2C:  AA        TAX
$FE2D:  80        .BYTE $80
$FE2E:  80        .BYTE $80
$FE2F:  80        .BYTE $80
$FE30:  8C 92 92  STY $9292
$FE33:  8C 80 80  STY $8080
$FE36:  80        .BYTE $80
$FE37:  80        .BYTE $80
$FE38:  9E        .BYTE $9E
$FE39:  88        DEY
$FE3A:  88        DEY
$FE3B:  94 92     STY $92,X
$FE3D:  80        .BYTE $80
$FE3E:  80        .BYTE $80
$FE3F:  80        .BYTE $80
$FE40:  BE A8 94  LDX $94A8,Y
$FE43:  AA        TAX
$FE44:  AA        TAX
$FE45:  80        .BYTE $80
$FE46:  80        .BYTE $80
$FE47:  80        .BYTE $80
$FE48:  88        DEY
$FE49:  9E        .BYTE $9E
$FE4A:  88        DEY
$FE4B:  94 92     STY $92,X
$FE4D:  80        .BYTE $80
$FE4E:  80        .BYTE $80
$FE4F:  80        .BYTE $80
$FE50:  9E        .BYTE $9E
$FE51:  90 9E     BCC $FDF1
$FE53:  90 80     BCC $FDD5
$FE55:  80        .BYTE $80
$FE56:  80        .BYTE $80
$FE57:  80        .BYTE $80
$FE58:  9E        .BYTE $9E
$FE59:  82        .BYTE $82
$FE5A:  9E        .BYTE $9E
$FE5B:  82        .BYTE $82
$FE5C:  9E        .BYTE $9E
$FE5D:  80        .BYTE $80
$FE5E:  80        .BYTE $80
$FE5F:  80        .BYTE $80
$FE60:  BE 94 94  LDX $9494,Y
$FE63:  BE 80 80  LDX $8080,Y
$FE66:  80        .BYTE $80
$FE67:  80        .BYTE $80
$FE68:  88        DEY
$FE69:  9E        .BYTE $9E
$FE6A:  8C 92 8C  STY $8C92
$FE6D:  80        .BYTE $80
$FE6E:  6F        .BYTE $6F
$FE6F:  63        .BYTE $63
$FE70:  65 6A     ADC $6A
$FE72:  48        PHA
$FE73:  6C 70 AD  JMP ($AD70)
$FE76:  B6 AE     LDX $AE,Y
$FE78:  AF        .BYTE $AF
$FE79:  BB        .BYTE $BB
$FE7A:  BB        .BYTE $BB
$FE7B:  74        .BYTE $74
$FE7C:  E5 EB     SBC $EB
$FE7E:  53        .BYTE $53
$FE7F:  42        .BYTE $42
$FE80:  6D 56 B5  ADC $B556
$FE83:  66 59     ROR $59
$FE85:  6B        .BYTE $6B
$FE86:  B4 6E     LDY $6E,X
$FE88:  00        BRK
$FE89:  00        BRK ; [SETVID]
$FE8A:  00        BRK
$FE8B:  00        BRK
$FE8C:  00        BRK
$FE8D:  00        BRK
$FE8E:  11 97     ORA ($97),Y
$FE90:  1A        .BYTE $1A
$FE91:  17        .BYTE $17
$FE92:  07        .BYTE $07
$FE93:  09 1E     ORA #$1E ; [SETKBD]
$FE95:  8C C4 C6  STY $C6C4
$FE98:  C2        .BYTE $C2
$FE99:  DC        .BYTE $DC
$FE9A:  9A        TXS
$FE9B:  93        .BYTE $93
$FE9C:  E3        .BYTE $E3
$FE9D:  E7        .BYTE $E7
$FE9E:  12        .BYTE $12
$FE9F:  01 04     ORA ($04,X)
$FEA1:  15 CA     ORA $CA,X
$FEA3:  1D 18 1C  ORA $1C18,X
$FEA6:  92        .BYTE $92
$FEA7:  1B        .BYTE $1B
$FEA8:  00        BRK
$FEA9:  F2        .BYTE $F2
$FEAA:  D2        .BYTE $D2
$FEAB:  C2        .BYTE $C2
$FEAC:  F3        .BYTE $F3
$FEAD:  C3        .BYTE $C3
$FEAE:  D6 E5     DEC $E5,X
$FEB0:  C5 E6     CMP $E6
$FEB2:  C4 D8     CPY $D8
$FEB4:  C6 D3     DEC $D3
$FEB6:  DA        .BYTE $DA
$FEB7:  C1 C7     CMP ($C7,X)
$FEB9:  E1 F1     SBC ($F1,X)
$FEBB:  D1 CE     CMP ($CE),Y
$FEBD:  F4        .BYTE $F4
$FEBE:  D4        .BYTE $D4
$FEBF:  E4 F7     CPX $F7
$FEC1:  D7        .BYTE $D7
$FEC2:  E3        .BYTE $E3
$FEC3:  FA        .BYTE $FA
$FEC4:  F8        SED
$FEC5:  F6 E7     INC $E7,X
$FEC7:  00        BRK
$FEC8:  EB        .BYTE $EB
$FEC9:  EF        .BYTE $EF
$FECA:  E9 CF     SBC #$CF ('O')
$FECC:  EA        NOP
$FECD:  F0 F5     BEQ $FEC4
$FECF:  D0 E8     BNE $FEB9
$FED1:  C8        INY
$FED2:  CA        DEX
$FED3:  CB        .BYTE $CB
$FED4:  F9 EE D9  SBC $D9EE,Y
$FED7:  D5 C9     CMP $C9,X
$FED9:  E2        .BYTE $E2
$FEDA:  ED CC CD  SBC $CDCC
$FEDD:  EC 00 00  CPX $0000
$FEE0:  C2        .BYTE $C2
$FEE1:  E3        .BYTE $E3
$FEE2:  C4 E5     CPY $E5
$FEE4:  C6 E7     DEC $E7
$FEE6:  00        BRK
$FEE7:  00        BRK
$FEE8:  CA        DEX
$FEE9:  EB        .BYTE $EB
$FEEA:  8C AD AE  STY $AEAD
$FEED:  AF        .BYTE $AF
$FEEE:  00        BRK
$FEEF:  00        BRK
$FEF0:  92        .BYTE $92
$FEF1:  93        .BYTE $93
$FEF2:  B4 B5     LDY $B5,X
$FEF4:  B6 97     LDX $97,Y
$FEF6:  00        BRK
$FEF7:  00        BRK
$FEF8:  9A        TXS
$FEF9:  BB        .BYTE $BB
$FEFA:  DC        .BYTE $DC
$FEFB:  FF        .BYTE $FF
$FEFC:  FF        .BYTE $FF
$FEFD:  FF        .BYTE $FF
$FEFE:  FF        .BYTE $FF
$FEFF:  FF        .BYTE $FF
$FF00:  A9 01     LDA #$01
$FF02:  8D E8 43  STA $43E8
$FF05:  A9 04     LDA #$04
$FF07:  A2 03     LDX #$03
$FF09:  4C 5A D6  JMP $D65A
$FF0C:  EA        NOP
$FF0D:  EA        NOP
$FF0E:  AD FE 53  LDA $53FE
$FF11:  F0 36     BEQ $FF49
$FF13:  AD FD 43  LDA $43FD
$FF16:  38        SEC
$FF17:  E9 04     SBC #$04
$FF19:  29 0E     AND #$0E
$FF1B:  8D F4 43  STA $43F4
$FF1E:  AD FD 43  LDA $43FD
$FF21:  29 F1     AND #$F1 ('q')
$FF23:  0D F4 43  ORA $43F4
$FF26:  8D FD 43  STA $43FD
$FF29:  38        SEC
$FF2A:  AD F4 43  LDA $43F4
$FF2D:  29 0F     AND #$0F
$FF2F:  EA        NOP
$FF30:  BA        TSX
$FF31:  8E 03 00  STX $0003
$FF34:  8C 06 00  STY $0006
$FF37:  86 02     STX $02
$FF39:  AA        TAX
$FF3A:  BD 8F C3  LDA $C38F,X ; [BELL]
$FF3D:  8D F7 53  STA $53F7
$FF40:  BD 90 C3  LDA $C390,X
$FF43:  8D F8 53  STA $53F8
$FF46:  6C F7 53  JMP ($53F7)
$FF49:  AD F3 43  LDA $43F3
$FF4C:  10 0E     BPL $FF5C
$FF4E:  18        CLC
$FF4F:  EA        NOP
$FF50:  EA        NOP
$FF51:  EA        NOP
$FF52:  EA        NOP
$FF53:  EA        NOP
$FF54:  EA        NOP
$FF55:  A9 80     LDA #$80
$FF57:  8D F4 43  STA $43F4
$FF5A:  D0 CE     BNE $FF2A
$FF5C:  A9 08     LDA #$08
$FF5E:  A2 04     LDX #$04
$FF60:  38        SEC
$FF61:  EA        NOP
$FF62:  B0 02     BCS $FF66
$FF64:  A2 09     LDX #$09
$FF66:  CA        DEX
$FF67:  D0 FD     BNE $FF66
$FF69:  BA        TSX
$FF6A:  8E 03 00  STX $0003
$FF6D:  8C 02 00  STY $0002
$FF70:  86 02     STX $02
$FF72:  E9 01     SBC #$01
$FF74:  D0 EE     BNE $FF64
$FF76:  A2 09     LDX #$09
$FF78:  CA        DEX
$FF79:  D0 FD     BNE $FF78
$FF7B:  EA        NOP
$FF7C:  BA        TSX
$FF7D:  86 03     STX $03
$FF7F:  8C 02 00  STY $0002
$FF82:  86 02     STX $02
$FF84:  4C 87 DF  JMP $DF87
$FF87:  AD FD 43  LDA $43FD
$FF8A:  0A        ASL
$FF8B:  10 0F     BPL $FF9C
$FF8D:  0A        ASL
$FF8E:  0A        ASL
$FF8F:  30 1B     BMI $FFAC
$FF91:  AD F3 43  LDA $43F3
$FF94:  29 7F     AND #$7F
$FF96:  8D F3 43  STA $43F3
$FF99:  4C 00 D5  JMP $D500
$FF9C:  0A        ASL
$FF9D:  0A        ASL
$FF9E:  10 03     BPL $FFA3
$FFA0:  4C 67 D5  JMP $D567
$FFA3:  AD 00 88  LDA $8800
$FFA6:  29 08     AND #$08
$FFA8:  EA        NOP
$FFA9:  38        SEC
$FFAA:  B0 09     BCS $FFB5
$FFAC:  AD FD 43  LDA $43FD
$FFAF:  29 80     AND #$80
$FFB1:  4A        LSR
$FFB2:  4A        LSR
$FFB3:  4A        LSR
$FFB4:  4A        LSR
$FFB5:  8D E8 43  STA $43E8
$FFB8:  AD 00 88  LDA $8800
$FFBB:  29 07     AND #$07
$FFBD:  EA        NOP
$FFBE:  EA        NOP
$FFBF:  EA        NOP
$FFC0:  EA        NOP
$FFC1:  EA        NOP
$FFC2:  BA        TSX
$FFC3:  86 03     STX $03
$FFC5:  8C 02 00  STY $0002
$FFC8:  86 02     STX $02
$FFCA:  0D E8 43  ORA $43E8
$FFCD:  4A        LSR
$FFCE:  AA        TAX
$FFCF:  BD 91 C9  LDA $C991,X
$FFD2:  8D 00 0C  STA $0C00
$FFD5:  BA        TSX
$FFD6:  8A        TXA
$FFD7:  09 08     ORA #$08
$FFD9:  8D E8 43  STA $43E8
$FFDC:  EA        NOP
$FFDD:  EA        NOP
$FFDE:  AD 00 88  LDA $8800
$FFE1:  29 0F     AND #$0F
$FFE3:  AA        TAX
$FFE4:  BD A1 C9  LDA $C9A1,X
$FFE7:  8D F0 43  STA $43F0
$FFEA:  BA        TSX
$FFEB:  CE F2 43  DEC $43F2
$FFEE:  86 03     STX $03
$FFF0:  8C 02 00  STY $0002
$FFF3:  86 02     STX $02
$FFF5:  4C AB CF  JMP $CFAB
$FFF8:  1E 5A 16  ASL $165A,X
$FFFB:  00        BRK
$FFFC:  00        BRK ; [RESET_VECTOR]
$FFFD:  C0 20     CPY #$20 (' ')
$FFFF:  21        .BYTE $21