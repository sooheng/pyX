/**
79h->7eh 时间显示缓冲区
-62h
**/	
debug_vaule equ 55h
/**公共变量 **/
old_run_func_vaule equ 68h;旧的功能键值
run_func_vaule equ 69h;功能键值
func_vaule equ 6ah;键值
kw_vaule equ 6bh;原始键值
/** 循环标志 **/
flag_miaobiao equ 66h;秒表的计数器标志
flag_flash equ 67h;闪烁的计数器标志
flag_kw_position equ 6ch;键盘位置的计数器标志
flag_kw equ 6dh;键盘的计数器标志
flag_delay equ 6eh;延迟的计数器标志
flag_time  equ 6fh;时间的计数器标志
flag_dig equ 70h;数码管显示标志
flag_disp  equ 71h;显示标志
/****/
mb_10ms equ 63h;秒表的10毫秒
mb_sec	equ 64h;秒表的秒
mb_min equ	65h;秒表的分
nz_sec  equ 72h;闹钟的秒
nz_min  equ 73h;闹钟的分
nz_hour  equ 74h;闹钟的时
sec  equ 75h;时钟的秒
min  equ 76h;时钟的分
hour  equ 77h;时钟的时
/** 形式参数 **/
arg_timer equ 78h;时间参数
/** 位标志 **/
bit_led equ 20h.0;led的开关
bit_anxia equ 20h.1;是否按下的位
bit_kw_chuli equ 20h.2;是否键盘处理的位
bit_keyboard equ 20h.3;是否键盘输入的位
bit_xiaodou equ 20h.4;是否已经消抖的位
bit_time equ 20h.5;时钟是否运行
bit_vol equ 20h.6;扬声器是否响一秒
bit_flash equ 20h.7;输入位的数码管是否闪烁
bit_flash_status equ 21h.0;闪烁的状态是亮或暗
bit_miaobiao equ 21h.1;秒表是否运行
/** 常量 **/
arg_display_buffer equ 79h
flag_miaobiao_number equ 2
flag_flash_number equ 125
flag_kw_freq equ 4
flag_delay_number equ 250
flag_dig_number equ 6
flag_disp_freq equ 1
flag_time_freq equ 250
time0_high equ 0f1h
time0_low equ 099h;4ms定时器
/** 中断入口 **/
org 0000h
sjmp main
org 000bh
jmp time0 
org 0050h
main:
/** 8255初始化 **/
  	mov dptr,#0ff23h
  	mov a,#89h
  	movx @dptr,a
/** 定时器初始化 **/
  mov tmod,#01h
  mov th0,#time0_high
  mov tl0,#time0_low
  setb ea
  setb et0
  setb tr0
/** 循环标志初始值 **/
  mov flag_miaobiao,#flag_miaobiao_number
  mov flag_flash,#flag_flash_number
  mov flag_kw,#flag_kw_freq
  mov flag_dig,#flag_dig_number;数码管
  mov flag_disp,#flag_disp_freq;显示标志
  mov flag_time,#flag_time_freq ;时间的计数器标志
  mov flag_delay,#flag_delay_number
  mov flag_kw_position,#6
/** 变量默认值 **/
  mov mb_10ms,#0
  mov mb_sec,#0
  mov mb_min,#0
  mov nz_sec,#0;闹钟秒
  mov nz_min,#0;闹钟分
  mov nz_hour,#0;闹钟时  
  mov sec,#0;秒
  mov min,#0;分
  mov hour,#0;时
  mov run_func_vaule,#0ah
/* 位变量默认值 */
  setb bit_keyboard
  setb bit_time
/**/  
do:
  call time_count
  call miaobiao
  call naozhong
  call dispath
  call function
  call time2buff
  call display
  sjmp do


function:
  mov a,run_func_vaule
  jnz next
  ret
  next:

  ;显示时间键
  cjne a,#0ah,func_skip1 
  mov flag_kw_position,#6
  mov arg_timer,#sec 
  ajmp function_exit
  func_skip1:

  ;闹钟键
  cjne a,#0bh,func_skip2 
  mov flag_kw_position,#6  
  mov arg_timer,#nz_sec 
  ajmp function_exit
  func_skip2:

  ;暂停
  cjne a,#0ch,func_skip3
  cpl bit_time  
  ajmp function_exit
  func_skip3:

  ;闪烁设置键
  cjne a,#0dh,func_skip4
  cpl bit_flash
  clr bit_flash_status
  ajmp function_exit
  func_skip4:

  ;正向计时器
  cjne a,#0eh,func_skip5
  mov mb_10ms,#0
  mov mb_sec,#0
  mov mb_min,#0
  mov arg_timer,#mb_10ms
  clr bit_flash
  clr bit_flash_status 
  ajmp function_exit
  func_skip5:

  ;计时器开关
  cjne a,#0fh,func_skip6
  cpl bit_miaobiao
  ajmp function_exit
  func_skip6:

  function_exit:
  mov old_run_func_vaule,run_func_vaule
  mov run_func_vaule,#00h  
  ret


