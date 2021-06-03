# Student-arena-bot

Discord bot for managing knowledge control system on a discord server. Bot creates and processes "arenas", where are the
players take a test in the form of a battle royale competition. Also, bot has simple system for getting and representing
statistic data about the participation of players. Basically, bot represents an interface for a teacher to manage and
running tests in different topics.

## Building and running

### Build backend and DB

```
$ docker-compose up --build
```

After build service available on http://0.0.0.0:8000

### Migrations

```
$ docker-compose run backend python3 manage.py makemigrations
$ docker-compose run backend python3 manage.py migrate
```

## Basic functionality

Bot was made with discordpy API and uses its basic classes and methods. By creating specific roles, channels and
reactions bot organizing tests. With this, bot can get reactions from players/users and process it. These features
provide main game logic and rules.

## Arena rules

Bot creates and process arenas(battle, game) with the next rules:

- players join an arena and play round by round;
- round consists of a question with 4 variants of answers;
- every question has only one right answer;
- time for answering is limited;
- when time is up, made answers recorded and processed;
- for every right answer player gets a point;
- if player made wrong answer, he out, in other way he passes to the next round;
- the winner is the one who became the last player on the arena or answered all questions.

## Features

1. Creating and launching arena battles on a server with parameters like amount of questions, time for answering,
   topics and processes it according to the rules;
2. Collecting and processing data about players game results;
3. Storing data;
4. Representing data about players.
5. Additional commands for deleting arenas, cleaning channels and other.

## Additional

- Create testing system. Feature, which makes bot be able to read a code provided by user, start docker container and
  test this code with specific configuration;
- Make command for deploying bot on any server.
