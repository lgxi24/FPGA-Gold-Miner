
import pygame
import gamebox
import random
import math
import socket
import json
from decimal import Decimal

print("we're in tcp client")
HOST = '18.132.245.115'  
PORT = 12000        

# 0-preparation
# general
result = ""
game_money = 0
camera=gamebox.Camera(1000, 700)
money=0
radins_1 = -70
radins_2 = -70
chain_distance=30
value_caught = 0 ; pict_index = 0 
speed = 5
weight_item_caught = speed +5
counter = 5
counter_up = 0
level = 1
shop_list = []
shop_price = []  
money_goal=[1000,2200,3600,5400,7500,10000,12500,17000,21500,26000,30000,45000]
scene = 0 
index = 0
popped_up_word_counterdown_1 = 16
popped_up_word_counterdown_2 = 16
shop_selection = 0
item_caught= gamebox.from_color(500,100,"black",1,1)
picture_list=["picture/gold_small.png","picture/gold_middle.png","picture/gold_big.png","picture/rock_small.png","picture/rock_big.png","picture/dimaond.png","picture/mystery_bag.png","picture/background.png","picture/background1.png","picture/Blitzcrank_Render.png","picture/starting.png","picture/logo.png","picture/Thresh_Render.png"]

text_list = ["Gold sands:Small gold worths more in the next level","Diamond polisher:Diamond worths 50% more in the next level","Lamp:More diamond would appear in the next level","The Gem of Time:You have 20 more seconds in the next level","The Gem of Luck:You have higher chance of getting good stuff from the random bags.","The Gem of Strength:Pulling minerals back takes less time in the next level","The lucky Rock:Rock worths 300% more in the next level","SOLD OUT!"]

# animation set up
frame= 0
frame1= 0
frame2 = 0
sheet1 = gamebox.load_sprite_sheet("picture/animation1.png", 1, 7)
sheet2 = gamebox.load_sprite_sheet("picture/character1_1.png", 1, 7)
sheet3= gamebox.load_sprite_sheet("picture/character1_2.png", 1, 8)
chainhead_1 = gamebox.from_image(200, 200, sheet1[frame])
chainhead_2 = gamebox.from_image(200, 200, sheet1[frame])
character1 = gamebox.from_image(475, 50, sheet2[frame1])
character2 = gamebox.from_image(525, 50, sheet2[frame2]) 

# booleans
direction_left_to_right_1=True
chain_thrown_out_1= False
chain_thrown_out_away_1 = True
chain_thrown_out_catchsomething_1 = False

#items
item_gold_modifer = False
item_polisher = False
item_lamp = False
item_time = False
item_luck = False
item_rocks = False

# lists
gold_middle = [gamebox.from_image(400,400,picture_list[1])]
gold_small = [gamebox.from_image(500,500,picture_list[0])]
gold_large = []
gold_dimaond = [gamebox.from_image(700, 500, picture_list[5])]
gold_small_rock = [gamebox.from_image(400, 600, picture_list[3])]
gold_big_rock = [gamebox.from_image(600, 600, picture_list[4])]
gold_random_big = [gamebox.from_image(200, 300,picture_list[6])]

def read_input_file(file_path='output.txt'):
    with open(file_path, 'r') as file:
        line = file.readline().strip()
        if not line:
            return '0', 'key0'
        # Assuming the line format is 'raw data: ffffffffd3 Button Status: key1'
        if 'Button Status: ' in line:
            raw_data_part, button_status_part = line.split('Button Status: ')
            raw_data = raw_data_part.split(': ')[1]
            button_status = button_status_part.strip()
    return raw_data, button_status
    
