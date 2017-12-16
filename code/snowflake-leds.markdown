---
layout: page
date:   2017-11-11 14:30:00 +0000
categories: code
permalink: "snow-led"
---

This Snowflake LED board is based around a PIC10F200 (202/204/206) microcontroller. 

<img src="/static/img/snow_led.JPG" alt="Snow LED board"/>

The code flashes LEDs connected to GPIO pins 0, 1 and 2, and changes the flashing pattern when GPIO 3 is pulled low and then released.

The code is as follows:

~~~~
;
; Snowflake LED PIC code
; http://packom.net/snow-led
;
; Copyright (C) 2017 Piers Finlayson
;
; This program is free software: you can redistribute it and/or modify it
; under the terms of the GNU General Public License as published by the Free
; Software Foundation, either version 3 of the License, or (at your option)
; any later version. 
;
; This program is distributed in the hope that it will be useful, but WITHOUT
; ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or
; FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
; more details.
;
; You should have received a copy of the GNU General Public License along with
; this program.  If not, see <http://www.gnu.org/licenses/>.
; 
    
;
; Supports 10F200, 10F202, 10F204 and 10F206 PICs
; 

; Modify the include header as appropriate for your device
; This is important for the PIC10F204 and 206 devices so that
; the comparitor is turned off
  INCLUDE "p10f200.inc"

  IFDEF __10F206
    #define PIC10F204_6
  ENDIF
  IFDEF __10F204
    #define PIC10F204_6
  ENDIF

; Used registers
TMR_COUNT_VAR EQU 10h
PROGRAM       EQU 11h
TMR_COUNT     EQU 12h
PWM           EQU 13h
PROG0B        EQU 14h

; #defines
#define PROGRAM0_MAX_TMR_BIT 5
	  
; Set __CONFIG
; WDTE_OFF = watchdog timer off
; CP_OFF = code protecton off
; MCLRE_OFF = GP3/MCLR pin fuction is digital I/O, MCLR internally tied to VDD
  __CONFIG _WDTE_OFF & _CP_OFF & _MCLRE_OFF

; Start
  ORG    0x0000
  
; Init - PROGRAM and TMR_COUNT to start on program 1
;
; Set OPTION:
; GPWU = 1 disabled, wake up on pin change bit GP0/1/3
; GPPU = 1 disabled, weak pull-ups GP0/1/3
; T0CS = 0 Transition on internal instruction cycle clock, Fosc/4
; T0SE = 1 Increment on high to low transition on T0CKI pin
; PSA = 0 prescaler assigned to Timer0
; PS2:0 = 111 1:256 (Timer0 rate)
init:
  MOVLW  ~((1<<T0CS)|(1<<PSA))  ;enable GPIO2 and 1:256 Timer0 prescaler
  OPTION
  MOVLW  ~((1<<TRISIO2)|(1<<TRISIO1)|(1<<TRISIO0)) ; Set GP2-0 to output
  TRIS   GPIO
  IFDEF PIC10F204_6
  ; Turn off comparitor (204/206 only)  
    MOVLW 0
    MOVWF CMCON0
  ENDIF
  CLRF   PROGRAM
  BSF    PROGRAM,0
  GOTO   program0_init
  
; Program 0 - Cycle through LEDs, one on at a time
program0_speed_up:
  RLF    TMR_COUNT,F
  BTFSS  TMR_COUNT,PROGRAM0_MAX_TMR_BIT ; If beyond 16 bail out of program0
  GOTO   program0 ; Was 16 or less
  RLF    PROGRAM,F  ; Was more than 16, switch to next program
  GOTO   program0a_init
program0_init:
  CLRF   PROGRAM ; wasn't program2 either - go back to program0
  BSF    PROGRAM,0
  CALL   program0_common_init
program0:
  ; put 0b100 into W
  MOVLW  ((1<<GP2)|(1<<GP1)) ; start with GP0 on
program0_loop:
  MOVWF  GPIO
  ; load tmr_count into variable
  MOVF   TMR_COUNT,W
  MOVWF  TMR_COUNT_VAR
