import subprocess

cmd_up = "docker-compose -f docker-compose.monolith.yml up -d"
cmd_down = "docker-compose -f docker-compose.monolith.yml down"
cmd_restart = "docker-compose -f docker-compose.monolith.yml restart"
cmd_rmi = "docker-compose -f docker-compose.monolith.yml down --rmi all"
cmd_rma = "docker-compose -f docker-compose.monolith.yml down --rmi all -v"


def compose(args):
    if hasattr(args, "up"):
        subprocess.run(cmd_up, shell=True)
    elif hasattr(args, "restart"):
        subprocess.run(cmd_restart, shell=True)
    elif hasattr(args, "down"):
        if args.images:
            subprocess.run(cmd_rmi, shell=True)
        elif args.all:
            subprocess.run(cmd_rma, shell=True)
        else:
            subprocess.run(cmd_down, shell=True)