def tick(keys):

    global radins_1, radins_2,game_money ,money , direction_left_to_right_1, chain_thrown_out_1 , chain_thrown_out_away_1, chain_distance , chainhead_1, chainhead_2
    global chain_thrown_out_catchsomething_1, chain_thrown_out_catchsomething_2 , item_caught , weight_item_caught , speed , background
    global value_caught , pict_index , counter , level, surface, counter_up, frame, frame1, frame2, scene, index
    global popped_up_word_counterdown_1,popped_up_word_counterdown_2, shop_selection, shop_list, shop_price
    global item_gold_modifer, item_polisher, item_lamp, item_time, item_luck, item_rocks
    camera.clear('black')
    

    # differetiate on scenes
    if scene == 0:
        screen = gamebox.from_image(500, 350,picture_list[10])
        screen.scale_by(0.70)
        camera.draw(screen)
        camera.draw(gamebox.from_color(500, 200, "white", 900, 60))
        camera.draw(gamebox.from_text(500,200,"WELCOME to IMPERIAL MINER","arial",60,"dark blue"))
        camera.draw(gamebox.from_text(500,500,"Press KEY1 to continue","arial",30,"green"))
        chainhead_1.image = sheet1[frame]
        if index == 0:
            chainhead_1 = gamebox.from_image(940, 546, sheet1[frame])
        else:
            chainhead_1 = gamebox.from_image(970, 546, sheet1[frame])
        chainhead_1.scale_by(0.5)
        camera.draw(chainhead_1)

        
        raw_data, button_status = read_input_file(file_path='output.txt')
        if  button_status == "key1" or pygame.K_SPACE in keys:
            scene = 2
            level_generation(level)
        if button_status == "key2" or pygame.K_s in keys:
            scene = 1

    if scene == 1:
        get_rank(HOST,PORT)
        raw_data, button_status = read_input_file(file_path='output.txt')
        if  button_status == "key2" or pygame.K_w in keys:
            scene = 0

    if scene == 2:
        #background
        counter_up += 1
        picture = gamebox.from_image(500, 380, picture_list[7])
        picture2 = gamebox.from_image(500, 37.5, picture_list[8])
        picture3 = gamebox.from_image(460, 65.5, picture_list[9])
        picture4 = gamebox.from_image(90, 155.5, picture_list[11])
        

        picture3.scale_by(0.1)
        picture2.scale_by(0.45)
        picture.scale_by(0.7)
        picture4.scale_by(0.1)
        camera.draw(picture)
        camera.draw(picture2)
        camera.draw(picture3)
        camera.draw(picture4)
        # camera.draw(character1)

        # animations
        frame += 1
        if frame == 7:
            frame = 0
        chainhead_1.image = sheet1[frame]
        if frame == 7:
            frame = 0

        if chain_thrown_out_1 == False:
            character1 = gamebox.from_image(755, 80, sheet2[int(frame1)])
            frame1 += 0.5
            if frame1 == 7:
                frame1 = 0
            character1.image = sheet2[int(frame1)]
        else:
            character1 = gamebox.from_image(755, 80, sheet3[int(frame1)])
            frame1 += 0.5
            if frame1 == 8:
                frame1 = 0
            character1.image = sheet3[int(frame1)]

        camera.draw(character1)


        # 2-when chain available
        # degree regular changes
        if chain_thrown_out_1 == False:
            if popped_up_word_counterdown_1 >= 16:
                raw_data, button_status = read_input_file(file_path='output.txt')
                if raw_data.startswith('f'):
                    radins_1 += 3
                elif raw_data.startswith('0'):
                    radins_1 = radins_1
                else:
                    radins_1 -= 3

            if radins_1 <= -70:
                radins_1 = -70
            if radins_1 >= 70:
                radins_1 = 70 


            # chain head displays
            chainhead_1.x = 500 + math.sin(radins_1 / 57.29) * 75
            chainhead_1.y = 75 + math.cos(radins_1 / 57.29) * 75
            camera.draw(chainhead_1)

            # chains display
            item = gamebox.from_color(500, 75, "black", 5, 5)
            for i in range(0, 25):
                item = gamebox.from_color(500 + math.sin(radins_1 / 57.29) * 2.5 * i,
                                          75 + math.cos(radins_1 / 57.29) * 2.5 * i, "black", 5, 5)
                camera.draw(item)
        

        # 3-chain_thrown_out
        # set up throwing chain
        raw_data, button_status = read_input_file(file_path='output.txt')
        if  button_status == "key1" and chain_thrown_out_1== False and popped_up_word_counterdown_1 >= 16:
            chain_thrown_out_1 = True
            chain_thrown_out_away_1 = True
            chain_thrown_out_catchsomething_1 = False
            chain_distance = 30
            character1.scale_by(1.2)


        # chain animation
        if chain_thrown_out_1 == True and chain_thrown_out_away_1 == True:
            chain_distance += speed
            for i in range(1, chain_distance):
                item = gamebox.from_color(500 + math.sin(radins_1 / 57.29) * 2.5 * i,
                                          75 + math.cos(radins_1 / 57.29) * 2.5 * i, "black", 5, 5)
                camera.draw(item)
            chainhead_1.x = 500 + math.sin(radins_1 / 57.29) * (10 + 2.5 * chain_distance)
            chainhead_1.y = 75 + math.cos(radins_1 / 57.29) * (10 + 2.5 * chain_distance)
            camera.draw(chainhead_1)

        if chain_thrown_out_1 == True and chain_thrown_out_away_1 == False:
            chain_distance -= weight_item_caught
            for i in range(1, chain_distance):
                item = gamebox.from_color(500 + math.sin(radins_1 / 57.29) * 2.5 * i,
                                          75 + math.cos(radins_1 / 57.29) * 2.5 * i, "black", 5, 5)
                camera.draw(item)
            chainhead_1.x = 500 + math.sin(radins_1 / 57.29) * (10 + 2.5 * chain_distance)
            chainhead_1.y = 75 + math.cos(radins_1 / 57.29) * (10 + 2.5 * chain_distance)
            camera.draw(chainhead_1)
        


        # boolans for throw/retriving chains
        if chainhead_1.x < 0 or chainhead_1.x > 1000 or chainhead_1.y > 700:
            chain_thrown_out_away_1 = False

        if chain_distance <= 29 and chain_thrown_out_1 == True:
            if chain_thrown_out_catchsomething_1 == True:
                if value_caught != 0:
                    popped_up_word_counterdown_1 = 1
                money += value_caught
                chain_thrown_out_catchsomething_1 = False
            chain_thrown_out_1 = False
            character1.scale_by(0.833)
            frame1 = 0  # prevent "out of range" error
            weight_item_caught = speed + 5

        # catching items
        for gold in gold_middle:
            if gold.touches(chainhead_1) and chain_thrown_out_catchsomething_1 == False:
                chain_thrown_out_away_1 = False
                chain_thrown_out_catchsomething_1 = True
                weight_item_caught = speed - 2
                pict_index = 1
                value_caught = 200
                gold_middle.remove(gold)
            camera.draw(gold)

        for gold in gold_small:
            if gold.touches(chainhead_1) and chain_thrown_out_catchsomething_1 == False:
                chain_thrown_out_away_1 = False
                chain_thrown_out_catchsomething_1 = True
                weight_item_caught = speed
                pict_index = 0
                if item_gold_modifer == True:
                    value_caught = 125 + 25 * level
                else:
                    value_caught = 75
                gold_small.remove(gold)
            camera.draw(gold)



        for gold in gold_large:
            if gold.touches(chainhead_1) and chain_thrown_out_catchsomething_1 == False:
                chain_thrown_out_away_1 = False
                chain_thrown_out_catchsomething_1 = True
                weight_item_caught = speed - 4
                pict_index = 2
                value_caught = 500
                gold_large.remove(gold)
            camera.draw(gold)


        for gold in gold_dimaond:
            if gold.touches(chainhead_1) and chain_thrown_out_catchsomething_1 == False:
                chain_thrown_out_away_1 = False
                chain_thrown_out_catchsomething_1 = True
                weight_item_caught = speed + 4
                pict_index = 5
                if item_polisher == True:
                    value_caught = 900 + 75 * level
                else:
                    value_caught = 600 + 50 * level
                gold_dimaond.remove(gold)
            camera.draw(gold)


        for gold in gold_small_rock:
            if gold.touches(chainhead_1) and chain_thrown_out_catchsomething_1 == False:
                chain_thrown_out_away_1 = False
                chain_thrown_out_catchsomething_1 = True
                weight_item_caught = speed - 2
                pict_index = 3
                value_caught = 20
                if item_rocks == True:
                    value_caught = value_caught * 4
                gold_small_rock.remove(gold)
            camera.draw(gold)


        for gold in gold_big_rock:
            if gold.touches(chainhead_1) and chain_thrown_out_catchsomething_1 == False:
                chain_thrown_out_away_1 = False
                chain_thrown_out_catchsomething_1 = True
                weight_item_caught = speed - 4
                pict_index = 4
                value_caught = 60
                if item_rocks == True:
                    value_caught = value_caught * 4
                gold_big_rock.remove(gold)
            camera.draw(gold)

        for gold in gold_random_big:
            if gold.touches(chainhead_1) and chain_thrown_out_catchsomething_1 == False:
                if chain_thrown_out_catchsomething_1 == False:
                    weight_item_caught = speed + random.randint(-4, 5)
                chain_thrown_out_away_1 = False
                chain_thrown_out_catchsomething_1 = True
                pict_index = 6
                if item_luck == True:
                    value_caught = random.randint(500, 1000)
                else:
                    value_caught = random.randint(-300, 700)
                gold_random_big.remove(gold)
            camera.draw(gold)


        if chain_thrown_out_catchsomething_1 == True:
            item = gamebox.from_image(500 + math.sin(radins_1 / 57.29) * 2.5 * (chain_distance+10),
                                      95 + math.cos(radins_1 / 57.29) * 2.5 * (chain_distance+10), picture_list[pict_index])
            camera.draw(item)

        # 6-score/time/environments display
        counter -= 1
        camera.draw(gamebox.from_text(895, 135, "Your money:" + str(money), "arial", 24, "yellow"))
        camera.draw(gamebox.from_text(895, 165, "Time remaining:" + str(int(counter/30)), "arial", 22, "yellow"))
        camera.draw(gamebox.from_color(500, 118, "black", 40000, 3))

        popped_up_word_counterdown_1 += 1
        if popped_up_word_counterdown_1 <= 15:
            if value_caught > 0:
                camera.draw(gamebox.from_text(300, 25, "+" + str(value_caught), "arial", 30, "green", bold=True))
            else:
                camera.draw(gamebox.from_text(300, 25,  str(value_caught), "arial", 30, "red", bold=True))

        elif popped_up_word_counterdown_1 == 16:
            value_caught = 0


        # 7 transition/time runs out
        if counter == 0 :
                level += 1
                # shop generations
                random_list = [0, 1, 2, 3, 4, 5, 6]
                # set value to default
                speed = 5
                item_gold_modifer = False
                item_polisher = False
                item_lamp = False
                item_time = False
                item_luck = False
                item_rocks = False
                scene = 4
                chain_thrown_out_catchsomething_1 = False
                chain_thrown_out_1 = False
                character1.scale_by(0.833)
                chain_thrown_out_catchsomething_2 = False
                frame2 = 0 
                weight_item_caught = speed + 5
                value_caught = 0
                game_money = money


    if scene == 4:
        result = send_score(HOST, PORT, game_money)
        camera.draw(gamebox.from_text(500, 350, result, "arial", 30, "yellow"))
        camera.draw(gamebox.from_text(400, 300, "Your score: ", "arial", 30, "red"))
        camera.draw(gamebox.from_text(600, 300, str(game_money), "arial",30, "green"))


    camera.display()