/**
定时器中断time0
**/
time0:
	clr et0
	mov th0,#time0_high
	mov tl0,#time0_low

	dec flag_disp
	dec flag_kw

	jnb bit_time,t_skip1
	dec flag_time
	t_skip1:

	jnb bit_miaobiao,t_skip2
	dec flag_miaobiao
	t_skip2:

	jnb bit_flash,t_skip3
	dec flag_flash
	t_skip3:

	jnb bit_led,t_skip4
	dec flag_delay
	t_skip4:
	
	jnb bit_vol,t_skip5
	dec flag_delay
	t_skip5:

	setb et0
	reti


/**led aj_chuli flash**/
dispath:

	jnb bit_led,skip1
	clr p1.0
	mov a,flag_delay
	jnz skip1
	setb p1.0
	mov flag_delay,#flag_delay_number 
	clr bit_led
	skip1:

	jnb bit_kw_chuli,skip2
	call kw_judg
	jb bit_anxia,skip2
	call kw_chuli
	skip2:

	jnb bit_keyboard,skip3
	call keyboard
	skip3:
	
	jnb bit_vol,skip4
	clr p1.1
	mov a,flag_delay
	jnz skip4
	setb p1.1
	mov flag_delay,#flag_delay_number 
	clr bit_vol
	skip4:

	jnb bit_flash,skip5	
	mov a,flag_flash
	jnz skip5	
	mov flag_flash,#flag_flash_number 
	cpl bit_flash_status	   ;0.5s定时翻转状态的开关
	skip5:

	ret


/**
消抖
**/
keyboard:
mov a,flag_kw
jnz kw_exit
mov flag_kw,#flag_kw_freq
  jb bit_xiaodou,kw_xiaodou
  call kw_judg
  jnb bit_anxia,kw_exit
  setb bit_xiaodou
  ajmp kw_exit
  kw_xiaodou:
  clr bit_xiaodou
  call kw_judg
  jnb bit_anxia,kw_exit
  clr bit_keyboard
  setb bit_kw_chuli
kw_exit:  
  ret
/**
判断有键？
获得原始键值kw_vaule
**/		   
kw_judg:
  	mov r4,#8
	mov r5,#11111110b
	kw_judg_loop:
	mov a,r5      	
	mov dptr ,#0ff20h
	movx @dptr,a		   ;A口输出
	 
	mov dptr ,#0ff22h	   
	movx a,@dptr		   ;C口输入kw

	anl a,#0fh
	cjne a,#0fh,you_anjian
	mov a,r5
	rl a
	mov r5,a
  djnz r4,kw_judg_loop
    clr bit_anxia
	ajmp kw_judg_exit
  you_anjian:					
	setb bit_anxia
	cjne a,#13,is_14
	mov a,#0
	ajmp goto
	is_14:
	mov a,#8
	goto:
	add a,r4
	mov kw_vaule,a
	kw_judg_exit:
	ret
/**
键值处理
原始键值kw_vaule翻译成func_vaule(0-9)或者run_func_vaule(a-f)
**/
kw_table: 
     db 0ffh,0dh,0ch,0eh,03h,0fh,02h,00h,01h,0bh,0ah,06h,09h,05h,08h,04h,07h
kw_chuli:
	setb bit_keyboard
	clr bit_kw_chuli
	setb bit_led

	mov a,kw_vaule		      
    mov dptr,#kw_table
	movc a,@a+dptr
    mov func_vaule,a

	subb a,#10
	jnc kw_chuli_exit
	jnb bit_flash,kw_chuli_exit2

	mov a,#79h
	dec flag_kw_position
	add a,flag_kw_position
	mov r1,a
	mov @r1,func_vaule
	call buff2time

	mov a,flag_kw_position
	jnz kw_chuli_exit2
	mov flag_kw_position,#6

   kw_chuli_exit2:
	ret

   kw_chuli_exit:
	mov a,func_vaule
	mov run_func_vaule,a				
	ret

/**
显示
**/
table: 					   ;0-f共阳数码表
     db 0c0h,0f9h,0a4h,0b0h,99h,92h,82h,0f8h,80h,90h,88h,83h,0c6h,0a1h,86h,8eh
