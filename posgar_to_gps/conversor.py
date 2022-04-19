import csv
from math import atan, exp, floor, pi, cos, sin, sqrt, tan
from pathlib import Path
import traceback
from typing import Dict, NamedTuple

import typer

from posgar_to_gps import CONVERSION_ERROR, FILE_READ_ERROR, FILE_WRITE_ERROR, PARSE_ERROR, SUCCESS


class ConversionResponse(NamedTuple):
    lat_long: Dict[str, float]
    error: int


class StatusResponse(NamedTuple):
    status: str
    error: int


class Conversor:
    def __init__(self, zone: str) -> None:
        self._zone = zone

    def convert(self, x: float, y: float, as_degrees: bool):
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
        else:
            try:
                x = float(x)
                if(x / 10000000 > 1):
                    typer.secho(
                        'x out of range, value: {}'.format(x),
                        fg=typer.colors.RED,
                    )
                    return StatusResponse('', CONVERSION_ERROR)
                try:
                    y = float(y)
                    if(x / 10000000 > 1):
                        typer.secho(
                            'y out of range, value: {}'.format(y),
                            fg=typer.colors.RED,
                        )
                        return StatusResponse('', CONVERSION_ERROR)
                except ValueError:
                    typer.secho(
                        'Y coordinate is not a number (value: {})'.format(
                            y),
                        fg=typer.colors.RED,
                    )
                    return StatusResponse('', CONVERSION_ERROR)
            except ValueError:
                typer.secho(
                    'X coordinate is not a number (value: {})'.format(
                        x),
                    fg=typer.colors.RED,
                )
                return StatusResponse('', CONVERSION_ERROR)
            [lat, long] = calcuXY(x, y, self._zone)
            if as_degrees:
                return ConversionResponse({"lat": agrad(lat), "long": agrad(long)}, SUCCESS)
            else:
                return ConversionResponse({"lat": lat, "long": long}, SUCCESS)

    def convert_batch(self, as_degrees: bool, batch_file: Path, delimiter: str, decimal_point: str, output_file: Path):
        try:
            with batch_file.open("r") as f:
                try:
                    reader = csv.DictReader(
                        f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
                    with output_file.open("w") as o:
                        writer = csv.DictWriter(o, ["Lat", "Long"])
                        i = 1
                        for row in reader:
                            keys = list(row)
                            try:
                                x = float(row[keys[0]])
                                if(x / 10000000 > 1):
                                    typer.secho(
                                        'x out of range, value: {} (row {})'.format(x, i),
                                        fg=typer.colors.RED,
                                    )
                                    return StatusResponse('', CONVERSION_ERROR)
                                try:
                                    y = float(row[keys[1]])
                                    if(x / 10000000 > 1):
                                        typer.secho(
                                            'y out of range, value: {} (row {})'.format(y, i),
                                            fg=typer.colors.RED,
                                        )
                                        return StatusResponse('', CONVERSION_ERROR)
                                    try:
                                        [lat, long] = calcuXY(x, y, self._zone)
                                        writer.writerow({"Lat": lat, "Long": long})
                                    except Exception:
                                        traceback.print_exc()
                                        typer.secho(
                                            'Conversion error (row {}, values: {} {})'.format(
                                                i, x, y),
                                            fg=typer.colors.RED,
                                        )
                                        return StatusResponse('', CONVERSION_ERROR)
                                except ValueError:
                                    typer.secho(
                                        'Y coordinate is not a number (row {}, value: {})'.format(
                                            i, row[keys[1]]),
                                        fg=typer.colors.RED,
                                    )
                                    return StatusResponse('', CONVERSION_ERROR)
                            except ValueError:
                                typer.secho(
                                    'X coordinate is not a number (row {}, value: {})'.format(
                                        i, row[keys[0]]),
                                    fg=typer.colors.RED,
                                )
                                return StatusResponse('', CONVERSION_ERROR)
                            i += 1
                        return StatusResponse("OK", SUCCESS)
                except OSError:
                    return StatusResponse([], FILE_WRITE_ERROR)        
                except Exception:
                    return StatusResponse([], PARSE_ERROR)
        except OSError:
            return StatusResponse([], FILE_READ_ERROR)


def calcuXY(X, Y, zone):
    f = 1
    FE = 1000000*zone+500000
    FN = 10001965.729
    loncero = (3*zone-75)*pi/180
    Y = Y-FN
    X = X-FE
    epri = 0.0820944380368543
    c = 6399593.62580398
    fipri = Y/(6366197.724*f)
    sigma = c*f/sqrt(1+pow((epri*cos(fipri)), 2))
    a = X/sigma
    A1 = sin(2*fipri)
    A2 = A1*pow(cos(fipri), 2)
    J2 = fipri+A1/2
    J4 = (3*J2+A2)/4
    J6 = (5*J4+A2*pow(cos(fipri), 2))/3
    alzone = (3/4)*pow(epri, 2)
    beta = (5/3)*pow(alzone, 2)
    gama = (35/27)*pow(alzone, 3)
    Bfi = f*c*(fipri-alzone*J2+beta*J4-gama*J6)
    b = (Y-Bfi)/sigma
    zeta = (1/2)*pow((epri*a*cos(epri)), 2)
    epsi = a*(1-zeta/3)
    eta = fipri+b*(1-zeta)
    lon = atan(((exp(epsi)-exp((-1*epsi)))/2)/cos(eta))
    tau = atan((cos(lon))*(tan(eta)))
    lon = lon+loncero
    lat = fipri+(1+pow((epri*cos(fipri)), 2)-(3/2)*pow(epri, 2) *
                 (sin(fipri))*(cos(fipri))*(tau-fipri))*(tau-fipri)
    lon = lon*180/pi
    lat = lat*180/pi
    lat = round(lat*100000000)/100000000
    lon = round(lon*100000000)/100000000
    coor = [lat, lon]
    return coor


def agrad(argu):
    sig = abs(argu)/argu
    argu = abs(argu)
    grad = floor(argu)
    min = (argu-grad)*60
    seg = (min-floor(min))*60
    min = floor(min)
    if((round(seg*1000))/1000 == 60):
        seg = 0
        min = min+1
    gms = "{}º {}' {}\"".format(sig*grad, min, (round(seg*1000))/1000)
    return gms
