
# Chess Coop

Chess Coop is an online multiplayer chess game built with Vue.js for the frontend and Django for the backend. The project uses Docker for easy setup and deployment. It leverages `chess.js` for chess game logic and `chessboard.js` for the chessboard UI.


## Features

- Create and join chess rooms
- Play real-time multiplayer chess games
- Persistent game state using Redis
- Responsive UI built with Vuetify
- WebSocket support for real-time communication

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:

```sh
git clone https://github.com/your-username/chess-coop.git
cd chess-coop
```
 
2. Build and run the Docker containers:

```sh
docker-compose up --build
```

3. Migrations

```sh
docker-compose run chesscoop_backend python manage.py migrate
```

4. Access the application:
Open your web browser and go to http://localhost:3000
