from collections import deque
import pygame
import random
import json 

move4 = [(0,-1),(0,1),(-1,0),(1,0)]
Yes = 'Yes'
No = "No"

pg = pygame
pg.init()

class maize:
    def __init__(s,diff=(15,15)) -> None:
        s.hi,s.wi = diff
        s.grid = [["#"]*s.wi for _ in range(s.hi)]
        s.sx,s.sy = 1,1
        s.gx,s.gy = s.hi-2,s.wi-2
        s.vis = [[False]*s.wi for _ in range(s.hi)]
        s.grid = s.make()

    def make(s):
        s.grid = [["#"]*s.wi for _ in range(s.hi)]
        s.pos = deque()
        for i in range(1,s.hi-1):
            for j in range(1,s.wi-1):
                if i%2 == 0 and j%2 == 0:
                    s.grid[i][j] = "#"
                    s.pos.append((i,j))
                else:
                    s.grid[i][j] = "."
        while s.pos:
            i,j = s.pos.pop()
            while True:
                xi,yj = random.choice(move4)
                if s.grid[i+xi][j+yj] != "#":
                    s.grid[i+xi][j+yj] = "#"
                    break
        return s.grid
    
    def dfs(s,pos):
        x,y = pos
        s.vis[x][y] = True
        for mx,my in move4:
            if s.grid[x+mx][y+my] == "." and s.vis[x+mx][y+my] == False:
                s.dfs((x+mx,y+my))

    def ch(s):
        s.vis = [[False]*s.wi for _ in range(s.hi)]
        s.dfs((1,1))
        return s.vis[s.gx][s.gy]
    
    def move(s,dx,dy):
        x = s.sx + dx
        y = s.sy + dy
        if s.grid[x][y] == ".":
            s.sx = x
            s.sy = y

    def reset(s):
        s.sx,s.sy = 1,1
        s.gx,s.gy = s.hi-2,s.wi-2
        s.grid = s.make()
        s.vis = [[False]*s.wi for _ in range(s.hi)]

    def clear(s):
        return s.sx == s.gx and s.sy == s.gy

    def ret(s):
        return s.grid

class visual:
    def __init__(s):
        s.WIDTH = 600
        s.HEIGHT = 600
        s.screen = pg.display.set_mode((s.WIDTH,s.HEIGHT))
        pg.display.set_caption("Maze")
        s.difficulties = [(15,15),(21,21),(31,31)]
        s.diff = 0
        s.mode = "home"
        s.maze = None
        s.back = (0,0,0)
        s.wall = (240,160,32)
        s.ailes = (21,110,21)
        s.player = (255,255,255)
        s.goal = (255,0,0)

    def draw_home(s):
        s.screen.fill(s.back)
        font = pg.font.Font(None,60)
        text = font.render("MAZE",True,(255,255,255))
        s.screen.blit(text,(230,80))
        font = pg.font.Font(None,40)
        for i,diff in enumerate(s.difficulties):
            color = (255,255,0) if i == s.diff else (255,255,255)
            text = font.render(f"{diff[0]} x {diff[1]}",True,color)
            s.screen.blit(text,(230,200+i*60))
        font = pg.font.Font(None,30)
        text = font.render("UP / DOWN : Select",True,(255,255,255))
        s.screen.blit(text,(190,420))
        text = font.render("ENTER : Start",True,(255,255,255))
        s.screen.blit(text,(220,460))

    def draw_game(s):
        s.screen.fill(s.back)
        maze = s.maze
        size = 150
        px = maze.sx
        py = maze.sy
        offset_x = (s.WIDTH - size*3)//2
        offset_y = (s.HEIGHT - size*3)//2
        for dx in range(-1,2):
            for dy in range(-1,2):
                x = px + dx
                y = py + dy
                screen_x = offset_x + (dy+1)*size
                screen_y = offset_y + (dx+1)*size
                if not (0 <= x < maze.hi and 0 <= y < maze.wi):
                    color = s.wall
                elif maze.grid[x][y] == "#":
                    color = s.wall
                else:
                    color = s.ailes
                pg.draw.rect(s.screen,color,(screen_x,screen_y,size,size))
                if maze.grid[x][y] == ".":
                    pg.draw.rect(s.screen,color,(screen_x+3,screen_y+3,size-6,size-6))
        pg.draw.circle(s.screen,s.player,(offset_x+size+size//2,offset_y+size+size//2),size//3)
        for dx in range(-1,2):
            for dy in range(-1,2):
                x = px + dx
                y = py + dy
                if x == maze.gx and y == maze.gy:
                    screen_x = offset_x + (dy+1)*size
                    screen_y = offset_y + (dx+1)*size
                    pg.draw.rect(s.screen,s.goal,(screen_x+size//3,screen_y+size//3,size//3,size//3))

        font = pg.font.Font(None,28)
        text = font.render("move : ↑ / ↓ / ← / →    restart : R    home : BackSpace    gameend : Esc",True,(255,255,255))
        s.screen.blit(text,(25,560))

    def draw_clear(s):
        s.screen.fill(s.back)
        font = pg.font.Font(None,70)
        text = font.render("CLEAR!",True,(255,255,255))
        s.screen.blit(text,(210,200))
        font = pg.font.Font(None,35)
        text = font.render("ENTER : New Game",True,(255,255,255))
        s.screen.blit(text,(190,320))
        text = font.render("BACKSPACE : Home",True,(255,255,255))
        s.screen.blit(text,(185,370))

    def run(s):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    if s.mode == "home":
                        if event.key == pg.K_UP:
                            s.diff = max(0,s.diff-1)
                        elif event.key == pg.K_DOWN:
                            s.diff = min(len(s.difficulties)-1,s.diff+1)
                        elif event.key == pg.K_RETURN:
                            s.maze = maize(s.difficulties[s.diff])
                            s.mode = "game"
                    elif s.mode == "game":
                        if event.key == pg.K_UP:
                            s.maze.move(-1,0)
                        elif event.key == pg.K_DOWN:
                            s.maze.move(1,0)
                        elif event.key == pg.K_LEFT:
                            s.maze.move(0,-1)
                        elif event.key == pg.K_RIGHT:
                            s.maze.move(0,1)
                        elif event.key == pg.K_r:
                            s.maze.reset()
                        elif event.key == pg.K_BACKSPACE:
                            s.mode = "home"
                        if s.maze.clear():
                            s.mode = "clear"
                    elif s.mode == "clear":
                        if event.key == pg.K_RETURN:
                            s.maze.reset()
                            s.mode = "game"
                        elif event.key == pg.K_BACKSPACE:
                            s.mode = "home"
            if s.mode == "home":
                s.draw_home()
            elif s.mode == "game":
                s.draw_game()
            elif s.mode == "clear":
                s.draw_clear()
            pg.display.update()
        pg.quit()

if __name__ == "__main__":
    gl = maize()
    grid = gl.ret()
    print(gl.ch())
    for i in grid:
        print(''.join(i))
    vi = visual()
    vi.run()