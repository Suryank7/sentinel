from typing import List, Dict, Tuple
import math

class GeospatialEngine:
    @staticmethod
    def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    @staticmethod
    def is_worker_in_zone(worker: Dict, zone: Dict) -> bool:
        # Check if worker coordinates fall within zone bounding box
        if not worker.get('x_position') or not worker.get('y_position'):
            return False
            
        zx, zy = zone['x_position'], zone['y_position']
        zw, zh = zone['width'], zone['height']
        
        wx, wy = worker['x_position'], worker['y_position']
        
        return (zx <= wx <= zx + zw) and (zy <= wy <= zy + zh)

    @staticmethod
    def get_workers_in_zone(workers: List[Dict], zone_id: str) -> List[Dict]:
        return [w for w in workers if w.get('current_zone_id') == zone_id]
        
    @staticmethod
    def check_worker_proximity_to_hazard(workers: List[Dict], hazard_x: float, hazard_y: float, safe_distance: float) -> List[Dict]:
        at_risk = []
        for w in workers:
            if not w.get('x_position') or not w.get('y_position'):
                continue
            dist = GeospatialEngine.calculate_distance(w['x_position'], w['y_position'], hazard_x, hazard_y)
            if dist < safe_distance:
                at_risk.append(w)
        return at_risk
