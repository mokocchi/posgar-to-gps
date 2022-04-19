__app_name__ = "posgar_to_gps"
__version__ = "0.1.0"

(
    SUCCESS,
    CONVERSION_ERROR,
    PARSE_ERROR,
    FILE_READ_ERROR,
    FILE_WRITE_ERROR
) = range(5)

ERRORS = {
  CONVERSION_ERROR: "There was a conversion error",
  PARSE_ERROR: "Wrong format for batch file",
  FILE_READ_ERROR: "Batch file error",
  FILE_WRITE_ERROR: "Output file error"
}
