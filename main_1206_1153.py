import time, random, datetime
import pyscreenshot as ImageGrab
import pyautogui as auto

pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True

L = 'left'
R = 'right'

BLIZZARD = 3.5
ICE_STRIKE = 1.0

SKILL_SAFETY_INTERVAL = 120
MACRO_DELAY = 3.5

HP_SAFETY_INTERVAL = 5.0
HP_RATE, MP_RATE = 0.6, 0.6
HP_CRITICAL = 0.7
SAFETY_MARGIN = HP_RATE/10

MP_MAX = 16993
MP_MIN = 200
MP_PER_SKILL = 2900 * 2
MP_CRITICAL = (MP_MIN + MP_PER_SKILL) / MP_MAX

class Map:
    previous_char_position = (0, 0, 0) #(x, y, direction)

    def __init__(self, geography, grind_edge_percentage, grind_attack, grind_move):
        self.geography = geography
        self.grind_edge_percentage = grind_edge_percentage
        self.grind_attack = grind_attack
        self.grind_move = grind_move

    def is_edge():
        # search for the char location from the previous position/direction
        # find which geographic component is it



def grind(start_dir=L, map, gchar, central_clock):
    current_direction = start_dir
    # check if it's en edge
    if map.is_edge():
        current_direction = other(current_direction)
    # check if need to auto skill
    if central_clock.check_auto_skill():
        gchar.auto_skill()
    # check if need to loot mesos
    if central_clock.check_auto_meso():
        map.auto_meso(gchar.key('jump'))
    # else, attack and move
    else:
        map.attack(gchar.key('grind_attack'), gchar.attack_delay)
        map.move(direction, gchar.key('tele'))


def c():
    maple_x, maple_y = 20, 600
    pause(0.1)
    auto.click(x=maple_x, y=maple_y)
    pause(0.1)
    auto.click(x=maple_x, y=maple_y)
    pause(0.1)
    auto.click(x=maple_x, y=maple_y)


def other(direction):
    if direction == L:
        return R
    elif direction == R:
        return L

def random_direction():
    return random.choice([L, R])

def get_time():
    sec = time.gmtime().tm_sec
    mini = time.gmtime().tm_min
    hour = time.gmtime().tm_hour
    return hour * 60 * 60 + mini * 60 + sec

def pause(sec):
    time.sleep(abs(sec))

def get_pixel(x, y):
    im = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    return im.load()[0,0]

def hp_safe(pot_rate):
    height = 608
    hp_range = (220, 325)
    critical_perc = HP_CRITICAL
    critical_pixel = int((hp_range[1] - hp_range[0] + 1) * critical_perc) + hp_range[0]
    R = get_pixel(critical_pixel, height)[0]
    return R > 200

def mp_safe(pot_rate):
    height = 608
    mp_range = (328, 433)
    critical_perc = MP_CRITICAL
    critical_pixel = int((mp_range[1] - mp_range[0] + 1) * critical_perc) + mp_range[0]
    R = get_pixel(critical_pixel, height)[0]
    return R < 100

def trace_hp(sec):
    init = get_time()
    while get_time() - init < sec:
        pause(0.5)


def auto_pot():
    hp_pot_rate, mp_pot_rate,  = HP_RATE, MP_RATE
    if not hp_safe(hp_rate) or not mp_safe(mp_rate):
        auto.press('shift')

def auto_hp():
    hp_rate, mp_rate = HP_RATE, MP_RATE
    if not hp_safe(hp_rate) or not mp_safe(mp_rate):
        auto.press('shift')

hp_clock = None
def hp(f):
    def g(*args):
        global hp_clock
        if hp_clock is not None:
            #print(hp_clock)
            elapsed = datetime.datetime.now() - hp_clock
            if elapsed.seconds >= 30:
                c()
            if elapsed.seconds >= HP_SAFETY_INTERVAL:
                #print(elapsed, elapsed.seconds, 'Auto HP')
                auto_hp()
                hp_clock = datetime.datetime.now()
        else:
            hp_clock = datetime.datetime.now()
        return f(*args)
    return g

