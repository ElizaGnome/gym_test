import gym
from gym import spaces
import numpy as np

class PhaserGameEnv(gym.Env):
    def __init__(self):
        super(PhaserGameEnv, self).__init__()

        self.action_space = spaces.Discrete(3)  
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)      
        self.reset()

    def reset(self):
        self.character_x =0.1
        self.character_y = 0.5
        self.enemy_x = 0.7
        self.enemy_y = 0.5
        self.egg_counter =0
        self.eggs = [(0.2, 0.5), (0.4, 0.5), (0.8, 0.3), (0.6, 0.2), (0.5, 0.6), (0.3, 0.4), (0.9, 0.5), (0.7, 0.6)]
        self.eggs_collected = [0] * len(self.eggs)
        self.health = 1.0
        self.state = np.array([self.character_x, self.character_y, self.enemy_x, self.enemy_y, self.health, self.egg_counter])

        return self.state


#general enemy patrolling - the same as the phaser game
    def initialize_enemy(self):
       
        return {
            'x': 0,
            'patrol_area': {'start': 0, 'end': 100},
            'speed': 50,
            'direction': 1,
            'throw_cooldown': False,
            'player_in_area_timer': 0,
            'throw_delay': 12000,
            'proximity_radius': 100,
            'face_direction': 0
        }

    def step(self, action):
        #left. right. jump
        if action == 0:
            self.character_x = max(self.character_x - 0.1, 0)
        elif action == 1:
            self.character_x = min(self.character_x + 0.1, 1)
        elif action == 2:
            if self.character_y == 0.5:
                self.character_y = 0.7
        #grvity for jump
        if self.character_y > 0.5:
            self.character_y = max(self.character_y - 0.1, 0.5)
        #based on user location we need ot have the user move
        self.enemy_x += 0.01 if self.character_x > self.enemy_x else -0.01
        if np.random.rand() <0.1:
            self.thrown_weapons.append([self.enemy_x, self.enemy_y])


        for weapon in self.throw_weapons:
            weapon[0] +=

        #reward negative if hit, positive if you collect eggs and if you do not get hit by enemy
        #if user runs into x location, they die -100
        
        reward =0
        if self.character_x ==self.enemy_x and self.character_y ==self.enemy_y:
            self.health -=0.1
            reward -=1
        if self.health <=0:
            done = True
            reward -= 100
        elif self.egg_counter == len(self.eggs):
            done = True
            reward += 100
        else:
            done = False
            reward +=1 
        
        for weapon in self.thrown_weapons:
            if np.linalg.norm([self.character_x - weapon[0],self.character_y - weapon[1]]) <0.1:
                self.health -= 0.1
                reward -=1
                self.thrown_weapons.remove(weapon)

        
        self.state = np.array([self.character_x, self.character_y, self.enemy_x, self.enemy_y, self.health, self.egg_counter])
        return self.state, reward, done, {}
    def render(self,mode = 'human' ):
        pass





    def update_enemy_behavior(self):
        # Update enemy patrol and throwing logic here
        enemy = self.enemy
        # Example patrol logic
        if enemy['x'] <= enemy['patrol_area']['start']:
            enemy['direction'] = 1
            enemy['face_direction'] = 1
        elif enemy['x'] > enemy['patrol_area']['end']:
            enemy['direction'] = -1
            enemy['face_direction'] = 0
        
        # Move enemy
        enemy['x'] += enemy['speed'] * enemy['direction']
        
        # Proximity and throwing logic (simplified)
        distance = np.linalg.norm(self.state[:2] - np.array([enemy['x'], 0]))  # Example player position in state
        if distance < enemy['proximity_radius']:
            enemy['player_in_area_timer'] += 1  # Example delta as 1
            if enemy['player_in_area_timer'] >= enemy['throw_delay'] and not enemy['throw_cooldown']:
                self.throw_item(enemy)
        else:
            enemy['player_in_area_timer'] = 0

    def throw_item(self, enemy):
        # Implement throwing logic
        enemy['throw_cooldown'] = True
        # Reset cooldown after delay
        enemy['throw_cooldown'] = False  # This should be delayed, consider using threading or a similar mechanism

    def render(self, mode='human'):
        # Optionally implement rendering of the game state
        pass

# Example usage
env = PhaserGameEnv()
state = env.reset()
print(state)