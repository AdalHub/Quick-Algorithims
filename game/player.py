
class player:
    def __init__(self, health=100, wealth= 0, position=(0,0)):
        self.health = health
        self.wealth= wealth
        self.position = position
    
    def moves(self, direction:tuple):
        x,y= self.position
        new_x, new_y= x+direction[0], y+direction[1]
        self.position=(new_x,new_y)
    def recieves_damage(self, damage:int):
        current_health = self.health - damage
        if current_health < 1:
            return -1
        self.health= current_health
    
    def recieves_wealth(self, cash:int):
        self.wealth+= cash
    