def auto_skill():
    auto_hp()
    auto.press('ctrl')
    if MACRO_DELAY > 1:
        for i in range(int(MACRO_DELAY)):
            auto_hp()
            pause(0.5)
        pause(MACRO_DELAY - int(MACRO_DELAY))
    else:
        pause(MACRO_DELAY)

def skill():
    global skill_clock
    if skill_clock is not None:
        #print(hp_clock)
        elapsed = datetime.datetime.now() - skill_clock
        if elapsed.seconds >= 30:
            c()
        if elapsed.seconds >= SKILL_SAFETY_INTERVAL:
            #print(elapsed, elapsed.seconds, 'Auto HP')
            auto_skill()
            skill_clock = datetime.datetime.now()
    else:
        auto_skill()
        skill_clock = datetime.datetime.now()


skill_clock = None
def skill_dec(f):
    def g(*args):
        global skill_clock
        if skill_clock is not None:
            #print(hp_clock)
            elapsed = datetime.datetime.now() - skill_clock
            if elapsed.seconds >= 30:
                c()
            if elapsed.seconds >= SKILL_SAFETY_INTERVAL:
                #print(elapsed, elapsed.seconds, 'Auto HP')
                auto_skill()
                skill_clock = datetime.datetime.now()
        else:
            auto_skill()
            skill_clock = datetime.datetime.now()
        return f(*args)
    return g

@hp
def tele(direction):
    auto.keyDown(direction)
    auto.keyDown(' ')
    pause(0.1)
    auto.keyUp(' ')
    auto.keyUp(direction)

@hp
def walk(direction, msec):
    auto.keyDown(direction)
    pause(mmsec)
    auto.keyUp(direction)

def random_walk():
    if prob(0.5):
        walk(random_direction(), abs(random.gauss(0.2, 0.2)))

def horizontal_1(direction):
    attack_delay = ICE_STRIKE
    combo(1, attack_delay)
    times = 5
    mean_times = (times - 1) / 2
    for i in range(times):
        deviation = abs(i - mean_times)
        dev_perc = deviation / mean_times
        cent_perc = 1 - dev_perc
        #print(i, deviation, dev_perc, dev_perc ** 0.5, cent_perc);
        tele_move(direction, 1 + 2 * dev_perc)
        walk(other(direction), 0.1)
        combo(int(4 + 2 * cent_perc**2), attack_delay)
        tele(direction)
        walk(other(direction), 0.1)
        combo(int(3 + 2 * cent_perc**2), attack_delay)

def is_edge_0(direction):
    # GS2
    mmap = ImageGrab.grab(bbox=(15, 122, 117, 123)).load()
    # GS7
    #mmap = ImageGrab.grab(bbox=(15, 118, 118, 119)).load()
    edge_L1, edge_L2 = mmap[4,0], mmap[9,0]
    edge_R1, edge_R2 = mmap[98, 0], mmap[93, 0]
    def is_yellow(rgba):
        return rgba[0] > 200 and rgba[1] > 200
    if direction == L:
        return is_yellow(edge_L1) or is_yellow(edge_L2)
    else:
        return is_yellow(edge_R1) or is_yellow(edge_R2)

@skill_dec
def horizontal_2(direction):
    attack_delay = ICE_STRIKE
    combo(1, attack_delay)
    while True:
        c();
        tele_move(direction, random.choice([1,2]))
        if is_edge(direction):
            print(direction, 'Edge detected')
            tele_move(other(direction), 1)
            return
        random_walk()
        #GS2:
        combo(random.choice([2,3]), attack_delay)
        # GS7:
        #combo(random.choice([3,4]), attack_delay)
        random_walk()
        if prob(0.2):
            tele_move(other(direction), 1)
            random_walk()
            combo(random.choice([1,2]), attack_delay)
            random_walk()

@skill_dec
def horizontal_3(direction):
    for i in range(5):
        if i <= 1 or i >= 5:
            safe_combo(random.choice([1,2]), attack_delay)
            tele_move(direction, 2)
        else:
            safe_combo(2, attack_delay)
            tele_move(direction, random.choice([2,3]))


def attack(times=1):
    for i in range(times):
        auto.keyDown('a')
        auto.keyUp('a')

