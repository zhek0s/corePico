"""Importing states for dict"""
from core.StateMachine.States.TestState import TestState
from core.StateMachine.States.BootState import BootState

class ConfigStates:
    StateMachineStates={
        "TestState":TestState, # type: ignore
        "BootState":BootState # type: ignore
    }
