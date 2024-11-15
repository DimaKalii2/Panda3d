class Hero():
    def __init__(self, pos, lend):
        self.land = lend
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 1)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
        self.mode = True

    def accept_events(self):
        base.accept('q', self.turn_left)
        base.accept('q' + '-repeat', self.turn_left)
        base.accept('e', self.turn_right)
        base.accept('e' + '-repeat', self.turn_right)
        base.accept( 'w' + '-repeat', self.forward)
        base.accept( 'w' , self.forward)
        base.accept('c', self.changeView)
        base.accept('z', self.up)
        base.accept('z' + '-repeat', self.up)
        base.accept('x', self.down)
        base.accept('x' + '-repeat', self.down)
        base.accept('t', self.changeMode)
        
        

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turn_left(self):
        self.hero.setH((self.hero.getH()+5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH()-5) % 360)

    def jast_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighesEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1 
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True



    def  move_to(self, angle):
        if self.mode:
            self.jast_move(angle)
        else:
            self.try_move(angle)

    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from
    
    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    def forward(self):
        angel =(self.hero.getH()) % 360
        self.move_to(angel)

    def up(self):
        self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        self.hero.setZ(self.hero.getZ() - 1)



    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseinterfaceNode.setPos(-pos[0],- pos[1], -pos[2] - 3)
        base.camera.reperentTo(render)
        base.enableMouse()
        self.cameraOn = False

                
        


        