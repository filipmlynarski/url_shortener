#### How to install:
1. install [docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) (please download [version 4.8.2](https://docs.docker.com/desktop/release-notes/#docker-desktop-482)).
2. inside cloned repo, build the container with `docker-compose build`
3. and run the project `docker-compose up`
4. (only after build) apply migrations `docker-compose exec web python manage.py migrate`
---

#### Example usage using curl:
```bash
# start the service
➜  ~ docker-compose up
```

Example requests
```bash
# create alias
➜  ~ curl -d "target=https://szkolawchmurze.org/edukacja-domowa/liceum" localhost:8000/generate
{"target":"https://szkolawchmurze.org/edukacja-domowa/liceum","alias":"http://localhost:8000/68D63D"}

# get target of just created alias
➜  ~ curl http://localhost:8000/68D63D
{"target":"https://szkolawchmurze.org/edukacja-domowa/liceum"}%

# try to generate alias to invalid url
➜  ~ curl -d "target=notfound://szkolawchmurze.org/edukacja-domowa" localhost:8000/generate
{"target":["Enter a valid URL."]}%

# generate second proper alias
➜  ~ curl -d "target=https://szkolawchmurze.org/edukacja-domowa" localhost:8000/generate
{"target":"https://szkolawchmurze.org/edukacja-domowa","alias":"http://localhost:8000/BFC936"}%

# try to generate alias that will point to already existing target
➜  ~ curl -d "target=https://szkolawchmurze.org/edukacja-domowa/liceum" localhost:8000/generate
{"target":"https://szkolawchmurze.org/edukacja-domowa/liceum","alias":"http://localhost:8000/68D63D"}
```
Aliases can also be accessed in admin view at localhost:8000/admin/alias/alias/

---

#### Running tests:
```bash
➜  ~ ./run_tests.sh 
***************
Clean Tests
***************
Stopping url_shortener_2_web_1 ... done
Stopping url_shortener_2_db_1  ... done
Removing url_shortener_2_web_1                ... done
Removing url_shortener_2_web_run_db82f994bd9d ... done
Removing url_shortener_2_db_1                 ... done
Removing network url_shortener_2_default
***************
Start new test session
***************
Creating network "url_shortener_2_default" with the default driver
Creating url_shortener_2_db_1 ... done
Creating url_shortener_2_web_run ... done
Found 12 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............
----------------------------------------------------------------------
Ran 12 tests in 0.072s

OK
Destroying test database for alias 'default'...
***************
Stop containers after tests
***************
Stopping url_shortener_2_db_1 ... done
```
