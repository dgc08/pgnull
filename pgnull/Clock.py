import pygame.time

class Clock:
    def __init__(self):
        self.pygame_obj = pygame.time.Clock()
        self.tick = self.pygame_obj.tick

        self.event_counter = 1
        self.time_events = {}
        self.time_event_functions = {}

    def schedule(self, function, interval:float):
        interval = int(interval*1000)
        event = self.time_events.get(interval, pygame.USEREVENT + self.event_counter)
        self.time_events[interval] = event
        pygame.time.set_timer(event, interval)

        self.event_counter += 1

        try:
            self.time_event_functions[event].append(function)
        except KeyError:
            self.time_event_functions[event] = [function]

    def check_schedule(self, event):
        for i in self.time_events.values():
            if event == i:
                for func in self.time_event_functions[event]:
                    func()