; Clear tmr0 and prescaler
  CLRF   TMR0
program0_delay:
  ; see if GP3 is clear - if so, button has been pressed
  BTFSS  GPIO,3
  GOTO   button_pressed
  BTFSS  TMR0,7 ;wait until TMR0 reaches 128(*256 due to prescaler * 1/4 osc)
  GOTO   program0_delay
  CLRF   TMR0
  DECFSZ TMR_COUNT_VAR,F
  GOTO   program0_delay
  ; Bit shift GPIO right one into W
  RRF    GPIO,W
  ANDLW  3
  ; carry bit not set 0 got pushed off the end, so need 0 in bit 2, otherwise
  ; need 1 in bit 2
  BTFSS  STATUS,C
  GOTO   program0_loop
  IORLW  (1<<GP2)
  GOTO   program0_loop
 
; Shared between program0 and program0a
program0_common_init:  
  MOVLW  ~((1<<T0CS)|(1<<PSA))  ;enable GPIO2 and 1:256 Timer0 prescaler
  OPTION
  MOVLW  1
  MOVWF  TMR_COUNT
  RETLW  1

; Program 0a/4 - Cycle through LEDs, two on at a time
program0a_speed_up:
  RLF    TMR_COUNT,F
  BTFSS  TMR_COUNT,PROGRAM0_MAX_TMR_BIT ; If beyond 16 bail out of program0
  GOTO   program0a ; Was 16 or less
  RLF    PROGRAM,F ; Was more than 16, switch to next program
  GOTO   program0b_init
program0a_init:
  CLRF   PROGRAM ; wasn't program2 either - go back to program0
  BSF    PROGRAM,1
  CALL   program0_common_init
program0a:
  ; put 0b100 into W
  MOVLW  (1<<GP2) ; start with GP1,0 on
  GOTO program0_loop

; Program 0b/5 - Cycle through LEDs, zero, 1, 2, 3 and start again
program0b_speed_up:
  RLF    TMR_COUNT,F
  BTFSS  TMR_COUNT,PROGRAM0_MAX_TMR_BIT ; If beyond 16 bail out of program0
  GOTO   program0b ; Was 16 or less
  RLF    PROGRAM,F  ; Was more than 16, switch to next program
  GOTO   select_program
program0b_init:
  CLRF   PROGRAM ; wasn't program2 either - go back to program0
  BSF    PROGRAM,2
  CALL   program0_common_init
program0b:
  ; put 0b100 into W
  MOVLW  7
  MOVWF  PROG0B
program0b_loop:
  MOVF   PROG0B,W
  MOVWF  GPIO
  ; load tmr_count into variable
  MOVF   TMR_COUNT,W
  MOVWF  TMR_COUNT_VAR
; Clear tmr0 and prescaler
  CLRF   TMR0
program0b_delay:
  ; see if GP3 is clear - if so, button has been pressed
  BTFSS  GPIO,3
  GOTO   button_pressed
  BTFSS  TMR0,7 ;wait until TMR0 reaches 128(*256 due to prescaler * 1/4 osc)
  GOTO   program0b_delay
  CLRF   TMR0
  DECFSZ TMR_COUNT_VAR,F
  GOTO   program0b_delay
  ; Bit shift GPIO right one into W
  RRF    PROG0B,F
  CLRW
  IORWF  PROG0B,W
  BTFSS  STATUS,Z
  GOTO   program0b_loop
  GOTO   program0b
 
; Program 1 - Turn all LEDs on
program1:
  ; Just turn all GPIOs on (0)
  CLRW
  MOVWF  GPIO
program1_loop:
  ; test for button press
  BTFSS  GPIO,3
  GOTO   button_pressed_inc
  GOTO   program1_loop

; Program 2 - Put GPIOs on ~50% duty cycle
program2:
  CLRW
  MOVWF  GPIO
  MOVLW  ((1<<GP2)|(1<<GP1)|(1<<GP0))
  MOVWF  GPIO
  BTFSS  GPIO,3
  GOTO   button_pressed_inc
  GOTO   program2

