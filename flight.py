import math
import bpnn

class Player() :
	# x = 0.0
	# y = 0.0
	# dx = 0.0
	# dy = 0.0
	# ddr = 0.0
	# phi = 0.0
	# dphi= 0.0
	# ddphi= 0.0
	
	def __init__(self,x_,y_,dx_,dy_,phi_,dphi_) :
		self.x=x_
		self.y=y_
		self.dx=dx_
		self.dy=dy_
		self.phi=phi_
		self.dphi=dphi_
		self.ddphi = 0.0
		self.ddr = 0.0
		self.brain = bpnn.NN(4,4,2)

		
	def think(self) :
		#for now use origin as target
		output = self.brain()
		
		self.ddphi = 0.0#rotate thrusters
		self.ddr = 0.1 # lateral 
	
	def tick(self,dt) :
		self.x+=self.dx*dt
		self.y+=self.dy*dt
		self.phi+=self.dphi*dt
		self.dphi+=self.ddphi*dt
		# print math.cos(self.phi)*self.ddr*dt
		self.dx+=math.cos(self.phi)*self.ddr*dt
		self.dy+=math.sin(self.phi)*self.ddr*dt
		if self.phi>math.pi :
			self.phi=self.phi - 2*math.pi
		
		
		
new_player = Player(0.0,0.0, 0.0,0.0, 0.0,0.1)

delta_t = 1.0

while(True) :
	new_player.think()
	new_player.tick(delta_t)
	print new_player.dx,new_player.dy