def grind(minute, init_skill=True):
    sec = minute * 60
    init = get_time()
    global skill_clock
    if init_skill:
        skill_clock = None
    else:
        skill_clock = datetime.datetime.now()
    direction = L

    c()
    skill()
    while get_time() - init < sec:
        print('Remaining: ', round((sec-(get_time() - init))/60), 'min')
        horizontal_4(direction, edge_fn=edge_ueii, combo_fn=combo_ueii, move_fn=move_ueii, edge_behavior=None)
        direction = other(direction)

def prob(p):
    return random.uniform(0,1) < p

def combo(times, attack_delay):
    auto.keyDown('a')
    pause( (times-1) * attack_delay)
    auto.keyUp('a')


def combo_test(times, attack_delay):
    auto.keyDown('a')
    for i in range(times-1):
        print(i+1)
        pause(attack_delay)
    pause(0.1)
    print(times)
    auto.keyUp('a')


def safe_combo(num_attack, attack_delay):
    auto_hp()
    safe_delay = 0.6
    safety_check_times = int(attack_delay / safe_delay)
    too_slow = 0.5
    for i in range(num_attack):
        print(i, 'th attack')
        for i in range(safety_check_times):
            auto.keyDown('a')
            pause(safe_delay / 2 * too_slow)
            auto.keyUp('a')
            pause(safe_delay / 2 * too_slow)
            auto_hp()


def tele_move(direction, steps):
    step_size = 0.55
    auto.keyDown(direction)
    pause(0.2)
    auto.keyDown(' ')
    pause(step_size * steps)
    auto.keyUp(' ')
    auto.keyUp(direction)

def safe_tele(direction, steps):
    for i in range(steps):
        auto_hp()
        tele_move(direction, 1)
    auto_hp()


def test_edge(sec):
    for i in range(sec*2):
        print('L:',is_edge(L),'R',is_edge(R))
        pause(0.5)

class PlayerNotFound(Exception):
    def __init__(self):
        x1, y1, x2, y2 = 0, 0, 1024, 768
        self.mmap = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    def __str__(self):
        return repr(self.mmap)
    def show(self):
        self.mmap.show()


def rel_pos(mmap_coord, reference_r):
    x1, y1, x2, y2 = mmap_coord[0], mmap_coord[1], mmap_coord[2], mmap_coord[3]
    is_player = lambda current_r: current_r == 255
    mmap = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    current_rs = [mmap.load()[i,0][0] for i in range(x2-x1)]
    for j in range(len(current_rs)):
        if is_player(current_rs[j]):
            return j/len(current_rs)
    raise PlayerNotFound()

mmap_coord_ueii = (8, 154, 133, 155)
reference_r_ueii = [17, 17, 40, 10, 48, 28, 102, 51, 51, 66, 82, 102, 102, 102, 85,\
170, 204, 204, 204, 153, 187, 170, 170, 187, 102, 68, 102, 85, 187, 102, 68,\
34, 51, 170, 153, 85, 51, 51, 68, 136, 51, 85, 102, 187, 119, 102, 102, 136,\
187, 170, 153, 136, 136, 73, 102, 48, 35, 102, 85, 85, 20, 51, 79, 79, 20, 9,\
62, 79, 51, 45, 37, 60, 61, 31, 39, 52, 46, 26, 85, 68, 102, 19, 9, 11, 11, 11,\
42, 62, 45, 76, 45, 61, 68, 34, 34, 45, 28, 57, 62, 62, 62, 65, 170, 85, 136,\
136, 34, 34, 68, 51, 68, 85, 51, 119, 119, 68, 85, 119, 136, 68, 68, 68, 68,\
119, 68, 85, 68, 52, 65, 65]

def get_empty_mmap(mmap_coord):
    mmap_pixel = ImageGrab.grab(bbox=mmap_coord).load()
    return [mmap_pixel[i,0][0:3] for i in range(mmap_coord[2] - mmap_coord[0])]

def is_edge(direc, mmap_coord, reference_r, edge_perc=0.3, num_attempts=10):
    for attempt in range(num_attempts):
        try:
            if direc == L:
                return rel_pos(mmap_coord, reference_r) < edge_perc
            else:
                return rel_pos(mmap_coord, reference_r) > 1 - edge_perc
        except:
            auto_hp
            pause(0.2)
            continue
    raise PlayerNotFound()

