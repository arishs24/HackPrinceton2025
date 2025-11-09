import os
from typing import List, Dict, Any
from app.models.schemas import SnowflakeSimulationData
import json

# Mock database for demo (replace with actual Snowflake connector in production)
# In production, use: import snowflake.connector

# In-memory storage for demo
mock_database = []


async def save_simulation(data: SnowflakeSimulationData) -> Dict[str, Any]:
    """
    Save simulation data to Snowflake
    (Currently using mock storage for demo)
    """
    # In production, use Snowflake connector:
    """
    conn = snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO simulations VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        data.case_id,
        data.timestamp,
        data.tumor_location,
        data.tumor_volume,
        data.max_displacement,
        data.avg_stress,
        json.dumps(data.affected_regions),
        json.dumps(data.simulation_json)
    ))
    conn.commit()
    cursor.close()
    conn.close()
    """

    # Mock implementation
    mock_database.append({
        "case_id": data.case_id,
        "timestamp": data.timestamp.isoformat(),
        "tumor_location": data.tumor_location,
        "tumor_volume": data.tumor_volume,
        "max_displacement": data.max_displacement,
        "avg_stress": data.avg_stress,
        "affected_regions": data.affected_regions,
        "simulation_json": data.simulation_json
    })

    return {"status": "success", "records_inserted": 1}


async def get_similar_cases(tumor_location: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve similar cases from Snowflake based on tumor location
    (Currently using mock data for demo)
    """
    # In production, use Snowflake connector:
    """
    conn = snowflake.connector.connect(...)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT case_id, tumor_location, tumor_volume, max_displacement, avg_stress
        FROM simulations
        WHERE tumor_location LIKE %s
        ORDER BY timestamp DESC
        LIMIT %s
    ''', (f'%{tumor_location}%', limit))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return [dict(zip(['case_id', 'tumor_location', 'tumor_volume', 'max_displacement', 'avg_stress'], row)) for row in results]
    """

    # Mock implementation - generate sample similar cases
    similar_cases = [
        {
            "case_id": "demo-001",
            "tumor_location": "right_frontal_lobe",
            "tumor_volume": 7.8,
            "max_displacement": 4.2,
            "avg_stress": 1.15
        },
        {
            "case_id": "demo-002",
            "tumor_location": "right_frontal_lobe",
            "tumor_volume": 9.1,
            "max_displacement": 5.1,
            "avg_stress": 1.42
        },
        {
            "case_id": "demo-003",
            "tumor_location": "frontal_lobe",
            "tumor_volume": 6.5,
            "max_displacement": 3.8,
            "avg_stress": 0.98
        }
    ]

    # Add any matching cases from mock database
    for case in mock_database:
        if tumor_location.lower() in case["tumor_location"].lower():
            similar_cases.append({
                "case_id": case["case_id"],
                "tumor_location": case["tumor_location"],
                "tumor_volume": case["tumor_volume"],
                "max_displacement": case["max_displacement"],
                "avg_stress": case["avg_stress"]
            })

    return similar_cases[:limit]


async def get_case_statistics() -> Dict[str, Any]:
    """
    Get aggregate statistics across all cases
    """
    if not mock_database:
        return {
            "total_cases": 3,
            "avg_displacement": 4.37,
            "avg_stress": 1.18,
            "common_locations": ["frontal_lobe", "parietal_lobe", "temporal_lobe"]
        }

    return {
        "total_cases": len(mock_database),
        "avg_displacement": sum(c["max_displacement"] for c in mock_database) / len(mock_database),
        "avg_stress": sum(c["avg_stress"] for c in mock_database) / len(mock_database),
        "common_locations": list(set(c["tumor_location"] for c in mock_database))
    }
