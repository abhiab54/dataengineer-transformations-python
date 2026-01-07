from dataclasses import dataclass
from typing import Optional


@dataclass
class Trip:
    """
    Domain model for a Citibike trip with validation logic.
    """

    start_station_latitude: Optional[float]
    start_station_longitude: Optional[float]
    end_station_latitude: Optional[float]
    end_station_longitude: Optional[float]

    def is_valid(self) -> bool:
        """
        Returns True if the trip has valid coordinates:
          - All four coordinate fields are non-null
          - Latitudes are in [-90, 90]
          - Longitudes are in [-180, 180]
        """
        # Check for null values
        if (
            self.start_station_latitude is None
            or self.start_station_longitude is None
            or self.end_station_latitude is None
            or self.end_station_longitude is None
        ):
            return False

        # Check latitude bounds
        if not (-90.0 <= self.start_station_latitude <= 90.0):
            return False
        if not (-90.0 <= self.end_station_latitude <= 90.0):
            return False

        # Check longitude bounds
        if not (-180.0 <= self.start_station_longitude <= 180.0):
            return False
        if not (-180.0 <= self.end_station_longitude <= 180.0):
            return False

        return True
