# Home-Assistant-Pico-Wake
An alternative to Wake on LAN that uses a Pico W emulating a keypress triggered by a command sent through Home Assistant to wake a computer. 

Designed for Circuit Python version 9

### Pico W setup

Install Circuit Python version 9 from here https://circuitpython.org/board/raspberry_pi_pico_w/

Import all the files inside the "Pico" folder to your RPi Pico W.
 
- Enter your WiFi network details into the code.py file

Plug your Pico W into the computer you want to wake

### Network Setup

Configure a static IP address for your Pico W. This will be what you enter into the /wakepc.py file

### Home Assistant setup

Add the shell command from shellcommand.yaml to your HA configuration.yaml

Type your Pico W's IP address into the wakepc.py file and put it in the same directory as your HA configuration.yaml

Then do:
1. Go to Settings → Automations & Scenes → Automations
2. Click "Create Automation"
3. Choose “Start with an empty automation”
4. Give it a name
5. Under Trigger:
    - Trigger type: State
    - Entity: input_button.wake_pc
    - Leave “From” and “To” fields blank (so any press triggers it)
6. Under Action:
    - Action type: Call service
    - Service: shell_command.run_wake_script
7. Click Save

You can now add a card to your HA dashboard using the entity "input_button.wake_pc"
