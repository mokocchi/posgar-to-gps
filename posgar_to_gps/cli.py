from typing import Optional

import typer

from posgar_to_gps import ERRORS, __app_name__, __version__, conversor

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def convert(x: Optional[str] = typer.Option(
        None,
        "--x-coordinate",
        "-x",
        help="X coordinate (POSGAR)",
        is_eager=True,
    ),
    y: Optional[str] = typer.Option(
        None,
        "--y-coordinate",
        "-y",
        help="Y coordinate (POSGAR)",
        is_eager=True,
),
    decimal_point: Optional[str] = typer.Option(
        None,
        "--decimal-point",
        "-d",
        help="Decimal point",
        is_eager=True,
),
    zone: Optional[str] = typer.Option(
        None,
        "--zone",
        "-z",
        help="POSGAR zone",
        is_eager=True,
),
    as_degrees: bool = typer.Option(
        False,
        "--as-degrees",
        "-D",
        help="Show the result as degrees",
        is_eager=True,
)
) -> None:
    """Convert the x and y POSGAR coordinates to latitude and longitude"""
    conversor = getConversor(x, y, zone, decimal_point, as_degrees)
    if conversor:
        lat_long, error = conversor.convert(bool(as_degrees))
        if error:
            typer.secho(
                f'Converting failed with "{ERRORS[error]}"', fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho("%s\t%s" % (
                lat_long["lat"], lat_long["long"]), fg=typer.colors.BLUE)


def getConversor(x: Optional[str], y: Optional[str], zone: Optional[str], decimal_point: Optional[str], as_degrees: Optional[str]):
    if (not x and x != 0):
        typer.secho(
            'X coordinate not specified',
            fg=typer.colors.RED,
        )
    elif (not y and y != 0):
        typer.secho(
            'y coordinate not specified',
            fg=typer.colors.RED,
        )
    elif (not zone and zone != 0):
        typer.secho(
            'POSGAR zone not specified',
            fg=typer.colors.RED,
        )
    else:
        if(decimal_point and decimal_point != "."):
            x = x.replace(decimal_point, ".")
            y = y.replace(decimal_point, ".")
        try:
            x = float(x)
            try:
                y = float(y)
                try:
                    zone = int(zone)
                    if(zone < 1 or zone > 7):
                        typer.secho(
                            'Zone must be a value between 1 and 7',
                            fg=typer.colors.RED,
                        )
                    else:
                        return conversor.Conversor(x, y, zone)
                except ValueError:
                    typer.secho(
                        'Y coordinate not a number',
                        fg=typer.colors.RED,
                    )
            except ValueError:
                typer.secho(
                    'Y coordinate not a number',
                    fg=typer.colors.RED,
                )
        except ValueError:
            typer.secho(
                'X coordinate not a number',
                fg=typer.colors.RED,
            )