def level_generation(level):
    # 5-golds generations
    global counter, gold_small_rock ,gold_large, gold_middle, gold_small, gold_random_big, gold_dimaond, gold_big_rock, chainhead_1, chainhead_2
    gold_middle = []
    gold_small = []
    gold_large = []
    gold_dimaond = []
    gold_small_rock = []
    gold_big_rock = []
    gold_random_big = []
    # item evaluation
    if item_time == True:
        counter = 2400
    else:
        counter = 1800

    if item_lamp == True:
        no_diamond = 3
    else:
        no_diamond = 0

    # generative algorithm
    if level % 2 == 0:
        no_diamond += 2
        no_diamond += int(level/3)
    if level % 2 == 0:
        no_random = 3
        no_random += int(level/2)
    else:
        no_random = 1
    if level >= 3:
        no_big = 1
        no_big += level//2
    else:
        no_big = 0
    if level >= 6:
        no_diamond += 2
        no_big += 2
        no_random += 2
        base = 1
    else:
        base = 0

    if level >= 8:
        no_diamond += 4
        no_big += 3
        no_random += 3
        base = 2
    if level == 12:
        no_diamond += 10
        base = 5
        no_big = 6
        no_random = 6

    if level >= 8:
        for c in range(0, random.randint(2,3)):
            item = gamebox.from_image(random.randint(50, 950), random.randint(230, 670), picture_list[0])
            gold_small.append(item)
        for c in range(0, 2):
            touched = True
            while touched:
                item = gamebox.from_image(random.randint(50, 950), random.randint(230, 670), picture_list[3])
                touched = False
                for evaluated_item in gold_small:
                    if item.touches(evaluated_item) == True:
                        touched = True
                for evaluated_item in gold_small_rock:
                    if item.touches(evaluated_item) == True:
                        touched = True
            gold_small_rock.append(item)

    else:
        for c in range(0, random.randint(5 + level // 2, 12 + level // 2)):
            item = gamebox.from_image(random.randint(50, 950), random.randint(230, 670), picture_list[0])
            gold_small.append(item)
        for c in range(0, random.randint(5, 7)):
            touched = True
            while touched:
                item = gamebox.from_image(random.randint(50, 950), random.randint(230, 670), picture_list[3])
                touched = False
                for evaluated_item in gold_small:
                    if item.touches(evaluated_item) == True:
                        touched = True
                for evaluated_item in gold_small_rock:
                    if item.touches(evaluated_item) == True:
                        touched = True
            gold_small_rock.append(item)



    for c in range(0, random.randint(8+level//2, 10+level//2)):
        touched = True
        while touched:
            item = gamebox.from_image(random.randint(50, 950), random.randint(230, 670), picture_list[1])
            touched = False
            for evaluated_item in gold_small:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_small_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_middle:
                if item.touches(evaluated_item) == True:
                    touched = True
        gold_middle.append(item)

    for c in range(0, random.randint(1+level//4+base, 2+level//4+base)):
        touched = True
        while touched:
            item = gamebox.from_image(random.randint(50, 950), random.randint(270, 700), picture_list[4])
            touched = False
            for evaluated_item in gold_small:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_small_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_middle:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_big_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
        gold_big_rock.append(item)

    for c in range(0, random.randint(base, no_big)):
        touched = True
        while touched:
            item = gamebox.from_image(random.randint(50, 950), random.randint(230, 670), picture_list[2])
            touched = False
            for evaluated_item in gold_small:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_small_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_middle:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_big_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_large:
                if item.touches(evaluated_item) == True:
                    touched = True
        gold_large.append(item)

    for c in range(0, random.randint(2, 3)):
        touched = True
        while touched:
            item = gamebox.from_image(random.randint(50, 950), random.randint(230, 670), picture_list[5])
            touched = False
            for evaluated_item in gold_small:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_small_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_middle:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_big_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_large:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_dimaond:
                if item.touches(evaluated_item) == True:
                    touched = True
        gold_dimaond.append(item)

    for c in range(0, random.randint(1, 2)):
        touched = True
        while touched:
            item = gamebox.from_image(random.randint(50, 950), random.randint(250, 700), picture_list[6])
            touched = False
            for evaluated_item in gold_small:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_small_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_middle:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_big_rock:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_large:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_dimaond:
                if item.touches(evaluated_item) == True:
                    touched = True
            for evaluated_item in gold_random_big:
                if item.touches(evaluated_item) == True:
                    touched = True
        gold_random_big.append(item)


def get_rank(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        rank_message = "get rank".encode()
        s.sendall(rank_message)
        response = s.recv(1024).decode()
        rank_data = json.loads(response)
        y_position = 300
        for rank in rank_data:
            player_id = rank['player_id']
            score = rank['score']

            rank_text = f"{player_id}: {score}"

            camera.draw(gamebox.from_text(500, y_position, rank_text, "arial", 30, "yellow"))
        
            y_position += 40

game_over = False  # Flag to track if the game result has been received
final_result ="Waiting for other player... "
def send_score(host, port, score):
    global game_over, final_result

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        score_message = str(score).encode()
        s.sendall(score_message)

        while True:
            response = s.recv(1024).decode()
            if response:
                if game_over:
                    return final_result
                if response in ["You win!", "You lose."]:
                    final_result = response  
                    game_over = True  
                    return final_result

ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)




