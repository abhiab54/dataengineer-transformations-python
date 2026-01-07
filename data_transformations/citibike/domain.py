from dataclasses import dataclass
from typing import Optional


@dataclass
class Trip:
    """
    Domain model for a CitiBike trip with validation logic.
    """

    start_station_latitude: Optional[float] = None
    start_station_longitude: Optional[float] = None
    end_station_latitude: Optional[float] = None
    end_station_longitude: Optional[float] = None

    def is_valid(self) -> bool:
        """
        Returns True if all four coordinate fields are non-null and within valid ranges:
          - Latitudes must be in [-90, 90]
          - Longitudes must be in [-180, 180]
        """
        # Check if all coordinates are non-null
        if any(
            coord is None
            for coord in [
                self.start_station_latitude,
                self.start_station_longitude,
                self.end_station_latitude,
                self.end_station_longitude,
            ]
        ):
            return False

        # Check latitude ranges
        if not (-90.0 <= self.start_station_latitude <= 90.0):
            return False
        if not (-90.0 <= self.end_station_latitude <= 90.0):
            return False

        # Check longitude ranges
        if not (-180.0 <= self.start_station_longitude <= 180.0):
            return False
        return -180.0 <= self.end_station_longitude <= 180.0
