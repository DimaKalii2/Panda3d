from panda3d.core import WindowProperties
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
        self.prev_mouse_x = None
        self.prev_mouse_y = None
        self.mouse_sensitivity = 100


    def accept_events(self):
        base.accept('q', self.turn_left)
        base.accept('q' + '-repeat', self.turn_left)
        base.accept('e', self.turn_right)
        base.accept('e' + '-repeat', self.turn_right)
        base.accept( 'w' + '-repeat', self.forward)
        base.accept( 'w' , self.forward)
        base.accept('s', self.back)
        base.accept('s' + '-repeat', self.back)
        base.accept('a', self.left)
        base.accept('a' + '-repeat', self.left)
        base.accept('d', self.right)
        base.accept('d' + '-repeat', self.right)
        base.accept('c', self.changeView)
        base.accept('z', self.up)
        base.accept('z' + '-repeat', self.up)
        base.accept('x', self.down)
        base.accept('x' + '-repeat', self.down)
        base.accept('t', self.changeMode)
        base.accept('mouse1', self.build)
        base.accept('mouse3', self.destroy)
        base.accept('f5', self.land.saveMap)
        base.accept('f6', self.land.loadMap)


        
        

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
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    def forward(self):
        angel = (self.hero.getH()) % 360
        self.move_to(angel)

    def back(self):
        angel = (self.hero.getH() + 180) % 360
        self.move_to(angel)

    def right(self):
        angel = (self.hero.getH() - 90) % 360
        self.move_to(angel)

    def left(self):
        angel = (self.hero.getH() + 90) % 360
        self.move_to(angel)

    def up(self):
        self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        self.hero.setZ(self.hero.getZ() - 1)



    def cameraBind(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        base.camera.setHpr(0, 0, 0)  # Скидаємо орієнтацію камери відносно героя
        self.cameraOn = True

        # Приховуємо курсор миші
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        # Центруємо мишу
        base.win.movePointer(0, int(base.win.getXSize() / 2), int(base.win.getYSize() / 2))
        taskMgr.add(self.mouseUpdate, 'moese-task')

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0],- pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        taskMgr.remove('moese-task')

    def mouseUpdate(self, task):
        if base.mouseWatcherNode.hasMouse():
            mouse_x = base.mouseWatcherNode.getMouseX()
            mouse_y = base.mouseWatcherNode.getMouseY()
            if self.prev_mouse_x is None:
                self.prev_mouse_x = mouse_x
                self.prev_mouse_y = mouse_y
            # Обчислюємо зміну позиції миші
            delta_x = mouse_x - self.prev_mouse_x
            delta_y = mouse_y - self.prev_mouse_y

            # Оновлюємо попередні значення
            self.prev_mouse_x = mouse_x
            self.prev_mouse_y = mouse_y

            # Оновлюємо кут повороту героя по горизонталі
            self.hero.setH(self.hero.getH() - delta_x * self.mouse_sensitivity)

            # Установлюємо кут повороту камери по горизонталі в 0
            base.camera.setH(0)

            # Оновлюємо кут нахилу камери по вертикалі
            camera_p = base.camera.getP() + delta_y * self.mouse_sensitivity
            # Обмежуємо кут нахилу від -45 до 45 градусів
            camera_p = max(-45, min(45, camera_p))
            base.camera.setP(camera_p)

            # Центруємо мишу, щоб уникнути обмежень на краях вікна
            base.win.movePointer(0, int(base.win.getXSize() / 2), int(base.win.getYSize() / 2))
            self.prev_mouse_x = 0
            self.prev_mouse_y = 0

        return task.cont


    



    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)



        