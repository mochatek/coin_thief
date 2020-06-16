import arcade
import random

MOVEMENT_SPEED = 2
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 10

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Coin Thief"

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.textures = []
        texture = arcade.load_texture("res\Thief.png", mirrored=True)
        self.textures.append(texture)
        texture = arcade.load_texture("res\Thief.png")
        self.textures.append(texture)
        self.scale = 0.1
        self.set_texture(TEXTURE_RIGHT)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.coin_list = None
        self.wall_list =  None
        self.ladder_list = None
        self.door_list =  None
        self.player = None
        self.player_list = None
        self.score = None
        self.game = None
        self.jump_sound = arcade.sound.load_sound("res\jump2.wav")
        self.coin_sound = arcade.sound.load_sound("res\coin5.wav")

    def setup(self):
        self.game = 'Running'
        self.score = 0
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.ladder_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.player = Player()
        self.player.center_x = 50
        self.player.center_y = 70
        self.player_list.append(self.player)
        map_name = "map.tmx"
        platforms_layer_name = 'Platform'
        coins_layer_name = 'Coins'
        ladder_layer_name = 'Ladder'
        door_layer_name = 'Exit'
        my_map = arcade.tilemap.read_tmx(map_name)
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, 0.2)
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, 0.2)
        self.ladder_list = arcade.tilemap.process_layer(my_map, ladder_layer_name, 0.2)
        self.door_list = arcade.tilemap.process_layer(my_map, door_layer_name, 0.2)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, GRAVITY, self.ladder_list)

    def on_draw(self):
        arcade.start_render()
        if self.game == 'Running':
            self.wall_list.draw()
            self.door_list.draw()
            self.ladder_list.draw()
            self.coin_list.draw()
            self.player_list.draw()
            score =  "SCORE : {}".format(self.score)
            arcade.draw_text(score,300, 450, arcade.color.RED, 18, bold=True)
        else:
            self.wall_list.draw()
            self.door_list.draw()
            self.ladder_list.draw()
            arcade.draw_text("Mission Passed!",220,300, arcade.color.RED,25, bold=True)
            arcade.draw_text("Level Upgraded.",220,270, arcade.color.BLACK, 18, bold=True)

    def on_update(self, delta_time):
        player_hit_door = arcade.check_for_collision(self.door_list[0], self.player)
        if player_hit_door == True and self.score == 100:
            self.game = 'End'
        else:
            self.player_list.update()
            self.physics_engine.update()

            hit_coins_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
            for coin in hit_coins_list:
                arcade.play_sound(self.coin_sound)
                coin.remove_from_sprite_lists()
                self.score += 5


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = MOVEMENT_SPEED
            elif self.physics_engine.can_jump():
                arcade.play_sound(self.jump_sound)
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
