import csv
import os
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

def get_caller_directory():
    """
    Retrieves the directory of the original caller script.
    
    Returns:
        Path: Absolute path to the caller's directory.
    """
    stack = inspect.stack()
    logging.debug(f"Stack: {stack}")
    try:
        # Ensure the stack has enough frames
        if len(stack) < 3:
            # Fallback to functions.py directory if stack is not deep enough
            return Path(__file__).parent.resolve()
        
        # Frame 0: get_caller_directory
        # Frame 1: load_csv
        # Frame 2: (original caller)
        caller_frame = stack[2]
        caller_file = caller_frame.filename
        caller_dir = Path(caller_file).parent.resolve()
        return caller_dir
    finally:
        # Clean up to prevent reference cycles
        del stack

def get_project_root():
    """
    Finds the project root directory by locating 'config.ini'.
    
    Returns:
        Path: Absolute path to the project root.
    
    Raises:
        FileNotFoundError: If 'config.ini' is not found in any parent directories.
    """
    caller_dir = get_caller_directory()
    current_dir = caller_dir
    while current_dir != current_dir.parent:
        if (current_dir / 'config.ini').is_file():
            return current_dir
        current_dir = current_dir.parent
    raise FileNotFoundError("Could not find 'config.ini' in any parent directories.")

def load_config():
    """
    Loads configuration from 'config.ini' located at the project root.
    
    Returns:
        configparser.ConfigParser: The loaded configuration object.
    
    Raises:
        FileNotFoundError: If 'config.ini' is not found.
        KeyError: If required configuration keys are missing.
        configparser.Error: If there's an error parsing the configuration.
    """
    project_root = get_project_root()
    config_path = project_root / 'config.ini'
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
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

def export_stl(model, relative_path):
    """
    Exports a CadQuery model to an STL file located at a path relative to the configured STL output directory.
    
    Args:
        model (cq.Workplane): The CadQuery model to export.
        relative_path (str): Relative path within the STL output directory.
    
    Raises:
        Exception: If exporting fails.
    """
    config = load_config()
    stl_output_dir = Path(config['Paths']['stl_output_dir'])
    
    # Ensure stl_output_dir is relative to project root
    project_root = get_project_root()
    stl_output_path = (project_root / stl_output_dir).resolve()
    
    # Construct the absolute path for the STL file
    stl_path = (stl_output_path / relative_path).resolve()
    stl_dir = stl_path.parent
    
    # Create the directory if it doesn't exist
    stl_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        cq.exporters.export(model, str(stl_path))
        logging.info(f"STL file successfully exported to '{stl_path}'.")
    except Exception as e:
        logging.error(f"Failed to export STL file: {e}")
        raise Exception(f"Failed to export STL file: {e}")
