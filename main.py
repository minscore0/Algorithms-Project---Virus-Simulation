import pygame
import math
import time
import random
import multiprocessing
from node_class import *
from threading import Thread
from collections import defaultdict, deque

# initialize pygame
pygame.init()
pygame.display.set_caption("model")
clock = pygame.time.Clock()

# make screen
screen = pygame.display.set_mode([1560, 900])
screen.fill((255, 255, 255))

# text
global BLACK, BLUE, GREEN, RED, GREY
BLACK, BLUE, GREEN, RED, GREY = (0, 0, 0), (66, 161, 245), (109, 237, 102), (242, 43, 29), (158, 158, 158)
font = pygame.font.Font("freesansbold.ttf", 20)
text1 = font.render("- regular node.", True, (0, 0, 0))
text2 = font.render("- infected node.", True, (0, 0, 0))
text3 = font.render("- masked node.", True, (0, 0, 0))
text4 = font.render("- immune node.", True, (0, 0, 0))
text5 = font.render("Q or ESC to quit.", True, (0, 0, 0))
text6 = font.render("G to generate graph.", True, (0, 0, 0))
text7 = font.render("S on a node to start.", True, (0, 0, 0))
text1Rect = text1.get_rect()
text2Rect = text2.get_rect()
text3Rect = text3.get_rect()
text4Rect = text4.get_rect()
text5Rect = text5.get_rect()
text6Rect = text6.get_rect()
text7Rect = text7.get_rect()
text1Rect.center = (1430, 50)
text2Rect.center = (1430, 100)
text3Rect.center = (1430, 150)
text4Rect.center = (1430, 200)
text5Rect.center = (1410, 300)
text6Rect.center = (1410, 350)
text7Rect.center = (1410, 400)


def translate_key(p_keys) -> float: #translates user input
    if p_keys[pygame.K_0]:
        return 1
    elif p_keys[pygame.K_1]:
        return 0.1
    elif p_keys[pygame.K_2]:
        return 0.2
    elif p_keys[pygame.K_3]:
        return 0.3
    elif p_keys[pygame.K_4]:
        return 0.4
    elif p_keys[pygame.K_5]:
        return 0.5
    elif p_keys[pygame.K_6]:
        return 0.6
    elif p_keys[pygame.K_7]:
        return 0.7
    elif p_keys[pygame.K_8]:
        return 0.8
    elif p_keys[pygame.K_9]:
        return 0.9
    else:
        return None


def create_nodes(node_objects, coords, mask, immune) -> dict: # create nodes
    for obj in node_objects:
        del obj

    for i in range(50):
        if mask > 0 and random.random() <= mask:
            has_mask = True
        else:
            has_mask = False
        if immune > 0 and random.random() <= immune:
            is_immune = True
        else:
            is_immune = False
    
        name = f"node{i+1}"
        node_objects[name] = Node(screen, name, coords, mask=has_mask, immune=is_immune)
        coords = node_objects[name].coords
        coords.append(node_objects[name].coord)

    return node_objects


def create_graph(graph, node_objects) -> dict: # create graph
    for obj1 in node_objects.values():
        for obj2 in node_objects.values():
            if obj1 == obj2:
                continue
            if math.dist(obj1.coord, obj2.coord) < 250:
                graph[obj1].add(obj2)
                graph[obj2].add(obj1)

    return graph


def start(graph, start_node, node_objects, incubation=None) -> float: #main DFS loop, returns finish time
    start_time = time.time()
    Q = deque([start_node])
    E = {start_node}
    start_node.color = RED
    start_node.infected = True
    start_node.visited = True
    update(node_objects, graph)

    while Q:
        
        center = Q.popleft()
        for node in graph[center]:
            if node in E:
                continue
            if center.immune:
                continue
            if node.immune:
                time.sleep(delay)
                node.visited = True
                E.add(node)
                update(node_objects, graph)
                Q.append(node)
                Q.append(center)
                continue
            if center.interactions == incubation:
                center.disappear()
                Q = deque([x for x in Q if x != center])
                continue
            if incubation is not None:
                center.interactions += 1
            if center.mask:
                time.sleep(delay)
                if node.mask:
                    if random.random() < R_t*mask_t*mask_t:
                        node.color = RED
                        node.infected = True
                        node.visited = True
                        E.add(node)
                        update(node_objects, graph)
                        Q.append(node)
                        continue

                    node.visited = True
                    update(node_objects, graph)
                    Q.append(center)
                    continue
                if random.random() < R_t*mask_t:
                    node.color = RED
                    node.infected = True
                    node.visited = True
                    E.add(node)
                    update(node_objects, graph)
                    Q.append(node)
                    continue

                node.visited = True
                update(node_objects, graph)
                Q.append(center)
                continue

            if node.mask:
                time.sleep(delay)
                if random.random() < R_t*mask_t:
                    node.color = RED
                    node.infected = True
                    node.visited = True
                    E.add(node)
                    update(node_objects, graph)
                    Q.append(node)
                    continue

                node.visited = True
                update(node_objects, graph)
                Q.append(center)
                continue

            time.sleep(delay)
            node.color = RED
            node.infected = True
            node.visited = True
            E.add(node)
            update(node_objects, graph)
            Q.append(node)
    
    update(node_objects, graph)
    per_node(graph, time.time()-start_time)
    return


def per_node(graph, time):
    infected = 0
    for node in graph.keys():
        if node.infected:
            infected += 1
    font0 = pygame.font.Font("freesansbold.ttf", 20)
    text0 = font0.render(f"per node: {round(time/infected, 3)}s", True, (0, 0, 0))
    text0Rect = text0.get_rect()
    text0Rect.center = (1425, 610)
    screen.blit(text0, text0Rect)


