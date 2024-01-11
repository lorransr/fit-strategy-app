# fit-strategy-app


## Features 🌈

1. **FastAPI Magic** - Because speed is not just about Fast & Furious movies!
2. **PostgreSQL Integration** - Store data like a pro. No more data loss nightmares!
3. **Docker Integration** - Set sail with a consistent environment. Because why let tech discrepancies ruin your day?
4. **Fixes, Fixes, Fixes** - All those bugs? Gone! (Well, most of them, but let's be optimistic!)

## Setup & Run 🏃‍♂️

To set this baby up:

If you don't have one yet, set up a .env file with your configuration.  For a basic version for local testing use:
```bash
cp dot-env-template .env
```
Be aware that .env is *excluded from git* because it contains secrets, API keys and so on.  **Never put your .env file into git.**

Then build and start the test/debug stack with:
```bash
docker-compose up --build
```

Then:
- Visit http://localhost:4000/docs for the interactive API docs (Swagger). For initial super-username and password to first authenticate see your **.env** file.
- Modify your code, which is linked into the *fastapi-app* container and watch uvicorn auto-restart your app when changes have been made.
- Run pytest in your container with `docker exec fastapi-app bash ./test.sh [optional parameters]`
- Visit http://localhost:5050/ for the PostgreSQL administrator. Upon first use you'll need to register your DB server using your **.env** file.


## Contribute! 🤝

Did you find more ancient bugs lurking around? Or perhaps you unearthed a potential treasure in the form of a feature? Pull requests are more than welcome. After all, multiple minds make light work. Let's polish this backend to be more radiant than a starry night! 💫

## Credits & A Bow 🎖️

A grand salute to the maestro behind the original `full-stack-fastapi-postgresql`. Their innovative groundwork laid the foundation, allowing this revamped symphony to come to life.


## Useful commands

start app: docker exec -it fastapi-app bash

testing: pytest app/tests/crud/test_user.py
