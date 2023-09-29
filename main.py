from machine import Pin,I2C
from config import ConfigPico

from core.StateMachine.StateMachineRunner import StateMachineRunner
from core.Debug import Debug

from core.StateMachine.configStates import ConfigStates

from lib.th06 import TH06
from lib.buttons import Buttons
from lib.display import Display

sdaP=Pin(2)
sclP=Pin(3)
i2cHandler=I2C(1, scl=sclP, sda=sdaP, freq=2000000)
th06=TH06(i2cHandler)
display=Display(i2cHandler)
buttons= Buttons()

logger=Debug()
logger.enablePrintConsole=True
logger.logText="StateMachine"
logger.warningText="StateMachine"
logger.errorText="StateMachine"

stateMachine=StateMachineRunner(logger)

state=ConfigPico.StateMachine["startUpState"]
stateClass=ConfigStates.StateMachineStates[state]
runState=stateClass(display.getHandler())
stateMachine.setState(runState)

def main():
    while True:
        stateMachine.Update()

if __name__ == "__main__":
    main()
