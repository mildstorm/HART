; ======================================================================
; 정원 HART U46 (2764, 8KB) 시스템 ROM: $E000-$FFFF
;   $E000-$F7FF: 표준 Applesoft BASIC 후반부 (6KB)
;   $F800-$FFFF: Apple II+ Autostart Monitor (2KB)
;   $FAA6: 콜드 리셋 루틴 - 슬롯 검색 생략, 내장 FDD 슬롯 6($C600) 즉시 부팅(JMP $C600)
;   $FFFA-$FFFF: 6502 벡터 (NMI: $03FB, RESET: $FA62, IRQ: $FA40)
; Base Address: $E000 - $FFFF (8192 bytes)
; ======================================================================

$E000:  4C 28 F1  JMP $F128
$E003:  4C 3C D4  JMP $D43C
$E006:  00        BRK
$E007:  20 B1 00  JSR $00B1
$E00A:  90 05     BCC $E011
$E00C:  20 7D E0  JSR $E07D
$E00F:  90 0B     BCC $E01C
$E011:  AA        TAX
$E012:  20 B1 00  JSR $00B1
$E015:  90 FB     BCC $E012
$E017:  20 7D E0  JSR $E07D
$E01A:  B0 F6     BCS $E012
$E01C:  C9 24     CMP #$24 ('$')
$E01E:  D0 06     BNE $E026
$E020:  A9 FF     LDA #$FF
$E022:  85 11     STA $11
$E024:  D0 10     BNE $E036
$E026:  C9 25     CMP #$25 ('%')
$E028:  D0 13     BNE $E03D
$E02A:  A5 14     LDA $14
$E02C:  30 C6     BMI $DFF4
$E02E:  A9 80     LDA #$80
$E030:  85 12     STA $12
$E032:  05 81     ORA $81
$E034:  85 81     STA $81
$E036:  8A        TXA
$E037:  09 80     ORA #$80
$E039:  AA        TAX
$E03A:  20 B1 00  JSR $00B1
$E03D:  86 82     STX $82
$E03F:  38        SEC
$E040:  05 14     ORA $14
$E042:  E9 28     SBC #$28 ('(')
$E044:  D0 03     BNE $E049
$E046:  4C 1E E1  JMP $E11E
$E049:  24 14     BIT $14
$E04B:  30 02     BMI $E04F
$E04D:  70 F7     BVS $E046
$E04F:  A9 00     LDA #$00
$E051:  85 14     STA $14
$E053:  A5 69     LDA $69
$E055:  A6 6A     LDX $6A
$E057:  A0 00     LDY #$00
$E059:  86 9C     STX $9C
$E05B:  85 9B     STA $9B
$E05D:  E4 6C     CPX $6C
$E05F:  D0 04     BNE $E065
$E061:  C5 6B     CMP $6B
$E063:  F0 22     BEQ $E087
$E065:  A5 81     LDA $81
$E067:  D1 9B     CMP ($9B),Y
$E069:  D0 08     BNE $E073
$E06B:  A5 82     LDA $82
$E06D:  C8        INY
$E06E:  D1 9B     CMP ($9B),Y
$E070:  F0 6C     BEQ $E0DE
$E072:  88        DEY
$E073:  18        CLC
$E074:  A5 9B     LDA $9B
$E076:  69 07     ADC #$07
$E078:  90 E1     BCC $E05B
$E07A:  E8        INX
$E07B:  D0 DC     BNE $E059
$E07D:  48        PHA
$E07E:  29 DF     AND #$DF ('_')
$E080:  C9 41     CMP #$41 ('A')
$E082:  20 2A D3  JSR $D32A
$E085:  68        PLA
$E086:  60        RTS
$E087:  68        PLA
$E088:  48        PHA
$E089:  C9 D7     CMP #$D7 ('W')
$E08B:  D0 0F     BNE $E09C
$E08D:  BA        TSX
$E08E:  BD 02 01  LDA $0102,X
$E091:  C9 DE     CMP #$DE ('^')
$E093:  D0 07     BNE $E09C
$E095:  A9 9A     LDA #$9A
$E097:  A0 E0     LDY #$E0 ('`')
$E099:  60        RTS
$E09A:  00        BRK
$E09B:  00        BRK
$E09C:  A5 6B     LDA $6B
$E09E:  A4 6C     LDY $6C
$E0A0:  85 9B     STA $9B
$E0A2:  84 9C     STY $9C
$E0A4:  A5 6D     LDA $6D
$E0A6:  A4 6E     LDY $6E
$E0A8:  85 96     STA $96
$E0AA:  84 97     STY $97
$E0AC:  18        CLC
$E0AD:  69 07     ADC #$07
$E0AF:  90 01     BCC $E0B2
$E0B1:  C8        INY
$E0B2:  85 94     STA $94
$E0B4:  84 95     STY $95
$E0B6:  20 93 D3  JSR $D393
$E0B9:  A5 94     LDA $94
$E0BB:  A4 95     LDY $95
$E0BD:  C8        INY
$E0BE:  85 6B     STA $6B
$E0C0:  84 6C     STY $6C
$E0C2:  A0 00     LDY #$00
$E0C4:  A5 81     LDA $81
$E0C6:  91 9B     STA ($9B),Y
$E0C8:  C8        INY
$E0C9:  A5 82     LDA $82
$E0CB:  91 9B     STA ($9B),Y
$E0CD:  A9 00     LDA #$00
$E0CF:  C8        INY
$E0D0:  91 9B     STA ($9B),Y
$E0D2:  C8        INY
$E0D3:  91 9B     STA ($9B),Y
$E0D5:  C8        INY
$E0D6:  91 9B     STA ($9B),Y
$E0D8:  C8        INY
$E0D9:  91 9B     STA ($9B),Y
$E0DB:  C8        INY
$E0DC:  91 9B     STA ($9B),Y
$E0DE:  A5 9B     LDA $9B
$E0E0:  18        CLC
$E0E1:  69 02     ADC #$02
$E0E3:  A4 9C     LDY $9C
$E0E5:  90 01     BCC $E0E8
$E0E7:  C8        INY
$E0E8:  85 83     STA $83
$E0EA:  84 84     STY $84
$E0EC:  60        RTS
$E0ED:  A5 0F     LDA $0F
$E0EF:  0A        ASL
$E0F0:  69 05     ADC #$05
$E0F2:  65 9B     ADC $9B
$E0F4:  A4 9C     LDY $9C
$E0F6:  90 01     BCC $E0F9
$E0F8:  C8        INY
$E0F9:  85 94     STA $94
$E0FB:  84 95     STY $95
$E0FD:  60        RTS
$E0FE:  90 80     BCC $E080
$E100:  00        BRK
$E101:  00        BRK
$E102:  20 B1 00  JSR $00B1
$E105:  20 67 DD  JSR $DD67
$E108:  A5 A2     LDA $A2
$E10A:  30 0D     BMI $E119
$E10C:  A5 9D     LDA $9D
$E10E:  C9 90     CMP #$90
$E110:  90 09     BCC $E11B
$E112:  A9 FE     LDA #$FE ('~')
$E114:  A0 E0     LDY #$E0 ('`')
$E116:  20 B2 EB  JSR $EBB2
$E119:  D0 7E     BNE $E199
$E11B:  4C F2 EB  JMP $EBF2
$E11E:  A5 14     LDA $14
$E120:  D0 47     BNE $E169
$E122:  A5 10     LDA $10
$E124:  05 12     ORA $12
$E126:  48        PHA
$E127:  A5 11     LDA $11
$E129:  48        PHA
$E12A:  A0 00     LDY #$00
$E12C:  98        TYA
$E12D:  48        PHA
$E12E:  A5 82     LDA $82
$E130:  48        PHA
$E131:  A5 81     LDA $81
$E133:  48        PHA
$E134:  20 02 E1  JSR $E102
$E137:  68        PLA
$E138:  85 81     STA $81
$E13A:  68        PLA
$E13B:  85 82     STA $82
$E13D:  68        PLA
$E13E:  A8        TAY
$E13F:  BA        TSX
$E140:  BD 02 01  LDA $0102,X
$E143:  48        PHA
$E144:  BD 01 01  LDA $0101,X
$E147:  48        PHA
$E148:  A5 A0     LDA $A0
$E14A:  9D 02 01  STA $0102,X
$E14D:  A5 A1     LDA $A1
$E14F:  9D 01 01  STA $0101,X
$E152:  C8        INY
$E153:  20 B7 00  JSR $00B7
$E156:  C9 2C     CMP #$2C (',')
$E158:  F0 D2     BEQ $E12C
$E15A:  84 0F     STY $0F
$E15C:  20 B8 DE  JSR $DEB8
$E15F:  68        PLA
$E160:  85 11     STA $11
$E162:  68        PLA
$E163:  85 12     STA $12
$E165:  29 7F     AND #$7F
$E167:  85 10     STA $10
$E169:  A6 6B     LDX $6B
$E16B:  A5 6C     LDA $6C
$E16D:  86 9B     STX $9B
$E16F:  85 9C     STA $9C
$E171:  C5 6E     CMP $6E
$E173:  D0 04     BNE $E179
$E175:  E4 6D     CPX $6D
$E177:  F0 3F     BEQ $E1B8
$E179:  A0 00     LDY #$00
$E17B:  B1 9B     LDA ($9B),Y
$E17D:  C8        INY
$E17E:  C5 81     CMP $81
$E180:  D0 06     BNE $E188
$E182:  A5 82     LDA $82
$E184:  D1 9B     CMP ($9B),Y
$E186:  F0 16     BEQ $E19E
$E188:  C8        INY
$E189:  B1 9B     LDA ($9B),Y
$E18B:  18        CLC
$E18C:  65 9B     ADC $9B
$E18E:  AA        TAX
$E18F:  C8        INY
$E190:  B1 9B     LDA ($9B),Y
$E192:  65 9C     ADC $9C
$E194:  90 D7     BCC $E16D
$E196:  A2 6B     LDX #$6B ('k')
$E198:  2C A2 35  BIT $35A2
$E19B:  4C 12 D4  JMP $D412
$E19E:  A2 78     LDX #$78 ('x')
$E1A0:  A5 10     LDA $10
$E1A2:  D0 F7     BNE $E19B
$E1A4:  A5 14     LDA $14
$E1A6:  F0 02     BEQ $E1AA
$E1A8:  38        SEC
$E1A9:  60        RTS
$E1AA:  20 ED E0  JSR $E0ED
$E1AD:  A5 0F     LDA $0F
$E1AF:  A0 04     LDY #$04
$E1B1:  D1 9B     CMP ($9B),Y
$E1B3:  D0 E1     BNE $E196
$E1B5:  4C 4B E2  JMP $E24B
$E1B8:  A5 14     LDA $14
$E1BA:  F0 05     BEQ $E1C1
$E1BC:  A2 2A     LDX #$2A ('*')
$E1BE:  4C 12 D4  JMP $D412
$E1C1:  20 ED E0  JSR $E0ED
$E1C4:  20 E3 D3  JSR $D3E3
$E1C7:  A9 00     LDA #$00
$E1C9:  A8        TAY
$E1CA:  85 AE     STA $AE
$E1CC:  A2 05     LDX #$05
$E1CE:  A5 81     LDA $81
$E1D0:  91 9B     STA ($9B),Y
$E1D2:  10 01     BPL $E1D5
$E1D4:  CA        DEX
$E1D5:  C8        INY
$E1D6:  A5 82     LDA $82
$E1D8:  91 9B     STA ($9B),Y
$E1DA:  10 02     BPL $E1DE
$E1DC:  CA        DEX
$E1DD:  CA        DEX
$E1DE:  86 AD     STX $AD
$E1E0:  A5 0F     LDA $0F
$E1E2:  C8        INY
$E1E3:  C8        INY
$E1E4:  C8        INY
$E1E5:  91 9B     STA ($9B),Y
$E1E7:  A2 0B     LDX #$0B
$E1E9:  A9 00     LDA #$00
$E1EB:  24 10     BIT $10
$E1ED:  50 08     BVC $E1F7
$E1EF:  68        PLA
$E1F0:  18        CLC
$E1F1:  69 01     ADC #$01
$E1F3:  AA        TAX
$E1F4:  68        PLA
$E1F5:  69 00     ADC #$00
$E1F7:  C8        INY
$E1F8:  91 9B     STA ($9B),Y
$E1FA:  C8        INY
$E1FB:  8A        TXA
$E1FC:  91 9B     STA ($9B),Y
$E1FE:  20 AD E2  JSR $E2AD
$E201:  86 AD     STX $AD
$E203:  85 AE     STA $AE
$E205:  A4 5E     LDY $5E
$E207:  C6 0F     DEC $0F
$E209:  D0 DC     BNE $E1E7
$E20B:  65 95     ADC $95
$E20D:  B0 5D     BCS $E26C
$E20F:  85 95     STA $95
$E211:  A8        TAY
$E212:  8A        TXA
$E213:  65 94     ADC $94
$E215:  90 03     BCC $E21A
$E217:  C8        INY
$E218:  F0 52     BEQ $E26C
$E21A:  20 E3 D3  JSR $D3E3
$E21D:  85 6D     STA $6D
$E21F:  84 6E     STY $6E
$E221:  A9 00     LDA #$00
$E223:  E6 AE     INC $AE
$E225:  A4 AD     LDY $AD
$E227:  F0 05     BEQ $E22E
$E229:  88        DEY
$E22A:  91 94     STA ($94),Y
$E22C:  D0 FB     BNE $E229
$E22E:  C6 95     DEC $95
$E230:  C6 AE     DEC $AE
$E232:  D0 F5     BNE $E229
$E234:  E6 95     INC $95
$E236:  38        SEC
$E237:  A5 6D     LDA $6D
$E239:  E5 9B     SBC $9B
$E23B:  A0 02     LDY #$02
$E23D:  91 9B     STA ($9B),Y
$E23F:  A5 6E     LDA $6E
$E241:  C8        INY
$E242:  E5 9C     SBC $9C
$E244:  91 9B     STA ($9B),Y
$E246:  A5 10     LDA $10
$E248:  D0 62     BNE $E2AC
$E24A:  C8        INY
$E24B:  B1 9B     LDA ($9B),Y
$E24D:  85 0F     STA $0F
$E24F:  A9 00     LDA #$00
$E251:  85 AD     STA $AD
$E253:  85 AE     STA $AE
$E255:  C8        INY
$E256:  68        PLA
$E257:  AA        TAX
$E258:  85 A0     STA $A0
$E25A:  68        PLA
$E25B:  85 A1     STA $A1
$E25D:  D1 9B     CMP ($9B),Y
$E25F:  90 0E     BCC $E26F
$E261:  D0 06     BNE $E269
$E263:  C8        INY
$E264:  8A        TXA
$E265:  D1 9B     CMP ($9B),Y
$E267:  90 07     BCC $E270
$E269:  4C 96 E1  JMP $E196
$E26C:  4C 10 D4  JMP $D410
$E26F:  C8        INY
$E270:  A5 AE     LDA $AE
$E272:  05 AD     ORA $AD
$E274:  18        CLC
$E275:  F0 0A     BEQ $E281
$E277:  20 AD E2  JSR $E2AD
$E27A:  8A        TXA
$E27B:  65 A0     ADC $A0
$E27D:  AA        TAX
$E27E:  98        TYA
$E27F:  A4 5E     LDY $5E
$E281:  65 A1     ADC $A1
$E283:  86 AD     STX $AD
$E285:  C6 0F     DEC $0F
$E287:  D0 CA     BNE $E253
$E289:  85 AE     STA $AE
$E28B:  A2 05     LDX #$05
$E28D:  A5 81     LDA $81
$E28F:  10 01     BPL $E292
$E291:  CA        DEX
$E292:  A5 82     LDA $82
$E294:  10 02     BPL $E298
$E296:  CA        DEX
$E297:  CA        DEX
$E298:  86 64     STX $64
$E29A:  A9 00     LDA #$00
$E29C:  20 B6 E2  JSR $E2B6
$E29F:  8A        TXA
$E2A0:  65 94     ADC $94
$E2A2:  85 83     STA $83
$E2A4:  98        TYA
$E2A5:  65 95     ADC $95
$E2A7:  85 84     STA $84
$E2A9:  A8        TAY
$E2AA:  A5 83     LDA $83
$E2AC:  60        RTS
$E2AD:  84 5E     STY $5E
$E2AF:  B1 9B     LDA ($9B),Y
$E2B1:  85 64     STA $64
$E2B3:  88        DEY
$E2B4:  B1 9B     LDA ($9B),Y
$E2B6:  85 65     STA $65
$E2B8:  A9 10     LDA #$10
$E2BA:  85 99     STA $99
$E2BC:  A2 00     LDX #$00
$E2BE:  A0 00     LDY #$00
$E2C0:  8A        TXA
$E2C1:  0A        ASL
$E2C2:  AA        TAX
$E2C3:  98        TYA
$E2C4:  2A        ROL
$E2C5:  A8        TAY
$E2C6:  B0 A4     BCS $E26C
$E2C8:  06 AD     ASL $AD
$E2CA:  26 AE     ROL $AE
$E2CC:  90 0B     BCC $E2D9
$E2CE:  18        CLC
$E2CF:  8A        TXA
$E2D0:  65 64     ADC $64
$E2D2:  AA        TAX
$E2D3:  98        TYA
$E2D4:  65 65     ADC $65
$E2D6:  A8        TAY
$E2D7:  B0 93     BCS $E26C
$E2D9:  C6 99     DEC $99
$E2DB:  D0 E3     BNE $E2C0
$E2DD:  60        RTS
$E2DE:  A5 11     LDA $11
$E2E0:  F0 03     BEQ $E2E5
$E2E2:  20 00 E6  JSR $E600
$E2E5:  20 84 E4  JSR $E484
$E2E8:  38        SEC
$E2E9:  A5 6F     LDA $6F
$E2EB:  E5 6D     SBC $6D
$E2ED:  A8        TAY
$E2EE:  A5 70     LDA $70
$E2F0:  E5 6E     SBC $6E
$E2F2:  A2 00     LDX #$00
$E2F4:  86 11     STX $11
$E2F6:  85 9E     STA $9E
$E2F8:  84 9F     STY $9F
$E2FA:  A2 90     LDX #$90
$E2FC:  4C 9B EB  JMP $EB9B
$E2FF:  A4 24     LDY $24
$E301:  A9 00     LDA #$00
$E303:  38        SEC
$E304:  F0 EC     BEQ $E2F2
$E306:  A6 76     LDX $76
$E308:  E8        INX
$E309:  D0 A1     BNE $E2AC
$E30B:  A2 95     LDX #$95
$E30D:  2C A2 E0  BIT $E0A2
$E310:  4C 12 D4  JMP $D412
$E313:  20 41 E3  JSR $E341
$E316:  20 06 E3  JSR $E306
$E319:  20 BB DE  JSR $DEBB
$E31C:  A9 80     LDA #$80
$E31E:  85 14     STA $14
$E320:  20 E3 DF  JSR $DFE3
$E323:  20 6A DD  JSR $DD6A
$E326:  20 B8 DE  JSR $DEB8
$E329:  A9 D0     LDA #$D0 ('P')
$E32B:  20 C0 DE  JSR $DEC0
$E32E:  48        PHA
$E32F:  A5 84     LDA $84
$E331:  48        PHA
$E332:  A5 83     LDA $83
$E334:  48        PHA
$E335:  A5 B9     LDA $B9
$E337:  48        PHA
$E338:  A5 B8     LDA $B8
$E33A:  48        PHA
$E33B:  20 95 D9  JSR $D995
$E33E:  4C AF E3  JMP $E3AF
$E341:  A9 C2     LDA #$C2 ('B')
$E343:  20 C0 DE  JSR $DEC0
$E346:  09 80     ORA #$80
$E348:  85 14     STA $14
$E34A:  20 EA DF  JSR $DFEA
$E34D:  85 8A     STA $8A
$E34F:  84 8B     STY $8B
$E351:  4C 6A DD  JMP $DD6A
$E354:  20 41 E3  JSR $E341
$E357:  A5 8B     LDA $8B
$E359:  48        PHA
$E35A:  A5 8A     LDA $8A
$E35C:  48        PHA
$E35D:  20 B2 DE  JSR $DEB2
$E360:  20 6A DD  JSR $DD6A
$E363:  68        PLA
$E364:  85 8A     STA $8A
$E366:  68        PLA
$E367:  85 8B     STA $8B
$E369:  A0 02     LDY #$02
$E36B:  B1 8A     LDA ($8A),Y
$E36D:  85 83     STA $83
$E36F:  AA        TAX
$E370:  C8        INY
$E371:  B1 8A     LDA ($8A),Y
$E373:  F0 99     BEQ $E30E
$E375:  85 84     STA $84
$E377:  C8        INY
$E378:  B1 83     LDA ($83),Y
$E37A:  48        PHA
$E37B:  88        DEY
$E37C:  10 FA     BPL $E378
$E37E:  A4 84     LDY $84
$E380:  20 2B EB  JSR $EB2B
$E383:  A5 B9     LDA $B9
$E385:  48        PHA
$E386:  A5 B8     LDA $B8
$E388:  48        PHA
$E389:  B1 8A     LDA ($8A),Y
$E38B:  85 B8     STA $B8
$E38D:  C8        INY
$E38E:  B1 8A     LDA ($8A),Y
$E390:  85 B9     STA $B9
$E392:  A5 84     LDA $84
$E394:  48        PHA
$E395:  A5 83     LDA $83
$E397:  48        PHA
$E398:  20 67 DD  JSR $DD67
$E39B:  68        PLA
$E39C:  85 8A     STA $8A
$E39E:  68        PLA
$E39F:  85 8B     STA $8B
$E3A1:  20 B7 00  JSR $00B7
$E3A4:  F0 03     BEQ $E3A9
$E3A6:  4C C9 DE  JMP $DEC9
$E3A9:  68        PLA
$E3AA:  85 B8     STA $B8
$E3AC:  68        PLA
$E3AD:  85 B9     STA $B9
$E3AF:  A0 00     LDY #$00
$E3B1:  68        PLA
$E3B2:  91 8A     STA ($8A),Y
$E3B4:  68        PLA
$E3B5:  C8        INY
$E3B6:  91 8A     STA ($8A),Y
$E3B8:  68        PLA
$E3B9:  C8        INY
$E3BA:  91 8A     STA ($8A),Y
$E3BC:  68        PLA
$E3BD:  C8        INY
$E3BE:  91 8A     STA ($8A),Y
$E3C0:  68        PLA
$E3C1:  C8        INY
$E3C2:  91 8A     STA ($8A),Y
$E3C4:  60        RTS
$E3C5:  20 6A DD  JSR $DD6A
$E3C8:  A0 00     LDY #$00
$E3CA:  20 36 ED  JSR $ED36
$E3CD:  68        PLA
$E3CE:  68        PLA
$E3CF:  A9 FF     LDA #$FF
$E3D1:  A0 00     LDY #$00
$E3D3:  F0 12     BEQ $E3E7
$E3D5:  A6 A0     LDX $A0
$E3D7:  A4 A1     LDY $A1
$E3D9:  86 8C     STX $8C
$E3DB:  84 8D     STY $8D
$E3DD:  20 52 E4  JSR $E452
$E3E0:  86 9E     STX $9E
$E3E2:  84 9F     STY $9F
$E3E4:  85 9D     STA $9D
$E3E6:  60        RTS
$E3E7:  A2 22     LDX #$22 ('"')
$E3E9:  86 0D     STX $0D
$E3EB:  86 0E     STX $0E
$E3ED:  85 AB     STA $AB
$E3EF:  84 AC     STY $AC
$E3F1:  85 9E     STA $9E
$E3F3:  84 9F     STY $9F
$E3F5:  A0 FF     LDY #$FF
$E3F7:  C8        INY
$E3F8:  B1 AB     LDA ($AB),Y
$E3FA:  F0 0C     BEQ $E408
$E3FC:  C5 0D     CMP $0D
$E3FE:  F0 04     BEQ $E404
$E400:  C5 0E     CMP $0E
$E402:  D0 F3     BNE $E3F7
$E404:  C9 22     CMP #$22 ('"')
$E406:  F0 01     BEQ $E409
$E408:  18        CLC
$E409:  84 9D     STY $9D
$E40B:  98        TYA
$E40C:  65 AB     ADC $AB
$E40E:  85 AD     STA $AD
$E410:  A6 AC     LDX $AC
$E412:  90 01     BCC $E415
$E414:  E8        INX
$E415:  86 AE     STX $AE
$E417:  A5 AC     LDA $AC
$E419:  F0 04     BEQ $E41F
$E41B:  C9 02     CMP #$02
$E41D:  D0 0B     BNE $E42A
$E41F:  98        TYA
$E420:  20 D5 E3  JSR $E3D5
$E423:  A6 AB     LDX $AB
$E425:  A4 AC     LDY $AC
$E427:  20 E2 E5  JSR $E5E2
$E42A:  A6 52     LDX $52
$E42C:  E0 5E     CPX #$5E ('^')
$E42E:  D0 05     BNE $E435
$E430:  A2 BF     LDX #$BF ('?')
$E432:  4C 12 D4  JMP $D412
$E435:  A5 9D     LDA $9D
$E437:  95 00     STA $00,X
$E439:  A5 9E     LDA $9E
$E43B:  95 01     STA $01,X
$E43D:  A5 9F     LDA $9F
$E43F:  95 02     STA $02,X
$E441:  A0 00     LDY #$00
$E443:  86 A0     STX $A0
$E445:  84 A1     STY $A1
$E447:  88        DEY
$E448:  84 11     STY $11
$E44A:  86 53     STX $53
$E44C:  E8        INX
$E44D:  E8        INX
$E44E:  E8        INX
$E44F:  86 52     STX $52
$E451:  60        RTS
$E452:  46 13     LSR $13
$E454:  48        PHA
$E455:  49 FF     EOR #$FF
$E457:  38        SEC
$E458:  65 6F     ADC $6F
$E45A:  A4 70     LDY $70
$E45C:  B0 01     BCS $E45F
$E45E:  88        DEY
$E45F:  C4 6E     CPY $6E
$E461:  90 11     BCC $E474
$E463:  D0 04     BNE $E469
$E465:  C5 6D     CMP $6D
$E467:  90 0B     BCC $E474
$E469:  85 6F     STA $6F
$E46B:  84 70     STY $70
$E46D:  85 71     STA $71
$E46F:  84 72     STY $72
$E471:  AA        TAX
$E472:  68        PLA
$E473:  60        RTS
$E474:  A2 4D     LDX #$4D ('M')
$E476:  A5 13     LDA $13
$E478:  30 B8     BMI $E432
$E47A:  20 84 E4  JSR $E484
$E47D:  A9 80     LDA #$80
$E47F:  85 13     STA $13
$E481:  68        PLA
$E482:  D0 D0     BNE $E454
$E484:  A6 73     LDX $73
$E486:  A5 74     LDA $74
$E488:  86 6F     STX $6F
$E48A:  85 70     STA $70
$E48C:  A0 00     LDY #$00
$E48E:  84 8B     STY $8B
$E490:  A5 6D     LDA $6D
$E492:  A6 6E     LDX $6E
$E494:  85 9B     STA $9B
$E496:  86 9C     STX $9C
$E498:  A9 55     LDA #$55 ('U')
$E49A:  A2 00     LDX #$00
$E49C:  85 5E     STA $5E
$E49E:  86 5F     STX $5F
$E4A0:  C5 52     CMP $52
$E4A2:  F0 05     BEQ $E4A9
$E4A4:  20 23 E5  JSR $E523
$E4A7:  F0 F7     BEQ $E4A0
$E4A9:  A9 07     LDA #$07
$E4AB:  85 8F     STA $8F
$E4AD:  A5 69     LDA $69
$E4AF:  A6 6A     LDX $6A
$E4B1:  85 5E     STA $5E
$E4B3:  86 5F     STX $5F
$E4B5:  E4 6C     CPX $6C
$E4B7:  D0 04     BNE $E4BD
$E4B9:  C5 6B     CMP $6B
$E4BB:  F0 05     BEQ $E4C2
$E4BD:  20 19 E5  JSR $E519
$E4C0:  F0 F3     BEQ $E4B5
$E4C2:  85 94     STA $94
$E4C4:  86 95     STX $95
$E4C6:  A9 03     LDA #$03
$E4C8:  85 8F     STA $8F
$E4CA:  A5 94     LDA $94
$E4CC:  A6 95     LDX $95
$E4CE:  E4 6E     CPX $6E
$E4D0:  D0 07     BNE $E4D9
$E4D2:  C5 6D     CMP $6D
$E4D4:  D0 03     BNE $E4D9
$E4D6:  4C 62 E5  JMP $E562
$E4D9:  85 5E     STA $5E
$E4DB:  86 5F     STX $5F
$E4DD:  A0 00     LDY #$00
$E4DF:  B1 5E     LDA ($5E),Y
$E4E1:  AA        TAX
$E4E2:  C8        INY
$E4E3:  B1 5E     LDA ($5E),Y
$E4E5:  08        PHP
$E4E6:  C8        INY
$E4E7:  B1 5E     LDA ($5E),Y
$E4E9:  65 94     ADC $94
$E4EB:  85 94     STA $94
$E4ED:  C8        INY
$E4EE:  B1 5E     LDA ($5E),Y
$E4F0:  65 95     ADC $95
$E4F2:  85 95     STA $95
$E4F4:  28        PLP
$E4F5:  10 D3     BPL $E4CA
$E4F7:  8A        TXA
$E4F8:  30 D0     BMI $E4CA
$E4FA:  C8        INY
$E4FB:  B1 5E     LDA ($5E),Y
$E4FD:  A0 00     LDY #$00
$E4FF:  0A        ASL
$E500:  69 05     ADC #$05
$E502:  65 5E     ADC $5E
$E504:  85 5E     STA $5E
$E506:  90 02     BCC $E50A
$E508:  E6 5F     INC $5F
$E50A:  A6 5F     LDX $5F
$E50C:  E4 95     CPX $95
$E50E:  D0 04     BNE $E514
$E510:  C5 94     CMP $94
$E512:  F0 BA     BEQ $E4CE
$E514:  20 23 E5  JSR $E523
$E517:  F0 F3     BEQ $E50C
$E519:  B1 5E     LDA ($5E),Y
$E51B:  30 35     BMI $E552
$E51D:  C8        INY
$E51E:  B1 5E     LDA ($5E),Y
$E520:  10 30     BPL $E552
$E522:  C8        INY
$E523:  B1 5E     LDA ($5E),Y
$E525:  F0 2B     BEQ $E552
$E527:  C8        INY
$E528:  B1 5E     LDA ($5E),Y
$E52A:  AA        TAX
$E52B:  C8        INY
$E52C:  B1 5E     LDA ($5E),Y
$E52E:  C5 70     CMP $70
$E530:  90 06     BCC $E538
$E532:  D0 1E     BNE $E552
$E534:  E4 6F     CPX $6F
$E536:  B0 1A     BCS $E552
$E538:  C5 9C     CMP $9C
$E53A:  90 16     BCC $E552
$E53C:  D0 04     BNE $E542
$E53E:  E4 9B     CPX $9B
$E540:  90 10     BCC $E552
$E542:  86 9B     STX $9B
$E544:  85 9C     STA $9C
$E546:  A5 5E     LDA $5E
$E548:  A6 5F     LDX $5F
$E54A:  85 8A     STA $8A
$E54C:  86 8B     STX $8B
$E54E:  A5 8F     LDA $8F
$E550:  85 91     STA $91
$E552:  A5 8F     LDA $8F
$E554:  18        CLC
$E555:  65 5E     ADC $5E
$E557:  85 5E     STA $5E
$E559:  90 02     BCC $E55D
$E55B:  E6 5F     INC $5F
$E55D:  A6 5F     LDX $5F
$E55F:  A0 00     LDY #$00
$E561:  60        RTS
$E562:  A6 8B     LDX $8B
$E564:  F0 F7     BEQ $E55D
$E566:  A5 91     LDA $91
$E568:  29 04     AND #$04
$E56A:  4A        LSR
$E56B:  A8        TAY
$E56C:  85 91     STA $91
$E56E:  B1 8A     LDA ($8A),Y
$E570:  65 9B     ADC $9B
$E572:  85 96     STA $96
$E574:  A5 9C     LDA $9C
$E576:  69 00     ADC #$00
$E578:  85 97     STA $97
$E57A:  A5 6F     LDA $6F
$E57C:  A6 70     LDX $70
$E57E:  85 94     STA $94
$E580:  86 95     STX $95
$E582:  20 9A D3  JSR $D39A
$E585:  A4 91     LDY $91
$E587:  C8        INY
$E588:  A5 94     LDA $94
$E58A:  91 8A     STA ($8A),Y
$E58C:  AA        TAX
$E58D:  E6 95     INC $95
$E58F:  A5 95     LDA $95
$E591:  C8        INY
$E592:  91 8A     STA ($8A),Y
$E594:  4C 88 E4  JMP $E488
$E597:  A5 A1     LDA $A1
$E599:  48        PHA
$E59A:  A5 A0     LDA $A0
$E59C:  48        PHA
$E59D:  20 60 DE  JSR $DE60
$E5A0:  20 6C DD  JSR $DD6C
$E5A3:  68        PLA
$E5A4:  85 AB     STA $AB
$E5A6:  68        PLA
$E5A7:  85 AC     STA $AC
$E5A9:  A0 00     LDY #$00
$E5AB:  B1 AB     LDA ($AB),Y
$E5AD:  18        CLC
$E5AE:  71 A0     ADC ($A0),Y
$E5B0:  90 05     BCC $E5B7
$E5B2:  A2 B0     LDX #$B0 ('0')
$E5B4:  4C 12 D4  JMP $D412
$E5B7:  20 D5 E3  JSR $E3D5
$E5BA:  20 D4 E5  JSR $E5D4
$E5BD:  A5 8C     LDA $8C
$E5BF:  A4 8D     LDY $8D
$E5C1:  20 04 E6  JSR $E604
$E5C4:  20 E6 E5  JSR $E5E6
$E5C7:  A5 AB     LDA $AB
$E5C9:  A4 AC     LDY $AC
$E5CB:  20 04 E6  JSR $E604
$E5CE:  20 2A E4  JSR $E42A
$E5D1:  4C 95 DD  JMP $DD95
$E5D4:  A0 00     LDY #$00
$E5D6:  B1 AB     LDA ($AB),Y
$E5D8:  48        PHA
$E5D9:  C8        INY
$E5DA:  B1 AB     LDA ($AB),Y
$E5DC:  AA        TAX
$E5DD:  C8        INY
$E5DE:  B1 AB     LDA ($AB),Y
$E5E0:  A8        TAY
$E5E1:  68        PLA
$E5E2:  86 5E     STX $5E
$E5E4:  84 5F     STY $5F
$E5E6:  A8        TAY
$E5E7:  F0 0A     BEQ $E5F3
$E5E9:  48        PHA
$E5EA:  88        DEY
$E5EB:  B1 5E     LDA ($5E),Y
$E5ED:  91 71     STA ($71),Y
$E5EF:  98        TYA
$E5F0:  D0 F8     BNE $E5EA
$E5F2:  68        PLA
$E5F3:  18        CLC
$E5F4:  65 71     ADC $71
$E5F6:  85 71     STA $71
$E5F8:  90 02     BCC $E5FC
$E5FA:  E6 72     INC $72
$E5FC:  60        RTS
$E5FD:  20 6C DD  JSR $DD6C
$E600:  A5 A0     LDA $A0
$E602:  A4 A1     LDY $A1
$E604:  85 5E     STA $5E
$E606:  84 5F     STY $5F
$E608:  20 35 E6  JSR $E635
$E60B:  08        PHP
$E60C:  A0 00     LDY #$00
$E60E:  B1 5E     LDA ($5E),Y
$E610:  48        PHA
$E611:  C8        INY
$E612:  B1 5E     LDA ($5E),Y
$E614:  AA        TAX
$E615:  C8        INY
$E616:  B1 5E     LDA ($5E),Y
$E618:  A8        TAY
$E619:  68        PLA
$E61A:  28        PLP
$E61B:  D0 13     BNE $E630
$E61D:  C4 70     CPY $70
$E61F:  D0 0F     BNE $E630
$E621:  E4 6F     CPX $6F
$E623:  D0 0B     BNE $E630
$E625:  48        PHA
$E626:  18        CLC
$E627:  65 6F     ADC $6F
$E629:  85 6F     STA $6F
$E62B:  90 02     BCC $E62F
$E62D:  E6 70     INC $70
$E62F:  68        PLA
$E630:  86 5E     STX $5E
$E632:  84 5F     STY $5F
$E634:  60        RTS
$E635:  C4 54     CPY $54
$E637:  D0 0C     BNE $E645
$E639:  C5 53     CMP $53
$E63B:  D0 08     BNE $E645
$E63D:  85 52     STA $52
$E63F:  E9 03     SBC #$03
$E641:  85 53     STA $53
$E643:  A0 00     LDY #$00
$E645:  60        RTS
$E646:  20 FB E6  JSR $E6FB
$E649:  8A        TXA
$E64A:  48        PHA
$E64B:  A9 01     LDA #$01
$E64D:  20 DD E3  JSR $E3DD
$E650:  68        PLA
$E651:  A0 00     LDY #$00
$E653:  91 9E     STA ($9E),Y
$E655:  68        PLA
$E656:  68        PLA
$E657:  4C 2A E4  JMP $E42A
$E65A:  20 B9 E6  JSR $E6B9
$E65D:  D1 8C     CMP ($8C),Y
$E65F:  98        TYA
$E660:  90 04     BCC $E666
$E662:  B1 8C     LDA ($8C),Y
$E664:  AA        TAX
$E665:  98        TYA
$E666:  48        PHA
$E667:  8A        TXA
$E668:  48        PHA
$E669:  20 DD E3  JSR $E3DD
$E66C:  A5 8C     LDA $8C
$E66E:  A4 8D     LDY $8D
$E670:  20 04 E6  JSR $E604
$E673:  68        PLA
$E674:  A8        TAY
$E675:  68        PLA
$E676:  18        CLC
$E677:  65 5E     ADC $5E
$E679:  85 5E     STA $5E
$E67B:  90 02     BCC $E67F
$E67D:  E6 5F     INC $5F
$E67F:  98        TYA
$E680:  20 E6 E5  JSR $E5E6
$E683:  4C 2A E4  JMP $E42A
$E686:  20 B9 E6  JSR $E6B9
$E689:  18        CLC
$E68A:  F1 8C     SBC ($8C),Y
$E68C:  49 FF     EOR #$FF
$E68E:  4C 60 E6  JMP $E660
$E691:  A9 FF     LDA #$FF
$E693:  85 A1     STA $A1
$E695:  20 B7 00  JSR $00B7
$E698:  C9 29     CMP #$29 (')')
$E69A:  F0 06     BEQ $E6A2
$E69C:  20 BE DE  JSR $DEBE
$E69F:  20 F8 E6  JSR $E6F8
$E6A2:  20 B9 E6  JSR $E6B9
$E6A5:  CA        DEX
$E6A6:  8A        TXA
$E6A7:  48        PHA
$E6A8:  18        CLC
$E6A9:  A2 00     LDX #$00
$E6AB:  F1 8C     SBC ($8C),Y
$E6AD:  B0 B8     BCS $E667
$E6AF:  49 FF     EOR #$FF
$E6B1:  C5 A1     CMP $A1
$E6B3:  90 B3     BCC $E668
$E6B5:  A5 A1     LDA $A1
$E6B7:  B0 AF     BCS $E668
$E6B9:  20 B8 DE  JSR $DEB8
$E6BC:  68        PLA
$E6BD:  A8        TAY
$E6BE:  68        PLA
$E6BF:  85 91     STA $91
$E6C1:  68        PLA
$E6C2:  68        PLA
$E6C3:  68        PLA
$E6C4:  AA        TAX
$E6C5:  68        PLA
$E6C6:  85 8C     STA $8C
$E6C8:  68        PLA
$E6C9:  85 8D     STA $8D
$E6CB:  A5 91     LDA $91
$E6CD:  48        PHA
$E6CE:  98        TYA
$E6CF:  48        PHA
$E6D0:  A0 00     LDY #$00
$E6D2:  8A        TXA
$E6D3:  F0 1D     BEQ $E6F2
$E6D5:  60        RTS
$E6D6:  20 DC E6  JSR $E6DC
$E6D9:  4C 01 E3  JMP $E301
$E6DC:  20 FD E5  JSR $E5FD
$E6DF:  A2 00     LDX #$00
$E6E1:  86 11     STX $11
$E6E3:  A8        TAY
$E6E4:  60        RTS
$E6E5:  20 DC E6  JSR $E6DC
$E6E8:  F0 08     BEQ $E6F2
$E6EA:  A0 00     LDY #$00
$E6EC:  B1 5E     LDA ($5E),Y
$E6EE:  A8        TAY
$E6EF:  4C 01 E3  JMP $E301
$E6F2:  4C 99 E1  JMP $E199
$E6F5:  20 B1 00  JSR $00B1
$E6F8:  20 67 DD  JSR $DD67
$E6FB:  20 08 E1  JSR $E108
$E6FE:  A6 A0     LDX $A0
$E700:  D0 F0     BNE $E6F2
$E702:  A6 A1     LDX $A1
$E704:  4C B7 00  JMP $00B7
$E707:  20 DC E6  JSR $E6DC
$E70A:  D0 03     BNE $E70F
$E70C:  4C 4E E8  JMP $E84E
$E70F:  A6 B8     LDX $B8
$E711:  A4 B9     LDY $B9
$E713:  86 AD     STX $AD
$E715:  84 AE     STY $AE
$E717:  A6 5E     LDX $5E
$E719:  86 B8     STX $B8
$E71B:  18        CLC
$E71C:  65 5E     ADC $5E
$E71E:  85 60     STA $60
$E720:  A6 5F     LDX $5F
$E722:  86 B9     STX $B9
$E724:  90 01     BCC $E727
$E726:  E8        INX
$E727:  86 61     STX $61
$E729:  A0 00     LDY #$00
$E72B:  B1 60     LDA ($60),Y
$E72D:  48        PHA
$E72E:  A9 00     LDA #$00
$E730:  91 60     STA ($60),Y
$E732:  20 B7 00  JSR $00B7
$E735:  20 4A EC  JSR $EC4A
$E738:  68        PLA
$E739:  A0 00     LDY #$00
$E73B:  91 60     STA ($60),Y
$E73D:  A6 AD     LDX $AD
$E73F:  A4 AE     LDY $AE
$E741:  86 B8     STX $B8
$E743:  84 B9     STY $B9
$E745:  60        RTS
$E746:  20 67 DD  JSR $DD67
$E749:  20 52 E7  JSR $E752
$E74C:  20 BE DE  JSR $DEBE
$E74F:  4C F8 E6  JMP $E6F8
$E752:  A5 9D     LDA $9D
$E754:  C9 91     CMP #$91
$E756:  B0 9A     BCS $E6F2
$E758:  20 F2 EB  JSR $EBF2
$E75B:  A5 A0     LDA $A0
$E75D:  A4 A1     LDY $A1
$E75F:  84 50     STY $50
$E761:  85 51     STA $51
$E763:  60        RTS
$E764:  A5 50     LDA $50
$E766:  48        PHA
$E767:  A5 51     LDA $51
$E769:  48        PHA
$E76A:  20 52 E7  JSR $E752
$E76D:  A0 00     LDY #$00
$E76F:  B1 50     LDA ($50),Y
$E771:  A8        TAY
$E772:  68        PLA
$E773:  85 51     STA $51
$E775:  68        PLA
$E776:  85 50     STA $50
$E778:  4C 01 E3  JMP $E301
$E77B:  20 46 E7  JSR $E746
$E77E:  8A        TXA
$E77F:  A0 00     LDY #$00
$E781:  91 50     STA ($50),Y
$E783:  60        RTS
$E784:  20 46 E7  JSR $E746
$E787:  86 85     STX $85
$E789:  A2 00     LDX #$00
$E78B:  20 B7 00  JSR $00B7
$E78E:  F0 03     BEQ $E793
$E790:  20 4C E7  JSR $E74C
$E793:  86 86     STX $86
$E795:  A0 00     LDY #$00
$E797:  B1 50     LDA ($50),Y
$E799:  45 86     EOR $86
$E79B:  25 85     AND $85
$E79D:  F0 F8     BEQ $E797
$E79F:  60        RTS
$E7A0:  A9 64     LDA #$64 ('d')
$E7A2:  A0 EE     LDY #$EE ('n')
$E7A4:  4C BE E7  JMP $E7BE
$E7A7:  20 E3 E9  JSR $E9E3
$E7AA:  A5 A2     LDA $A2
$E7AC:  49 FF     EOR #$FF
$E7AE:  85 A2     STA $A2
$E7B0:  45 AA     EOR $AA
$E7B2:  85 AB     STA $AB
$E7B4:  A5 9D     LDA $9D
$E7B6:  4C C1 E7  JMP $E7C1
$E7B9:  20 F0 E8  JSR $E8F0
$E7BC:  90 3C     BCC $E7FA
$E7BE:  20 E3 E9  JSR $E9E3
$E7C1:  D0 03     BNE $E7C6
$E7C3:  4C 53 EB  JMP $EB53
$E7C6:  A6 AC     LDX $AC
$E7C8:  86 92     STX $92
$E7CA:  A2 A5     LDX #$A5 ('%')
$E7CC:  A5 A5     LDA $A5
$E7CE:  A8        TAY
$E7CF:  F0 CE     BEQ $E79F
$E7D1:  38        SEC
$E7D2:  E5 9D     SBC $9D
$E7D4:  F0 24     BEQ $E7FA
$E7D6:  90 12     BCC $E7EA
$E7D8:  84 9D     STY $9D
$E7DA:  A4 AA     LDY $AA
$E7DC:  84 A2     STY $A2
$E7DE:  49 FF     EOR #$FF
$E7E0:  69 00     ADC #$00
$E7E2:  A0 00     LDY #$00
$E7E4:  84 92     STY $92
$E7E6:  A2 9D     LDX #$9D
$E7E8:  D0 04     BNE $E7EE
$E7EA:  A0 00     LDY #$00
$E7EC:  84 AC     STY $AC
$E7EE:  C9 F9     CMP #$F9 ('y')
$E7F0:  30 C7     BMI $E7B9
$E7F2:  A8        TAY
$E7F3:  A5 AC     LDA $AC
$E7F5:  56 01     LSR $01,X
$E7F7:  20 07 E9  JSR $E907
$E7FA:  24 AB     BIT $AB
$E7FC:  10 57     BPL $E855
$E7FE:  A0 9D     LDY #$9D
$E800:  E0 A5     CPX #$A5 ('%')
$E802:  F0 02     BEQ $E806
$E804:  A0 A5     LDY #$A5 ('%')
$E806:  38        SEC
$E807:  49 FF     EOR #$FF
$E809:  65 92     ADC $92
$E80B:  85 AC     STA $AC
$E80D:  B9 04 00  LDA $0004,Y
$E810:  F5 04     SBC $04,X
$E812:  85 A1     STA $A1
$E814:  B9 03 00  LDA $0003,Y
$E817:  F5 03     SBC $03,X
$E819:  85 A0     STA $A0
$E81B:  B9 02 00  LDA $0002,Y
$E81E:  F5 02     SBC $02,X
$E820:  85 9F     STA $9F
$E822:  B9 01 00  LDA $0001,Y
$E825:  F5 01     SBC $01,X
$E827:  85 9E     STA $9E
$E829:  B0 03     BCS $E82E
$E82B:  20 9E E8  JSR $E89E
$E82E:  A0 00     LDY #$00
$E830:  98        TYA
$E831:  18        CLC
$E832:  A6 9E     LDX $9E
$E834:  D0 4A     BNE $E880
$E836:  A6 9F     LDX $9F
$E838:  86 9E     STX $9E
$E83A:  A6 A0     LDX $A0
$E83C:  86 9F     STX $9F
$E83E:  A6 A1     LDX $A1
$E840:  86 A0     STX $A0
$E842:  A6 AC     LDX $AC
$E844:  86 A1     STX $A1
$E846:  84 AC     STY $AC
$E848:  69 08     ADC #$08
$E84A:  C9 20     CMP #$20 (' ')
$E84C:  D0 E4     BNE $E832
$E84E:  A9 00     LDA #$00
$E850:  85 9D     STA $9D
$E852:  85 A2     STA $A2
$E854:  60        RTS
$E855:  65 92     ADC $92
$E857:  85 AC     STA $AC
$E859:  A5 A1     LDA $A1
$E85B:  65 A9     ADC $A9
$E85D:  85 A1     STA $A1
$E85F:  A5 A0     LDA $A0
$E861:  65 A8     ADC $A8
$E863:  85 A0     STA $A0
$E865:  A5 9F     LDA $9F
$E867:  65 A7     ADC $A7
$E869:  85 9F     STA $9F
$E86B:  A5 9E     LDA $9E
$E86D:  65 A6     ADC $A6
$E86F:  85 9E     STA $9E
$E871:  4C 8D E8  JMP $E88D
$E874:  69 01     ADC #$01
$E876:  06 AC     ASL $AC
$E878:  26 A1     ROL $A1
$E87A:  26 A0     ROL $A0
$E87C:  26 9F     ROL $9F
$E87E:  26 9E     ROL $9E
$E880:  10 F2     BPL $E874
$E882:  38        SEC
$E883:  E5 9D     SBC $9D
$E885:  B0 C7     BCS $E84E
$E887:  49 FF     EOR #$FF
$E889:  69 01     ADC #$01
$E88B:  85 9D     STA $9D
$E88D:  90 0E     BCC $E89D
$E88F:  E6 9D     INC $9D
$E891:  F0 42     BEQ $E8D5
$E893:  66 9E     ROR $9E
$E895:  66 9F     ROR $9F
$E897:  66 A0     ROR $A0
$E899:  66 A1     ROR $A1
$E89B:  66 AC     ROR $AC
$E89D:  60        RTS
$E89E:  A5 A2     LDA $A2
$E8A0:  49 FF     EOR #$FF
$E8A2:  85 A2     STA $A2
$E8A4:  A5 9E     LDA $9E
$E8A6:  49 FF     EOR #$FF
$E8A8:  85 9E     STA $9E
$E8AA:  A5 9F     LDA $9F
$E8AC:  49 FF     EOR #$FF
$E8AE:  85 9F     STA $9F
$E8B0:  A5 A0     LDA $A0
$E8B2:  49 FF     EOR #$FF
$E8B4:  85 A0     STA $A0
$E8B6:  A5 A1     LDA $A1
$E8B8:  49 FF     EOR #$FF
$E8BA:  85 A1     STA $A1
$E8BC:  A5 AC     LDA $AC
$E8BE:  49 FF     EOR #$FF
$E8C0:  85 AC     STA $AC
$E8C2:  E6 AC     INC $AC
$E8C4:  D0 0E     BNE $E8D4
$E8C6:  E6 A1     INC $A1
$E8C8:  D0 0A     BNE $E8D4
$E8CA:  E6 A0     INC $A0
$E8CC:  D0 06     BNE $E8D4
$E8CE:  E6 9F     INC $9F
$E8D0:  D0 02     BNE $E8D4
$E8D2:  E6 9E     INC $9E
$E8D4:  60        RTS
$E8D5:  A2 45     LDX #$45 ('E')
$E8D7:  4C 12 D4  JMP $D412
$E8DA:  A2 61     LDX #$61 ('a')
$E8DC:  B4 04     LDY $04,X
$E8DE:  84 AC     STY $AC
$E8E0:  B4 03     LDY $03,X
$E8E2:  94 04     STY $04,X
$E8E4:  B4 02     LDY $02,X
$E8E6:  94 03     STY $03,X
$E8E8:  B4 01     LDY $01,X
$E8EA:  94 02     STY $02,X
$E8EC:  A4 A4     LDY $A4
$E8EE:  94 01     STY $01,X
$E8F0:  69 08     ADC #$08
$E8F2:  30 E8     BMI $E8DC
$E8F4:  F0 E6     BEQ $E8DC
$E8F6:  E9 08     SBC #$08
$E8F8:  A8        TAY
$E8F9:  A5 AC     LDA $AC
$E8FB:  B0 14     BCS $E911
$E8FD:  16 01     ASL $01,X
$E8FF:  90 02     BCC $E903
$E901:  F6 01     INC $01,X
$E903:  76 01     ROR $01,X
$E905:  76 01     ROR $01,X
$E907:  76 02     ROR $02,X
$E909:  76 03     ROR $03,X
$E90B:  76 04     ROR $04,X
$E90D:  6A        ROR
$E90E:  C8        INY
$E90F:  D0 EC     BNE $E8FD
$E911:  18        CLC
$E912:  60        RTS
$E913:  81 00     STA ($00,X)
$E915:  00        BRK
$E916:  00        BRK
$E917:  00        BRK
$E918:  03        .BYTE $03
$E919:  7F        .BYTE $7F
$E91A:  5E 56 CB  LSR $CB56,X
$E91D:  79 80 13  ADC $1380,Y
$E920:  9B        .BYTE $9B
$E921:  0B        .BYTE $0B
$E922:  64        .BYTE $64
$E923:  80        .BYTE $80
$E924:  76 38     ROR $38,X
$E926:  93        .BYTE $93
$E927:  16 82     ASL $82,X
$E929:  38        SEC
$E92A:  AA        TAX
$E92B:  3B        .BYTE $3B
$E92C:  20 80 35  JSR $3580
$E92F:  04        .BYTE $04
$E930:  F3        .BYTE $F3
$E931:  34        .BYTE $34
$E932:  81 35     STA ($35,X)
$E934:  04        .BYTE $04
$E935:  F3        .BYTE $F3
$E936:  34        .BYTE $34
$E937:  80        .BYTE $80
$E938:  80        .BYTE $80
$E939:  00        BRK
$E93A:  00        BRK
$E93B:  00        BRK
$E93C:  80        .BYTE $80
$E93D:  31 72     AND ($72),Y
$E93F:  17        .BYTE $17
$E940:  F8        SED
$E941:  20 82 EB  JSR $EB82
$E944:  F0 02     BEQ $E948
$E946:  10 03     BPL $E94B
$E948:  4C 99 E1  JMP $E199
$E94B:  A5 9D     LDA $9D
$E94D:  E9 7F     SBC #$7F
$E94F:  48        PHA
$E950:  A9 80     LDA #$80
$E952:  85 9D     STA $9D
$E954:  A9 2D     LDA #$2D ('-')
$E956:  A0 E9     LDY #$E9 ('i')
$E958:  20 BE E7  JSR $E7BE
$E95B:  A9 32     LDA #$32 ('2')
$E95D:  A0 E9     LDY #$E9 ('i')
$E95F:  20 66 EA  JSR $EA66
$E962:  A9 13     LDA #$13
$E964:  A0 E9     LDY #$E9 ('i')
$E966:  20 A7 E7  JSR $E7A7
$E969:  A9 18     LDA #$18
$E96B:  A0 E9     LDY #$E9 ('i')
$E96D:  20 5C EF  JSR $EF5C
$E970:  A9 37     LDA #$37 ('7')
$E972:  A0 E9     LDY #$E9 ('i')
$E974:  20 BE E7  JSR $E7BE
$E977:  68        PLA
$E978:  20 D5 EC  JSR $ECD5
$E97B:  A9 3C     LDA #$3C ('<')
$E97D:  A0 E9     LDY #$E9 ('i')
$E97F:  20 E3 E9  JSR $E9E3
$E982:  D0 03     BNE $E987
$E984:  4C E2 E9  JMP $E9E2
$E987:  20 0E EA  JSR $EA0E
$E98A:  A9 00     LDA #$00
$E98C:  85 62     STA $62
$E98E:  85 63     STA $63
$E990:  85 64     STA $64
$E992:  85 65     STA $65
$E994:  A5 AC     LDA $AC
$E996:  20 B0 E9  JSR $E9B0
$E999:  A5 A1     LDA $A1
$E99B:  20 B0 E9  JSR $E9B0
$E99E:  A5 A0     LDA $A0
$E9A0:  20 B0 E9  JSR $E9B0
$E9A3:  A5 9F     LDA $9F
$E9A5:  20 B0 E9  JSR $E9B0
$E9A8:  A5 9E     LDA $9E
$E9AA:  20 B5 E9  JSR $E9B5
$E9AD:  4C E6 EA  JMP $EAE6
$E9B0:  D0 03     BNE $E9B5
$E9B2:  4C DA E8  JMP $E8DA
$E9B5:  4A        LSR
$E9B6:  09 80     ORA #$80
$E9B8:  A8        TAY
$E9B9:  90 19     BCC $E9D4
$E9BB:  18        CLC
$E9BC:  A5 65     LDA $65
$E9BE:  65 A9     ADC $A9
$E9C0:  85 65     STA $65
$E9C2:  A5 64     LDA $64
$E9C4:  65 A8     ADC $A8
$E9C6:  85 64     STA $64
$E9C8:  A5 63     LDA $63
$E9CA:  65 A7     ADC $A7
$E9CC:  85 63     STA $63
$E9CE:  A5 62     LDA $62
$E9D0:  65 A6     ADC $A6
$E9D2:  85 62     STA $62
$E9D4:  66 62     ROR $62
$E9D6:  66 63     ROR $63
$E9D8:  66 64     ROR $64
$E9DA:  66 65     ROR $65
$E9DC:  66 AC     ROR $AC
$E9DE:  98        TYA
$E9DF:  4A        LSR
$E9E0:  D0 D6     BNE $E9B8
$E9E2:  60        RTS
$E9E3:  85 5E     STA $5E
$E9E5:  84 5F     STY $5F
$E9E7:  A0 04     LDY #$04
$E9E9:  B1 5E     LDA ($5E),Y
$E9EB:  85 A9     STA $A9
$E9ED:  88        DEY
$E9EE:  B1 5E     LDA ($5E),Y
$E9F0:  85 A8     STA $A8
$E9F2:  88        DEY
$E9F3:  B1 5E     LDA ($5E),Y
$E9F5:  85 A7     STA $A7
$E9F7:  88        DEY
$E9F8:  B1 5E     LDA ($5E),Y
$E9FA:  85 AA     STA $AA
$E9FC:  45 A2     EOR $A2
$E9FE:  85 AB     STA $AB
$EA00:  A5 AA     LDA $AA
$EA02:  09 80     ORA #$80
$EA04:  85 A6     STA $A6
$EA06:  88        DEY
$EA07:  B1 5E     LDA ($5E),Y
$EA09:  85 A5     STA $A5
$EA0B:  A5 9D     LDA $9D
$EA0D:  60        RTS
$EA0E:  A5 A5     LDA $A5
$EA10:  F0 1F     BEQ $EA31
$EA12:  18        CLC
$EA13:  65 9D     ADC $9D
$EA15:  90 04     BCC $EA1B
$EA17:  30 1D     BMI $EA36
$EA19:  18        CLC
$EA1A:  2C 10 14  BIT $1410
$EA1D:  69 80     ADC #$80
$EA1F:  85 9D     STA $9D
$EA21:  D0 03     BNE $EA26
$EA23:  4C 52 E8  JMP $E852
$EA26:  A5 AB     LDA $AB
$EA28:  85 A2     STA $A2
$EA2A:  60        RTS
$EA2B:  A5 A2     LDA $A2
$EA2D:  49 FF     EOR #$FF
$EA2F:  30 05     BMI $EA36
$EA31:  68        PLA
$EA32:  68        PLA
$EA33:  4C 4E E8  JMP $E84E
$EA36:  4C D5 E8  JMP $E8D5
$EA39:  20 63 EB  JSR $EB63
$EA3C:  AA        TAX
$EA3D:  F0 10     BEQ $EA4F
$EA3F:  18        CLC
$EA40:  69 02     ADC #$02
$EA42:  B0 F2     BCS $EA36
$EA44:  A2 00     LDX #$00
$EA46:  86 AB     STX $AB
$EA48:  20 CE E7  JSR $E7CE
$EA4B:  E6 9D     INC $9D
$EA4D:  F0 E7     BEQ $EA36
$EA4F:  60        RTS
$EA50:  84 20     STY $20
$EA52:  00        BRK
$EA53:  00        BRK
$EA54:  00        BRK
$EA55:  20 63 EB  JSR $EB63
$EA58:  A9 50     LDA #$50 ('P')
$EA5A:  A0 EA     LDY #$EA ('j')
$EA5C:  A2 00     LDX #$00
$EA5E:  86 AB     STX $AB
$EA60:  20 F9 EA  JSR $EAF9
$EA63:  4C 69 EA  JMP $EA69
$EA66:  20 E3 E9  JSR $E9E3
$EA69:  F0 76     BEQ $EAE1
$EA6B:  20 72 EB  JSR $EB72
$EA6E:  A9 00     LDA #$00
$EA70:  38        SEC
$EA71:  E5 9D     SBC $9D
$EA73:  85 9D     STA $9D
$EA75:  20 0E EA  JSR $EA0E
$EA78:  E6 9D     INC $9D
$EA7A:  F0 BA     BEQ $EA36
$EA7C:  A2 FC     LDX #$FC ('|')
$EA7E:  A9 01     LDA #$01
$EA80:  A4 A6     LDY $A6
$EA82:  C4 9E     CPY $9E
$EA84:  D0 10     BNE $EA96
$EA86:  A4 A7     LDY $A7
$EA88:  C4 9F     CPY $9F
$EA8A:  D0 0A     BNE $EA96
$EA8C:  A4 A8     LDY $A8
$EA8E:  C4 A0     CPY $A0
$EA90:  D0 04     BNE $EA96
$EA92:  A4 A9     LDY $A9
$EA94:  C4 A1     CPY $A1
$EA96:  08        PHP
$EA97:  2A        ROL
$EA98:  90 09     BCC $EAA3
$EA9A:  E8        INX
$EA9B:  95 65     STA $65,X
$EA9D:  F0 32     BEQ $EAD1
$EA9F:  10 34     BPL $EAD5
$EAA1:  A9 01     LDA #$01
$EAA3:  28        PLP
$EAA4:  B0 0E     BCS $EAB4
$EAA6:  06 A9     ASL $A9
$EAA8:  26 A8     ROL $A8
$EAAA:  26 A7     ROL $A7
$EAAC:  26 A6     ROL $A6
$EAAE:  B0 E6     BCS $EA96
$EAB0:  30 CE     BMI $EA80
$EAB2:  10 E2     BPL $EA96
$EAB4:  A8        TAY
$EAB5:  A5 A9     LDA $A9
$EAB7:  E5 A1     SBC $A1
$EAB9:  85 A9     STA $A9
$EABB:  A5 A8     LDA $A8
$EABD:  E5 A0     SBC $A0
$EABF:  85 A8     STA $A8
$EAC1:  A5 A7     LDA $A7
$EAC3:  E5 9F     SBC $9F
$EAC5:  85 A7     STA $A7
$EAC7:  A5 A6     LDA $A6
$EAC9:  E5 9E     SBC $9E
$EACB:  85 A6     STA $A6
$EACD:  98        TYA
$EACE:  4C A6 EA  JMP $EAA6
$EAD1:  A9 40     LDA #$40 ('@')
$EAD3:  D0 CE     BNE $EAA3
$EAD5:  0A        ASL
$EAD6:  0A        ASL
$EAD7:  0A        ASL
$EAD8:  0A        ASL
$EAD9:  0A        ASL
$EADA:  0A        ASL
$EADB:  85 AC     STA $AC
$EADD:  28        PLP
$EADE:  4C E6 EA  JMP $EAE6
$EAE1:  A2 85     LDX #$85
$EAE3:  4C 12 D4  JMP $D412
$EAE6:  A5 62     LDA $62
$EAE8:  85 9E     STA $9E
$EAEA:  A5 63     LDA $63
$EAEC:  85 9F     STA $9F
$EAEE:  A5 64     LDA $64
$EAF0:  85 A0     STA $A0
$EAF2:  A5 65     LDA $65
$EAF4:  85 A1     STA $A1
$EAF6:  4C 2E E8  JMP $E82E
$EAF9:  85 5E     STA $5E
$EAFB:  84 5F     STY $5F
$EAFD:  A0 04     LDY #$04
$EAFF:  B1 5E     LDA ($5E),Y
$EB01:  85 A1     STA $A1
$EB03:  88        DEY
$EB04:  B1 5E     LDA ($5E),Y
$EB06:  85 A0     STA $A0
$EB08:  88        DEY
$EB09:  B1 5E     LDA ($5E),Y
$EB0B:  85 9F     STA $9F
$EB0D:  88        DEY
$EB0E:  B1 5E     LDA ($5E),Y
$EB10:  85 A2     STA $A2
$EB12:  09 80     ORA #$80
$EB14:  85 9E     STA $9E
$EB16:  88        DEY
$EB17:  B1 5E     LDA ($5E),Y
$EB19:  85 9D     STA $9D
$EB1B:  84 AC     STY $AC
$EB1D:  60        RTS
$EB1E:  A2 98     LDX #$98
$EB20:  2C A2 93  BIT $93A2
$EB23:  A0 00     LDY #$00
$EB25:  F0 04     BEQ $EB2B
$EB27:  A6 85     LDX $85
$EB29:  A4 86     LDY $86
$EB2B:  20 72 EB  JSR $EB72
$EB2E:  86 5E     STX $5E
$EB30:  84 5F     STY $5F
$EB32:  A0 04     LDY #$04
$EB34:  A5 A1     LDA $A1
$EB36:  91 5E     STA ($5E),Y
$EB38:  88        DEY
$EB39:  A5 A0     LDA $A0
$EB3B:  91 5E     STA ($5E),Y
$EB3D:  88        DEY
$EB3E:  A5 9F     LDA $9F
$EB40:  91 5E     STA ($5E),Y
$EB42:  88        DEY
$EB43:  A5 A2     LDA $A2
$EB45:  09 7F     ORA #$7F
$EB47:  25 9E     AND $9E
$EB49:  91 5E     STA ($5E),Y
$EB4B:  88        DEY
$EB4C:  A5 9D     LDA $9D
$EB4E:  91 5E     STA ($5E),Y
$EB50:  84 AC     STY $AC
$EB52:  60        RTS
$EB53:  A5 AA     LDA $AA
$EB55:  85 A2     STA $A2
$EB57:  A2 05     LDX #$05
$EB59:  B5 A4     LDA $A4,X
$EB5B:  95 9C     STA $9C,X
$EB5D:  CA        DEX
$EB5E:  D0 F9     BNE $EB59
$EB60:  86 AC     STX $AC
$EB62:  60        RTS
$EB63:  20 72 EB  JSR $EB72
$EB66:  A2 06     LDX #$06
$EB68:  B5 9C     LDA $9C,X
$EB6A:  95 A4     STA $A4,X
$EB6C:  CA        DEX
$EB6D:  D0 F9     BNE $EB68
$EB6F:  86 AC     STX $AC
$EB71:  60        RTS
$EB72:  A5 9D     LDA $9D
$EB74:  F0 FB     BEQ $EB71
$EB76:  06 AC     ASL $AC
$EB78:  90 F7     BCC $EB71
$EB7A:  20 C6 E8  JSR $E8C6
$EB7D:  D0 F2     BNE $EB71
$EB7F:  4C 8F E8  JMP $E88F
$EB82:  A5 9D     LDA $9D
$EB84:  F0 09     BEQ $EB8F
$EB86:  A5 A2     LDA $A2
$EB88:  2A        ROL
$EB89:  A9 FF     LDA #$FF
$EB8B:  B0 02     BCS $EB8F
$EB8D:  A9 01     LDA #$01
$EB8F:  60        RTS
$EB90:  20 82 EB  JSR $EB82
$EB93:  85 9E     STA $9E
$EB95:  A9 00     LDA #$00
$EB97:  85 9F     STA $9F
$EB99:  A2 88     LDX #$88
$EB9B:  A5 9E     LDA $9E
$EB9D:  49 FF     EOR #$FF
$EB9F:  2A        ROL
$EBA0:  A9 00     LDA #$00
$EBA2:  85 A1     STA $A1
$EBA4:  85 A0     STA $A0
$EBA6:  86 9D     STX $9D
$EBA8:  85 AC     STA $AC
$EBAA:  85 A2     STA $A2
$EBAC:  4C 29 E8  JMP $E829
$EBAF:  46 A2     LSR $A2
$EBB1:  60        RTS
$EBB2:  85 60     STA $60
$EBB4:  84 61     STY $61
$EBB6:  A0 00     LDY #$00
$EBB8:  B1 60     LDA ($60),Y
$EBBA:  C8        INY
$EBBB:  AA        TAX
$EBBC:  F0 C4     BEQ $EB82
$EBBE:  B1 60     LDA ($60),Y
$EBC0:  45 A2     EOR $A2
$EBC2:  30 C2     BMI $EB86
$EBC4:  E4 9D     CPX $9D
$EBC6:  D0 21     BNE $EBE9
$EBC8:  B1 60     LDA ($60),Y
$EBCA:  09 80     ORA #$80
$EBCC:  C5 9E     CMP $9E
$EBCE:  D0 19     BNE $EBE9
$EBD0:  C8        INY
$EBD1:  B1 60     LDA ($60),Y
$EBD3:  C5 9F     CMP $9F
$EBD5:  D0 12     BNE $EBE9
$EBD7:  C8        INY
$EBD8:  B1 60     LDA ($60),Y
$EBDA:  C5 A0     CMP $A0
$EBDC:  D0 0B     BNE $EBE9
$EBDE:  C8        INY
$EBDF:  A9 7F     LDA #$7F
$EBE1:  C5 AC     CMP $AC
$EBE3:  B1 60     LDA ($60),Y
$EBE5:  E5 A1     SBC $A1
$EBE7:  F0 28     BEQ $EC11
$EBE9:  A5 A2     LDA $A2
$EBEB:  90 02     BCC $EBEF
$EBED:  49 FF     EOR #$FF
$EBEF:  4C 88 EB  JMP $EB88
$EBF2:  A5 9D     LDA $9D
$EBF4:  F0 4A     BEQ $EC40
$EBF6:  38        SEC
$EBF7:  E9 A0     SBC #$A0 (' ')
$EBF9:  24 A2     BIT $A2
$EBFB:  10 09     BPL $EC06
$EBFD:  AA        TAX
$EBFE:  A9 FF     LDA #$FF
$EC00:  85 A4     STA $A4
$EC02:  20 A4 E8  JSR $E8A4
$EC05:  8A        TXA
$EC06:  A2 9D     LDX #$9D
$EC08:  C9 F9     CMP #$F9 ('y')
$EC0A:  10 06     BPL $EC12
$EC0C:  20 F0 E8  JSR $E8F0
$EC0F:  84 A4     STY $A4
$EC11:  60        RTS
$EC12:  A8        TAY
$EC13:  A5 A2     LDA $A2
$EC15:  29 80     AND #$80
$EC17:  46 9E     LSR $9E
$EC19:  05 9E     ORA $9E
$EC1B:  85 9E     STA $9E
$EC1D:  20 07 E9  JSR $E907
$EC20:  84 A4     STY $A4
$EC22:  60        RTS
$EC23:  A5 9D     LDA $9D
$EC25:  C9 A0     CMP #$A0 (' ')
$EC27:  B0 20     BCS $EC49
$EC29:  20 F2 EB  JSR $EBF2
$EC2C:  84 AC     STY $AC
$EC2E:  A5 A2     LDA $A2
$EC30:  84 A2     STY $A2
$EC32:  49 80     EOR #$80
$EC34:  2A        ROL
$EC35:  A9 A0     LDA #$A0 (' ')
$EC37:  85 9D     STA $9D
$EC39:  A5 A1     LDA $A1
$EC3B:  85 0D     STA $0D
$EC3D:  4C 29 E8  JMP $E829
$EC40:  85 9E     STA $9E
$EC42:  85 9F     STA $9F
$EC44:  85 A0     STA $A0
$EC46:  85 A1     STA $A1
$EC48:  A8        TAY
$EC49:  60        RTS
$EC4A:  A0 00     LDY #$00
$EC4C:  A2 0A     LDX #$0A
$EC4E:  94 99     STY $99,X
$EC50:  CA        DEX
$EC51:  10 FB     BPL $EC4E
$EC53:  90 0F     BCC $EC64
$EC55:  C9 2D     CMP #$2D ('-')
$EC57:  D0 04     BNE $EC5D
$EC59:  86 A3     STX $A3
$EC5B:  F0 04     BEQ $EC61
$EC5D:  C9 2B     CMP #$2B ('+')
$EC5F:  D0 05     BNE $EC66
$EC61:  20 B1 00  JSR $00B1
$EC64:  90 5B     BCC $ECC1
$EC66:  C9 2E     CMP #$2E ('.')
$EC68:  F0 2E     BEQ $EC98
$EC6A:  C9 45     CMP #$45 ('E')
$EC6C:  D0 30     BNE $EC9E
$EC6E:  20 B1 00  JSR $00B1
$EC71:  90 17     BCC $EC8A
$EC73:  C9 C9     CMP #$C9 ('I')
$EC75:  F0 0E     BEQ $EC85
$EC77:  C9 2D     CMP #$2D ('-')
$EC79:  F0 0A     BEQ $EC85
$EC7B:  C9 C8     CMP #$C8 ('H')
$EC7D:  F0 08     BEQ $EC87
$EC7F:  C9 2B     CMP #$2B ('+')
$EC81:  F0 04     BEQ $EC87
$EC83:  D0 07     BNE $EC8C
$EC85:  66 9C     ROR $9C
$EC87:  20 B1 00  JSR $00B1
$EC8A:  90 5C     BCC $ECE8
$EC8C:  24 9C     BIT $9C
$EC8E:  10 0E     BPL $EC9E
$EC90:  A9 00     LDA #$00
$EC92:  38        SEC
$EC93:  E5 9A     SBC $9A
$EC95:  4C A0 EC  JMP $ECA0
$EC98:  66 9B     ROR $9B
$EC9A:  24 9B     BIT $9B
$EC9C:  50 C3     BVC $EC61
$EC9E:  A5 9A     LDA $9A
$ECA0:  38        SEC
$ECA1:  E5 99     SBC $99
$ECA3:  85 9A     STA $9A
$ECA5:  F0 12     BEQ $ECB9
$ECA7:  10 09     BPL $ECB2
$ECA9:  20 55 EA  JSR $EA55
$ECAC:  E6 9A     INC $9A
$ECAE:  D0 F9     BNE $ECA9
$ECB0:  F0 07     BEQ $ECB9
$ECB2:  20 39 EA  JSR $EA39
$ECB5:  C6 9A     DEC $9A
$ECB7:  D0 F9     BNE $ECB2
$ECB9:  A5 A3     LDA $A3
$ECBB:  30 01     BMI $ECBE
$ECBD:  60        RTS
$ECBE:  4C D0 EE  JMP $EED0
$ECC1:  48        PHA
$ECC2:  24 9B     BIT $9B
$ECC4:  10 02     BPL $ECC8
$ECC6:  E6 99     INC $99
$ECC8:  20 39 EA  JSR $EA39
$ECCB:  68        PLA
$ECCC:  38        SEC
$ECCD:  E9 30     SBC #$30 ('0')
$ECCF:  20 D5 EC  JSR $ECD5
$ECD2:  4C 61 EC  JMP $EC61
$ECD5:  48        PHA
$ECD6:  20 63 EB  JSR $EB63
$ECD9:  68        PLA
$ECDA:  20 93 EB  JSR $EB93
$ECDD:  A5 AA     LDA $AA
$ECDF:  45 A2     EOR $A2
$ECE1:  85 AB     STA $AB
$ECE3:  A6 9D     LDX $9D
$ECE5:  4C C1 E7  JMP $E7C1
$ECE8:  A5 9A     LDA $9A
$ECEA:  C9 0A     CMP #$0A
$ECEC:  90 09     BCC $ECF7
$ECEE:  A9 64     LDA #$64 ('d')
$ECF0:  24 9C     BIT $9C
$ECF2:  30 11     BMI $ED05
$ECF4:  4C D5 E8  JMP $E8D5
$ECF7:  0A        ASL
$ECF8:  0A        ASL
$ECF9:  18        CLC
$ECFA:  65 9A     ADC $9A
$ECFC:  0A        ASL
$ECFD:  18        CLC
$ECFE:  A0 00     LDY #$00
$ED00:  71 B8     ADC ($B8),Y
$ED02:  38        SEC
$ED03:  E9 30     SBC #$30 ('0')
$ED05:  85 9A     STA $9A
$ED07:  4C 87 EC  JMP $EC87
$ED0A:  9B        .BYTE $9B
$ED0B:  3E BC 1F  ROL $1FBC,X
$ED0E:  FD 9E 6E  SBC $6E9E,X
$ED11:  6B        .BYTE $6B
$ED12:  27        .BYTE $27
$ED13:  FD 9E 6E  SBC $6E9E,X
$ED16:  6B        .BYTE $6B
$ED17:  28        PLP
$ED18:  00        BRK
$ED19:  A9 58     LDA #$58 ('X')
$ED1B:  A0 D3     LDY #$D3 ('S')
$ED1D:  20 31 ED  JSR $ED31
$ED20:  A5 76     LDA $76
$ED22:  A6 75     LDX $75
$ED24:  85 9E     STA $9E
$ED26:  86 9F     STX $9F
$ED28:  A2 90     LDX #$90
$ED2A:  38        SEC
$ED2B:  20 A0 EB  JSR $EBA0
$ED2E:  20 34 ED  JSR $ED34
$ED31:  4C 3A DB  JMP $DB3A
$ED34:  A0 01     LDY #$01
$ED36:  A9 2D     LDA #$2D ('-')
$ED38:  88        DEY
$ED39:  24 A2     BIT $A2
$ED3B:  10 04     BPL $ED41
$ED3D:  C8        INY
$ED3E:  99 FF 00  STA $00FF,Y
$ED41:  85 A2     STA $A2
$ED43:  84 AD     STY $AD
$ED45:  C8        INY
$ED46:  A9 30     LDA #$30 ('0')
$ED48:  A6 9D     LDX $9D
$ED4A:  D0 03     BNE $ED4F
$ED4C:  4C 57 EE  JMP $EE57
$ED4F:  A9 00     LDA #$00
$ED51:  E0 80     CPX #$80
$ED53:  F0 02     BEQ $ED57
$ED55:  B0 09     BCS $ED60
$ED57:  A9 14     LDA #$14
$ED59:  A0 ED     LDY #$ED ('m')
$ED5B:  20 7F E9  JSR $E97F
$ED5E:  A9 F7     LDA #$F7 ('w')
$ED60:  85 99     STA $99
$ED62:  A9 0F     LDA #$0F
$ED64:  A0 ED     LDY #$ED ('m')
$ED66:  20 B2 EB  JSR $EBB2
$ED69:  F0 1E     BEQ $ED89
$ED6B:  10 12     BPL $ED7F
$ED6D:  A9 0A     LDA #$0A
$ED6F:  A0 ED     LDY #$ED ('m')
$ED71:  20 B2 EB  JSR $EBB2
$ED74:  F0 02     BEQ $ED78
$ED76:  10 0E     BPL $ED86
$ED78:  20 39 EA  JSR $EA39
$ED7B:  C6 99     DEC $99
$ED7D:  D0 EE     BNE $ED6D
$ED7F:  20 55 EA  JSR $EA55
$ED82:  E6 99     INC $99
$ED84:  D0 DC     BNE $ED62
$ED86:  20 A0 E7  JSR $E7A0
$ED89:  20 F2 EB  JSR $EBF2
$ED8C:  A2 01     LDX #$01
$ED8E:  A5 99     LDA $99
$ED90:  18        CLC
$ED91:  69 0A     ADC #$0A
$ED93:  30 09     BMI $ED9E
$ED95:  C9 0B     CMP #$0B
$ED97:  B0 06     BCS $ED9F
$ED99:  69 FF     ADC #$FF
$ED9B:  AA        TAX
$ED9C:  A9 02     LDA #$02
$ED9E:  38        SEC
$ED9F:  E9 02     SBC #$02
$EDA1:  85 9A     STA $9A
$EDA3:  86 99     STX $99
$EDA5:  8A        TXA
$EDA6:  F0 02     BEQ $EDAA
$EDA8:  10 13     BPL $EDBD
$EDAA:  A4 AD     LDY $AD
$EDAC:  A9 2E     LDA #$2E ('.')
$EDAE:  C8        INY
$EDAF:  99 FF 00  STA $00FF,Y
$EDB2:  8A        TXA
$EDB3:  F0 06     BEQ $EDBB
$EDB5:  A9 30     LDA #$30 ('0')
$EDB7:  C8        INY
$EDB8:  99 FF 00  STA $00FF,Y
$EDBB:  84 AD     STY $AD
$EDBD:  A0 00     LDY #$00
$EDBF:  A2 80     LDX #$80
$EDC1:  A5 A1     LDA $A1
$EDC3:  18        CLC
$EDC4:  79 6C EE  ADC $EE6C,Y
$EDC7:  85 A1     STA $A1
$EDC9:  A5 A0     LDA $A0
$EDCB:  79 6B EE  ADC $EE6B,Y
$EDCE:  85 A0     STA $A0
$EDD0:  A5 9F     LDA $9F
$EDD2:  79 6A EE  ADC $EE6A,Y
$EDD5:  85 9F     STA $9F
$EDD7:  A5 9E     LDA $9E
$EDD9:  79 69 EE  ADC $EE69,Y
$EDDC:  85 9E     STA $9E
$EDDE:  E8        INX
$EDDF:  B0 04     BCS $EDE5
$EDE1:  10 DE     BPL $EDC1
$EDE3:  30 02     BMI $EDE7
$EDE5:  30 DA     BMI $EDC1
$EDE7:  8A        TXA
$EDE8:  90 04     BCC $EDEE
$EDEA:  49 FF     EOR #$FF
$EDEC:  69 0A     ADC #$0A
$EDEE:  69 2F     ADC #$2F ('/')
$EDF0:  C8        INY
$EDF1:  C8        INY
$EDF2:  C8        INY
$EDF3:  C8        INY
$EDF4:  84 83     STY $83
$EDF6:  A4 AD     LDY $AD
$EDF8:  C8        INY
$EDF9:  AA        TAX
$EDFA:  29 7F     AND #$7F
$EDFC:  99 FF 00  STA $00FF,Y
$EDFF:  C6 99     DEC $99
$EE01:  D0 06     BNE $EE09
$EE03:  A9 2E     LDA #$2E ('.')
$EE05:  C8        INY
$EE06:  99 FF 00  STA $00FF,Y
$EE09:  84 AD     STY $AD
$EE0B:  A4 83     LDY $83
$EE0D:  8A        TXA
$EE0E:  49 FF     EOR #$FF
$EE10:  29 80     AND #$80
$EE12:  AA        TAX
$EE13:  C0 24     CPY #$24 ('$')
$EE15:  D0 AA     BNE $EDC1
$EE17:  A4 AD     LDY $AD
$EE19:  B9 FF 00  LDA $00FF,Y
$EE1C:  88        DEY
$EE1D:  C9 30     CMP #$30 ('0')
$EE1F:  F0 F8     BEQ $EE19
$EE21:  C9 2E     CMP #$2E ('.')
$EE23:  F0 01     BEQ $EE26
$EE25:  C8        INY
$EE26:  A9 2B     LDA #$2B ('+')
$EE28:  A6 9A     LDX $9A
$EE2A:  F0 2E     BEQ $EE5A
$EE2C:  10 08     BPL $EE36
$EE2E:  A9 00     LDA #$00
$EE30:  38        SEC
$EE31:  E5 9A     SBC $9A
$EE33:  AA        TAX
$EE34:  A9 2D     LDA #$2D ('-')
$EE36:  99 01 01  STA $0101,Y
$EE39:  A9 45     LDA #$45 ('E')
$EE3B:  99 00 01  STA $0100,Y
$EE3E:  8A        TXA
$EE3F:  A2 2F     LDX #$2F ('/')
$EE41:  38        SEC
$EE42:  E8        INX
$EE43:  E9 0A     SBC #$0A
$EE45:  B0 FB     BCS $EE42
$EE47:  69 3A     ADC #$3A (':')
$EE49:  99 03 01  STA $0103,Y
$EE4C:  8A        TXA
$EE4D:  99 02 01  STA $0102,Y
$EE50:  A9 00     LDA #$00
$EE52:  99 04 01  STA $0104,Y
$EE55:  F0 08     BEQ $EE5F
$EE57:  99 FF 00  STA $00FF,Y
$EE5A:  A9 00     LDA #$00
$EE5C:  99 00 01  STA $0100,Y
$EE5F:  A9 00     LDA #$00
$EE61:  A0 01     LDY #$01
$EE63:  60        RTS
$EE64:  80        .BYTE $80
$EE65:  00        BRK
$EE66:  00        BRK
$EE67:  00        BRK
$EE68:  00        BRK
$EE69:  FA        .BYTE $FA
$EE6A:  0A        ASL
$EE6B:  1F        .BYTE $1F
$EE6C:  00        BRK
$EE6D:  00        BRK
$EE6E:  98        TYA
$EE6F:  96 80     STX $80,Y
$EE71:  FF        .BYTE $FF
$EE72:  F0 BD     BEQ $EE31
$EE74:  C0 00     CPY #$00
$EE76:  01 86     ORA ($86,X)
$EE78:  A0 FF     LDY #$FF
$EE7A:  FF        .BYTE $FF
$EE7B:  D8        CLD
$EE7C:  F0 00     BEQ $EE7E
$EE7E:  00        BRK
$EE7F:  03        .BYTE $03
$EE80:  E8        INX
$EE81:  FF        .BYTE $FF
$EE82:  FF        .BYTE $FF
$EE83:  FF        .BYTE $FF
$EE84:  9C        .BYTE $9C
$EE85:  00        BRK
$EE86:  00        BRK
$EE87:  00        BRK
$EE88:  0A        ASL
$EE89:  FF        .BYTE $FF
$EE8A:  FF        .BYTE $FF
$EE8B:  FF        .BYTE $FF
$EE8C:  FF        .BYTE $FF
$EE8D:  20 63 EB  JSR $EB63
$EE90:  A9 64     LDA #$64 ('d')
$EE92:  A0 EE     LDY #$EE ('n')
$EE94:  20 F9 EA  JSR $EAF9
$EE97:  F0 70     BEQ $EF09
$EE99:  A5 A5     LDA $A5
$EE9B:  D0 03     BNE $EEA0
$EE9D:  4C 50 E8  JMP $E850
$EEA0:  A2 8A     LDX #$8A
$EEA2:  A0 00     LDY #$00
$EEA4:  20 2B EB  JSR $EB2B
$EEA7:  A5 AA     LDA $AA
$EEA9:  10 0F     BPL $EEBA
$EEAB:  20 23 EC  JSR $EC23
$EEAE:  A9 8A     LDA #$8A
$EEB0:  A0 00     LDY #$00
$EEB2:  20 B2 EB  JSR $EBB2
$EEB5:  D0 03     BNE $EEBA
$EEB7:  98        TYA
$EEB8:  A4 0D     LDY $0D
$EEBA:  20 55 EB  JSR $EB55
$EEBD:  98        TYA
$EEBE:  48        PHA
$EEBF:  20 41 E9  JSR $E941
$EEC2:  A9 8A     LDA #$8A
$EEC4:  A0 00     LDY #$00
$EEC6:  20 7F E9  JSR $E97F
$EEC9:  20 09 EF  JSR $EF09
$EECC:  68        PLA
$EECD:  4A        LSR
$EECE:  90 0A     BCC $EEDA
$EED0:  A5 9D     LDA $9D
$EED2:  F0 06     BEQ $EEDA
$EED4:  A5 A2     LDA $A2
$EED6:  49 FF     EOR #$FF
$EED8:  85 A2     STA $A2
$EEDA:  60        RTS
$EEDB:  81 38     STA ($38,X)
$EEDD:  AA        TAX
$EEDE:  3B        .BYTE $3B
$EEDF:  29 07     AND #$07
$EEE1:  71 34     ADC ($34),Y
$EEE3:  58        CLI
$EEE4:  3E 56 74  ROL $7456,X
$EEE7:  16 7E     ASL $7E,X
$EEE9:  B3        .BYTE $B3
$EEEA:  1B        .BYTE $1B
$EEEB:  77        .BYTE $77
$EEEC:  2F        .BYTE $2F
$EEED:  EE E3 85  INC $85E3
$EEF0:  7A        .BYTE $7A
$EEF1:  1D 84 1C  ORA $1C84,X
$EEF4:  2A        ROL
$EEF5:  7C        .BYTE $7C
$EEF6:  63        .BYTE $63
$EEF7:  59 58 0A  EOR $0A58,Y
$EEFA:  7E 75 FD  ROR $FD75,X
$EEFD:  E7        .BYTE $E7
$EEFE:  C6 80     DEC $80
$EF00:  31 72     AND ($72),Y
$EF02:  18        CLC
$EF03:  10 81     BPL $EE86
$EF05:  00        BRK
$EF06:  00        BRK
$EF07:  00        BRK
$EF08:  00        BRK
$EF09:  A9 DB     LDA #$DB ('[')
$EF0B:  A0 EE     LDY #$EE ('n')
$EF0D:  20 7F E9  JSR $E97F
$EF10:  A5 AC     LDA $AC
$EF12:  69 50     ADC #$50 ('P')
$EF14:  90 03     BCC $EF19
$EF16:  20 7A EB  JSR $EB7A
$EF19:  85 92     STA $92
$EF1B:  20 66 EB  JSR $EB66
$EF1E:  A5 9D     LDA $9D
$EF20:  C9 88     CMP #$88
$EF22:  90 03     BCC $EF27
$EF24:  20 2B EA  JSR $EA2B
$EF27:  20 23 EC  JSR $EC23
$EF2A:  A5 0D     LDA $0D
$EF2C:  18        CLC
$EF2D:  69 81     ADC #$81
$EF2F:  F0 F3     BEQ $EF24
$EF31:  38        SEC
$EF32:  E9 01     SBC #$01
$EF34:  48        PHA
$EF35:  A2 05     LDX #$05
$EF37:  B5 A5     LDA $A5,X
$EF39:  B4 9D     LDY $9D,X
$EF3B:  95 9D     STA $9D,X
$EF3D:  94 A5     STY $A5,X
$EF3F:  CA        DEX
$EF40:  10 F5     BPL $EF37
$EF42:  A5 92     LDA $92
$EF44:  85 AC     STA $AC
$EF46:  20 AA E7  JSR $E7AA
$EF49:  20 D0 EE  JSR $EED0
$EF4C:  A9 E0     LDA #$E0 ('`')
$EF4E:  A0 EE     LDY #$EE ('n')
$EF50:  20 72 EF  JSR $EF72
$EF53:  A9 00     LDA #$00
$EF55:  85 AB     STA $AB
$EF57:  68        PLA
$EF58:  20 10 EA  JSR $EA10
$EF5B:  60        RTS
$EF5C:  85 AD     STA $AD
$EF5E:  84 AE     STY $AE
$EF60:  20 21 EB  JSR $EB21
$EF63:  A9 93     LDA #$93
$EF65:  20 7F E9  JSR $E97F
$EF68:  20 76 EF  JSR $EF76
$EF6B:  A9 93     LDA #$93
$EF6D:  A0 00     LDY #$00
$EF6F:  4C 7F E9  JMP $E97F
$EF72:  85 AD     STA $AD
$EF74:  84 AE     STY $AE
$EF76:  20 1E EB  JSR $EB1E
$EF79:  B1 AD     LDA ($AD),Y
$EF7B:  85 A3     STA $A3
$EF7D:  A4 AD     LDY $AD
$EF7F:  C8        INY
$EF80:  98        TYA
$EF81:  D0 02     BNE $EF85
$EF83:  E6 AE     INC $AE
$EF85:  85 AD     STA $AD
$EF87:  A4 AE     LDY $AE
$EF89:  20 7F E9  JSR $E97F
$EF8C:  A5 AD     LDA $AD
$EF8E:  A4 AE     LDY $AE
$EF90:  18        CLC
$EF91:  69 05     ADC #$05
$EF93:  90 01     BCC $EF96
$EF95:  C8        INY
$EF96:  85 AD     STA $AD
$EF98:  84 AE     STY $AE
$EF9A:  20 BE E7  JSR $E7BE
$EF9D:  A9 98     LDA #$98
$EF9F:  A0 00     LDY #$00
$EFA1:  C6 A3     DEC $A3
$EFA3:  D0 E4     BNE $EF89
$EFA5:  60        RTS
$EFA6:  98        TYA
$EFA7:  35 44     AND $44,X
$EFA9:  7A        .BYTE $7A
$EFAA:  68        PLA
$EFAB:  28        PLP
$EFAC:  B1 46     LDA ($46),Y
$EFAE:  20 82 EB  JSR $EB82
$EFB1:  AA        TAX
$EFB2:  30 18     BMI $EFCC
$EFB4:  A9 C9     LDA #$C9 ('I')
$EFB6:  A0 00     LDY #$00
$EFB8:  20 F9 EA  JSR $EAF9
$EFBB:  8A        TXA
$EFBC:  F0 E7     BEQ $EFA5
$EFBE:  A9 A6     LDA #$A6 ('&')
$EFC0:  A0 EF     LDY #$EF ('o')
$EFC2:  20 7F E9  JSR $E97F
$EFC5:  A9 AA     LDA #$AA ('*')
$EFC7:  A0 EF     LDY #$EF ('o')
$EFC9:  20 BE E7  JSR $E7BE
$EFCC:  A6 A1     LDX $A1
$EFCE:  A5 9E     LDA $9E
$EFD0:  85 A1     STA $A1
$EFD2:  86 9E     STX $9E
$EFD4:  A9 00     LDA #$00
$EFD6:  85 A2     STA $A2
$EFD8:  A5 9D     LDA $9D
$EFDA:  85 AC     STA $AC
$EFDC:  A9 80     LDA #$80
$EFDE:  85 9D     STA $9D
$EFE0:  20 2E E8  JSR $E82E
$EFE3:  A2 C9     LDX #$C9 ('I')
$EFE5:  A0 00     LDY #$00
$EFE7:  4C 2B EB  JMP $EB2B
$EFEA:  A9 66     LDA #$66 ('f')
$EFEC:  A0 F0     LDY #$F0 ('p')
$EFEE:  20 BE E7  JSR $E7BE
$EFF1:  20 63 EB  JSR $EB63
$EFF4:  A9 6B     LDA #$6B ('k')
$EFF6:  A0 F0     LDY #$F0 ('p')
$EFF8:  A6 AA     LDX $AA
$EFFA:  20 5E EA  JSR $EA5E
$EFFD:  20 63 EB  JSR $EB63
$F000:  20 23 EC  JSR $EC23
$F003:  A9 00     LDA #$00
$F005:  85 AB     STA $AB
$F007:  20 AA E7  JSR $E7AA
$F00A:  A9 70     LDA #$70 ('p')
$F00C:  A0 F0     LDY #$F0 ('p')
$F00E:  20 A7 E7  JSR $E7A7
$F011:  A5 A2     LDA $A2
$F013:  48        PHA
$F014:  10 0D     BPL $F023
$F016:  20 A0 E7  JSR $E7A0
$F019:  A5 A2     LDA $A2
$F01B:  30 09     BMI $F026
$F01D:  A5 16     LDA $16
$F01F:  49 FF     EOR #$FF
$F021:  85 16     STA $16
$F023:  20 D0 EE  JSR $EED0
$F026:  A9 70     LDA #$70 ('p')
$F028:  A0 F0     LDY #$F0 ('p')
$F02A:  20 BE E7  JSR $E7BE
$F02D:  68        PLA
$F02E:  10 03     BPL $F033
$F030:  20 D0 EE  JSR $EED0
$F033:  A9 75     LDA #$75 ('u')
$F035:  A0 F0     LDY #$F0 ('p')
$F037:  4C 5C EF  JMP $EF5C
$F03A:  20 21 EB  JSR $EB21
$F03D:  A9 00     LDA #$00
$F03F:  85 16     STA $16
$F041:  20 F1 EF  JSR $EFF1
$F044:  A2 8A     LDX #$8A
$F046:  A0 00     LDY #$00
$F048:  20 E7 EF  JSR $EFE7
$F04B:  A9 93     LDA #$93
$F04D:  A0 00     LDY #$00
$F04F:  20 F9 EA  JSR $EAF9
$F052:  A9 00     LDA #$00
$F054:  85 A2     STA $A2
$F056:  A5 16     LDA $16
$F058:  20 62 F0  JSR $F062
$F05B:  A9 8A     LDA #$8A
$F05D:  A0 00     LDY #$00
$F05F:  4C 66 EA  JMP $EA66
$F062:  48        PHA
$F063:  4C 23 F0  JMP $F023
$F066:  81 49     STA ($49,X)
$F068:  0F        .BYTE $0F
$F069:  DA        .BYTE $DA
$F06A:  A2 83     LDX #$83
$F06C:  49 0F     EOR #$0F
$F06E:  DA        .BYTE $DA
$F06F:  A2 7F     LDX #$7F
$F071:  00        BRK
$F072:  00        BRK
$F073:  00        BRK
$F074:  00        BRK
$F075:  05 84     ORA $84
$F077:  E6 1A     INC $1A
$F079:  2D 1B 86  AND $861B
$F07C:  28        PLP
$F07D:  07        .BYTE $07
$F07E:  FB        .BYTE $FB
$F07F:  F8        SED
$F080:  87        .BYTE $87
$F081:  99 68 89  STA $8968,Y
$F084:  01 87     ORA ($87,X)
$F086:  23        .BYTE $23
$F087:  35 DF     AND $DF,X
$F089:  E1 86     SBC ($86,X)
$F08B:  A5 5D     LDA $5D
$F08D:  E7        .BYTE $E7
$F08E:  28        PLP
$F08F:  83        .BYTE $83
$F090:  49 0F     EOR #$0F
$F092:  DA        .BYTE $DA
$F093:  A2 A6     LDX #$A6 ('&')
$F095:  D3        .BYTE $D3
$F096:  C1 C8     CMP ($C8,X)
$F098:  D4        .BYTE $D4
$F099:  C8        INY
$F09A:  D5 C4     CMP $C4,X
$F09C:  CE CA A5  DEC $A5CA
$F09F:  A2 48     LDX #$48 ('H')
$F0A1:  10 03     BPL $F0A6
$F0A3:  20 D0 EE  JSR $EED0
$F0A6:  A5 9D     LDA $9D
$F0A8:  48        PHA
$F0A9:  C9 81     CMP #$81
$F0AB:  90 07     BCC $F0B4
$F0AD:  A9 13     LDA #$13
$F0AF:  A0 E9     LDY #$E9 ('i')
$F0B1:  20 66 EA  JSR $EA66
$F0B4:  A9 CE     LDA #$CE ('N')
$F0B6:  A0 F0     LDY #$F0 ('p')
$F0B8:  20 5C EF  JSR $EF5C
$F0BB:  68        PLA
$F0BC:  C9 81     CMP #$81
$F0BE:  90 07     BCC $F0C7
$F0C0:  A9 66     LDA #$66 ('f')
$F0C2:  A0 F0     LDY #$F0 ('p')
$F0C4:  20 A7 E7  JSR $E7A7
$F0C7:  68        PLA
$F0C8:  10 03     BPL $F0CD
$F0CA:  4C D0 EE  JMP $EED0
$F0CD:  60        RTS
$F0CE:  0B        .BYTE $0B
$F0CF:  76 B3     ROR $B3,X
$F0D1:  83        .BYTE $83
$F0D2:  BD D3 79  LDA $79D3,X
$F0D5:  1E F4 A6  ASL $A6F4,X
$F0D8:  F5 7B     SBC $7B,X
$F0DA:  83        .BYTE $83
$F0DB:  FC        .BYTE $FC
$F0DC:  B0 10     BCS $F0EE
$F0DE:  7C        .BYTE $7C
$F0DF:  0C        .BYTE $0C
$F0E0:  1F        .BYTE $1F
$F0E1:  67        .BYTE $67
$F0E2:  CA        DEX
$F0E3:  7C        .BYTE $7C
$F0E4:  DE 53 CB  DEC $CB53,X
$F0E7:  C1 7D     CMP ($7D,X)
$F0E9:  14        .BYTE $14
$F0EA:  64        .BYTE $64
$F0EB:  70 4C     BVS $F139
$F0ED:  7D B7 EA  ADC $EAB7,X
$F0F0:  51 7A     EOR ($7A),Y
$F0F2:  7D 63 30  ADC $3063,X
$F0F5:  88        DEY
$F0F6:  7E 7E 92  ROR $927E,X
$F0F9:  44        .BYTE $44
$F0FA:  99 3A 7E  STA $7E3A,Y
$F0FD:  4C CC 91  JMP $91CC
$F100:  C7        .BYTE $C7
$F101:  7F        .BYTE $7F
$F102:  AA        TAX
$F103:  AA        TAX
$F104:  AA        TAX
$F105:  13        .BYTE $13
$F106:  81 00     STA ($00,X)
$F108:  00        BRK
$F109:  00        BRK
$F10A:  00        BRK
$F10B:  E6 B8     INC $B8
$F10D:  D0 02     BNE $F111
$F10F:  E6 B9     INC $B9
$F111:  AD 60 EA  LDA $EA60
$F114:  C9 3A     CMP #$3A (':')
$F116:  B0 0A     BCS $F122
$F118:  C9 20     CMP #$20 (' ')
$F11A:  F0 EF     BEQ $F10B
$F11C:  38        SEC
$F11D:  E9 30     SBC #$30 ('0')
$F11F:  38        SEC
$F120:  E9 D0     SBC #$D0 ('P')
$F122:  60        RTS
$F123:  80        .BYTE $80
$F124:  4F        .BYTE $4F
$F125:  C7        .BYTE $C7
$F126:  52        .BYTE $52
$F127:  58        CLI
$F128:  A2 FF     LDX #$FF
$F12A:  86 76     STX $76
$F12C:  A2 FB     LDX #$FB ('{')
$F12E:  9A        TXS
$F12F:  A9 28     LDA #$28 ('(')
$F131:  A0 F1     LDY #$F1 ('q')
$F133:  85 01     STA $01
$F135:  84 02     STY $02
$F137:  85 04     STA $04
$F139:  84 05     STY $05
$F13B:  20 73 F2  JSR $F273
$F13E:  A9 4C     LDA #$4C ('L')
$F140:  85 00     STA $00
$F142:  85 03     STA $03
$F144:  85 90     STA $90
$F146:  85 0A     STA $0A
$F148:  A9 99     LDA #$99
$F14A:  A0 E1     LDY #$E1 ('a')
$F14C:  85 0B     STA $0B
$F14E:  84 0C     STY $0C
$F150:  A2 1C     LDX #$1C
$F152:  BD 0A F1  LDA $F10A,X
$F155:  95 B0     STA $B0,X
$F157:  86 F1     STX $F1
$F159:  CA        DEX
$F15A:  D0 F6     BNE $F152
$F15C:  86 F2     STX $F2
$F15E:  8A        TXA
$F15F:  85 A4     STA $A4
$F161:  85 54     STA $54
$F163:  48        PHA
$F164:  A9 03     LDA #$03
$F166:  85 8F     STA $8F
$F168:  20 FB DA  JSR $DAFB
$F16B:  A9 01     LDA #$01
$F16D:  8D FD 01  STA $01FD
$F170:  8D FC 01  STA $01FC
$F173:  A2 55     LDX #$55 ('U')
$F175:  86 52     STX $52
$F177:  A9 00     LDA #$00
$F179:  A0 08     LDY #$08
$F17B:  85 50     STA $50
$F17D:  84 51     STY $51
$F17F:  A0 00     LDY #$00
$F181:  E6 51     INC $51
$F183:  B1 50     LDA ($50),Y
$F185:  49 FF     EOR #$FF
$F187:  91 50     STA ($50),Y
$F189:  D1 50     CMP ($50),Y
$F18B:  D0 08     BNE $F195
$F18D:  49 FF     EOR #$FF
$F18F:  91 50     STA ($50),Y
$F191:  D1 50     CMP ($50),Y
$F193:  F0 EC     BEQ $F181
$F195:  A4 50     LDY $50
$F197:  A5 51     LDA $51
$F199:  29 F0     AND #$F0 ('p')
$F19B:  84 73     STY $73
$F19D:  85 74     STA $74
$F19F:  84 6F     STY $6F
$F1A1:  85 70     STA $70
$F1A3:  A2 00     LDX #$00
$F1A5:  A0 08     LDY #$08
$F1A7:  86 67     STX $67
$F1A9:  84 68     STY $68
$F1AB:  A0 00     LDY #$00
$F1AD:  84 D6     STY $D6
$F1AF:  98        TYA
$F1B0:  91 67     STA ($67),Y
$F1B2:  E6 67     INC $67
$F1B4:  D0 02     BNE $F1B8
$F1B6:  E6 68     INC $68
$F1B8:  A5 67     LDA $67
$F1BA:  A4 68     LDY $68
$F1BC:  20 E3 D3  JSR $D3E3
$F1BF:  20 4B D6  JSR $D64B
$F1C2:  A9 3A     LDA #$3A (':')
$F1C4:  A0 DB     LDY #$DB ('[')
$F1C6:  85 04     STA $04
$F1C8:  84 05     STY $05
$F1CA:  A9 3C     LDA #$3C ('<')
$F1CC:  A0 D4     LDY #$D4 ('T')
$F1CE:  85 01     STA $01
$F1D0:  84 02     STY $02
$F1D2:  6C 01 00  JMP ($0001)
$F1D5:  20 67 DD  JSR $DD67
$F1D8:  20 52 E7  JSR $E752
$F1DB:  6C 50 00  JMP ($0050)
$F1DE:  20 F8 E6  JSR $E6F8
$F1E1:  8A        TXA
$F1E2:  4C 8B FE  JMP $FE8B
$F1E5:  20 F8 E6  JSR $E6F8
$F1E8:  8A        TXA
$F1E9:  4C 95 FE  JMP $FE95
$F1EC:  20 F8 E6  JSR $E6F8
$F1EF:  E0 30     CPX #$30 ('0')
$F1F1:  B0 13     BCS $F206
$F1F3:  86 F0     STX $F0
$F1F5:  A9 2C     LDA #$2C (',')
$F1F7:  20 C0 DE  JSR $DEC0
$F1FA:  20 F8 E6  JSR $E6F8
$F1FD:  E0 30     CPX #$30 ('0')
$F1FF:  B0 05     BCS $F206
$F201:  86 2C     STX $2C
$F203:  86 2D     STX $2D
$F205:  60        RTS
$F206:  4C 99 E1  JMP $E199
$F209:  20 EC F1  JSR $F1EC
$F20C:  E4 F0     CPX $F0
$F20E:  B0 08     BCS $F218
$F210:  A5 F0     LDA $F0
$F212:  85 2C     STA $2C
$F214:  85 2D     STA $2D
$F216:  86 F0     STX $F0
$F218:  A9 C5     LDA #$C5 ('E')
$F21A:  20 C0 DE  JSR $DEC0
$F21D:  20 F8 E6  JSR $E6F8
$F220:  E0 30     CPX #$30 ('0')
$F222:  B0 E2     BCS $F206
$F224:  60        RTS
$F225:  20 EC F1  JSR $F1EC
$F228:  8A        TXA
$F229:  A4 F0     LDY $F0
$F22B:  C0 28     CPY #$28 ('(')
$F22D:  B0 D7     BCS $F206
$F22F:  4C 00 F8  JMP $F800 ; PLOT
$F232:  20 09 F2  JSR $F209
$F235:  8A        TXA
$F236:  A4 2C     LDY $2C
$F238:  C0 28     CPY #$28 ('(')
$F23A:  B0 CA     BCS $F206
$F23C:  A4 F0     LDY $F0
$F23E:  4C 19 F8  JMP $F819 ; HLINE
$F241:  20 09 F2  JSR $F209
$F244:  8A        TXA
$F245:  A8        TAY
$F246:  C0 28     CPY #$28 ('(')
$F248:  B0 BC     BCS $F206
$F24A:  A5 F0     LDA $F0
$F24C:  4C 28 F8  JMP $F828 ; VLINE
$F24F:  20 F8 E6  JSR $E6F8
$F252:  8A        TXA
$F253:  4C 64 F8  JMP $F864
$F256:  20 F8 E6  JSR $E6F8
$F259:  CA        DEX
$F25A:  8A        TXA
$F25B:  C9 18     CMP #$18
$F25D:  B0 A7     BCS $F206
$F25F:  4C 5B FB  JMP $FB5B
$F262:  20 F8 E6  JSR $E6F8
$F265:  8A        TXA
$F266:  49 FF     EOR #$FF
$F268:  AA        TAX
$F269:  E8        INX
$F26A:  86 F1     STX $F1
$F26C:  60        RTS
$F26D:  38        SEC
$F26E:  90 18     BCC $F288
$F270:  66 F2     ROR $F2
$F272:  60        RTS
$F273:  A9 FF     LDA #$FF
$F275:  D0 02     BNE $F279
$F277:  A9 3F     LDA #$3F ('?')
$F279:  A2 00     LDX #$00
$F27B:  85 32     STA $32
$F27D:  86 F3     STX $F3
$F27F:  60        RTS
$F280:  A9 7F     LDA #$7F
$F282:  A2 40     LDX #$40 ('@')
$F284:  D0 F5     BNE $F27B
$F286:  20 67 DD  JSR $DD67
$F289:  20 52 E7  JSR $E752
$F28C:  A5 50     LDA $50
$F28E:  C5 6D     CMP $6D
$F290:  A5 51     LDA $51
$F292:  E5 6E     SBC $6E
$F294:  B0 03     BCS $F299
$F296:  4C 10 D4  JMP $D410
$F299:  A5 50     LDA $50
$F29B:  85 73     STA $73
$F29D:  85 6F     STA $6F
$F29F:  A5 51     LDA $51
$F2A1:  85 74     STA $74
$F2A3:  85 70     STA $70
$F2A5:  60        RTS
$F2A6:  20 67 DD  JSR $DD67
$F2A9:  20 52 E7  JSR $E752
$F2AC:  A5 50     LDA $50
$F2AE:  C5 73     CMP $73
$F2B0:  A5 51     LDA $51
$F2B2:  E5 74     SBC $74
$F2B4:  B0 E0     BCS $F296
$F2B6:  A5 50     LDA $50
$F2B8:  C5 69     CMP $69
$F2BA:  A5 51     LDA $51
$F2BC:  E5 6A     SBC $6A
$F2BE:  90 D6     BCC $F296
$F2C0:  A5 50     LDA $50
$F2C2:  85 69     STA $69
$F2C4:  A5 51     LDA $51
$F2C6:  85 6A     STA $6A
$F2C8:  4C 6C D6  JMP $D66C
$F2CB:  A9 AB     LDA #$AB ('+')
$F2CD:  20 C0 DE  JSR $DEC0
$F2D0:  A5 B8     LDA $B8
$F2D2:  85 F4     STA $F4
$F2D4:  A5 B9     LDA $B9
$F2D6:  85 F5     STA $F5
$F2D8:  38        SEC
$F2D9:  66 D8     ROR $D8
$F2DB:  A5 75     LDA $75
$F2DD:  85 F6     STA $F6
$F2DF:  A5 76     LDA $76
$F2E1:  85 F7     STA $F7
$F2E3:  20 A6 D9  JSR $D9A6
$F2E6:  4C 98 D9  JMP $D998
$F2E9:  86 DE     STX $DE
$F2EB:  A6 F8     LDX $F8
$F2ED:  86 DF     STX $DF
$F2EF:  A5 75     LDA $75
$F2F1:  85 DA     STA $DA
$F2F3:  A5 76     LDA $76
$F2F5:  85 DB     STA $DB
$F2F7:  A5 79     LDA $79
$F2F9:  85 DC     STA $DC
$F2FB:  A5 7A     LDA $7A
$F2FD:  85 DD     STA $DD
$F2FF:  A5 F4     LDA $F4
$F301:  85 B8     STA $B8
$F303:  A5 F5     LDA $F5
$F305:  85 B9     STA $B9
$F307:  A5 F6     LDA $F6
$F309:  85 75     STA $75
$F30B:  A5 F7     LDA $F7
$F30D:  85 76     STA $76
$F30F:  20 B7 00  JSR $00B7
$F312:  20 3E D9  JSR $D93E
$F315:  4C D2 D7  JMP $D7D2
$F318:  A5 DA     LDA $DA
$F31A:  85 75     STA $75
$F31C:  A5 DB     LDA $DB
$F31E:  85 76     STA $76
$F320:  A5 DC     LDA $DC
$F322:  85 B8     STA $B8
$F324:  A5 DD     LDA $DD
$F326:  85 B9     STA $B9
$F328:  A6 DF     LDX $DF
$F32A:  9A        TXS
$F32B:  4C D2 D7  JMP $D7D2
$F32E:  4C C9 DE  JMP $DEC9
$F331:  B0 FB     BCS $F32E
$F333:  A6 AF     LDX $AF
$F335:  86 69     STX $69
$F337:  A6 B0     LDX $B0
$F339:  86 6A     STX $6A
$F33B:  20 0C DA  JSR $DA0C
$F33E:  20 1A D6  JSR $D61A
$F341:  A5 9B     LDA $9B
$F343:  85 60     STA $60
$F345:  A5 9C     LDA $9C
$F347:  85 61     STA $61
$F349:  A9 2C     LDA #$2C (',')
$F34B:  20 C0 DE  JSR $DEC0
$F34E:  20 0C DA  JSR $DA0C
$F351:  E6 50     INC $50
$F353:  D0 02     BNE $F357
$F355:  E6 51     INC $51
$F357:  20 1A D6  JSR $D61A
$F35A:  A5 9B     LDA $9B
$F35C:  C5 60     CMP $60
$F35E:  A5 9C     LDA $9C
$F360:  E5 61     SBC $61
$F362:  B0 01     BCS $F365
$F364:  60        RTS
$F365:  A0 00     LDY #$00
$F367:  B1 9B     LDA ($9B),Y
$F369:  91 60     STA ($60),Y
$F36B:  E6 9B     INC $9B
$F36D:  D0 02     BNE $F371
$F36F:  E6 9C     INC $9C
$F371:  E6 60     INC $60
$F373:  D0 02     BNE $F377
$F375:  E6 61     INC $61
$F377:  A5 69     LDA $69
$F379:  C5 9B     CMP $9B
$F37B:  A5 6A     LDA $6A
$F37D:  E5 9C     SBC $9C
$F37F:  B0 E6     BCS $F367
$F381:  A6 61     LDX $61
$F383:  A4 60     LDY $60
$F385:  D0 01     BNE $F388
$F387:  CA        DEX
$F388:  88        DEY
$F389:  86 6A     STX $6A
$F38B:  84 69     STY $69
$F38D:  4C F2 D4  JMP $D4F2
$F390:  AD 56 C0  LDA $C056 ; HIRESOFF
$F393:  AD 53 C0  LDA $C053 ; MIXEDON
$F396:  4C 40 FB  JMP $FB40 ; SETCOL
$F399:  AD 54 C0  LDA $C054 ; PAGE2OFF
$F39C:  4C 39 FB  JMP $FB39 ; SETGR
$F39F:  20 D9 F7  JSR $F7D9
$F3A2:  A0 03     LDY #$03
$F3A4:  B1 9B     LDA ($9B),Y
$F3A6:  AA        TAX
$F3A7:  88        DEY
$F3A8:  B1 9B     LDA ($9B),Y
$F3AA:  E9 01     SBC #$01
$F3AC:  B0 01     BCS $F3AF
$F3AE:  CA        DEX
$F3AF:  85 50     STA $50
$F3B1:  86 51     STX $51
$F3B3:  20 CD FE  JSR $FECD
$F3B6:  20 BC F7  JSR $F7BC
$F3B9:  4C CD FE  JMP $FECD
$F3BC:  20 D9 F7  JSR $F7D9
$F3BF:  20 FD FE  JSR $FEFD
$F3C2:  A0 02     LDY #$02
$F3C4:  B1 9B     LDA ($9B),Y
$F3C6:  C5 50     CMP $50
$F3C8:  C8        INY
$F3C9:  B1 9B     LDA ($9B),Y
$F3CB:  E5 51     SBC $51
$F3CD:  B0 03     BCS $F3D2
$F3CF:  4C 10 D4  JMP $D410
$F3D2:  20 BC F7  JSR $F7BC
$F3D5:  4C FD FE  JMP $FEFD
$F3D8:  2C 55 C0  BIT $C055 ; PAGE2ON
$F3DB:  2C 52 C0  BIT $C052 ; MIXEDOFF
$F3DE:  A9 40     LDA #$40 ('@')
$F3E0:  D0 08     BNE $F3EA
$F3E2:  A9 20     LDA #$20 (' ')
$F3E4:  2C 54 C0  BIT $C054 ; PAGE2OFF
$F3E7:  2C 53 C0  BIT $C053 ; MIXEDON
$F3EA:  85 E6     STA $E6
$F3EC:  AD 57 C0  LDA $C057 ; HIRESON
$F3EF:  AD 50 C0  LDA $C050 ; TEXTOFF
$F3F2:  A9 00     LDA #$00
$F3F4:  85 1C     STA $1C
$F3F6:  A5 E6     LDA $E6
$F3F8:  85 1B     STA $1B
$F3FA:  A0 00     LDY #$00
$F3FC:  84 1A     STY $1A
$F3FE:  A5 1C     LDA $1C
$F400:  91 1A     STA ($1A),Y
$F402:  20 7E F4  JSR $F47E
$F405:  C8        INY
$F406:  D0 F6     BNE $F3FE
$F408:  E6 1B     INC $1B
$F40A:  A5 1B     LDA $1B
$F40C:  29 1F     AND #$1F
$F40E:  D0 EE     BNE $F3FE
$F410:  60        RTS
$F411:  85 E2     STA $E2
$F413:  86 E0     STX $E0
$F415:  84 E1     STY $E1
$F417:  48        PHA
$F418:  29 C0     AND #$C0 ('@')
$F41A:  85 26     STA $26
$F41C:  4A        LSR
$F41D:  4A        LSR
$F41E:  05 26     ORA $26
$F420:  85 26     STA $26
$F422:  68        PLA
$F423:  85 27     STA $27
$F425:  0A        ASL
$F426:  0A        ASL
$F427:  0A        ASL
$F428:  26 27     ROL $27
$F42A:  0A        ASL
$F42B:  26 27     ROL $27
$F42D:  0A        ASL
$F42E:  66 26     ROR $26
$F430:  A5 27     LDA $27
$F432:  29 1F     AND #$1F
$F434:  05 E6     ORA $E6
$F436:  85 27     STA $27
$F438:  8A        TXA
$F439:  C0 00     CPY #$00
$F43B:  F0 05     BEQ $F442
$F43D:  A0 23     LDY #$23 ('#')
$F43F:  69 04     ADC #$04
$F441:  C8        INY
$F442:  E9 07     SBC #$07
$F444:  B0 FB     BCS $F441
$F446:  84 E5     STY $E5
$F448:  AA        TAX
$F449:  BD B9 F4  LDA $F4B9,X
$F44C:  85 30     STA $30
$F44E:  98        TYA
$F44F:  4A        LSR
$F450:  A5 E4     LDA $E4
$F452:  85 1C     STA $1C
$F454:  B0 28     BCS $F47E
$F456:  60        RTS
$F457:  20 11 F4  JSR $F411
$F45A:  A5 1C     LDA $1C
$F45C:  51 26     EOR ($26),Y
$F45E:  25 30     AND $30
$F460:  51 26     EOR ($26),Y
$F462:  91 26     STA ($26),Y
$F464:  60        RTS
$F465:  10 23     BPL $F48A
$F467:  A5 30     LDA $30
$F469:  4A        LSR
$F46A:  B0 05     BCS $F471
$F46C:  49 C0     EOR #$C0 ('@')
$F46E:  85 30     STA $30
$F470:  60        RTS
$F471:  88        DEY
$F472:  10 02     BPL $F476
$F474:  A0 27     LDY #$27 (''')
$F476:  A9 C0     LDA #$C0 ('@')
$F478:  85 30     STA $30
$F47A:  84 E5     STY $E5
$F47C:  A5 1C     LDA $1C
$F47E:  0A        ASL
$F47F:  C9 C0     CMP #$C0 ('@')
$F481:  10 06     BPL $F489
$F483:  A5 1C     LDA $1C
$F485:  49 7F     EOR #$7F
$F487:  85 1C     STA $1C
$F489:  60        RTS
$F48A:  A5 30     LDA $30
$F48C:  0A        ASL
$F48D:  49 80     EOR #$80
$F48F:  30 DD     BMI $F46E
$F491:  A9 81     LDA #$81
$F493:  C8        INY
$F494:  C0 28     CPY #$28 ('(')
$F496:  90 E0     BCC $F478
$F498:  A0 00     LDY #$00
$F49A:  B0 DC     BCS $F478
$F49C:  18        CLC
$F49D:  A5 D1     LDA $D1
$F49F:  29 04     AND #$04
$F4A1:  F0 25     BEQ $F4C8
$F4A3:  A9 7F     LDA #$7F
$F4A5:  25 30     AND $30
$F4A7:  31 26     AND ($26),Y
$F4A9:  D0 19     BNE $F4C4
$F4AB:  E6 EA     INC $EA
$F4AD:  A9 7F     LDA #$7F
$F4AF:  25 30     AND $30
$F4B1:  10 11     BPL $F4C4
$F4B3:  18        CLC
$F4B4:  A5 D1     LDA $D1
$F4B6:  29 04     AND #$04
$F4B8:  F0 0E     BEQ $F4C8
$F4BA:  B1 26     LDA ($26),Y
$F4BC:  45 1C     EOR $1C
$F4BE:  25 30     AND $30
$F4C0:  D0 02     BNE $F4C4
$F4C2:  E6 EA     INC $EA
$F4C4:  51 26     EOR ($26),Y
$F4C6:  91 26     STA ($26),Y
$F4C8:  A5 D1     LDA $D1
$F4CA:  65 D3     ADC $D3
$F4CC:  29 03     AND #$03
$F4CE:  C9 02     CMP #$02
$F4D0:  6A        ROR
$F4D1:  B0 92     BCS $F465
$F4D3:  30 30     BMI $F505
$F4D5:  18        CLC
$F4D6:  A5 27     LDA $27
$F4D8:  2C B9 F5  BIT $F5B9
$F4DB:  D0 22     BNE $F4FF
$F4DD:  06 26     ASL $26
$F4DF:  B0 1A     BCS $F4FB
$F4E1:  2C CD F4  BIT $F4CD
$F4E4:  F0 05     BEQ $F4EB
$F4E6:  69 1F     ADC #$1F
$F4E8:  38        SEC
$F4E9:  B0 12     BCS $F4FD
$F4EB:  69 23     ADC #$23 ('#')
$F4ED:  48        PHA
$F4EE:  A5 26     LDA $26
$F4F0:  69 B0     ADC #$B0 ('0')
$F4F2:  B0 02     BCS $F4F6
$F4F4:  69 F0     ADC #$F0 ('p')
$F4F6:  85 26     STA $26
$F4F8:  68        PLA
$F4F9:  B0 02     BCS $F4FD
$F4FB:  69 1F     ADC #$1F
$F4FD:  66 26     ROR $26
$F4FF:  69 FC     ADC #$FC ('|')
$F501:  85 27     STA $27
$F503:  60        RTS
$F504:  18        CLC
$F505:  A5 27     LDA $27
$F507:  69 04     ADC #$04
$F509:  2C B9 F5  BIT $F5B9
$F50C:  D0 F3     BNE $F501
$F50E:  06 26     ASL $26
$F510:  90 18     BCC $F52A
$F512:  69 E0     ADC #$E0 ('`')
$F514:  18        CLC
$F515:  2C 08 F5  BIT $F508
$F518:  F0 12     BEQ $F52C
$F51A:  A5 26     LDA $26
$F51C:  69 50     ADC #$50 ('P')
$F51E:  49 F0     EOR #$F0 ('p')
$F520:  F0 02     BEQ $F524
$F522:  49 F0     EOR #$F0 ('p')
$F524:  85 26     STA $26
$F526:  A5 E6     LDA $E6
$F528:  90 02     BCC $F52C
$F52A:  69 E0     ADC #$E0 ('`')
$F52C:  66 26     ROR $26
$F52E:  90 D1     BCC $F501
$F530:  48        PHA
$F531:  A9 00     LDA #$00
$F533:  85 E0     STA $E0
$F535:  85 E1     STA $E1
$F537:  85 E2     STA $E2
$F539:  68        PLA
$F53A:  48        PHA
$F53B:  38        SEC
$F53C:  E5 E0     SBC $E0
$F53E:  48        PHA
$F53F:  8A        TXA
$F540:  E5 E1     SBC $E1
$F542:  85 D3     STA $D3
$F544:  B0 0A     BCS $F550
$F546:  68        PLA
$F547:  49 FF     EOR #$FF
$F549:  69 01     ADC #$01
$F54B:  48        PHA
$F54C:  A9 00     LDA #$00
$F54E:  E5 D3     SBC $D3
$F550:  85 D1     STA $D1
$F552:  85 D5     STA $D5
$F554:  68        PLA
$F555:  85 D0     STA $D0
$F557:  85 D4     STA $D4
$F559:  68        PLA
$F55A:  85 E0     STA $E0
$F55C:  86 E1     STX $E1
$F55E:  98        TYA
$F55F:  18        CLC
$F560:  E5 E2     SBC $E2
$F562:  90 04     BCC $F568
$F564:  49 FF     EOR #$FF
$F566:  69 FE     ADC #$FE ('~')
$F568:  85 D2     STA $D2
$F56A:  84 E2     STY $E2
$F56C:  66 D3     ROR $D3
$F56E:  38        SEC
$F56F:  E5 D0     SBC $D0
$F571:  AA        TAX
$F572:  A9 FF     LDA #$FF
$F574:  E5 D1     SBC $D1
$F576:  85 1D     STA $1D
$F578:  A4 E5     LDY $E5
$F57A:  B0 05     BCS $F581
$F57C:  0A        ASL
$F57D:  20 65 F4  JSR $F465
$F580:  38        SEC
$F581:  A5 D4     LDA $D4
$F583:  65 D2     ADC $D2
$F585:  85 D4     STA $D4
$F587:  A5 D5     LDA $D5
$F589:  E9 00     SBC #$00
$F58B:  85 D5     STA $D5
$F58D:  B1 26     LDA ($26),Y
$F58F:  45 1C     EOR $1C
$F591:  25 30     AND $30
$F593:  51 26     EOR ($26),Y
$F595:  91 26     STA ($26),Y
$F597:  E8        INX
$F598:  D0 04     BNE $F59E
$F59A:  E6 1D     INC $1D
$F59C:  F0 62     BEQ $F600
$F59E:  A5 D3     LDA $D3
$F5A0:  B0 DA     BCS $F57C
$F5A2:  20 D3 F4  JSR $F4D3
$F5A5:  18        CLC
$F5A6:  A5 D4     LDA $D4
$F5A8:  65 D0     ADC $D0
$F5AA:  85 D4     STA $D4
$F5AC:  A5 D5     LDA $D5
$F5AE:  65 D1     ADC $D1
$F5B0:  50 D9     BVC $F58B
$F5B2:  81 82     STA ($82,X)
$F5B4:  84 88     STY $88
$F5B6:  90 A0     BCC $F558
$F5B8:  C0 1C     CPY #$1C
$F5BA:  FF        .BYTE $FF
$F5BB:  FE FA F4  INC $F4FA,X
$F5BE:  EC E1 D4  CPX $D4E1
$F5C1:  C5 B4     CMP $B4
$F5C3:  A1 8D     LDA ($8D,X)
$F5C5:  78        SEI
$F5C6:  61 49     ADC ($49,X)
$F5C8:  31 18     AND ($18),Y
$F5CA:  FF        .BYTE $FF
$F5CB:  A5 26     LDA $26
$F5CD:  0A        ASL
$F5CE:  A5 27     LDA $27
$F5D0:  29 03     AND #$03
$F5D2:  2A        ROL
$F5D3:  05 26     ORA $26
$F5D5:  0A        ASL
$F5D6:  0A        ASL
$F5D7:  0A        ASL
$F5D8:  85 E2     STA $E2
$F5DA:  A5 27     LDA $27
$F5DC:  4A        LSR
$F5DD:  4A        LSR
$F5DE:  29 07     AND #$07
$F5E0:  05 E2     ORA $E2
$F5E2:  85 E2     STA $E2
$F5E4:  A5 E5     LDA $E5
$F5E6:  0A        ASL
$F5E7:  65 E5     ADC $E5
$F5E9:  0A        ASL
$F5EA:  AA        TAX
$F5EB:  CA        DEX
$F5EC:  A5 30     LDA $30
$F5EE:  29 7F     AND #$7F
$F5F0:  E8        INX
$F5F1:  4A        LSR
$F5F2:  D0 FC     BNE $F5F0
$F5F4:  85 E1     STA $E1
$F5F6:  8A        TXA
$F5F7:  18        CLC
$F5F8:  65 E5     ADC $E5
$F5FA:  90 02     BCC $F5FE
$F5FC:  E6 E1     INC $E1
$F5FE:  85 E0     STA $E0
$F600:  60        RTS
$F601:  86 1A     STX $1A
$F603:  84 1B     STY $1B
$F605:  AA        TAX
$F606:  4A        LSR
$F607:  4A        LSR
$F608:  4A        LSR
$F609:  4A        LSR
$F60A:  85 D3     STA $D3
$F60C:  8A        TXA
$F60D:  29 0F     AND #$0F
$F60F:  AA        TAX
$F610:  BC BA F5  LDY $F5BA,X
$F613:  84 D0     STY $D0
$F615:  49 0F     EOR #$0F
$F617:  AA        TAX
$F618:  BC BB F5  LDY $F5BB,X
$F61B:  C8        INY
$F61C:  84 D2     STY $D2
$F61E:  A4 E5     LDY $E5
$F620:  A2 00     LDX #$00
$F622:  86 EA     STX $EA
$F624:  A1 1A     LDA ($1A,X)
$F626:  85 D1     STA $D1
$F628:  A2 80     LDX #$80
$F62A:  86 D4     STX $D4
$F62C:  86 D5     STX $D5
$F62E:  A6 E7     LDX $E7
$F630:  A5 D4     LDA $D4
$F632:  38        SEC
$F633:  65 D0     ADC $D0
$F635:  85 D4     STA $D4
$F637:  90 04     BCC $F63D
$F639:  20 B3 F4  JSR $F4B3
$F63C:  18        CLC
$F63D:  A5 D5     LDA $D5
$F63F:  65 D2     ADC $D2
$F641:  85 D5     STA $D5
$F643:  90 03     BCC $F648
$F645:  20 B4 F4  JSR $F4B4
$F648:  CA        DEX
$F649:  D0 E5     BNE $F630
$F64B:  A5 D1     LDA $D1
$F64D:  4A        LSR
$F64E:  4A        LSR
$F64F:  4A        LSR
$F650:  D0 D4     BNE $F626
$F652:  E6 1A     INC $1A
$F654:  D0 02     BNE $F658
$F656:  E6 1B     INC $1B
$F658:  A1 1A     LDA ($1A,X)
$F65A:  D0 CA     BNE $F626
$F65C:  60        RTS
$F65D:  86 1A     STX $1A
$F65F:  84 1B     STY $1B
$F661:  AA        TAX
$F662:  4A        LSR
$F663:  4A        LSR
$F664:  4A        LSR
$F665:  4A        LSR
$F666:  85 D3     STA $D3
$F668:  8A        TXA
$F669:  29 0F     AND #$0F
$F66B:  AA        TAX
$F66C:  BC BA F5  LDY $F5BA,X
$F66F:  84 D0     STY $D0
$F671:  49 0F     EOR #$0F
$F673:  AA        TAX
$F674:  BC BB F5  LDY $F5BB,X
$F677:  C8        INY
$F678:  84 D2     STY $D2
$F67A:  A4 E5     LDY $E5
$F67C:  A2 00     LDX #$00
$F67E:  86 EA     STX $EA
$F680:  A1 1A     LDA ($1A,X)
$F682:  85 D1     STA $D1
$F684:  A2 80     LDX #$80
$F686:  86 D4     STX $D4
$F688:  86 D5     STX $D5
$F68A:  A6 E7     LDX $E7
$F68C:  A5 D4     LDA $D4
$F68E:  38        SEC
$F68F:  65 D0     ADC $D0
$F691:  85 D4     STA $D4
$F693:  90 04     BCC $F699
$F695:  20 9C F4  JSR $F49C
$F698:  18        CLC
$F699:  A5 D5     LDA $D5
$F69B:  65 D2     ADC $D2
$F69D:  85 D5     STA $D5
$F69F:  90 03     BCC $F6A4
$F6A1:  20 9D F4  JSR $F49D
$F6A4:  CA        DEX
$F6A5:  D0 E5     BNE $F68C
$F6A7:  A5 D1     LDA $D1
$F6A9:  4A        LSR
$F6AA:  4A        LSR
$F6AB:  4A        LSR
$F6AC:  D0 D4     BNE $F682
$F6AE:  E6 1A     INC $1A
$F6B0:  D0 02     BNE $F6B4
$F6B2:  E6 1B     INC $1B
$F6B4:  A1 1A     LDA ($1A,X)
$F6B6:  D0 CA     BNE $F682
$F6B8:  60        RTS
$F6B9:  20 67 DD  JSR $DD67
$F6BC:  20 52 E7  JSR $E752
$F6BF:  A4 51     LDY $51
$F6C1:  A6 50     LDX $50
$F6C3:  C0 01     CPY #$01
$F6C5:  90 06     BCC $F6CD
$F6C7:  D0 1D     BNE $F6E6
$F6C9:  E0 18     CPX #$18
$F6CB:  B0 19     BCS $F6E6
$F6CD:  8A        TXA
$F6CE:  48        PHA
$F6CF:  98        TYA
$F6D0:  48        PHA
$F6D1:  A9 2C     LDA #$2C (',')
$F6D3:  20 C0 DE  JSR $DEC0
$F6D6:  20 F8 E6  JSR $E6F8
$F6D9:  E0 C0     CPX #$C0 ('@')
$F6DB:  B0 09     BCS $F6E6
$F6DD:  86 9D     STX $9D
$F6DF:  68        PLA
$F6E0:  A8        TAY
$F6E1:  68        PLA
$F6E2:  AA        TAX
$F6E3:  A5 9D     LDA $9D
$F6E5:  60        RTS
$F6E6:  4C 06 F2  JMP $F206
$F6E9:  20 F8 E6  JSR $E6F8
$F6EC:  E0 08     CPX #$08
$F6EE:  B0 F6     BCS $F6E6
$F6F0:  BD F6 F6  LDA $F6F6,X
$F6F3:  85 E4     STA $E4
$F6F5:  60        RTS
$F6F6:  00        BRK
$F6F7:  2A        ROL
$F6F8:  55 7F     EOR $7F,X
$F6FA:  80        .BYTE $80
$F6FB:  AA        TAX
$F6FC:  D5 FF     CMP $FF,X
$F6FE:  C9 C1     CMP #$C1 ('A')
$F700:  F0 0D     BEQ $F70F
$F702:  20 B9 F6  JSR $F6B9
$F705:  20 57 F4  JSR $F457
$F708:  20 B7 00  JSR $00B7
$F70B:  C9 C1     CMP #$C1 ('A')
$F70D:  D0 E6     BNE $F6F5
$F70F:  20 C0 DE  JSR $DEC0
$F712:  20 B9 F6  JSR $F6B9
$F715:  84 9D     STY $9D
$F717:  A8        TAY
$F718:  8A        TXA
$F719:  A6 9D     LDX $9D
$F71B:  20 3A F5  JSR $F53A
$F71E:  4C 08 F7  JMP $F708
$F721:  20 F8 E6  JSR $E6F8
$F724:  86 F9     STX $F9
$F726:  60        RTS
$F727:  20 F8 E6  JSR $E6F8
$F72A:  86 E7     STX $E7
$F72C:  60        RTS
$F72D:  20 F8 E6  JSR $E6F8
$F730:  A5 E8     LDA $E8
$F732:  85 1A     STA $1A
$F734:  A5 E9     LDA $E9
$F736:  85 1B     STA $1B
$F738:  8A        TXA
$F739:  A2 00     LDX #$00
$F73B:  C1 1A     CMP ($1A,X)
$F73D:  F0 02     BEQ $F741
$F73F:  B0 A5     BCS $F6E6
$F741:  0A        ASL
$F742:  90 03     BCC $F747
$F744:  E6 1B     INC $1B
$F746:  18        CLC
$F747:  A8        TAY
$F748:  B1 1A     LDA ($1A),Y
$F74A:  65 1A     ADC $1A
$F74C:  AA        TAX
$F74D:  C8        INY
$F74E:  B1 1A     LDA ($1A),Y
$F750:  65 E9     ADC $E9
$F752:  85 1B     STA $1B
$F754:  86 1A     STX $1A
$F756:  20 B7 00  JSR $00B7
$F759:  C9 C5     CMP #$C5 ('E')
$F75B:  D0 09     BNE $F766
$F75D:  20 C0 DE  JSR $DEC0
$F760:  20 B9 F6  JSR $F6B9
$F763:  20 11 F4  JSR $F411
$F766:  A5 F9     LDA $F9
$F768:  60        RTS
$F769:  20 2D F7  JSR $F72D
$F76C:  4C 05 F6  JMP $F605
$F76F:  20 2D F7  JSR $F72D
$F772:  4C 61 F6  JMP $F661
$F775:  A9 00     LDA #$00
$F777:  85 3D     STA $3D
$F779:  85 3F     STA $3F
$F77B:  A0 50     LDY #$50 ('P')
$F77D:  84 3C     STY $3C
$F77F:  C8        INY
$F780:  84 3E     STY $3E
$F782:  20 FD FE  JSR $FEFD
$F785:  18        CLC
$F786:  A5 73     LDA $73
$F788:  AA        TAX
$F789:  CA        DEX
$F78A:  86 3E     STX $3E
$F78C:  E5 50     SBC $50
$F78E:  48        PHA
$F78F:  A5 74     LDA $74
$F791:  A8        TAY
$F792:  E8        INX
$F793:  D0 01     BNE $F796
$F795:  88        DEY
$F796:  84 3F     STY $3F
$F798:  E5 51     SBC $51
$F79A:  C5 6E     CMP $6E
$F79C:  90 02     BCC $F7A0
$F79E:  D0 03     BNE $F7A3
$F7A0:  4C 10 D4  JMP $D410
$F7A3:  85 74     STA $74
$F7A5:  85 70     STA $70
$F7A7:  85 3D     STA $3D
$F7A9:  85 E9     STA $E9
$F7AB:  68        PLA
$F7AC:  85 E8     STA $E8
$F7AE:  85 73     STA $73
$F7B0:  85 6F     STA $6F
$F7B2:  85 3C     STA $3C
$F7B4:  20 FA FC  JSR $FCFA
$F7B7:  A9 03     LDA #$03
$F7B9:  4C 02 FF  JMP $FF02
$F7BC:  18        CLC
$F7BD:  A5 9B     LDA $9B
$F7BF:  65 50     ADC $50
$F7C1:  85 3E     STA $3E
$F7C3:  A5 9C     LDA $9C
$F7C5:  65 51     ADC $51
$F7C7:  85 3F     STA $3F
$F7C9:  A0 04     LDY #$04
$F7CB:  B1 9B     LDA ($9B),Y
$F7CD:  20 EF E0  JSR $E0EF
$F7D0:  A5 94     LDA $94
$F7D2:  85 3C     STA $3C
$F7D4:  A5 95     LDA $95
$F7D6:  85 3D     STA $3D
$F7D8:  60        RTS
$F7D9:  A9 40     LDA #$40 ('@')
$F7DB:  85 14     STA $14
$F7DD:  20 E3 DF  JSR $DFE3
$F7E0:  A9 00     LDA #$00
$F7E2:  85 14     STA $14
$F7E4:  4C F0 D8  JMP $D8F0
$F7E7:  20 F8 E6  JSR $E6F8
$F7EA:  CA        DEX
$F7EB:  8A        TXA
$F7EC:  C9 28     CMP #$28 ('(')
$F7EE:  90 0A     BCC $F7FA
$F7F0:  E9 28     SBC #$28 ('(')
$F7F2:  48        PHA
$F7F3:  20 FB DA  JSR $DAFB
$F7F6:  68        PLA
$F7F7:  4C EC F7  JMP $F7EC
$F7FA:  85 24     STA $24
$F7FC:  60        RTS
$F7FD:  CB        .BYTE $CB
$F7FE:  D2        .BYTE $D2
$F7FF:  D7        .BYTE $D7
$F800:  4A        LSR ; [PLOT]
$F801:  08        PHP
$F802:  20 47 F8  JSR $F847
$F805:  28        PLP
$F806:  A9 0F     LDA #$0F
$F808:  90 02     BCC $F80C
$F80A:  69 E0     ADC #$E0 ('`')
$F80C:  85 2E     STA $2E
$F80E:  B1 26     LDA ($26),Y
$F810:  45 30     EOR $30
$F812:  25 2E     AND $2E
$F814:  51 26     EOR ($26),Y
$F816:  91 26     STA ($26),Y
$F818:  60        RTS
$F819:  20 00 F8  JSR $F800 ; PLOT ; [HLINE]
$F81C:  C4 2C     CPY $2C
$F81E:  B0 11     BCS $F831
$F820:  C8        INY
$F821:  20 0E F8  JSR $F80E
$F824:  90 F6     BCC $F81C
$F826:  69 01     ADC #$01
$F828:  48        PHA ; [VLINE]
$F829:  20 00 F8  JSR $F800 ; PLOT
$F82C:  68        PLA
$F82D:  C5 2D     CMP $2D
$F82F:  90 F5     BCC $F826
$F831:  60        RTS
$F832:  A0 2F     LDY #$2F ('/') ; [CLRSCR]
$F834:  D0 02     BNE $F838
$F836:  A0 27     LDY #$27 (''') ; [CLRTOP]
$F838:  84 2D     STY $2D
$F83A:  A0 27     LDY #$27 (''')
$F83C:  A9 00     LDA #$00
$F83E:  85 30     STA $30
$F840:  20 28 F8  JSR $F828 ; VLINE
$F843:  88        DEY
$F844:  10 F6     BPL $F83C
$F846:  60        RTS
$F847:  48        PHA
$F848:  4A        LSR
$F849:  29 03     AND #$03
$F84B:  09 04     ORA #$04
$F84D:  85 27     STA $27
$F84F:  68        PLA
$F850:  29 18     AND #$18
$F852:  90 02     BCC $F856
$F854:  69 7F     ADC #$7F
$F856:  85 26     STA $26
$F858:  0A        ASL
$F859:  0A        ASL
$F85A:  05 26     ORA $26
$F85C:  85 26     STA $26
$F85E:  60        RTS
$F85F:  A5 30     LDA $30
$F861:  18        CLC
$F862:  69 03     ADC #$03
$F864:  29 0F     AND #$0F
$F866:  85 30     STA $30
$F868:  0A        ASL
$F869:  0A        ASL
$F86A:  0A        ASL
$F86B:  0A        ASL
$F86C:  05 30     ORA $30
$F86E:  85 30     STA $30
$F870:  60        RTS
$F871:  4A        LSR
$F872:  08        PHP
$F873:  20 47 F8  JSR $F847
$F876:  B1 26     LDA ($26),Y
$F878:  28        PLP
$F879:  90 04     BCC $F87F
$F87B:  4A        LSR
$F87C:  4A        LSR
$F87D:  4A        LSR
$F87E:  4A        LSR
$F87F:  29 0F     AND #$0F
$F881:  60        RTS
$F882:  A6 3A     LDX $3A
$F884:  A4 3B     LDY $3B
$F886:  20 96 FD  JSR $FD96
$F889:  20 48 F9  JSR $F948
$F88C:  A1 3A     LDA ($3A,X)
$F88E:  A8        TAY
$F88F:  4A        LSR
$F890:  90 09     BCC $F89B
$F892:  6A        ROR
$F893:  B0 10     BCS $F8A5
$F895:  C9 A2     CMP #$A2 ('"')
$F897:  F0 0C     BEQ $F8A5
$F899:  29 87     AND #$87
$F89B:  4A        LSR
$F89C:  AA        TAX
$F89D:  BD 62 F9  LDA $F962,X
$F8A0:  20 79 F8  JSR $F879
$F8A3:  D0 04     BNE $F8A9
$F8A5:  A0 80     LDY #$80
$F8A7:  A9 00     LDA #$00
$F8A9:  AA        TAX
$F8AA:  BD A6 F9  LDA $F9A6,X
$F8AD:  85 2E     STA $2E
$F8AF:  29 03     AND #$03
$F8B1:  85 2F     STA $2F
$F8B3:  98        TYA
$F8B4:  29 8F     AND #$8F
$F8B6:  AA        TAX
$F8B7:  98        TYA
$F8B8:  A0 03     LDY #$03
$F8BA:  E0 8A     CPX #$8A
$F8BC:  F0 0B     BEQ $F8C9
$F8BE:  4A        LSR
$F8BF:  90 08     BCC $F8C9
$F8C1:  4A        LSR
$F8C2:  4A        LSR
$F8C3:  09 20     ORA #$20 (' ')
$F8C5:  88        DEY
$F8C6:  D0 FA     BNE $F8C2
$F8C8:  C8        INY
$F8C9:  88        DEY
$F8CA:  D0 F2     BNE $F8BE
$F8CC:  60        RTS
$F8CD:  FF        .BYTE $FF
$F8CE:  FF        .BYTE $FF
$F8CF:  FF        .BYTE $FF
$F8D0:  20 82 F8  JSR $F882
$F8D3:  48        PHA
$F8D4:  B1 3A     LDA ($3A),Y
$F8D6:  20 DA FD  JSR $FDDA ; PRBYTE
$F8D9:  A2 01     LDX #$01
$F8DB:  20 4A F9  JSR $F94A
$F8DE:  C4 2F     CPY $2F
$F8E0:  C8        INY
$F8E1:  90 F1     BCC $F8D4
$F8E3:  A2 03     LDX #$03
$F8E5:  C0 04     CPY #$04
$F8E7:  90 F2     BCC $F8DB
$F8E9:  68        PLA
$F8EA:  A8        TAY
$F8EB:  B9 C0 F9  LDA $F9C0,Y
$F8EE:  85 2C     STA $2C
$F8F0:  B9 00 FA  LDA $FA00,Y
$F8F3:  85 2D     STA $2D
$F8F5:  A9 00     LDA #$00
$F8F7:  A0 05     LDY #$05
$F8F9:  06 2D     ASL $2D
$F8FB:  26 2C     ROL $2C
$F8FD:  2A        ROL
$F8FE:  88        DEY
$F8FF:  D0 F8     BNE $F8F9
$F901:  69 BF     ADC #$BF ('?')
$F903:  20 ED FD  JSR $FDED ; COUT
$F906:  CA        DEX
$F907:  D0 EC     BNE $F8F5
$F909:  20 48 F9  JSR $F948
$F90C:  A4 2F     LDY $2F
$F90E:  A2 06     LDX #$06
$F910:  E0 03     CPX #$03
$F912:  F0 1C     BEQ $F930
$F914:  06 2E     ASL $2E
$F916:  90 0E     BCC $F926
$F918:  BD B3 F9  LDA $F9B3,X
$F91B:  20 ED FD  JSR $FDED ; COUT
$F91E:  BD B9 F9  LDA $F9B9,X
$F921:  F0 03     BEQ $F926
$F923:  20 ED FD  JSR $FDED ; COUT
$F926:  CA        DEX
$F927:  D0 E7     BNE $F910
$F929:  60        RTS
$F92A:  88        DEY
$F92B:  30 E7     BMI $F914
$F92D:  20 DA FD  JSR $FDDA ; PRBYTE
$F930:  A5 2E     LDA $2E
$F932:  C9 E8     CMP #$E8 ('h')
$F934:  B1 3A     LDA ($3A),Y
$F936:  90 F2     BCC $F92A
$F938:  20 56 F9  JSR $F956
$F93B:  AA        TAX
$F93C:  E8        INX
$F93D:  D0 01     BNE $F940
$F93F:  C8        INY
$F940:  98        TYA
$F941:  20 DA FD  JSR $FDDA ; PRBYTE
$F944:  8A        TXA
$F945:  4C DA FD  JMP $FDDA ; PRBYTE
$F948:  A2 03     LDX #$03
$F94A:  A9 A0     LDA #$A0 (' ')
$F94C:  20 ED FD  JSR $FDED ; COUT
$F94F:  CA        DEX
$F950:  D0 F8     BNE $F94A
$F952:  60        RTS
$F953:  38        SEC
$F954:  A5 2F     LDA $2F
$F956:  A4 3B     LDY $3B
$F958:  AA        TAX
$F959:  10 01     BPL $F95C
$F95B:  88        DEY
$F95C:  65 3A     ADC $3A
$F95E:  90 01     BCC $F961
$F960:  C8        INY
$F961:  60        RTS
$F962:  04        .BYTE $04
$F963:  20 54 30  JSR $3054
$F966:  0D 80 04  ORA $0480
$F969:  90 03     BCC $F96E
$F96B:  22        .BYTE $22
$F96C:  54        .BYTE $54
$F96D:  33        .BYTE $33
$F96E:  0D 80 04  ORA $0480
$F971:  90 04     BCC $F977
$F973:  20 54 33  JSR $3354
$F976:  0D 80 04  ORA $0480
$F979:  90 04     BCC $F97F
$F97B:  20 54 3B  JSR $3B54
$F97E:  0D 80 04  ORA $0480
$F981:  90 00     BCC $F983
$F983:  22        .BYTE $22
$F984:  44        .BYTE $44
$F985:  33        .BYTE $33
$F986:  0D C8 44  ORA $44C8
$F989:  00        BRK
$F98A:  11 22     ORA ($22),Y
$F98C:  44        .BYTE $44
$F98D:  33        .BYTE $33
$F98E:  0D C8 44  ORA $44C8
$F991:  A9 01     LDA #$01
$F993:  22        .BYTE $22
$F994:  44        .BYTE $44
$F995:  33        .BYTE $33
$F996:  0D 80 04  ORA $0480
$F999:  90 01     BCC $F99C
$F99B:  22        .BYTE $22
$F99C:  44        .BYTE $44
$F99D:  33        .BYTE $33
$F99E:  0D 80 04  ORA $0480
$F9A1:  90 26     BCC $F9C9
$F9A3:  31 87     AND ($87),Y
$F9A5:  9A        TXS
$F9A6:  00        BRK
$F9A7:  21 81     AND ($81,X)
$F9A9:  82        .BYTE $82
$F9AA:  00        BRK
$F9AB:  00        BRK
$F9AC:  59 4D 91  EOR $914D,Y
$F9AF:  92        .BYTE $92
$F9B0:  86 4A     STX $4A
$F9B2:  85 9D     STA $9D
$F9B4:  AC A9 AC  LDY $ACA9
$F9B7:  A3        .BYTE $A3
$F9B8:  A8        TAY
$F9B9:  A4 D9     LDY $D9
$F9BB:  00        BRK
$F9BC:  D8        CLD
$F9BD:  A4 A4     LDY $A4
$F9BF:  00        BRK
$F9C0:  1C        .BYTE $1C
$F9C1:  8A        TXA
$F9C2:  1C        .BYTE $1C
$F9C3:  23        .BYTE $23
$F9C4:  5D 8B 1B  EOR $1B8B,X
$F9C7:  A1 9D     LDA ($9D,X)
$F9C9:  8A        TXA
$F9CA:  1D 23 9D  ORA $9D23,X
$F9CD:  8B        .BYTE $8B
$F9CE:  1D A1 00  ORA $00A1,X
$F9D1:  29 19     AND #$19
$F9D3:  AE 69 A8  LDX $A869
$F9D6:  19 23 24  ORA $2423,Y
$F9D9:  53        .BYTE $53
$F9DA:  1B        .BYTE $1B
$F9DB:  23        .BYTE $23
$F9DC:  24 53     BIT $53
$F9DE:  19 A1 00  ORA $00A1,Y
$F9E1:  1A        .BYTE $1A
$F9E2:  5B        .BYTE $5B
$F9E3:  5B        .BYTE $5B
$F9E4:  A5 69     LDA $69
$F9E6:  24 24     BIT $24
$F9E8:  AE AE A8  LDX $A8AE
$F9EB:  AD 29 00  LDA $0029
$F9EE:  7C        .BYTE $7C
$F9EF:  00        BRK
$F9F0:  15 9C     ORA $9C,X
$F9F2:  6D 9C A5  ADC $A59C
$F9F5:  69 29     ADC #$29 (')')
$F9F7:  53        .BYTE $53
$F9F8:  84 13     STY $13
$F9FA:  34        .BYTE $34
$F9FB:  11 A5     ORA ($A5),Y
$F9FD:  69 23     ADC #$23 ('#')
$F9FF:  A0 D8     LDY #$D8 ('X')
$FA01:  62        .BYTE $62
$FA02:  5A        .BYTE $5A
$FA03:  48        PHA
$FA04:  26 62     ROL $62
$FA06:  94 88     STY $88,X
$FA08:  54        .BYTE $54
$FA09:  44        .BYTE $44
$FA0A:  C8        INY
$FA0B:  54        .BYTE $54
$FA0C:  68        PLA
$FA0D:  44        .BYTE $44
$FA0E:  E8        INX
$FA0F:  94 00     STY $00,X
$FA11:  B4 08     LDY $08,X
$FA13:  84 74     STY $74
$FA15:  B4 28     LDY $28,X
$FA17:  6E 74 F4  ROR $F474
$FA1A:  CC 4A 72  CPY $724A
$FA1D:  F2        .BYTE $F2
$FA1E:  A4 8A     LDY $8A
$FA20:  00        BRK
$FA21:  AA        TAX
$FA22:  A2 A2     LDX #$A2 ('"')
$FA24:  74        .BYTE $74
$FA25:  74        .BYTE $74
$FA26:  74        .BYTE $74
$FA27:  72        .BYTE $72
$FA28:  44        .BYTE $44
$FA29:  68        PLA
$FA2A:  B2        .BYTE $B2
$FA2B:  32        .BYTE $32
$FA2C:  B2        .BYTE $B2
$FA2D:  00        BRK
$FA2E:  22        .BYTE $22
$FA2F:  00        BRK
$FA30:  1A        .BYTE $1A
$FA31:  1A        .BYTE $1A
$FA32:  26 26     ROL $26
$FA34:  72        .BYTE $72
$FA35:  72        .BYTE $72
$FA36:  88        DEY
$FA37:  C8        INY
$FA38:  C4 CA     CPY $CA
$FA3A:  26 48     ROL $48
$FA3C:  44        .BYTE $44
$FA3D:  44        .BYTE $44
$FA3E:  A2 C8     LDX #$C8 ('H')
$FA40:  85 45     STA $45
$FA42:  68        PLA
$FA43:  48        PHA
$FA44:  0A        ASL
$FA45:  0A        ASL
$FA46:  0A        ASL
$FA47:  30 03     BMI $FA4C
$FA49:  6C FE 03  JMP ($03FE)
$FA4C:  28        PLP
$FA4D:  20 4C FF  JSR $FF4C
$FA50:  68        PLA
$FA51:  85 3A     STA $3A
$FA53:  68        PLA
$FA54:  85 3B     STA $3B
$FA56:  6C F0 03  JMP ($03F0)
$FA59:  20 82 F8  JSR $F882
$FA5C:  20 DA FA  JSR $FADA
$FA5F:  4C 65 FF  JMP $FF65
$FA62:  D8        CLD
$FA63:  20 84 FE  JSR $FE84 ; SETNORM
$FA66:  20 2F FB  JSR $FB2F ; TEXT
$FA69:  20 93 FE  JSR $FE93 ; SETKBD
$FA6C:  20 89 FE  JSR $FE89 ; SETVID
$FA6F:  AD 58 C0  LDA $C058 ; AN0OFF
$FA72:  AD 5A C0  LDA $C05A ; AN1OFF
$FA75:  AD 5D C0  LDA $C05D ; AN2ON
$FA78:  AD 5F C0  LDA $C05F ; AN3ON
$FA7B:  AD FF CF  LDA $CFFF
$FA7E:  2C 10 C0  BIT $C010 ; KBDSTRB
$FA81:  D8        CLD
$FA82:  20 3A FF  JSR $FF3A ; BELL
$FA85:  AD F3 03  LDA $03F3 ; SOFTEV_H
$FA88:  49 A5     EOR #$A5 ('%')
$FA8A:  CD F4 03  CMP $03F4 ; PWREDGE
$FA8D:  D0 17     BNE $FAA6
$FA8F:  AD F2 03  LDA $03F2 ; SOFTEV
$FA92:  D0 0F     BNE $FAA3
$FA94:  A9 E0     LDA #$E0 ('`')
$FA96:  CD F3 03  CMP $03F3 ; SOFTEV_H
$FA99:  D0 08     BNE $FAA3
$FA9B:  A0 03     LDY #$03
$FA9D:  8C F2 03  STY $03F2 ; SOFTEV
$FAA0:  4C 00 E0  JMP $E000
$FAA3:  6C F2 03  JMP ($03F2) ; (SOFTEV)
$FAA6:  20 58 FC  JSR $FC58 ; HOME
$FAA9:  A2 05     LDX #$05
$FAAB:  BD FC FA  LDA $FAFC,X
$FAAE:  9D EF 03  STA $03EF,X
$FAB1:  CA        DEX
$FAB2:  D0 F7     BNE $FAAB
$FAB4:  A9 C6     LDA #$C6 ('F')
$FAB6:  8D F8 07  STA $07F8
$FAB9:  4C 00 C6  JMP $C600 ; DISK2_BOOT_ENTRY
$FABC:  90 05     BCC $FAC3
$FABE:  8D 78 06  STA $0678
$FAC1:  05 F3     ORA $F3
$FAC3:  20 ED FD  JSR $FDED ; COUT
$FAC6:  4E 78 06  LSR $0678
$FAC9:  60        RTS
$FACA:  B0 3A     BCS $FB06
$FACC:  A8        TAY
$FACD:  30 38     BMI $FB07
$FACF:  A0 E0     LDY #$E0 ('`')
$FAD1:  CC 78 06  CPY $0678
$FAD4:  90 2C     BCC $FB02
$FAD6:  60        RTS
$FAD7:  20 8E FD  JSR $FD8E ; CROUT
$FADA:  A9 45     LDA #$45 ('E')
$FADC:  85 40     STA $40
$FADE:  A9 00     LDA #$00
$FAE0:  85 41     STA $41
$FAE2:  A2 FB     LDX #$FB ('{')
$FAE4:  A9 A0     LDA #$A0 (' ')
$FAE6:  20 ED FD  JSR $FDED ; COUT
$FAE9:  BD 1E FA  LDA $FA1E,X
$FAEC:  20 ED FD  JSR $FDED ; COUT
$FAEF:  A9 BD     LDA #$BD ('=')
$FAF1:  20 ED FD  JSR $FDED ; COUT
$FAF4:  B5 4A     LDA $4A,X
$FAF6:  20 DA FD  JSR $FDDA ; PRBYTE
$FAF9:  E8        INX
$FAFA:  30 E8     BMI $FAE4
$FAFC:  60        RTS
$FAFD:  59 FA 00  EOR $00FA,Y
$FB00:  E0 45     CPX #$45 ('E')
$FB02:  29 1F     AND #$1F
$FB04:  09 80     ORA #$80
$FB06:  38        SEC
$FB07:  60        RTS
$FB08:  29 0F     AND #$0F
$FB0A:  D0 08     BNE $FB14
$FB0C:  B1 28     LDA ($28),Y
$FB0E:  10 04     BPL $FB14
$FB10:  49 60     EOR #$60 ('`')
$FB12:  91 28     STA ($28),Y
$FB14:  68        PLA
$FB15:  60        RTS
$FB16:  EA        NOP
$FB17:  EA        NOP
$FB18:  EA        NOP
$FB19:  C1 D8     CMP ($D8,X)
$FB1B:  D9 D0 D3  CMP $D3D0,Y
$FB1E:  AD 70 C0  LDA $C070
$FB21:  A0 00     LDY #$00
$FB23:  EA        NOP
$FB24:  EA        NOP
$FB25:  BD 64 C0  LDA $C064,X
$FB28:  10 04     BPL $FB2E
$FB2A:  C8        INY
$FB2B:  D0 F8     BNE $FB25
$FB2D:  88        DEY
$FB2E:  60        RTS
$FB2F:  A9 00     LDA #$00 ; [TEXT]
$FB31:  85 48     STA $48
$FB33:  AD 56 C0  LDA $C056 ; HIRESOFF
$FB36:  AD 54 C0  LDA $C054 ; PAGE2OFF
$FB39:  AD 51 C0  LDA $C051 ; TEXTON ; [SETGR]
$FB3C:  A9 00     LDA #$00
$FB3E:  F0 0B     BEQ $FB4B
$FB40:  AD 50 C0  LDA $C050 ; TEXTOFF ; [SETCOL]
$FB43:  AD 53 C0  LDA $C053 ; MIXEDON
$FB46:  20 36 F8  JSR $F836 ; CLRTOP
$FB49:  A9 14     LDA #$14
$FB4B:  85 22     STA $22
$FB4D:  A9 00     LDA #$00
$FB4F:  85 20     STA $20
$FB51:  A9 28     LDA #$28 ('(')
$FB53:  85 21     STA $21
$FB55:  A9 18     LDA #$18
$FB57:  85 23     STA $23
$FB59:  A9 17     LDA #$17
$FB5B:  85 25     STA $25
$FB5D:  4C 22 FC  JMP $FC22
$FB60:  51 28     EOR ($28),Y
$FB62:  49 40     EOR #$40 ('@')
$FB64:  0A        ASL
$FB65:  60        RTS
$FB66:  48        PHA
$FB67:  D0 AB     BNE $FB14
$FB69:  E6 4F     INC $4F
$FB6B:  A5 4F     LDA $4F
$FB6D:  90 99     BCC $FB08
$FB6F:  AD F3 03  LDA $03F3 ; SOFTEV_H
$FB72:  49 A5     EOR #$A5 ('%')
$FB74:  8D F4 03  STA $03F4 ; PWREDGE
$FB77:  60        RTS
$FB78:  C9 8D     CMP #$8D
$FB7A:  D0 18     BNE $FB94
$FB7C:  AC 00 C0  LDY $C000 ; KBD
$FB7F:  10 13     BPL $FB94
$FB81:  C0 93     CPY #$93
$FB83:  D0 0F     BNE $FB94
$FB85:  2C 10 C0  BIT $C010 ; KBDSTRB
$FB88:  AC 00 C0  LDY $C000 ; KBD
$FB8B:  10 FB     BPL $FB88
$FB8D:  C0 83     CPY #$83
$FB8F:  F0 03     BEQ $FB94
$FB91:  2C 10 C0  BIT $C010 ; KBDSTRB
$FB94:  4C FD FB  JMP $FBFD
$FB97:  38        SEC
$FB98:  4C 2C FC  JMP $FC2C
$FB9B:  A8        TAY
$FB9C:  B9 FC FD  LDA $FDFC,Y
$FB9F:  20 97 FB  JSR $FB97
$FBA2:  20 0C FD  JSR $FD0C ; RDKEY
$FBA5:  C9 CE     CMP #$CE ('N')
$FBA7:  B0 EE     BCS $FB97
$FBA9:  C9 C9     CMP #$C9 ('I')
$FBAB:  90 EA     BCC $FB97
$FBAD:  C9 CC     CMP #$CC ('L')
$FBAF:  F0 E6     BEQ $FB97
$FBB1:  D0 E8     BNE $FB9B
$FBB3:  0A        ASL
$FBB4:  90 08     BCC $FBBE
$FBB6:  48        PHA
$FBB7:  20 60 FB  JSR $FB60
$FBBA:  0A        ASL
$FBBB:  68        PLA
$FBBC:  B0 02     BCS $FBC0
$FBBE:  09 80     ORA #$80
$FBC0:  60        RTS
$FBC1:  48        PHA
$FBC2:  4A        LSR
$FBC3:  29 03     AND #$03
$FBC5:  09 04     ORA #$04
$FBC7:  85 29     STA $29
$FBC9:  68        PLA
$FBCA:  29 18     AND #$18
$FBCC:  90 02     BCC $FBD0
$FBCE:  69 7F     ADC #$7F
$FBD0:  85 28     STA $28
$FBD2:  0A        ASL
$FBD3:  0A        ASL
$FBD4:  05 28     ORA $28
$FBD6:  85 28     STA $28
$FBD8:  60        RTS
$FBD9:  C9 87     CMP #$87
$FBDB:  D0 12     BNE $FBEF
$FBDD:  A9 40     LDA #$40 ('@')
$FBDF:  20 A8 FC  JSR $FCA8
$FBE2:  A0 C0     LDY #$C0 ('@')
$FBE4:  A9 0C     LDA #$0C
$FBE6:  20 A8 FC  JSR $FCA8
$FBE9:  AD 30 C0  LDA $C030 ; SPKR
$FBEC:  88        DEY
$FBED:  D0 F5     BNE $FBE4
$FBEF:  60        RTS
$FBF0:  A4 24     LDY $24
$FBF2:  91 28     STA ($28),Y
$FBF4:  E6 24     INC $24
$FBF6:  A5 24     LDA $24
$FBF8:  C5 21     CMP $21
$FBFA:  B0 66     BCS $FC62
$FBFC:  60        RTS
$FBFD:  C9 A0     CMP #$A0 (' ')
$FBFF:  20 CA FA  JSR $FACA
$FC02:  B0 EC     BCS $FBF0
$FC04:  C9 8D     CMP #$8D
$FC06:  F0 5A     BEQ $FC62
$FC08:  C9 8A     CMP #$8A
$FC0A:  F0 5A     BEQ $FC66
$FC0C:  C9 88     CMP #$88
$FC0E:  D0 C9     BNE $FBD9
$FC10:  C6 24     DEC $24
$FC12:  10 E8     BPL $FBFC
$FC14:  A5 21     LDA $21
$FC16:  85 24     STA $24
$FC18:  C6 24     DEC $24
$FC1A:  A5 22     LDA $22
$FC1C:  C5 25     CMP $25
$FC1E:  B0 0B     BCS $FC2B
$FC20:  C6 25     DEC $25
$FC22:  A5 25     LDA $25
$FC24:  20 C1 FB  JSR $FBC1
$FC27:  65 20     ADC $20
$FC29:  85 28     STA $28
$FC2B:  60        RTS
$FC2C:  49 C0     EOR #$C0 ('@')
$FC2E:  F0 28     BEQ $FC58
$FC30:  69 FD     ADC #$FD ('}')
$FC32:  90 C0     BCC $FBF4
$FC34:  F0 DA     BEQ $FC10
$FC36:  69 FD     ADC #$FD ('}')
$FC38:  90 2C     BCC $FC66
$FC3A:  F0 DE     BEQ $FC1A
$FC3C:  69 FD     ADC #$FD ('}')
$FC3E:  90 5C     BCC $FC9C
$FC40:  D0 E9     BNE $FC2B
$FC42:  A4 24     LDY $24
$FC44:  A5 25     LDA $25
$FC46:  48        PHA
$FC47:  20 24 FC  JSR $FC24
$FC4A:  20 9E FC  JSR $FC9E
$FC4D:  A0 00     LDY #$00
$FC4F:  68        PLA
$FC50:  69 00     ADC #$00
$FC52:  C5 23     CMP $23
$FC54:  90 F0     BCC $FC46
$FC56:  B0 CA     BCS $FC22
$FC58:  A5 22     LDA $22 ; [HOME]
$FC5A:  85 25     STA $25
$FC5C:  A0 00     LDY #$00
$FC5E:  84 24     STY $24
$FC60:  F0 E4     BEQ $FC46
$FC62:  A9 00     LDA #$00
$FC64:  85 24     STA $24
$FC66:  E6 25     INC $25
$FC68:  A5 25     LDA $25
$FC6A:  C5 23     CMP $23
$FC6C:  90 B6     BCC $FC24
$FC6E:  C6 25     DEC $25
$FC70:  A5 22     LDA $22
$FC72:  48        PHA
$FC73:  20 24 FC  JSR $FC24
$FC76:  A5 28     LDA $28
$FC78:  85 2A     STA $2A
$FC7A:  A5 29     LDA $29
$FC7C:  85 2B     STA $2B
$FC7E:  A4 21     LDY $21
$FC80:  88        DEY
$FC81:  68        PLA
$FC82:  69 01     ADC #$01
$FC84:  C5 23     CMP $23
$FC86:  B0 0D     BCS $FC95
$FC88:  48        PHA
$FC89:  20 24 FC  JSR $FC24
$FC8C:  B1 28     LDA ($28),Y
$FC8E:  91 2A     STA ($2A),Y
$FC90:  88        DEY
$FC91:  10 F9     BPL $FC8C
$FC93:  30 E1     BMI $FC76
$FC95:  A0 00     LDY #$00
$FC97:  20 9E FC  JSR $FC9E
$FC9A:  B0 86     BCS $FC22
$FC9C:  A4 24     LDY $24
$FC9E:  A9 A0     LDA #$A0 (' ')
$FCA0:  91 28     STA ($28),Y
$FCA2:  C8        INY
$FCA3:  C4 21     CPY $21
$FCA5:  90 F9     BCC $FCA0
$FCA7:  60        RTS
$FCA8:  38        SEC
$FCA9:  48        PHA
$FCAA:  E9 01     SBC #$01
$FCAC:  D0 FC     BNE $FCAA
$FCAE:  68        PLA
$FCAF:  E9 01     SBC #$01
$FCB1:  D0 F6     BNE $FCA9
$FCB3:  60        RTS
$FCB4:  E6 42     INC $42
$FCB6:  D0 02     BNE $FCBA
$FCB8:  E6 43     INC $43
$FCBA:  A5 3C     LDA $3C
$FCBC:  C5 3E     CMP $3E
$FCBE:  A5 3D     LDA $3D
$FCC0:  E5 3F     SBC $3F
$FCC2:  E6 3C     INC $3C
$FCC4:  D0 02     BNE $FCC8
$FCC6:  E6 3D     INC $3D
$FCC8:  60        RTS
$FCC9:  A0 4B     LDY #$4B ('K')
$FCCB:  20 DB FC  JSR $FCDB
$FCCE:  D0 F9     BNE $FCC9
$FCD0:  69 FE     ADC #$FE ('~')
$FCD2:  B0 F5     BCS $FCC9
$FCD4:  A0 21     LDY #$21 ('!')
$FCD6:  20 DB FC  JSR $FCDB
$FCD9:  C8        INY
$FCDA:  C8        INY
$FCDB:  88        DEY
$FCDC:  D0 FD     BNE $FCDB
$FCDE:  90 05     BCC $FCE5
$FCE0:  A0 32     LDY #$32 ('2')
$FCE2:  88        DEY
$FCE3:  D0 FD     BNE $FCE2
$FCE5:  AC 20 C0  LDY $C020 ; TAPEOUT
$FCE8:  A0 2C     LDY #$2C (',')
$FCEA:  CA        DEX
$FCEB:  60        RTS
$FCEC:  A2 08     LDX #$08
$FCEE:  48        PHA
$FCEF:  20 FA FC  JSR $FCFA
$FCF2:  68        PLA
$FCF3:  2A        ROL
$FCF4:  A0 3A     LDY #$3A (':')
$FCF6:  CA        DEX
$FCF7:  D0 F5     BNE $FCEE
$FCF9:  60        RTS
$FCFA:  20 FD FC  JSR $FCFD
$FCFD:  88        DEY
$FCFE:  AD 60 C0  LDA $C060 ; CASSETTE_IN
$FD01:  45 2F     EOR $2F
$FD03:  10 F8     BPL $FCFD
$FD05:  45 2F     EOR $2F
$FD07:  85 2F     STA $2F
$FD09:  C0 80     CPY #$80
$FD0B:  60        RTS
$FD0C:  A4 24     LDY $24 ; [RDKEY]
$FD0E:  B1 28     LDA ($28),Y
$FD10:  48        PHA
$FD11:  20 B3 FB  JSR $FBB3
$FD14:  6A        ROR
$FD15:  91 28     STA ($28),Y
$FD17:  68        PLA
$FD18:  6C 38 00  JMP ($0038)
$FD1B:  E6 4E     INC $4E ; [KEYIN]
$FD1D:  18        CLC
$FD1E:  20 66 FB  JSR $FB66
$FD21:  2C 00 C0  BIT $C000 ; KBD
$FD24:  10 F5     BPL $FD1B
$FD26:  91 28     STA ($28),Y
$FD28:  AD 00 C0  LDA $C000 ; KBD
$FD2B:  2C 10 C0  BIT $C010 ; KBDSTRB
$FD2E:  60        RTS
$FD2F:  20 0C FD  JSR $FD0C ; RDKEY
$FD32:  20 A5 FB  JSR $FBA5
$FD35:  20 0C FD  JSR $FD0C ; RDKEY ; [RDCHAR]
$FD38:  C9 9B     CMP #$9B
$FD3A:  F0 F3     BEQ $FD2F
$FD3C:  60        RTS
$FD3D:  A5 32     LDA $32
$FD3F:  48        PHA
$FD40:  A9 FF     LDA #$FF
$FD42:  85 32     STA $32
$FD44:  BD 00 02  LDA $0200,X
$FD47:  20 ED FD  JSR $FDED ; COUT
$FD4A:  68        PLA
$FD4B:  85 32     STA $32
$FD4D:  BD 00 02  LDA $0200,X
$FD50:  C9 88     CMP #$88
$FD52:  F0 1D     BEQ $FD71
$FD54:  C9 98     CMP #$98
$FD56:  F0 0A     BEQ $FD62
$FD58:  E0 F8     CPX #$F8 ('x')
$FD5A:  90 03     BCC $FD5F
$FD5C:  20 3A FF  JSR $FF3A ; BELL
$FD5F:  E8        INX
$FD60:  D0 13     BNE $FD75
$FD62:  A9 DC     LDA #$DC ('\')
$FD64:  20 ED FD  JSR $FDED ; COUT
$FD67:  20 8E FD  JSR $FD8E ; CROUT ; [GETLNZ]
$FD6A:  A5 33     LDA $33 ; [GETLN]
$FD6C:  20 ED FD  JSR $FDED ; COUT
$FD6F:  A2 01     LDX #$01
$FD71:  8A        TXA
$FD72:  F0 F3     BEQ $FD67
$FD74:  CA        DEX
$FD75:  20 35 FD  JSR $FD35 ; RDCHAR
$FD78:  C9 95     CMP #$95
$FD7A:  D0 08     BNE $FD84
$FD7C:  B1 28     LDA ($28),Y
$FD7E:  10 04     BPL $FD84
$FD80:  C9 A0     CMP #$A0 (' ')
$FD82:  90 F1     BCC $FD75
$FD84:  9D 00 02  STA $0200,X
$FD87:  C9 8D     CMP #$8D
$FD89:  D0 B2     BNE $FD3D
$FD8B:  20 9C FC  JSR $FC9C
$FD8E:  A9 8D     LDA #$8D ; [CROUT]
$FD90:  D0 5B     BNE $FDED
$FD92:  A4 3D     LDY $3D
$FD94:  A6 3C     LDX $3C
$FD96:  20 8E FD  JSR $FD8E ; CROUT
$FD99:  20 40 F9  JSR $F940
$FD9C:  A0 00     LDY #$00
$FD9E:  A9 AD     LDA #$AD ('-')
$FDA0:  4C ED FD  JMP $FDED ; COUT
$FDA3:  A5 3C     LDA $3C ; [PRA1]
$FDA5:  09 07     ORA #$07
$FDA7:  85 3E     STA $3E
$FDA9:  A5 3D     LDA $3D
$FDAB:  85 3F     STA $3F
$FDAD:  A5 3C     LDA $3C
$FDAF:  29 07     AND #$07
$FDB1:  D0 03     BNE $FDB6
$FDB3:  20 92 FD  JSR $FD92
$FDB6:  A9 A0     LDA #$A0 (' ')
$FDB8:  20 ED FD  JSR $FDED ; COUT
$FDBB:  B1 3C     LDA ($3C),Y
$FDBD:  20 DA FD  JSR $FDDA ; PRBYTE
$FDC0:  20 BA FC  JSR $FCBA
$FDC3:  90 E8     BCC $FDAD
$FDC5:  60        RTS
$FDC6:  4A        LSR
$FDC7:  90 EA     BCC $FDB3
$FDC9:  4A        LSR
$FDCA:  4A        LSR
$FDCB:  A5 3E     LDA $3E
$FDCD:  90 02     BCC $FDD1
$FDCF:  49 FF     EOR #$FF
$FDD1:  65 3C     ADC $3C
$FDD3:  48        PHA
$FDD4:  A9 BD     LDA #$BD ('=')
$FDD6:  20 ED FD  JSR $FDED ; COUT
$FDD9:  68        PLA
$FDDA:  48        PHA ; [PRBYTE]
$FDDB:  4A        LSR
$FDDC:  4A        LSR
$FDDD:  4A        LSR
$FDDE:  4A        LSR
$FDDF:  20 E5 FD  JSR $FDE5
$FDE2:  68        PLA
$FDE3:  29 0F     AND #$0F
$FDE5:  09 B0     ORA #$B0 ('0')
$FDE7:  C9 BA     CMP #$BA (':')
$FDE9:  90 02     BCC $FDED
$FDEB:  69 06     ADC #$06
$FDED:  6C 36 00  JMP ($0036) ; [COUT]
$FDF0:  C9 A0     CMP #$A0 (' ')
$FDF2:  90 02     BCC $FDF6
$FDF4:  25 32     AND $32
$FDF6:  84 35     STY $35
$FDF8:  48        PHA
$FDF9:  20 78 FB  JSR $FB78
$FDFC:  68        PLA
$FDFD:  A4 35     LDY $35
$FDFF:  60        RTS
$FE00:  C6 34     DEC $34
$FE02:  F0 9F     BEQ $FDA3
$FE04:  CA        DEX
$FE05:  D0 16     BNE $FE1D
$FE07:  C9 BA     CMP #$BA (':')
$FE09:  D0 BB     BNE $FDC6
$FE0B:  85 31     STA $31
$FE0D:  A5 3E     LDA $3E
$FE0F:  91 40     STA ($40),Y
$FE11:  E6 40     INC $40
$FE13:  D0 02     BNE $FE17
$FE15:  E6 41     INC $41
$FE17:  60        RTS
$FE18:  A4 34     LDY $34
$FE1A:  B9 FF 01  LDA $01FF,Y
$FE1D:  85 31     STA $31
$FE1F:  60        RTS
$FE20:  A2 01     LDX #$01
$FE22:  B5 3E     LDA $3E,X
$FE24:  95 42     STA $42,X
$FE26:  95 44     STA $44,X
$FE28:  CA        DEX
$FE29:  10 F7     BPL $FE22
$FE2B:  60        RTS
$FE2C:  B1 3C     LDA ($3C),Y
$FE2E:  91 42     STA ($42),Y
$FE30:  20 B4 FC  JSR $FCB4
$FE33:  90 F7     BCC $FE2C
$FE35:  60        RTS
$FE36:  B1 3C     LDA ($3C),Y
$FE38:  D1 42     CMP ($42),Y
$FE3A:  F0 1C     BEQ $FE58
$FE3C:  20 92 FD  JSR $FD92
$FE3F:  B1 3C     LDA ($3C),Y
$FE41:  20 DA FD  JSR $FDDA ; PRBYTE
$FE44:  A9 A0     LDA #$A0 (' ')
$FE46:  20 ED FD  JSR $FDED ; COUT
$FE49:  A9 A8     LDA #$A8 ('(')
$FE4B:  20 ED FD  JSR $FDED ; COUT
$FE4E:  B1 42     LDA ($42),Y
$FE50:  20 DA FD  JSR $FDDA ; PRBYTE
$FE53:  A9 A9     LDA #$A9 (')')
$FE55:  20 ED FD  JSR $FDED ; COUT
$FE58:  20 B4 FC  JSR $FCB4
$FE5B:  90 D9     BCC $FE36
$FE5D:  60        RTS
$FE5E:  20 75 FE  JSR $FE75
$FE61:  A9 14     LDA #$14
$FE63:  48        PHA
$FE64:  20 D0 F8  JSR $F8D0
$FE67:  20 53 F9  JSR $F953
$FE6A:  85 3A     STA $3A
$FE6C:  84 3B     STY $3B
$FE6E:  68        PLA
$FE6F:  38        SEC
$FE70:  E9 01     SBC #$01
$FE72:  D0 EF     BNE $FE63
$FE74:  60        RTS
$FE75:  8A        TXA
$FE76:  F0 07     BEQ $FE7F
$FE78:  B5 3C     LDA $3C,X
$FE7A:  95 3A     STA $3A,X
$FE7C:  CA        DEX
$FE7D:  10 F9     BPL $FE78
$FE7F:  60        RTS
$FE80:  A0 3F     LDY #$3F ('?')
$FE82:  D0 02     BNE $FE86
$FE84:  A0 FF     LDY #$FF ; [SETNORM]
$FE86:  84 32     STY $32
$FE88:  60        RTS
$FE89:  A9 00     LDA #$00 ; [SETVID]
$FE8B:  85 3E     STA $3E
$FE8D:  A2 38     LDX #$38 ('8')
$FE8F:  A0 1B     LDY #$1B
$FE91:  D0 08     BNE $FE9B
$FE93:  A9 00     LDA #$00 ; [SETKBD]
$FE95:  85 3E     STA $3E
$FE97:  A2 36     LDX #$36 ('6')
$FE99:  A0 F0     LDY #$F0 ('p')
$FE9B:  A5 3E     LDA $3E
$FE9D:  29 0F     AND #$0F
$FE9F:  F0 06     BEQ $FEA7
$FEA1:  09 C0     ORA #$C0 ('@')
$FEA3:  A0 00     LDY #$00
$FEA5:  F0 02     BEQ $FEA9
$FEA7:  A9 FD     LDA #$FD ('}')
$FEA9:  94 00     STY $00,X
$FEAB:  95 01     STA $01,X
$FEAD:  60        RTS
$FEAE:  EA        NOP
$FEAF:  EA        NOP
$FEB0:  4C 00 E0  JMP $E000
$FEB3:  4C 03 E0  JMP $E003
$FEB6:  20 75 FE  JSR $FE75
$FEB9:  20 3F FF  JSR $FF3F
$FEBC:  6C 3A 00  JMP ($003A)
$FEBF:  4C D7 FA  JMP $FAD7
$FEC2:  60        RTS
$FEC3:  EA        NOP
$FEC4:  60        RTS
$FEC5:  C4 C2     CPY $C2
$FEC7:  C1 FF     CMP ($FF,X)
$FEC9:  C3        .BYTE $C3
$FECA:  4C F8 03  JMP $03F8
$FECD:  A9 40     LDA #$40 ('@')
$FECF:  20 C9 FC  JSR $FCC9
$FED2:  A0 27     LDY #$27 (''')
$FED4:  A2 00     LDX #$00
$FED6:  41 3C     EOR ($3C,X)
$FED8:  48        PHA
$FED9:  A1 3C     LDA ($3C,X)
$FEDB:  20 ED FE  JSR $FEED
$FEDE:  20 BA FC  JSR $FCBA
$FEE1:  A0 1D     LDY #$1D
$FEE3:  68        PLA
$FEE4:  90 EE     BCC $FED4
$FEE6:  A0 22     LDY #$22 ('"')
$FEE8:  20 ED FE  JSR $FEED
$FEEB:  F0 4D     BEQ $FF3A
$FEED:  A2 10     LDX #$10
$FEEF:  0A        ASL
$FEF0:  20 D6 FC  JSR $FCD6
$FEF3:  D0 FA     BNE $FEEF
$FEF5:  60        RTS
$FEF6:  20 00 FE  JSR $FE00
$FEF9:  68        PLA
$FEFA:  68        PLA
$FEFB:  D0 6C     BNE $FF69
$FEFD:  20 FA FC  JSR $FCFA
$FF00:  A9 16     LDA #$16
$FF02:  20 C9 FC  JSR $FCC9
$FF05:  85 2E     STA $2E
$FF07:  20 FA FC  JSR $FCFA
$FF0A:  A0 24     LDY #$24 ('$')
$FF0C:  20 FD FC  JSR $FCFD
$FF0F:  B0 F9     BCS $FF0A
$FF11:  20 FD FC  JSR $FCFD
$FF14:  A0 3B     LDY #$3B (';')
$FF16:  20 EC FC  JSR $FCEC
$FF19:  81 3C     STA ($3C,X)
$FF1B:  45 2E     EOR $2E
$FF1D:  85 2E     STA $2E
$FF1F:  20 BA FC  JSR $FCBA
$FF22:  A0 35     LDY #$35 ('5')
$FF24:  90 F0     BCC $FF16
$FF26:  20 EC FC  JSR $FCEC
$FF29:  C5 2E     CMP $2E
$FF2B:  F0 0D     BEQ $FF3A
$FF2D:  A9 C5     LDA #$C5 ('E')
$FF2F:  20 ED FD  JSR $FDED ; COUT
$FF32:  A9 D2     LDA #$D2 ('R')
$FF34:  20 ED FD  JSR $FDED ; COUT
$FF37:  20 ED FD  JSR $FDED ; COUT
$FF3A:  A9 87     LDA #$87 ; [BELL]
$FF3C:  4C ED FD  JMP $FDED ; COUT
$FF3F:  A5 48     LDA $48
$FF41:  48        PHA
$FF42:  A5 45     LDA $45
$FF44:  A6 46     LDX $46
$FF46:  A4 47     LDY $47
$FF48:  28        PLP
$FF49:  60        RTS
$FF4A:  85 45     STA $45
$FF4C:  86 46     STX $46
$FF4E:  84 47     STY $47
$FF50:  08        PHP
$FF51:  68        PLA
$FF52:  85 48     STA $48
$FF54:  BA        TSX
$FF55:  86 49     STX $49
$FF57:  D8        CLD
$FF58:  60        RTS
$FF59:  20 84 FE  JSR $FE84 ; SETNORM
$FF5C:  20 2F FB  JSR $FB2F ; TEXT
$FF5F:  20 93 FE  JSR $FE93 ; SETKBD
$FF62:  20 89 FE  JSR $FE89 ; SETVID
$FF65:  D8        CLD
$FF66:  20 3A FF  JSR $FF3A ; BELL
$FF69:  A9 AA     LDA #$AA ('*')
$FF6B:  85 33     STA $33
$FF6D:  20 67 FD  JSR $FD67 ; GETLNZ
$FF70:  20 C7 FF  JSR $FFC7
$FF73:  20 A7 FF  JSR $FFA7
$FF76:  84 34     STY $34
$FF78:  A0 17     LDY #$17
$FF7A:  88        DEY
$FF7B:  30 E8     BMI $FF65
$FF7D:  D9 CC FF  CMP $FFCC,Y
$FF80:  D0 F8     BNE $FF7A
$FF82:  20 BE FF  JSR $FFBE
$FF85:  A4 34     LDY $34
$FF87:  4C 73 FF  JMP $FF73
$FF8A:  A2 03     LDX #$03
$FF8C:  0A        ASL
$FF8D:  0A        ASL
$FF8E:  0A        ASL
$FF8F:  0A        ASL
$FF90:  0A        ASL
$FF91:  26 3E     ROL $3E
$FF93:  26 3F     ROL $3F
$FF95:  CA        DEX
$FF96:  10 F8     BPL $FF90
$FF98:  A5 31     LDA $31
$FF9A:  D0 06     BNE $FFA2
$FF9C:  B5 3F     LDA $3F,X
$FF9E:  95 3D     STA $3D,X
$FFA0:  95 41     STA $41,X
$FFA2:  E8        INX
$FFA3:  F0 F3     BEQ $FF98
$FFA5:  D0 06     BNE $FFAD
$FFA7:  A2 00     LDX #$00
$FFA9:  86 3E     STX $3E
$FFAB:  86 3F     STX $3F
$FFAD:  B9 00 02  LDA $0200,Y
$FFB0:  C8        INY
$FFB1:  49 B0     EOR #$B0 ('0')
$FFB3:  C9 0A     CMP #$0A
$FFB5:  90 D3     BCC $FF8A
$FFB7:  69 88     ADC #$88
$FFB9:  C9 FA     CMP #$FA ('z')
$FFBB:  B0 CD     BCS $FF8A
$FFBD:  60        RTS
$FFBE:  A9 FE     LDA #$FE ('~')
$FFC0:  48        PHA
$FFC1:  B9 E3 FF  LDA $FFE3,Y
$FFC4:  48        PHA
$FFC5:  A5 31     LDA $31
$FFC7:  A0 00     LDY #$00
$FFC9:  84 31     STY $31
$FFCB:  60        RTS
$FFCC:  BC B2 BE  LDY $BEB2,X
$FFCF:  B2        .BYTE $B2
$FFD0:  EF        .BYTE $EF
$FFD1:  C4 B2     CPY $B2
$FFD3:  A9 BB     LDA #$BB (';')
$FFD5:  A6 A4     LDX $A4
$FFD7:  06 95     ASL $95
$FFD9:  07        .BYTE $07
$FFDA:  02        .BYTE $02
$FFDB:  05 F0     ORA $F0
$FFDD:  00        BRK
$FFDE:  EB        .BYTE $EB
$FFDF:  93        .BYTE $93
$FFE0:  A7        .BYTE $A7
$FFE1:  C6 99     DEC $99
$FFE3:  B2        .BYTE $B2
$FFE4:  C9 BE     CMP #$BE ('>')
$FFE6:  C1 35     CMP ($35,X)
$FFE8:  8C C9 96  STY $96C9
$FFEB:  AF        .BYTE $AF
$FFEC:  17        .BYTE $17
$FFED:  17        .BYTE $17
$FFEE:  2B        .BYTE $2B
$FFEF:  1F        .BYTE $1F
$FFF0:  83        .BYTE $83
$FFF1:  7F        .BYTE $7F
$FFF2:  5D CC B5  EOR $B5CC,X
$FFF5:  FC        .BYTE $FC
$FFF6:  17        .BYTE $17
$FFF7:  17        .BYTE $17
$FFF8:  F5 03     SBC $03,X
$FFFA:  FB        .BYTE $FB ; [NMI_VECTOR]
$FFFB:  03        .BYTE $03
$FFFC:  62        .BYTE $62 ; [RESET_VECTOR]
$FFFD:  FA        .BYTE $FA
$FFFE:  40        RTI ; [IRQ_VECTOR]
$FFFF:  FA        .BYTE $FA