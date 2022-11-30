# Dendrite-script

Initialize and run dendrive with python scripts.

# Requirements
- git
- docker
- docker-compose
- [GitPython](http://gitpython.readthedocs.org/)

# Initilize

## Method 1

```sh
python3 sample/__init__.py init --target <target_path>
```

## Method 2 - recommanded

```sh
pip3 install .
```

```sh
cd <target_path>
dendrite init

or

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
python3 sample/__init__.py compose up
```

## Method 2 - recommanded

```sh
cd <target_path>
dendrite compose up
```

# Stop running

## Method 1

```sh
cd <target_path>
python3 sample/__init__.py compose down
```

## Method 2 - recommanded

```sh
cd <target_path>
dendrite compose down -i
```

# Remove all images

## Method 1

```sh
cd <target_path>
python3 <root>/sample/__init__.py compose down -i
```

## Method 2 - recommanded

```sh
cd <target_path>
dendrite compose down -i
```

# Remove all containers, images, volumes, and networks

## Method 1

```sh
cd <target_path>
python3 <root>/sample/__init__.py compose down -a
```

## Method 2 - recommanded

```sh
cd <target_path>
dendrite compose down -a
```

# Uninstall
If you installed this package with Method 2

To uninstall
```sh
pip3 uninstall dendrite-cli
```