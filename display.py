import os
import pygame
import RPi.GPIO as GPIO
import time
import subprocess
from pygame.locals import *
import searchtext 
import getdata

code_run = time.time()
flag=True



os.putenv('SDL_VIDEODRIVER', 'fbcon') #display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 
os.putenv('SDL_MOUSEDRV', 'TSLIB') #track mouse click on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen') 

pygame.init()
pygame.mouse.set_visible(False)

black = 0,0,0
white = 255,255,255
screen = pygame.display.set_mode((320,240))
my_font=pygame.font.Font(None,15)
data_font=pygame.font.SysFont('Verdana',15)
title_font=pygame.font.Font(None,30)

first_button={'>>>':(310,230)}
#second_button={'NewYork':(70,200),'California':(130,200),'Texas':(190,200),'Florida':(250,200),'Illinois':(130,100),'return':(305,230)}
second_buton={'return':(305,230)}
third_button={'today':(80,20),'history':(240,20),'return':(305,230)}
screen.fill(black)

size = width,height = 320,240
mapimg = pygame.image.load('covid-19-map.png')

mapimg = pygame.transform.scale(mapimg,(290,210))

rect1 = mapimg.get_rect(center=[160,120])


GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down = GPIO.PUD_UP)
def GPIO27_callback(channel):
	print ('Falling detected on 27')
	GPIO.cleanup()
	exit(0)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback,bouncetime = 300)


#pygame.display.flip()

first_page=True
second_page=False
third_page=False
history_img=mapimg
today_img=mapimg
img=mapimg
state=""
stateimg=""
third_flag=0


while time.time()-code_run < 3000 and flag:
	#the first page
	if (first_page):
		stateimg=""
		#show the map image
		#screen.blit(mapimg,rect1)
		
		#show first page buttons
		for button, position in first_button.items():
			text_surface = my_font.render(button, True, white)
			rect = text_surface.get_rect(center= position)
			screen.blit(text_surface,rect)
			
		#hit the first page button
		for event in pygame.event.get():
			screen.fill(black)
			if(event.type is MOUSEBUTTONDOWN):
				pos=pygame.mouse.get_pos()
			elif(event.type is MOUSEBUTTONUP):
				pos=pygame.mouse.get_pos()
				x,y=pos
				a ="touch at: "+str (pos)
				text_surface1 = my_font.render(a, True, white)
				rect = text_surface1.get_rect(center= [x,y])
				screen.blit(text_surface1,rect)
				if y>200:
					if x>260:
						print("start")
						first_page=False
						second_page=True #turn to the next page
		pygame.display.flip()
		
	if (second_page):
		screen.fill(black)
		#hit the second page return
			
		while(stateimg == ""):
			#research
			state,second_page,first_page = searchtext.search(second_page,first_page)
			stateimg = state + ".png"
		if(stateimg != ".png"):
			#today_img = pygame.image.load('covid-19-map.png')
			history_img = pygame.image.load(stateimg)
			second_page=False
			third_page=True
		
	if (third_page):
		screen.fill(black)
		state_surface = my_font.render(state, True, white)
		state_rect = text_surface.get_rect(center=[160,10])
		screen.blit(state_surface,state_rect)
		stateimg=""
		#show third page buttons
		for button, position in third_button.items():
			text_surface = my_font.render(button, True, white)
			rect = text_surface.get_rect(center= position)
			screen.blit(text_surface,rect)
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONDOWN):
				pos=pygame.mouse.get_pos()
			elif(event.type is MOUSEBUTTONUP):
				pos=pygame.mouse.get_pos()
				x,y=pos
				# 'today':(80,40),'history':(240,40),'return':(280,210)
				if y < 60:
					if x < 100 and x > 60:
						#img=pygame.transform.scale(today_img,(250,170))
						td1 = title_font.render("New case today", True, white)
						td2 = title_font.render("death today", True, white)
						td3 = title_font.render("recovered total", True, white)
						
						state_dict=getdata.getdict(state)
						newcase = state_dict['infected_today']
						dd1 = data_font.render(newcase, True, (255,127,0))
						death = state_dict['death_today']
						dd2 = data_font.render(death,True,(128,128,128))
						recover = state_dict['recovered_total']
						dd3 = data_font.render(recover,True,(0,128,0))
						
						third_flag=1
					if x > 220 and x < 260:
						img=pygame.transform.scale(history_img,(300,180))
						third_flag=2
				if y > 200 and x > 260:
					third_page=False
					second_page=True
		if third_flag==1:
			rect = td1.get_rect(center=[160,50])
			screen.blit(td1,rect)
			rect = dd1.get_rect(center=[160,75])
			screen.blit(dd1,rect)
			
			rect = td1.get_rect(center=[160,100])
			screen.blit(td2,rect)
			rect = dd2.get_rect(center=[160,125])
			screen.blit(dd2,rect)
			
			rect = td1.get_rect(center=[160,150])
			screen.blit(td3,rect)
			rect = dd3.get_rect(center=[160,175])
			screen.blit(dd3,rect)
			
		elif third_flag==2:			
			rect2 = img.get_rect(center=[160,120])
			screen.blit(img,rect2)		
		pygame.display.flip()
