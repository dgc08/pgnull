import pygame.time

class Clock:
    def __init__(self):
        self.pygame_obj = pygame.time.Clock()
        self.tick = self.pygame_obj.tick

        self.event_counter = 1
        self.time_events = {}
        self.time_event_functions = {}

        #self.at_tick_funcs = {}

    def schedule(self, function, interval:float, loops=0):
        interval = int(interval*1000)

        event = pygame.USEREVENT + self.event_counter #self.time_events.get(interval, pygame.USEREVENT + self.event_counter)
        self.time_events[interval] = event
        pygame.time.set_timer(event, interval, 1)
        self.event_counter += 1

        try:
            self.time_event_functions[event].append(function)
        except KeyError:
            self.time_event_functions[event] = [function]
        else:
            time_at = pygame.time.get_ticks() + interval
            self.at_tick_funcs[time_at] = function


    def check_schedule(self, event):
        to_execute = []

        for i in self.time_events.values():
            if event == i:
                for func in self.time_event_functions[event]:
                    to_execute.append( func ) # if we execute the function directly, we may get unintended side effects

        # current = pygame.time.get_ticks()
        # if self.at_tick_funcs:
        #     for time_at in list(self.at_tick_funcs.keys()):
        #         if time_at >= current:
        #             to_execute.append(self.at_tick_funcs.pop(time_at))

        for f in to_execute:
            f()
