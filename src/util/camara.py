import arcade

class Camara(arcade.Camera2D):
    def __init__(self):
        super().__init__()
        self.left_border = 0
        self.right_border = None
        self.bottom_border = 0
        self.top_border = None
    
    def on_update(self):
        if(self.bottom_left[0] <= 0):
            self.position = [self.width/2, self.position[1]]
        
        if(self.bottom_right[0] >= self.right_border):
            self.position = [self.right_border - self.width/2, self.position[1]]
        
        if(self.top_right[1] >= self.top_border):
            self.position = [self.position[0], self.top_border - self.height/2]
        
        if(self.bottom_left[1] <= 0):
            self.position = [self.position[0], self.height/2]