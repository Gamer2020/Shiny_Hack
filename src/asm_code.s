.text
.align 2
.thumb
.thumb_func

shiny_hack_main:
	lsr r0, r4, #0x18
	cmp r0, #0x3
	bne return
	ldr r0, .SHINY_COUNTER
	ldrb r0, [r0]
	cmp r0, #0x0
	bne shiny_hack

return:
	bx lr

shiny_hack:
	push {r2-r5, lr}
	sub r3, r0, #0x1
	ldr r0, .SHINY_COUNTER
	strb r3, [r0]
	ldrb r4, [r0, #0x1]
	cmp r4, #0x0
	bne is_trainer
	add r4, r1, #0x0

no_trainer:
	ldr r2, .RANDOM
	bl branch_r2
	mov r3, #0x7
	and r0, r3
	add r3, r0, #0x0
	ldr r2, .RANDOM
	bl branch_r2
	lsl r5, r0, #0x10
	orr r5, r0
	eor r5, r3
	eor r5, r4
	push {r4-r6}
	lsr r1, r5, #0x10
	lsl r0, r5, #0x10
	mvn r3, r3
	lsr r3, r3, #0x10
	ldr r4, .RND_MULTIPLIER
	ldr r5, .RND_INCREMENT

rnd_loop:
	add r6, r0, #0x0
	mul r6, r4
	add r6, r5
	lsr r2, r6, #0x10
	cmp r2, r1
	beq rnd_end
	add r0, #0x1
	sub r3, #0x1
	cmp r3, #0x0
	bne rnd_loop
	b not_found
	
rnd_end:
	ldr r2, .RND_ADDRESS
	str r6, [r2]
	pop {r1, r5-r6}
	str r5, [r7]

shiny_ret:
	pop {r2-r5, pc}

not_found:
	pop {r4-r6}
	b no_trainer

is_trainer:
	mov r5, #0x1
	lsl r5, r3
	and r4, r5
	cmp r4, #0x0
	beq trainer_ret
	ldr r1, [r7]

trainer_ret:
	b shiny_ret

branch_r2:
	bx r2
	
.align 2
.RND_MULTIPLIER:
	.word 0x41C64E6D
.RND_INCREMENT:
	.word 0x00006073
.RND_ADDRESS:
	.word 0x03005D80
.SHINY_COUNTER:
	.word 0x020375DE
.RANDOM:
	.word 0x0806F5CC|1
	