display:
	   mov a,flag_disp
	   jnz display_exit
	   mov flag_disp,#flag_disp_freq
	   dec flag_dig

	   mov a,flag_dig
	   add a,#1
	   cjne a,flag_kw_position,display_next
	   jb bit_flash_status,display_skip;0,next;1,skip

	display_next:
	   mov a,#arg_display_buffer	   
	   add a,flag_dig
	   mov r0,a	 ;显示缓冲区地址

	   mov a,#01h
	   mov r3,flag_dig
	   rool_loop:
	   RL a
	   djnz r3,rool_loop
       mov r2, a  ;6个数码管的选择位

	  mov a,r2 
      cpl a
      mov dptr ,#0ff20h
	  movx @dptr,a		   ;A口输出r2的取反,数码管6选1

	  mov a,@r0		      
      mov dptr,#table
	  movc a,@a+dptr	   ;查表取出79h-7eh相对应的字形

      mov dptr ,#0ff21h	   
	  movx @dptr,a		   ;B口输出字形
	  
	  call delay

	  mov a,#0ffh
	  mov dptr ,#0ff21h	   
	  movx @dptr,a		   ;B口输出全灭字形   

	display_skip:
	  mov a,flag_dig
	  jnz display_exit
	  mov flag_dig,#flag_dig_number
display_exit:
	  ret

/**
秒表
**/
miaobiao:
	jnb bit_miaobiao,mb_exit
	mov a,flag_miaobiao
	jnz mb_exit

	mov flag_miaobiao,#flag_miaobiao_number
	inc mb_10ms

	mov a,#99
	subb a,mb_10ms
	jnc mb_exit
	mov mb_10ms,#0
	inc mb_sec

	mov a,#59
	subb a,mb_sec
	jnc mb_exit
	mov mb_sec,#0
	inc mb_min

	mov a,#59
	subb a,mb_min
	jnc mb_exit	
	mov mb_min,#0
	mb_exit:
	ret

/**
计时
**/
time_count:
	jnb bit_time,time_exit

	mov a,flag_time
	jnz time_exit
		 
	mov flag_time,#flag_time_freq
	inc sec
	
	mov a,#59
	subb a,sec
	jnc time_exit
	mov sec,#0
	inc min

	mov a,#59
	subb a,min
	jnc time_exit
	mov min,#0
	inc hour

	mov a,#23
	subb a,hour
	jnc time_exit	
	mov hour,#0
  time_exit:
	ret
/**
闹钟
**/	 
naozhong:
	mov r0,#hour
	mov r1,#nz_hour
	mov r2,#3
  naozhong_loop:
	mov a,@r0
	subb a,@r1
	jnz naozhong_exit
	dec r0
	dec r1
	djnz r2,naozhong_loop
	call naozhong_event
  naozhong_exit:
    ret
 naozhong_event:
	setb bit_vol	
	ret

/****
***辅助函数***
****/
;显示格式6字节变成时间变量3字节
limit:
       mov a,r2
       cjne	a,#3,b2t_skip1
        mov a,#59
        subb a,@r0
        jnc b2t_exit
        mov @r0,#59
       b2t_skip1:
       mov a,r2
       cjne	a,#2,b2t_skip2
         mov a,#59
         subb a,@r0
         jnc b2t_exit
         mov @r0,#59
       b2t_skip2:
       mov a,r2
       cjne	a,#1,b2t_skip3
        mov a,#23
        subb a,@r0
        jnc b2t_exit
        mov @r0,#23
       b2t_skip3:
       b2t_exit:
       ret           
buff2time:
	mov r0,arg_timer
	mov r1,#arg_display_buffer
	mov r2,#3
	buff2time_loop:
		   mov a,@r1
		   mov r3,a
		   inc r1
		   mov a,@r1
		   mov b,#10
		   mul ab

		   add a,r3
		   mov @r0,a
		   ;限制
           call limit
		   ;
		   inc r0
		   inc r1
		   djnz r2,buff2time_loop
	ret

;时间变量3字节变成显示格式6字节
time2buff:
	mov r0,arg_timer
	mov r1,#arg_display_buffer
	mov r2,#3
	time2buff_loop:
		mov b,#10	;除数->b
		mov a,@r0	;
		div ab
		mov @r1,b	;b是商
		inc r1
		mov @r1,a	;a是余数
		inc r0
		inc r1
		djnz r2,time2buff_loop
	ret
	
;延时
delay:
	  mov r7,#02h
	  de1:  mov r6,#0ffh
	  de2:  djnz r6,de2
        	djnz r7,de1
        	ret

;debug
debug_dispaly:	  
	  mov a,#01h 
      cpl a
      mov dptr ,#0ff20h
	  movx @dptr,a		   ;A口输出r2的取反,数码管6选1
	  mov a,debug_vaule		      
      mov dptr,#table
	  movc a,@a+dptr	   ;查表取出79h-7eh相对应的字形
      mov dptr ,#0ff21h	   
	  movx @dptr,a
	  ret
end


