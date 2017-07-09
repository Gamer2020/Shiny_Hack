	.org 0x0806AF90
	ldrh    r1,[r4]
	ldrh    r0,[r4,2h]
	lsl     r0,r0,10h
	add     r1,r1,r0
	ldr     r0, =shiny_hack_main|1
	mov     r14,r15
	bx      r0
	.pool
