import pygame,time,sys,json,logging,enum
import map as MAP

pygame.init()
logging.basicConfig(filename="latest.log",level=logging.DEBUG)
def log(tp,scr,tx):
    logging.debug(tx)
    tp.tprint(scr,tx)
    pygame.display.flip()

class tool(enum.Enum):
    build = enum.auto()
    none = enum.auto()


class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 15)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (255,255,255))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 15
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

class MAIN:

    tp = TextPrint()


    engeneLogo = pygame.image.load("assets/engene.png")

    def __init__(self,scr:pygame.Surface,tex:dict[str,str]) -> None:
        self.scr = scr
        pygame.display.set_icon(self.engeneLogo)

        scr.blit(self.engeneLogo,(5,5))
        pygame.display.flip()
        log(self.tp,scr,"      DeepSpace")
        log(self.tp,scr,"Loading...")
        time.sleep(1)

        self.assets = {}

        for k,v in tex.items():
            self.assets[k] = pygame.image.load(f"assets/{v}.png")
            log(self.tp,scr,f"mapping assets/{v}.png to {k}")
            time.sleep(0.1)


        log(self.tp,scr,"done loading textures...")
        time.sleep(1)
        self.Sw,self.Sh = scr.get_width(),scr.get_height()
        self.gridtx = pygame.Surface((self.Sw,self.Sh))
        self.gridtx.fill((0,0,0,0))
        log(self.tp,scr,"generating grid texture...")

        time.sleep(0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        log(self.tp,scr,f"{str((self.Sw//16)*(self.Sh//16))}(16x16) segments")
        self.MSW,self.MSH = (self.Sw//16),(self.Sh//16)
        time.sleep(1)

        for x in range(0,self.Sw-(self.Sw%16),16):
            pygame.draw.line(self.gridtx,(100,100,100,100),(x,0),(x,self.Sh))
            time.sleep(0.01)

        log(self.tp,scr,"done X axis lines...")
        time.sleep(0.5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for y in range(0,self.Sh-(self.Sh%16),16):
            pygame.draw.line(self.gridtx,(100,100,100,100),(0,y),(self.Sw,y))
            time.sleep(0.01)

        log(self.tp,scr,"done Y axis lines...")

        time.sleep(0.5)


        log(self.tp,scr,"done preping assets..")

        time.sleep(1)

        log(self.tp,scr,"loading tiles...")

        time.sleep(1)

        f = open("assets/tiles.json")
        td = json.load(f)

        self.tileMappings = {}

        for k,v in td.items():
            self.tileMappings[int(k)] = v
            log(self.tp,scr,f"mapping {k} to {str(v)}")
            time.sleep(0.01)

        log(self.tp,scr,"done..")

        time.sleep(1)
        self.cs = 0

        self.grid = []
        self.mode = tool.none
        MAP.new("map.map",self.MSH*self.MSW)
        f = open("map.map","rb")
        for x in range(self.MSW):
            R = []
            for y in range(self.MSH):
                R.append(self.assets[self.tileMappings[int.from_bytes(f.read(1),"big")]["tex"]])
            self.grid.append(R)
        




    def editor(self,events:list[pygame.event.Event]):
        self.scr.fill((0,0,0))
        X = 0
        for x in self.grid:
            Y = 0
            for y in x:
                scr.blit(y,(X,Y))
                Y += 16
            X += 16
        
        self.scr.blit(self.gridtx,(0,0),special_flags=pygame.BLEND_RGBA_ADD)
        kb = pygame.key.get_pressed()
        if kb[pygame.K_TAB]:
            self.scr.blits(((self.assets["blueprint"],(0,0)),(self.assets["build"],(16,0)),(self.assets["code"],(32,0)),(self.assets["run"],(48,0))))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                cx, cy = mx//16, my//16
                if kb[pygame.K_TAB]:
                    if cy == 0:
                        if cx == 0:
                            pass
                        elif cx == 1:
                            self.mode = tool.build
                        elif cx == 3:
                            pass
                        if cx == 4:
                            pass
                elif self.mode == tool.build:
                    self.grid[cx][cy] = self.assets[self.tileMappings[self.cs]["tex"]]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_0:
                    self.cs = int(input("sellect>"))



        pygame.display.flip()
        

scr = pygame.display.set_mode((500,400))

e = MAIN(scr,{
    'logo':"engene",
    "blueprint":"blueprint",
    "build":"build",
    "object":"object",
    "code":"code",
    "run":"run",
    "warning":"warning",
    "air":"air"
})

while True:
    events = pygame.event.get()
    e.editor(events)
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