; Program 3 - Dim LEDs in step and then start again
program3:
  CLRF   PROGRAM ; wasn't program2 either - go back to program0
  BSF    PROGRAM,3
  MOVLW  ~((1<<T0CS)|(1<<PSA)|3)  ;enable GPIO2 and 1:32 Timer0 prescaler
  OPTION
  CLRF   PWM
  BSF    PWM,0
  MOVLW  ~0
  MOVWF  TMR_COUNT
  MOVWF  TMR_COUNT_VAR
  CLRF   TMR0
  MOVLW  1
program3_loop:
  BTFSS  TMR0,7
  GOTO   program3_carry_on
  CLRF   TMR0
  DECFSZ TMR_COUNT_VAR,F
  goto   program3_carry_on
  MOVF   TMR_COUNT,W
  MOVWF  TMR_COUNT_VAR
  RLF    PWM,F
program3_carry_on:
  BTFSS  PWM,5 ; do 5 PWM steps
  GOTO   program3_on
  GOTO   program3_loop
program3_on:
  CLRW
  MOVWF  GPIO ; Turn GPIOs on
program3_on_test:
  ; check if button pressed
  BTFSS  GPIO,3
  GOTO   button_pressed_inc
  BTFSS  TMR0,1
  GOTO   program3_on_test
program3_off:
  MOVLW  ((1<<GP2)|(1<<GP1)|(1<<GP0))
  MOVWF  GPIO ; Turn GPIOs off
program3_off_test:
  ; check if button pressed
  BTFSS  GPIO,3
  GOTO   button_pressed_inc
  ; button not pressed - see if time to move on
  BTFSC  PWM,0
  GOTO   program3_loop
  BTFSC  PWM,1
  GOTO   program3_pwm1
  BTFSC  PWM,2
  GOTO   program3_pwm2
  BTFSC  PWM,3
  GOTO   program3_pwm3
  BTFSC  PWM,4
  GOTO   program3_pwm4
  GOTO   program3_loop
program3_pwm1:
  BTFSS  TMR0,1 ;wait until TMR0 reaches 2(*256 due to prescaler * 1/4 osc)
  GOTO   program3_off_test
  GOTO   program3_loop
program3_pwm2:
  BTFSS  TMR0,2 ;wait until TMR0 reaches 4(*256 due to prescaler * 1/4 osc)
  GOTO   program3_off_test
  GOTO   program3_loop
program3_pwm3:
  BTFSS  TMR0,5 ;wait until TMR0 reaches 32(*256 due to prescaler * 1/4 osc)
  GOTO   program3_off_test
  GOTO   program3_loop
program3_pwm4:
  BTFSS  TMR0,6 ;wait until TMR0 reaches 64(*256 due to prescaler * 1/4 osc)
  GOTO   program3_off_test
  GOTO   program3_loop

; Handle button being pressed
button_pressed_inc:
  RLF   PROGRAM,F
button_pressed:
  ; wait until button not pressed anymore
  BTFSS  GPIO,3
  GOTO   button_pressed
  CLRF   TMR0
button_pressed_debounce_loop:
  BTFSS  TMR0,7
  GOTO   button_pressed_debounce_loop
select_program:  
  ; Test if program == 0
  BTFSC  PROGRAM,0 ; chasing leds, one on at once
  GOTO   program0_speed_up
  BTFSC  PROGRAM,1 ; chasing leds, two on at once
  GOTO   program0a_speed_up
  BTFSC  PROGRAM,2 ; chasing leds, two on at once
  GOTO   program0b_speed_up
  BTFSC  PROGRAM,3 ; pwm, getting dimmer then restarting
  GOTO   program3
  BTFSC  PROGRAM,4 ; all leds full on
  GOTO   program1
  BTFSC  PROGRAM,5 ; all leds on, using pwm, 50% duty cycle
  GOTO   program2
  GOTO   program0_init

  END
~~~~