def horizontal_4(current_dir, edge_fn=None, combo_fn=None, move_fn=None, back=False, edge_behavior=None):
    try:
        while not edge_fn(current_dir):
            c()
            skill()
            move_fn(current_dir)
            combo_fn()
            if back and prob(0.2):
                move_fn(other(current_dir))
                combo_fn()
        if edge_behavior:
            edge_behavior(current_dir)
    except PlayerNotFound as e:
        e.show()

combo_fn = lambda num_attack, attack_delay: safe_combo(num_attack, attack_delay)
#else:
    #combo_fn = lambda num_attack, attack_delay: combo(random.choice([num_attack,num_attack+1]), attack_delay)
move_fn = lambda direc, num_moves: safe_tele(direc, num_moves)

combo_ueii = lambda : combo_fn(1, BLIZZARD)
move_ueii = lambda direc: move_fn(direc, 2)
edge_ueii = lambda direc: is_edge(direc, mmap_coord_ueii, reference_r_ueii)

def click_seller():
    pause(1)
    seller_pos = (450, 240)
    sell_option_pos = (330, 374)
    yes_pos = (580, 445)
    move_to_click(seller_pos, 2) #; pause(0.5)
    move_to_click(sell_option_pos, 1) #; pause(0.5)
    move_to_click(yes_pos, 1) #; pause(0.5)

def special_grind(n):
    for i in range(n):
        c()
        safe_combo(2, BLIZZARD)
        pause(5)
        safe_combo(2, BLIZZARD)
        pause(8)
        cc_next()

def cc_next():
    auto.press('esc')
    auto.press('\n')
    #pause(0.1)
    auto.press('left')
    #pause(0.1)
    auto.press('\n')
    pause(3)

def sell(start_item=0, full_stack=True):
    if start_item > 4:
        raise Exception('Item out of shop view.')
    shop_outer = (404, 279)
    item_size = (35,35)
    separation_size = (35, 4)
    item_pos = (560, 307 + start_item * item_size[1])
    #item_pos = \
    #(int(shop_outer[0] + item_size[0]/2 + \
    # (separation_size[0]+item_size[0])* start_item),
    # int(shop_outer[1] + item_size[1]/2 + \
    # (separation_size[1]+item_size[1])* start_item))
    ok_left_top = (422, 350)
    ok_right_bot = (469, 368)
    ok_center = (ok_left_top[0]+ok_right_bot[0])/2
    move_to_click(item_pos, 2)
    pause(0.5)
    count = 0
    item_empty = lambda pixel: pixel[0]>200 and pixel[1]>200 and pixel[2]>200
    #while not item_empty(get_pixel(item_pos[0], item_pos[1])):# and count < 10:
    full_backpack = 20 * 4
    if full_stack:
        item_left = full_backpack - start_item
    else:
        item_left = full_backpack / 2 - start_item
    while count < item_left:
        double_click()
        pause(0.2)
        auto.keyDown('\n')
        pause(0.2)
        auto.keyUp('\n')
        pause(0.2)
        count += 1

def xmas(n=10, x=365, y=250):
    for i in range(n):

        move_to_click((x,y)); pause(0.1)
        auto.press('down'); pause(0.2)
        auto.press('\n'); pause(0.2)
        auto.press('left'); pause(0.2)
        auto.press('left'); pause(0.2)
        auto.press('\n'); pause(0.2)
        auto.press('\n'); pause(0.2)

def full_scroll(scroll_success, scroll_price, ws_price, slots):
    spent = 0

    while slots > 0:
        if prob(scroll_success):
            slots -= 1
        spent += scroll_price + ws_price
    return spent
def scroll_simulate(times, scroll_success, scroll_price, ws_price, slots):
    trial_list = list()
    for i in range(times):
        trial_list += [full_scroll(scroll_success, scroll_price, ws_price, slots)]
    return trial_list
def simulate_matk60(times):
    trial_list = scroll_simulate(times, 0.6, 3e5, 3e8, 8)
    return trial_list
def simulate_matk10(times):
    trial_list = scroll_simulate(times, 0.1, 1e6, 3e8, 8)
    return trial_list
