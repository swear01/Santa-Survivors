    def nearest_enemy(self):
        if not self.enemies : return None
        return min(self.enemies, key=lambda enemy: norm(enemy.pos-self.pos))