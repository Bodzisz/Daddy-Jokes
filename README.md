# Daddy-Jokes
Daddy-Jokes is a flask CRUD application where you can manage some unfunny, silly jokes.

### 1. Setup ###
To run the app locally you need to have docker installed on your computer.
Then you just need to run compose up in the project directory:
````
docker-compose up --build
````
If you are on mac with apple silicon (arm) chip, there is an alterntive docker-compose file:
````
docker-compose -f docker-compose-arm.yml up --build
````
### 2. Features ###
- Jokes CRUD (create, read, update, delete)
- User authorization
- Joke search
- Joke sorting
- Likes
- Pagination
- Random Joke on landing page  
- Very unfunny jokes
### 3. Technology Stack ###
- flask
- docker  
- mongodb (jokes)
- mysql (user authorization)
- sqlalchemy (ORM)
- bootstrap
- jinja2
