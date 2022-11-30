import git, shutil
import subprocess
from typing import Iterable
from pathlib import Path

sparse_paths = [
    "dendrite-sample.monolith.yaml",
    "build/docker/docker-compose.monolith.yml",
    "build/docker/postgres",
]

generate_key_script = """docker run --rm --entrypoint="" \
  -v $(pwd):/mnt \
  matrixdotorg/dendrite-monolith:latest \
  /usr/bin/generate-keys \
  -private-key /mnt/matrix_key.pem \
  -tls-cert /mnt/server.crt \
  -tls-key /mnt/server.key"""


def sparse_clone(target: str, url: str, sparse_paths: Iterable[str]):
    """
    Clone git repository with sparse checkouts.

    :param target:
        target path.

    :param url:
        URL of remote repo.

    :param sparse_paths:
        List of remote sparse paths.
    """
    temp_path = Path(target) / "temp"

    # rm -rf <target>
    shutil.rmtree(temp_path, ignore_errors=True)

    # git init temp && cd temp
    with git.Repo.init(temp_path) as repo:
        # git sparse-checkout set <sparse_paths>
        repo.git.execute(f"git sparse-checkout set {' '.join(sparse_paths)}".split())

        # git remote add <url>
        origin = repo.create_remote("origin", url)

        # git pull origin main
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)


def dendrite_init(args):
    temp_path = Path(args.target) / "temp"

    # git clone
    sparse_clone(args.target, args.url, args.sparse_paths or sparse_paths)

    # download docker-compose.yaml
    shutil.copytree(temp_path / "build" / "docker", args.target, dirs_exist_ok=True)

    # generate keys under <target>
    subprocess.run(generate_key_script, shell=True, cwd=args.target)

    # copy config files and keys to <target>/config
    target_path = Path(args.target)
    config_path = target_path / "config"
    config_path.mkdir(exist_ok=True)
    shutil.move(temp_path / sparse_paths[0], config_path / "dendrite.yaml")
    shutil.move(target_path / "matrix_key.pem", config_path / "matrix_key.pem")
    shutil.move(target_path / "server.crt", config_path / "server.crt")
    shutil.move(target_path / "server.key", config_path / "server.key")

    if args.delete_temp:
        shutil.rmtree(temp_path)
