import aiosqlite
import json
from typing import List, Dict, Any

class KnowledgeGraph:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.nodes = {}
        self.edges = []
        
    async def load_graph(self):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            
            # Load Zones
            async with db.execute("SELECT * FROM zones") as cursor:
                async for row in cursor:
                    self.nodes[row['id']] = {"type": "ZONE", **dict(row)}
                    adj = json.loads(row['adjacent_zones'])
                    for a_zone in adj:
                        self.edges.append({"source": row['id'], "target": a_zone, "type": "adjacent_to"})
                        
            # Load Sensors
            async with db.execute("SELECT * FROM sensors") as cursor:
                async for row in cursor:
                    self.nodes[row['id']] = {"type": "SENSOR", **dict(row)}
                    self.edges.append({"source": row['zone_id'], "target": row['id'], "type": "contains"})
                    if row['equipment_id']:
                        self.edges.append({"source": row['equipment_id'], "target": row['id'], "type": "monitored_by"})
                        
            # Load Equipment
            async with db.execute("SELECT * FROM equipment") as cursor:
                async for row in cursor:
                    self.nodes[row['id']] = {"type": "EQUIPMENT", **dict(row)}
                    self.edges.append({"source": row['zone_id'], "target": row['id'], "type": "contains"})
                    connected = json.loads(row['connected_equipment'])
                    for c_eq in connected:
                        self.edges.append({"source": row['id'], "target": c_eq, "type": "connected_to"})
                        
            # Load Permits
            async with db.execute("SELECT * FROM work_permits WHERE status='ACTIVE'") as cursor:
                async for row in cursor:
                    self.nodes[row['id']] = {"type": "PERMIT", **dict(row)}
                    self.edges.append({"source": row['id'], "target": row['zone_id'], "type": "authorizes_work_in"})
                    if row['equipment_id']:
                        self.edges.append({"source": row['id'], "target": row['equipment_id'], "type": "applies_to"})

    def find_permits_near_zone(self, zone_id: str, max_distance: str = "ADJACENT") -> List[Dict]:
        target_zones = [zone_id]
        if max_distance == "ADJACENT":
            for edge in self.edges:
                if edge["type"] == "adjacent_to" and edge["source"] == zone_id:
                    target_zones.append(edge["target"])
                    
        permits = []
        for node_id, node in self.nodes.items():
            if node["type"] == "PERMIT" and node["zone_id"] in target_zones:
                permits.append(node)
        return permits
        
    def find_connected_equipment(self, equipment_id: str) -> List[Dict]:
        connected = []
        for edge in self.edges:
            if edge["type"] == "connected_to" and edge["source"] == equipment_id:
                if edge["target"] in self.nodes:
                    connected.append(self.nodes[edge["target"]])
            elif edge["type"] == "connected_to" and edge["target"] == equipment_id:
                if edge["source"] in self.nodes:
                    connected.append(self.nodes[edge["source"]])
        return connected
        
    def check_permit_conflicts(self, permit_id: str) -> List[Dict]:
        conflicts = []
        permit = self.nodes.get(permit_id)
        if not permit or permit["type"] != "PERMIT":
            return conflicts
            
        near_permits = self.find_permits_near_zone(permit["zone_id"], "ADJACENT")
        for other_p in near_permits:
            if other_p["id"] == permit_id:
                continue
            
            p_types = {permit["type"], other_p["type"]}
            if "HOT_WORK" in p_types and "CONFINED_SPACE" in p_types:
                conflicts.append({"conflict_type": "INCOMPATIBLE_TYPES", "permit": other_p["id"], "reason": "Hot work near confined space"})
                
        return conflicts
