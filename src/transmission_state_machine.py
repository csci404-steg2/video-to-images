from moviepy.editor import *

from dataclasses import dataclass

from .handshake import HandshakeMeta, HandshakeColors

"""
VERY UNFINISHED AND CURRENTLY NOT BEING USED.
"""

@dataclass
class TransmissionStatus:
    success: bool

    # if success true
    request_transition_to: TransmissionState

    # if success false
    failure_reason: str
    failed_at: str

class TransmissionState:
    def __init__(self, name):
        self.name = name
        self.output_states = set()

        self.identifier = hash(name)

    def add_transition_to(self, state):
        """add a transition to the given state
        params:
            state(TransmissionState) - state to add to transition list
        """
        self.output_states.update(state.identifier)
    
    def can_transition_to(self, state):
        """test if the state can transition to the given one
        params:
            state(TransmissionState) - state to test transitionability
        returns:
            true if state can be transitioned to, otherwise false
        """
        return state.identifier in self.output_states

    def verify(self, clip: VideoFileClip, start_time: str, end_time: str):
        raise NotImplementedError("child state must implement a verify routine.")
            

class TransmissionStateMachine:
    # for ease of reference and to keep strings more tidy
    STATE_INIT_FULL_BLACK = "init_full_black"
    STATE_INIT_DEAD_TIME = "init_dead_time"
    STATE_INIT_ALIVE_TIME = "init_alive_time"
    STATE_INIT_OFFSET_TIME  = "init_offset_time"
    STATE_INIT_TRANSMISSION_LENGTH = "init_transmission_length"
    STATE_DELAY_WAIT_OFFSET = "delay_wait_offset"
    STATE_CAPTURE_ACTIVE = "capture_active"
    STATE_CAPTURE_DEAD = "capture_dead"
    STATE_CAPTURE_END = "capture_end"

    def __init__(self):
        self._init_states()

        # dead time is the default first state
        self._starting_state = self.states[STATE_INIT_FULL_BLACK]
        # start at starting state
        self._current_state = self._starting_state

    def _init_states(self):
        """initialize the default states of the machine"""
        # base set of states
        self.states = {
            STATE_INIT_FULL_BLACK  : TransmissionState(STATE_INIT_FULL_BLACK),
            STATE_INIT_DEAD_TIME   : TransmissionState(STATE_INIT_DEAD_TIME),
            STATE_INIT_ALIVE_TIME  : TransmissionState(STATE_INIT_ALIVE_TIME),
            STATE_INIT_OFFSET_TIME : TransmissionState(STATE_INIT_OFFSET_TIME),
            STATE_INIT_TRANSMISSION_LENGTH:TransmissionState(STATE_INIT_TRANSMISSION_LENGTH),
            STATE_DELAY_WAIT_OFFSET: TransmissionState(STATE_DELAY_WAIT_OFFSET),
            STATE_CAPTURE_ACTIVE   : TransmissionState(STATE_CAPTURE_ACTIVE),
            STATE_CAPTURE_DEAD     : TransmissionState(STATE_CAPTURE_DEAD),
            STATE_CAPTURE_END      : TransmissionState(STATE_CAPTURE_END)
        }

        # full black signifies start of handshake, next frame transmits dead time
        self.states[STATE_INIT_FULL_BLACK].add_transition_to(self.states[STATE_INIT_DEAD_TIME])
        # after dead time is transmitted, alive time is transmitted
        self.states[STATE_INIT_DEAD_TIME].add_transition_to(self.states[STATE_INIT_ALIVE_TIME])
        # after alive its the offset time
        self.states[STATE_INIT_ALIVE_TIME].add_transition_to(self.states[STATE_INIT_OFFSET_TIME])
        # after the offset time is the transmission length
        self.states[STATE_INIT_OFFSET_TIME].add_transition_to(self.states[STATE_INIT_TRANSMISSION_LENGTH])
        # after the length we wait offset time (can be zero)
        self.states[STATE_INIT_TRANSMISSION_LENGTH].add_transition_to(self.states[STATE_DELAY_WAIT_OFFSET])
        # after we have waited the offset time, we start to actively capture information
        self.states[STATE_DELAY_WAIT_OFFSET].add_transition_to(self.states[STATE_CAPTURE_ACTIVE])

        # actively capture info, then move to dead time
        self.states[STATE_CAPTURE_ACTIVE].add_transition_to(self.states[STATE_CAPTURE_DEAD])
        # after dead time the capture either ends or we capture more information
        self.states[STATE_CAPTURE_DEAD].add_transition_to(self.states[STATE_CAPTURE_ACTIVE])
        self.states[STATE_CAPTURE_DEAD].add_transition_to(self.states[STATE_CAPTURE_END])

    def run_at(self, clip, starting_time):
        transmission = Transmission()
        test_time = starting_time

        state_response = self._starting_state.verify(clip, test_time, transmission)
        
        while state_response == RESPONSE.GOOD:
            self._current_state = self.states[state_response.request_transition_to]
            test_time += state_response.consumed_time

            state_response = self._current_state.verify(clip, test_time, transmission)

        if state_response == RESPONSE.FAILURE:
            return 

        if state_response == RESPONSE.FINISHED:
            return handshake

    def get_current_state(self):
        """get the current state of the machine"""
        return self._current_state

    def transition_to(self, state):
        """transition to a new state
        params:
            state(str or TransmissionState) - state to transition to
        raises:
            ValueError - state given as string does not exist
            RuntimeError - state cannot be transitioned to from current
        """
        if type(state) == str:
            if state not in self.states:
                raise ValueError("Given state does not exist.")
            state = self.states[state]

        if not self._current_state.can_transition_to(state):
            raise RuntimeError(
                f"Cannot transition to given state {state.name} from state {self._current_state.name}.")
        
        self._current_state = state
    
    def auto_transition(self):
        """if the current state only has one output, transition to it automatically
        raises:
            RuntimeError - current state has more than one output or no outputs
        """
        if len(self._current_state.output_states) != 1:
            raise RuntimeError(
                f"Cannot auto transition as state does not have exactly 1 output (actual: {len(self._current_state.output_states)})")
        # pop only state that can be transitioned to, transition to it, then add it back 
        # onto the state it was taken from
        temp = self._current_state
        self._current_state = self._current_state.output_states.pop()
        temp.output_states.add(self._current_state)

    def reset_machine(self):
        """reset the machine back to the starting state"""
        self._current_state = self._starting_state