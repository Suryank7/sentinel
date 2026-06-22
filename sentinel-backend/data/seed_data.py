import aiosqlite
import asyncio
import json
from datetime import datetime, timezone, timedelta

DB_PATH = "sentinel.db"

async def seed_data():
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.now(timezone.utc).isoformat()
        
        # 1. ZONES
        zones = [
            ("zone-001", "Coke Oven Battery", "COB", "Zone 1", 2400.0, 12, 10.0, 10.0, 25.0, 30.0, "#1a3a2a", '["zone-002","zone-003"]', "Coke production", now),
            ("zone-002", "Blast Furnace", "BF", "Zone 1", 3200.0, 15, 40.0, 10.0, 25.0, 35.0, "#1a3a2a", '["zone-001","zone-003","zone-005"]', "Iron smelting", now),
            ("zone-003", "Steel Melting Shop", "SMS", "Zone 2", 4000.0, 18, 70.0, 10.0, 25.0, 35.0, "#1a3a2a", '["zone-001","zone-002","zone-006"]', "Steel production", now),
            ("zone-004", "Gas Holder Area", "GHA", "Zone 0", 800.0, 4, 10.0, 50.0, 20.0, 20.0, "#1a3a2a", '["zone-001","zone-005"]', "Gas storage", now),
            ("zone-005", "Rolling Mill", "RM", "Non-hazardous", 5000.0, 20, 40.0, 55.0, 30.0, 25.0, "#1a3a2a", '["zone-002","zone-004","zone-006"]', "Steel rolling", now),
            ("zone-006", "Control Room", "CR", "Non-hazardous", 200.0, 8, 75.0, 55.0, 20.0, 20.0, "#1a3a2a", '["zone-003","zone-005"]', "Central command", now)
        ]
        await db.executemany("INSERT OR IGNORE INTO zones VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", zones)

        # 2. SENSORS
        last_calib = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
        sensors = [
            # Zone 1 (COB)
            ("sensor-001", "zone-001", None, "H2S", "H₂S Detector GD-001", "ppm", 7.0, 10.0, 0.0, 2.0, last_calib, 30, "ACTIVE", 15.0, 15.0, now),
            ("sensor-002", "zone-001", None, "CH4", "CH₄ Detector GD-002", "%LEL", 1.0, 2.0, 0.0, 0.5, last_calib, 30, "ACTIVE", 25.0, 15.0, now),
            ("sensor-003", "zone-001", None, "TEMPERATURE", "Temp Sensor TS-001", "°C", 350.0, 400.0, 200.0, 300.0, last_calib, 90, "ACTIVE", 15.0, 25.0, now),
            ("sensor-004", "zone-001", None, "CO", "CO Detector GD-003", "ppm", 25.0, 35.0, 0.0, 10.0, last_calib, 30, "ACTIVE", 25.0, 25.0, now),
            # Zone 2 (BF)
            ("sensor-005", "zone-002", None, "CO", "CO Detector GD-004", "ppm", 25.0, 35.0, 0.0, 10.0, last_calib, 30, "ACTIVE", 45.0, 15.0, now),
            ("sensor-006", "zone-002", None, "TEMPERATURE", "Temp Sensor TS-002", "°C", 800.0, 900.0, 500.0, 700.0, last_calib, 90, "ACTIVE", 55.0, 15.0, now),
            ("sensor-007", "zone-002", None, "PRESSURE", "Pressure PT-001", "bar", 2.5, 3.0, 1.0, 2.0, last_calib, 90, "ACTIVE", 45.0, 25.0, now),
            ("sensor-008", "zone-002", None, "VIBRATION", "Vibration VS-001", "mm/s", 7.0, 10.0, 1.0, 4.0, last_calib, 90, "ACTIVE", 55.0, 25.0, now),
            # Zone 3 (SMS)
            ("sensor-009", "zone-003", None, "O2", "O₂ Monitor OM-001", "%", 19.5, 19.0, 20.9, 21.0, last_calib, 30, "ACTIVE", 75.0, 15.0, now),
            ("sensor-010", "zone-003", None, "TEMPERATURE", "Temp Sensor TS-003", "°C", 1200.0, 1400.0, 900.0, 1100.0, last_calib, 90, "ACTIVE", 85.0, 15.0, now),
            ("sensor-011", "zone-003", None, "CO", "CO Detector GD-005", "ppm", 25.0, 35.0, 0.0, 10.0, last_calib, 30, "ACTIVE", 75.0, 25.0, now),
            ("sensor-012", "zone-003", None, "PRESSURE", "Pressure PT-002", "bar", 1.5, 2.0, 0.5, 1.2, last_calib, 90, "ACTIVE", 85.0, 25.0, now),
            # Zone 4 (GHA)
            ("sensor-013", "zone-004", None, "CH4", "CH₄ Detector GD-006", "%LEL", 0.8, 1.5, 0.0, 0.3, last_calib, 30, "ACTIVE", 15.0, 55.0, now),
            ("sensor-014", "zone-004", None, "H2S", "H₂S Detector GD-007", "ppm", 5.0, 10.0, 0.0, 1.0, (datetime.now(timezone.utc) - timedelta(days=33)).isoformat(), 30, "ACTIVE", 25.0, 55.0, now), # Overdue calib
            ("sensor-015", "zone-004", None, "PRESSURE", "Pressure PT-003", "bar", 0.8, 1.0, 0.2, 0.6, last_calib, 90, "ACTIVE", 15.0, 65.0, now),
            ("sensor-016", "zone-004", None, "O2", "O₂ Monitor OM-002", "%", 19.5, 19.0, 20.9, 21.0, last_calib, 30, "ACTIVE", 25.0, 65.0, now),
            # Zone 5 (RM)
            ("sensor-017", "zone-005", None, "TEMPERATURE", "Temp Sensor TS-004", "°C", 200.0, 250.0, 100.0, 180.0, last_calib, 90, "ACTIVE", 45.0, 65.0, now),
            ("sensor-018", "zone-005", None, "VIBRATION", "Vibration VS-002", "mm/s", 8.0, 12.0, 2.0, 5.0, last_calib, 90, "ACTIVE", 55.0, 65.0, now),
            ("sensor-019", "zone-005", None, "NOISE", "Noise Level", "dB", 85.0, 90.0, 60.0, 80.0, last_calib, 90, "ACTIVE", 65.0, 65.0, now),
            ("sensor-020", "zone-005", None, "TEMPERATURE", "Temp Sensor TS-005", "°C", 180.0, 220.0, 100.0, 150.0, last_calib, 90, "ACTIVE", 45.0, 75.0, now),
            # Zone 6 (CR)
            ("sensor-021", "zone-006", None, "TEMPERATURE", "Temp Sensor TS-006", "°C", 28.0, 32.0, 20.0, 24.0, last_calib, 90, "ACTIVE", 80.0, 60.0, now),
            ("sensor-022", "zone-006", None, "SMOKE", "Smoke Detector", "obs/m", 0.5, 1.0, 0.0, 0.1, last_calib, 90, "ACTIVE", 90.0, 60.0, now),
            ("sensor-023", "zone-006", None, "O2", "O₂ Monitor OM-003", "%", 19.5, 19.0, 20.9, 21.0, last_calib, 30, "ACTIVE", 80.0, 70.0, now),
            ("sensor-024", "zone-006", None, "CO", "CO Detector GD-008", "ppm", 9.0, 15.0, 0.0, 2.0, last_calib, 30, "ACTIVE", 90.0, 70.0, now),
        ]
        await db.executemany("INSERT OR IGNORE INTO sensors VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", sensors)

        # 3. EQUIPMENT
        maint_date = (datetime.now(timezone.utc) - timedelta(days=44)).isoformat()
        equipment = [
            ("equip-001", "zone-001", "Coke Oven Door", "VALVE", "HIGH", last_calib, 30, "OPERATIONAL", '[]', now),
            ("equip-002", "zone-001", "Gas Extractor", "PUMP", "HIGH", last_calib, 30, "OPERATIONAL", '["equip-001"]', now),
            ("equip-003", "zone-003", "Gas Line Valve E-012", "VALVE", "HIGH", maint_date, 30, "OPERATIONAL", '[]', now), # Overdue maintenance by 14 days
            ("equip-004", "zone-003", "Ladle Crane Support", "STRUCTURAL", "HIGH", last_calib, 90, "OPERATIONAL", '[]', now),
            ("equip-005", "zone-004", "Gas Holder Pump", "PUMP", "HIGH", last_calib, 30, "OPERATIONAL", '["equip-003"]', now)
        ]
        await db.executemany("INSERT OR IGNORE INTO equipment VALUES (?,?,?,?,?,?,?,?,?,?)", equipment)

        # 4. WORKERS
        workers = [
            ("worker-001", "Rajesh Menon", "SAFETY_OFFICER", "zone-006", "A", '["gas_testing","hot_work","confined_space"]', "ON_DUTY", 85.0, 65.0, now),
            ("worker-002", "Ananya Reddy", "SUPERVISOR", "zone-001", "A", '["gas_testing","hot_work"]', "ON_DUTY", 20.0, 20.0, now),
        ]
        # Generate 45 more generic workers
        for i in range(3, 48):
            zone = f"zone-00{1 + (i % 5)}"
            workers.append((f"worker-{i:03d}", f"Worker {i}", "OPERATOR", zone, "A", '[]', "ON_DUTY", 10.0 + (i%20)*0.5, 10.0 + (i%20)*0.5, now))
            
        await db.executemany("INSERT OR IGNORE INTO workers VALUES (?,?,?,?,?,?,?,?,?,?)", workers)

        # 5. PERMITS
        valid_from = now
        valid_until = (datetime.now(timezone.utc) + timedelta(hours=8)).isoformat()
        permits = [
            ("PTW-2026-0147", "HOT_WORK", "zone-003", "equip-004", "Welding repair on ladle crane support beam", "HIGH", "Ananya Reddy", "Suresh Welding", 4, '["Fire extinguisher present","Spark shields up"]', 1, '{"H2S":0,"CH4":0,"O2":20.9}', 0, None, valid_from, valid_until, "ACTIVE", None, now),
            ("PTW-2026-0148", "CONFINED_SPACE", "zone-004", "equip-005", "Internal inspection of Gas Holder Pump", "HIGH", "Rajesh Menon", "Pump Techs", 3, '["Ventilation active","Lifeline attached"]', 1, '{"H2S":0,"CH4":0,"O2":20.9}', 1, "APPLIED", valid_from, valid_until, "ACTIVE", None, now),
            ("PTW-2026-0149", "GENERAL", "zone-005", None, "Routine inspection of rolling mill bearings", "LOW", "Ramesh Kumar", "Maint Team A", 2, '["Standard PPE"]', 0, None, 0, None, valid_from, valid_until, "ACTIVE", None, now)
        ]
        await db.executemany("INSERT OR IGNORE INTO work_permits VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", permits)

        # 6. REGULATIONS
        regs = [
            ("OISD-105-4.3", "OISD", "OISD-STD-105", "Section 4.3", "Hot Work Permit Requirements", "Hot work shall be suspended immediately if flammable gas is detected in the vicinity or within 50 meters of the hot work location.", '["HOT_WORK", "FLAMMABLE_GAS"]', "CRITICAL"),
            ("OISD-105-6.2", "OISD", "OISD-STD-105", "Section 6.2", "Gas Detector Calibration", "All portable and fixed gas detectors shall be calibrated at intervals not exceeding 30 days.", '["GAS_DETECTOR"]', "MAJOR"),
            ("IS-17893-5.4", "IS", "IS 17893:2023", "Section 5.4", "Gas Testing", "Gas testing must be conducted and documented prior to issuance of any hot work or confined space entry permit.", '["HOT_WORK", "CONFINED_SPACE"]', "CRITICAL"),
            ("FA-7A-2", "FACTORY_ACT", "Factories Act", "Section 7A(2)", "Emergency Procedures", "Every occupier shall ensure that adequate emergency response procedures are established to deal with critical situations such as gas leaks or fires.", '["EMERGENCY", "GAS_LEAK", "FIRE"]', "MAJOR")
        ]
        await db.executemany("INSERT OR IGNORE INTO regulations VALUES (?,?,?,?,?,?,?,?)", regs)

        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed_data())
    print("Database seeded successfully.")
