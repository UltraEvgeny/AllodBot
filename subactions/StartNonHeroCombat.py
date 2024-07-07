from subactions.SubactionWithRotation import SubactionWithRotation, sleep_c
from asyncio import sleep


class StartNonHeroCombat(SubactionWithRotation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotation = [
            lambda: self.parent_model.kb.click(['tab']),
            sleep_c(0.1),
            lambda: (self.parent_model.kb.click(['3']) if not self.parent_model.screen_scanner.state.target_is_hero else sleep_c(0)),
            sleep_c(0.3),
            lambda: self.parent_model.kb.click(['arrow_left'], delay=0.6),
        ]

    @property
    def success_condition(self):
        return self.parent_model.screen_scanner.state.is_combat_me
