from subactions.SubactionWithRotation import SubactionWithRotation, sleep_c
from asyncio import sleep


class FindNonHeroCombatTarget(SubactionWithRotation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.single_target = True
        self.targets_changed = 0
        self.rotation = [
            lambda: self.parent_model.kb.click(['tab']),
            sleep_c(0.25),
            self.increase_target_counter,
            sleep_c(0.25),
            lambda: self.parent_model.kb.click(['tab']),
            sleep_c(0.5),
            self.increase_target_counter,
            lambda: self.parent_model.kb.click(['arrow_left'], delay=0.4),
        ]

    async def reset(self):
        await super().reset()
        self.targets_changed = 0

    async def increase_target_counter(self):
        self.targets_changed += 1

    @property
    def success_condition(self):
        if self.single_target:
            return self.parent_model.screen_scanner.state.is_combat_me \
                and self.parent_model.screen_scanner.state.is_combat_target \
                and not self.parent_model.screen_scanner.state.target_is_hero \
                and not self.parent_model.screen_scanner.state.target_is_invul \
                or not self.parent_model.screen_scanner.state.is_combat_me
        else:
            return self.parent_model.screen_scanner.state.is_combat_me \
                and self.parent_model.screen_scanner.state.is_combat_target \
                and not self.parent_model.screen_scanner.state.target_is_hero \
                and not self.parent_model.screen_scanner.state.target_is_invul \
                and self.targets_changed > 0 \
                or not self.parent_model.screen_scanner.state.is_combat_me
                # and (not self.parent_model.screen_scanner.state.target_has_neurotoxin or not self.parent_model.screen_scanner.state.is_nearby_enemy_combat_unit_without_neurotoxin) \
