import aiosqlite
import asyncio
import json
from datetime import datetime, timezone

DB_PATH = "sentinel.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS zones (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                hazard_classification TEXT NOT NULL,
                area_sqm REAL NOT NULL,
                max_workers INTEGER NOT NULL,
                x_position REAL NOT NULL,
                y_position REAL NOT NULL,
                width REAL NOT NULL,
                height REAL NOT NULL,
                color_normal TEXT NOT NULL,
                adjacent_zones TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS sensors (
                id TEXT PRIMARY KEY,
                zone_id TEXT NOT NULL,
                equipment_id TEXT,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                threshold_warning REAL NOT NULL,
                threshold_alarm REAL NOT NULL,
                normal_range_low REAL NOT NULL,
                normal_range_high REAL NOT NULL,
                last_calibration TEXT NOT NULL,
                calibration_interval_days INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                x_position REAL NOT NULL,
                y_position REAL NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(zone_id) REFERENCES zones(id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                value REAL NOT NULL,
                normalized_risk REAL NOT NULL,
                is_anomaly INTEGER NOT NULL DEFAULT 0,
                anomaly_type TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(sensor_id) REFERENCES sensors(id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS equipment (
                id TEXT PRIMARY KEY,
                zone_id TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                criticality TEXT NOT NULL,
                last_maintenance TEXT NOT NULL,
                maintenance_interval_days INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'OPERATIONAL',
                connected_equipment TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(zone_id) REFERENCES zones(id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS workers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                current_zone_id TEXT,
                shift TEXT NOT NULL,
                certification TEXT,
                status TEXT NOT NULL DEFAULT 'ON_DUTY',
                x_position REAL,
                y_position REAL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(current_zone_id) REFERENCES zones(id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS work_permits (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                zone_id TEXT NOT NULL,
                equipment_id TEXT,
                description TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                issued_by TEXT NOT NULL,
                issued_to TEXT NOT NULL,
                workers_involved INTEGER NOT NULL,
                precautions TEXT NOT NULL,
                gas_test_required INTEGER NOT NULL DEFAULT 0,
                gas_test_result TEXT,
                loto_required INTEGER NOT NULL DEFAULT 0,
                loto_status TEXT,
                valid_from TEXT NOT NULL,
                valid_until TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                suspended_reason TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(zone_id) REFERENCES zones(id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS risk_events (
                id TEXT PRIMARY KEY,
                crs_score REAL NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                risk_factors TEXT NOT NULL,
                zones_affected TEXT NOT NULL,
                workers_at_risk INTEGER NOT NULL,
                crs_breakdown TEXT NOT NULL,
                cascade_factor REAL NOT NULL,
                regulatory_violations TEXT,
                prediction TEXT,
                recommended_actions TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                detected_at TEXT NOT NULL,
                resolved_at TEXT
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS emergency_actions (
                id TEXT PRIMARY KEY,
                risk_event_id TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                target TEXT NOT NULL,
                urgency TEXT NOT NULL,
                requires_confirmation INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'PROPOSED',
                executed_by TEXT,
                result TEXT,
                proposed_at TEXT NOT NULL,
                executed_at TEXT,
                FOREIGN KEY(risk_event_id) REFERENCES risk_events(id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS compliance_checks (
                id TEXT PRIMARY KEY,
                regulation_id TEXT NOT NULL,
                regulation_name TEXT NOT NULL,
                check_description TEXT NOT NULL,
                status TEXT NOT NULL,
                deviation_details TEXT,
                corrective_action TEXT,
                deadline TEXT,
                zone_id TEXT,
                equipment_id TEXT,
                checked_at TEXT NOT NULL,
                FOREIGN KEY(zone_id) REFERENCES zones(id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS incident_history (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                location TEXT NOT NULL,
                type TEXT NOT NULL,
                severity TEXT NOT NULL,
                casualties INTEGER NOT NULL,
                injuries INTEGER NOT NULL,
                root_cause TEXT NOT NULL,
                contributing_factors TEXT NOT NULL,
                description TEXT NOT NULL,
                lessons_learned TEXT NOT NULL,
                regulatory_references TEXT NOT NULL,
                tags TEXT NOT NULL,
                embedding TEXT
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS agent_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                action TEXT NOT NULL,
                input_summary TEXT NOT NULL,
                output_summary TEXT NOT NULL,
                duration_ms INTEGER NOT NULL,
                tokens_used INTEGER,
                status TEXT NOT NULL,
                error_message TEXT,
                timestamp TEXT NOT NULL
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS regulations (
                id TEXT PRIMARY KEY,
                framework TEXT NOT NULL,
                standard TEXT NOT NULL,
                section TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                applicability TEXT NOT NULL,
                severity_if_violated TEXT NOT NULL
            )
        ''')

        await db.commit()

if __name__ == "__main__":
    asyncio.run(init_db())
    print("Database initialized successfully.")
