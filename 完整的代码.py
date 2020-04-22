from arcade import*
import pygame
pygame.init()
touch = pygame.mixer.Sound("撞击.wav")  # 撞击音效
touch2 = pygame.mixer.Sound("背景.wav")  # 背景音效
touch3 = pygame.mixer.Sound("结束.wav")  # 结束音效
touch2.play(1000)
# 设置窗体宽与高
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
# 设置窗体标题
SCREEN_TITLE = "冒险小车"


class Road(Sprite):
    def __init__(self, image):
        super().__init__(image)
        # 车道
        self.center_x = SCREEN_WIDTH//2
        self.center_y = SCREEN_HEIGHT//2
        # 设置车道的改变值
        self.change_y = 0

    def update(self):
        super().update()
        if self.center_y <= SCREEN_HEIGHT//2 - SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT//2 + SCREEN_HEIGHT

    def setSpeed(self, speed):
        self.change_y = - speed


class SmallCar(Sprite):
    def __init__(self, image):
        super().__init__(image)
        # 小车图片
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 100


class Cart(Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.center_y = random.randint(
            SCREEN_HEIGHT, SCREEN_HEIGHT + SCREEN_HEIGHT // 2)
        # 设置大车的改变值
        self.change_y = -10


class GameOver(Sprite):
    def __init__(self, image):
        super().__init__(image)
        # 小车图片
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2


class StatusBar():
    def __init__(self):
        self.distance = 0
        self.hp = 3
        self.speed = float(1.0)

    def draw_bar(self):
            draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15, SCREEN_WIDTH, 30, color.WHITE
            )

    def draw_sp(self):
        pos_x = 500
        pos_y = SCREEN_HEIGHT - 20

        draw_text(f"速度: {float(self.speed)} m/s", pos_x, pos_y,
                  color.BLACK, font_name={"simhei", "PingFang"})

    def draw_distance(self):
        pos_x = 10
        pos_y = SCREEN_HEIGHT - 20
        draw_text(f"路程: {self.distance} m", pos_x, pos_y,
                  color.BLACK, font_name={"simhei", "PingFang"})

    def draw_hp(self):
        # 提示字
        pos_x = SCREEN_WIDTH // 2 - 50
        pos_y = SCREEN_HEIGHT - 20
        draw_text("血量:", pos_x, pos_y, color.BLACK,
                  font_name={"simhei", "PingFang"})
        # 心
        hearts = SpriteList()
        for i in range(self.hp):
            heart = Sprite("images/血量.png")
            heart.center_x = pos_x + 50 + heart.width * i
            heart.center_y = pos_y + 5
            hearts.append(heart)
        hearts.draw()


class MyCar(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # 窗体初始化
        self.setup()

    def setup(self):
        # 车道
        self.road1 = Road("images/车道.png")
        self.road2 = Road("images/车道.png")
        self.road2.center_y = SCREEN_HEIGHT // 2 + SCREEN_HEIGHT
        # 小车
        self.small_car = SmallCar("images/小车3.png")
        # 大车
        self.carts = SpriteList()
        self.create_carts()
        # 程序运行时间
        self.total_time = 0
        # 初始速度
        self.speed = 1
        # 上一次计时
        self.last_time = 0
        # 状态栏
        self.status_bar = StatusBar()
        # 游戏状态
        self.game_status = True
        # 游戏结束界面
        self.gameover = GameOver("images/gameover.png")

    def on_draw(self):
        start_render()
        # 绘制车道
        self.road1.draw()
        self.road2.draw()
        # 绘制小车
        self.small_car.draw()
        # 绘制大车
        for cart in self.carts:
            cart.draw()
        # 绘制状态栏
        self.status_bar.draw_bar()
        self.status_bar.draw_distance()
        self.status_bar.draw_hp()
        self.status_bar.draw_sp()   
        self.speed = self.total_time  // 5
        self.road1.setSpeed(self.speed)
        self.road2.setSpeed(self.speed)
        self.status_bar.speed = self.speed
        # 绘制游戏结束后界面
        if not self.game_status:
            self.gameover.draw()

    def on_update(self, delta_time: float):
        if self.game_status:
            self.small_car.update()
            # 移动车道
            self.road1.update()
            self.road2.update()
            # 移动大车
            for cart in self.carts:
                cart.update()
                if cart.top < 0:
                    cart.kill()
            # 程序运行总时间
            self.total_time += delta_time
            if int(self.last_time) != int(self.total_time) and int(self.total_time) % 6 == 0:
                self.create_carts()
                self.last_time = self.total_time
            # 状态栏
            self.status_bar.distance = int(self.total_time * 4)

            # 碰撞检测
            hit_list = check_for_collision_with_list(
                self.small_car, self.carts)
            if hit_list:
                for hit in hit_list:
                    hit.kill()
                    self.status_bar.hp -= 1
                    if self.status_bar.hp > 0:
                        touch.play()
            # 判断游戏状态
            self.judge_game_status()

    def on_key_release(self, symbol: int, modifiers: int):
        # 左移
        if symbol == key.LEFT and self.small_car.center_x >= SCREEN_WIDTH // 2:
            self.small_car.center_x -= 200
        # 右移
        elif symbol == key.RIGHT and self.small_car.center_x <= SCREEN_WIDTH // 2:
            self.small_car.center_x += 200
        # 上移
        elif symbol == key.UP and self.small_car.top <= SCREEN_HEIGHT:
            self.small_car.center_y += 50
        # 下移
        elif symbol == key.DOWN and self.small_car.bottom >= 0:
            self.small_car.center_y -= 50

    def create_carts(self):
        import random
        cart_list = ("images/大车1.png", "images/大车2.png", "images/大车3.png")
        num = 2
        x = random.sample(
            [SCREEN_WIDTH // 2 - 200, SCREEN_WIDTH // 2, SCREEN_WIDTH // 2 + 200], 2)
        for i in range(num):
            cart = Cart(random.choice(cart_list))
            cart.center_x = x[i]
            self.carts.append(cart)

    def judge_game_status(self):
        if self.status_bar.hp <= 0:
            self.game_status = False
            touch3.play()

if __name__ == '__main__':
    game = MyCar(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    run()
