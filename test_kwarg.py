import click
@click.command()
@click.option("--disc", is_flag=True, default=False)
@click.option("--disk", "disc", is_flag=True, default=False)
def cli(disc):
    print("disc =", disc)

if __name__ == "__main__":
    cli(["--disk"], standalone_mode=False)
