import csv
import inspect
import configparser
from pathlib import Path
import cadquery as cq
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# cqlib/ always lives directly under the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_caller_directory():
    """
    Retrieves the directory of the script that called into this module (used to resolve
    paths like CSVs relative to the calling model script, not this library file).
    
    Returns:
        Path: Absolute path to the caller's directory.
    """
    stack = inspect.stack()
    try:
        # Frame 0: get_caller_directory, frame 1: the function in this module that
        # called us (e.g. load_csv_points), frame 2: the original external caller.
        if len(stack) < 3:
            return Path(__file__).parent.resolve()
        caller_frame = stack[2]
        caller_file = caller_frame.filename
        caller_dir = Path(caller_file).parent.resolve()
        return caller_dir
    finally:
        # Clean up to prevent reference cycles
        del stack

def load_config():
    """
    Loads configuration from 'config.ini' located at the project root.
    
    Returns:
        configparser.ConfigParser: The loaded configuration object.
    
    Raises:
        KeyError: If required configuration keys are missing.
    """
    config = configparser.ConfigParser()
    config.read(PROJECT_ROOT / 'config.ini')
    
    if 'Paths' not in config or 'stl_output_dir' not in config['Paths']:
        raise KeyError("Configuration file is missing 'stl_output_dir' under 'Paths' section.")
    
    return config

def load_csv_points(relative_path):
    """
    Loads points from a CSV file located at a path relative to the caller's script.
    
    Args:
        relative_path (str): Relative path to the CSV file from the caller's directory.
    
    Returns:
        list of tuple: List of (x, y) float tuples.
    
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV contains non-float values.
    """
    caller_dir = get_caller_directory()
    logging.info(f"Caller directory: {caller_dir}")
    csv_path = (caller_dir / relative_path).resolve()
    logging.info(f"CSV path: {csv_path}")
    
    if not csv_path.is_file():
        logging.error(f"The file '{csv_path}' does not exist.")
        raise FileNotFoundError(f"The file '{csv_path}' does not exist.")
    
    points = []
    with csv_path.open(mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line_number, row in enumerate(reader, start=1):
            if len(row) != 2:
                logging.warning(f"Skipping malformed line {line_number}: {row}")
                continue  # Skip malformed lines
            try:
                x, y = map(float, row)
                points.append((x, y))
            except ValueError:
                logging.warning(f"Non-float values on line {line_number}: {row}")
                continue  # Skip lines with non-float values
    return points

def export_stl(model, filename):
    """
    Export a CadQuery model to an STL file in the directory configured by
    'stl_output_dir' in config.ini (relative to the project root).

    Parameters:
        model (cq.Workplane): The CadQuery model to export.
        filename (str): The name of the output STL file.
    """
    try:
        config = load_config()
        output_dir = PROJECT_ROOT / config['Paths']['stl_output_dir']
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        cq.exporters.export(model, str(output_path))
        print(f"STL file successfully exported to '{output_path}'.")
    except Exception as e:
        print(f"Failed to export STL file: {e}")
        raise
