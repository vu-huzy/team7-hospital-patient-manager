"""
SQL Query Loader - Load queries from SQL files
This ensures all queries come from SQL files, not hardcoded strings
"""
import re
import os

def load_query_from_file(filepath, query_number):
    """
    Load a specific query from a SQL file
    
    Args:
        filepath: Path to SQL file (e.g., 'app/queries/multi_join.sql')
        query_number: Query number to extract (e.g., 1, 2, 3)
        
    Returns:
        SQL query string
    """
    # Convert to absolute path if relative
    if not os.path.isabs(filepath):
        # Get the project root (where app/ folder is)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        filepath = os.path.join(project_root, filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by query comments
    queries = content.split('-- Query')
    
    for q in queries:
        # Check if this is the query we want
        if q.strip().startswith(f'{query_number}:'):
            # Remove comment line and get SQL
            lines = q.split('\n')[1:]
            query = '\n'.join(lines).strip()
            
            # Remove any trailing query separator
            if '-- Query' in query:
                query = query.split('-- Query')[0].strip()
            
            # Remove trailing semicolon if present
            query = query.rstrip(';').strip()
            
            return query
    
    raise ValueError(f"Query {query_number} not found in {filepath}")

def load_all_queries_from_file(filepath):
    """
    Load all queries from a SQL file
    
    Args:
        filepath: Path to SQL file
        
    Returns:
        Dictionary mapping query number to SQL string
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    queries = {}
    parts = content.split('-- Query')
    
    for part in parts[1:]:  # Skip first part (file header)
        lines = part.strip().split('\n')
        if not lines:
            continue
            
        # Extract query number from first line
        first_line = lines[0].strip()
        match = re.match(r'^(\d+):', first_line)
        if match:
            query_num = int(match.group(1))
            
            # Get SQL (skip comment line)
            sql_lines = lines[1:]
            query = '\n'.join(sql_lines).strip()
            
            # Remove trailing query separator
            if '-- Query' in query:
                query = query.split('-- Query')[0].strip()
            
            query = query.rstrip(';').strip()
            queries[query_num] = query
    
    return queries
