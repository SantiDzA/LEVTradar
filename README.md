#LEVTradar
This is a simple Telegram bot that sends a message whenever a plane is found in the vicinity of an airport (Vitoria LEVT/VIT in this case). It uses data from [Airplanes.live](https://airplanes.live/) ([API guide](https://airplanes.live/api-guide/)).

## Features
- The bot will send messages to a single Telegram group.
- As the bot determines whether a given aircraft is approaching an airport based on positional data only, false positives can occur, particularly if there are other airports nearby. The callsigns of regular flights arriving/departing from other airports can be added to   the [false_positive_callsigns.json](https://github.com/SantiDzA/LEVTradar/blob/main/false_positive_callsigns.json) file.
- The operator of the bot can edit false_positive_callsigns.json by chatting directly with the bot. The bot will ignore messages sent by other users.
