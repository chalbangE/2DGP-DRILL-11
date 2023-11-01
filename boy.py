# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
import game_world
import game_framework
import random

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

# time_out = lambda e : e[0] == 'TIME_OUT'

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 40.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0) # 분당 몇미터?
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) # 초당 몇미터?
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) # 초당 몇픽셀?

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class Run:

    @staticmethod
    def enter(boy, e):
        boy.dir = 1
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if boy.frame >= 4:
            boy.action -= 1
            boy.frame = 0
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if boy.frame >= 3 and boy.action == 0:
            boy.frame = 0
            boy.action = 2

        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.x <= 25 or boy.x >= 1600 - 25:
            boy.dir *= -1
            boy.face_dir *= -1

    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.image.clip_composite_draw(int(boy.frame) * 182, boy.action * 168, 182, 167, 0, 'h', boy.x, boy.y, 100, 100)
        else:
            boy.image.clip_draw(int(boy.frame) * 182, boy.action * 167, 182, 167, boy.x, boy.y, 100, 100)

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Run

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        pass
    def draw(self):
        self.cur_state.draw(self.boy)





class Boy:
    def __init__(self):
        self.x, self.y = 100, random.randint(100, 500)
        self.frame = 0
        self.action = 2
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
