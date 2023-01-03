# still considering if to use the backend class
class Backend:
    def __init__(self) -> None:
        self.main_page = True
        self.select_character = False
        self.selected_character = ''
        self.start_game = False
        self.tutorial = False
        self.shop = False
        self.paused = False
        self.upgrade = False
        self.upgrade_menu = False
        self.game_over = False
        self.game_over_menu = False
        pass

    @staticmethod
    def draw(screen, *surfaces):
        for surface in surfaces:
            surface.draw(screen)


    
    