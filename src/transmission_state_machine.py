

class TransmissionState:
    def __init__(self, name):
        self.name = name
        self.output_states = set()

        self.identifier = hash(name)

    def add_transition_to(state):
        self.output_states.update(state.identifier)
    
    def can_transition_to(state):
        return state.identifier in self.output_states
            

class TransmissionStateMachine:
    def __init__(self):
        self._init_states()

    def _init_states(self):
        self.states = {
            "init_full_black"  : TransmissionState("init_full_black"),
            "init_dead_time"   : TransmissionState("init_dead_time"),
            "init_alive_time"  : TransmissionState("init_alive_time"),
            "init_offset_time" : TransmissionState("init_offset_time"),
            "init_transmission_length":TransmissionState("init_transmission_length"),
            "delay_wait_offset": TransmissionState("delay_wait_offset"),
            "capture_active"   : TransmissionState("capture_active"),
            "capture_dead"     : TransmissionState("capture_dead"),
            "capture_end"      : TransmissionState("capture_end")
        }

        self.states["init_full_black"].add_transition_to(self.states["init_dead_time"])
        self.states["init_dead_time"].add_transition_to(self.states["init_alive_time"])
        self.states["init_alive_time"].add_transition_to(self.states["init_offset_time"])
        self.states["init_offset_time"].add_transition_to(self.states["init_transmission_length"])
        self.states["init_transmission_length"].add_transition_to(self.states["delay_wait_offset"])
        self.states["delay_wait_offset"].add_transition_to(self.states["capture_active"])

        self.states["capture_active"].add_transition_to(self.states["capture_dead"])
        self.states["capture_dead"].add_transition_to(self.states["capture_active"])
        self.states["capture_dead"].add_transition_to(self.states["capture_end"])

