# Laptimes-Leaderboard

This simple utility tracks laptime submissions from Assetto Corsa (it could be extended to many racing games/simulators) and displays it on a leaderboard that refreshes automatically. It consists of a Ruby on Rails app for the server-side and a Python client running inside or alongside the racing game of choice.

Since the Rails server accepts HTTP POST requests, one could even use this for real-life racing if the vehicle had real-time capability to send POSTs.

[//]: # (Image References)
[image1]: Progress2.jpg "Runtime Example 1"
[image2]: Progress3.jpg "Runtime Example 2"

## Install

Although this app has not been deployed online yet, you can test it on a local machine if you have Ruby on Rails and Assetto Corsa. Clone this repository, navigate to the repo folder and starter the server with

```bash
git clone https://github.com/briansfma/laptimes-leaderboard.git
cd laptimes-leaderboard
rails server
```

Once the Rails server is up, you should be able to see the leaderboard by navigating to http://localhost:3000 in your browser.

The Python client app is found in `/python/toleaderboard` in this repository. To install it, copy the `toleaderboard` folder to the `apps/python` folder in your main `assettocorsa` installation directory. On a typical Windows installation that directory should be something like 

```
C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\python
```

 Then launch Assetto Corsa, enter Settings > General > scroll to the bottom and check the "toleaderboard" box to enable the app. It will be available to turn on as soon as you start a driving session.

## Usage

Once you have the Python app enabled within Assetto Corsa, it will send an update to the leaderboard upon the completion of a valid lap.

![alt text][image1]

Your Steam username and track/config/vehicle settings are automatically gathered from the game and submitted with the laptime and a unique identifier (allows the server to reject duplicate submissions). The server will then refresh the browser to show the update in almost real-time.

![alt text][image2]

## Known issues/workarounds/hacks

More time was spent debugging Assetto Corsa than actually prototyping this app. The embedded Python used in AC appears to lack several critical DLLs and libraries to actually use HTTP POST; these have been extracted now from a separate installation of Python 3.3 and included in the main repository.

More to cover in a future update:

* Ruby version

* System dependencies

* Configuration

* ...