def update(node_objects, graph) -> None: # update screen
    pygame.draw.circle(screen, (0, 0, 0), (1335, 50), 10)
    pygame.draw.circle(screen, (242, 43, 29), (1335, 100), 10)
    pygame.draw.circle(screen, (66, 161, 245), (1335, 150), 10)
    pygame.draw.circle(screen, (109, 237, 102), (1335, 200), 10)
    screen.blit(text1, text1Rect)
    screen.blit(text2, text2Rect)
    screen.blit(text3, text3Rect)
    screen.blit(text4, text4Rect)
    screen.blit(text5, text5Rect)
    screen.blit(text6, text6Rect)
    screen.blit(text7, text7Rect)
    pygame.display.flip()

    for key, value in graph.items():
        for node in value:
            if (node.infected or (node.immune and node.visited)) and \
               (key.infected or (key.immune and key.visited)) and not \
               (node.immune and key.immune): 
                pygame.draw.aaline(screen, (242, 43, 29), key.coord, node.coord)
            else:
                pygame.draw.aaline(screen, (0, 0, 0), key.coord, node.coord)

    for obj in node_objects.values():
        obj.draw_node()


def reset(node_objects, graph, mask=0, immune=0) -> tuple[dict, dict]: # creates all nodes
    coords = list()
    graph = defaultdict(set)
    node_objects = create_nodes(node_objects, coords, mask, immune)
    graph = create_graph(graph, node_objects)
    screen.fill((255, 255, 255))
    update(node_objects, graph)

    return node_objects, graph


def check_mouse(node_objects) -> object: # check if the mouse is on a node
    for node in node_objects.values():
        if math.dist(pygame.mouse.get_pos(), node.coord) <= 30:
            return node

    return False


def edit_node(node_objects, p_mask, p_immune) -> None: # changes status of nodes
    for node in node_objects.values():
        if random.random() <= p_mask:
            node.give_mask()
        if random.random() <= p_immune:
            node.make_immune()


def timer() -> None:
    start_time = time.time()
    font0 = pygame.font.Font("freesansbold.ttf", 40)
    while True:
        text0 = font0.render(f"{round(time.time()-start_time, 2)}s", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(1300, 640, 200, 80))
        text0Rect = text0.get_rect()
        text0Rect.center = (1425, 660)
        screen.blit(text0, text0Rect)
        global stop_timer
        if stop_timer:
            break
        time.sleep(0.0003)


def three_seconds() -> None:
    time.sleep(3)
    global graph
    _node_objects = graph.keys()
    infected = 0
    total = len(_node_objects)
    for node in _node_objects:
        if node.infected:
            infected += 1
    
    font0 = pygame.font.Font("freesansbold.ttf", 30)
    text10 = font0.render(f"At 3s: {round(100*(infected/total), 2)}%", True, (0, 0, 0))
    text10Rect = text10.get_rect()
    text10Rect.center = (1430, 840)
    screen.blit(text10, text10Rect)

    

# variables
node_objects = dict()
graph = defaultdict(set)
start_time = None
end_time = None
stop_timer = False
global delay, R_t, mask_t
delay = 0.08
R_t = 1
mask_t = .75
timer_threads = list()
timer_thread_index = 0
start_threads = list()
start_thread_index = 0
three_seconds_threads = list()
three_seconds_thread_index = 0
incubation = None


if __name__ == "__main__":

    # game loop
    update(node_objects, graph)
    running = True
    while running:

        clock.tick(60)

        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False

                elif event.key == pygame.K_g:
                    start_time, end_time, incubation = None, None, None
                    node_objects, graph = reset(node_objects, graph)

                elif event.key == pygame.K_s:
                    start_node = check_mouse(node_objects)
                    if start_node:
                        start_threads.append(Thread(target=start, args=(graph , start_node, node_objects, incubation)))
                        timer_threads.append(Thread(target=timer))
                        three_seconds_threads.append(Thread(target=three_seconds))
                        start_threads[start_thread_index].start()
                        timer_threads[timer_thread_index].start()
                        three_seconds_threads[three_seconds_thread_index].start()
                        start_threads[start_thread_index].join()
                        stop_timer = True
                        timer_threads[timer_thread_index].join()
                        three_seconds_threads[three_seconds_thread_index].join()
                        start_thread_index += 1
                        timer_thread_index += 1
                        three_seconds_thread_index += 1
                        stop_timer = False
                
                elif event.key == pygame.K_m:
                    percent = translate_key(pressed_keys)
                    if percent is not None:
                        start_time, end_time = None, None
                        edit_node(node_objects, p_mask=percent, p_immune=0)
                    else:
                        node = check_mouse(node_objects)
                        if node is not False:
                            node.give_mask()
                            node.draw_node()
                
                elif event.key == pygame.K_i:
                    percent = translate_key(pressed_keys)
                    if percent is not None:
                        start_time, end_time = None, None
                        edit_node(node_objects, p_mask=0, p_immune=percent)
                    else:
                        node = check_mouse(node_objects)
                        if node is not False:
                            node.make_immune()
                            node.draw_node()

                elif event.key == pygame.K_n:
                    node = check_mouse(node_objects)
                    if node is not False:
                        node.make_normal()
                
                elif event.key == pygame.K_e:
                    incubation = int(input("Enter incubation period (interaction based): "))
                
        update(node_objects, graph)
        pygame.display.flip()

    pygame.quit()
