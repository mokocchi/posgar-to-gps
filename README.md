# posgar-to-gps
A tool for converting from POSGAR to GPS (lat, long)

## Available commands
- `convert`
  ```
  Usage: posgar_to_gps convert [OPTIONS]

    Convert the x and y POSGAR coordinates to latitude and longitude

  Options:
    -x, --x-coordinate TEXT   X coordinate (POSGAR)
    -y, --y-coordinate TEXT   Y coordinate (POSGAR)
    -d, --decimal-point TEXT  Decimal point
    -z, --zone TEXT           POSGAR zone
    -D, --as-degrees          Show the result as degrees
    --help                    Show this message and exit.
  ```

_Based in the code written by Ing. Nelson Guerra:_ https://sites.google.com/site/calculadorageografica/
