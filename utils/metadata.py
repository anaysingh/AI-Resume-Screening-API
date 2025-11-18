# utils/metadata.py

import uuid
from datetime import datetime

def generate_metadata(start_time):
    """
    Returns SaaS-style metadata for the API response including:
    - unique request ID
    - timestamp
    - processing time in ms
    - service version info
    """
    end_time = datetime.now()
    processing_ms = (end_time - start_time).total_seconds() * 1000

    metadata = {
        "service": "AI Resume Screening SaaS",
        "version": "1.0.3",
        "candidate_id": str(uuid.uuid4()),
        "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "processing_time_ms": round(processing_ms, 2)
    }
    return metadata
