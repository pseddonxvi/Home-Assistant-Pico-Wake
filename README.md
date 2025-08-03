# Home-Assistant-Pico-Wake
Alternative to Wake on LAN that uses a Pico W acting as an HID to send a keypress through Home Assistant to wake a computer.

Designed for Circuit Python version 9

Import all the files inside the "Pico" folder to your RPi Pico W.

Add the shell command from shellcommand.yaml to your HA configuration.yaml

Add the wakepc.py file to the same directory as your HA configuration.yaml

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
