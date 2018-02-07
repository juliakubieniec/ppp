
from GameScene import *

try:
    scene = BaseScene()
    scene.run_game(800, 600, 60, TitleScene())
except:
    print('Load game failed')
