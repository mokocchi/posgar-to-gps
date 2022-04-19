from pathlib import Path
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
    conversor = getConversor(zone, decimal_point)
    if conversor:
        lat_long, error = conversor.convert(x, y, bool(as_degrees))
        if error:
            typer.secho(
                f'Converting failed with "{ERRORS[error]}"', fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho("%s\t%s" % (
                lat_long["lat"], lat_long["long"]), fg=typer.colors.BLUE)


@app.command()
def convert_batch(
    batch_file: Optional[str] = typer.Option(
        None,
        "--file",
        "-f",
        help="Batch file",
        is_eager=True,
    ),
    delimiter: Optional[str] = typer.Option(
        None,
        "--delimiter",
        "-d",
        help="Batch element delimiter",
        is_eager=True,
    ),
    decimal_point: Optional[str] = typer.Option(
        ".",
        "--decimal-point",
        "-D",
        help="Decimal point",
        is_eager=True
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
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output-file",
        "-o",
        help="Output file",
        is_eager=True,
    )
) -> None:
    """Convert the x and y POSGAR coordinates to latitude and longitude"""
    if(batch_file and not Path(batch_file).exists()):
        typer.secho(
            f'Batch file not found', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if(not output_file):
        typer.secho(
            f'Output file not specified', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    conversor = getConversor(zone, decimal_point)
    if conversor:
        status, error = conversor.convert_batch(
            bool(as_degrees), Path(batch_file) if batch_file else None, delimiter, decimal_point, Path(output_file))
        if error:
            typer.secho(
                f'Converting failed with "{ERRORS[error]}"', fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho("Conversion succeeded with status: {}".format(
                status), fg=typer.colors.GREEN)


def getConversor(zone: Optional[str], decimal_point: Optional[str]):
    if (not zone and zone != 0):
        typer.secho(
            'POSGAR zone not specified',
            fg=typer.colors.RED,
        )
    else:
        if(decimal_point and decimal_point != "."):
            x = x.replace(decimal_point, ".")
            y = y.replace(decimal_point, ".")
        try:
            zone = int(zone)
            if(zone < 1 or zone > 7):
                typer.secho(
                    'Zone must be a value between 1 and 7',
                    fg=typer.colors.RED,
                )
            else:
                return conversor.Conversor(zone)
        except ValueError:
            typer.secho(
                'Zone is not a number',
                fg=typer.colors.RED,
            )