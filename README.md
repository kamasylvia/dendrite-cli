# Dendrite-script

Initialize and run dendrive with python scripts.

# Requirements

- git
- docker
- docker-compose
- [GitPython](http://gitpython.readthedocs.org/)
- `./local/bin` in `$PATH`

# Initialization

```sh
# Install requirements
pip3 install GitPython
# or
pip3 install -r requirements.txt

# From Azure DevOps
git clone https://kamasylvia@dev.azure.com/kamasylvia/Kamasylvia/_git/dendrite <local_repo>

# From GitHub
git clone https://github.com/kamasylvia/dendrite-cli.git

cd <local_repo>
pip3 install .
```

then

```sh
cd <target_path>
dendrite init

# or

dendrite init --target <target_path>
```

# Configs

Edit `<target_path>/docker-compose.monolith.yml`

```yml
version: '3.4'
services:
  postgres:
    hostname: postgres
    image: postgres:14
    restart: always
    volumes:
      - ./postgres/create_db.sh:/docker-entrypoint-initdb.d/20-create_db.sh
      # To persist your PostgreSQL databases outside of the Docker image,
      # to prevent data loss, modify the following ./path_to path:
      #   - ./path_to/postgresql:/var/lib/postgresql/data
      - ./postgres/postgresql:/var/lib/postgresql/data
```

Edit `<target_path>/config/dendrite.yaml`

```yml
database:
  # connection_string: postgresql://username:password@hostname/dendrite?sslmode=disable
  connection_string: postgresql://dendrite:itsasecret@postgres/dendrite?sslmode=disable
  # max_open_conns: 100
  max_open_conns: 97
  max_idle_conns: 5
  conn_max_lifetime: -1
```

# Run

```sh
cd <target_path>
dendrite compose up
```

# Stop running

```sh
cd <target_path>
dendrite compose down -i
```

# Remove all images

```sh
cd <target_path>
dendrite compose down -i
```

# Remove all containers, images, volumes, and networks

```sh
cd <target_path>
dendrite compose down -a
```

# Uninstall

```sh
pip3 uninstall dendrite-cli
```
