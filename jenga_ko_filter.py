import itertools
import random
from typing import Dict, List, Tuple, Any

morphological_box = {
    "Energieversorgung": ["Batterie", "Netzteil", "Solarzelle", "Brennstoffzelle", "Stromgenerator"],
    "Energieuebertragung": ["Sicherung/PTC", "Entkopplungskondensatoren", "Kurze Leitungen", "Shottky Dioden",
                            "Verdrillung der Leitungen", "Separate Strompfade", "Koaxialkabel"],
    "Basisstruktur_Geometrie": ["Quadratisch", "Rechteckig", "Rund", "Elliptisch", "Parallelogram", "Reifen",
                                "Kreuzförmig", "H-Förmig", "Dreieckförmig", "Scheren-Basis", "Portalbasis",
                                "Roboterarm", "Spinne"],
    "Material_Basisstruktur": ["Aluminium", "3D-Druck", "Karton", "Sperrholz", "Acryl", "Stahl", "Glas"],
    "Dateneingabe": ["Keypad", "Laptop", "Bluetooth Steuerung", "Controller/Joystick", "Cloud", "Seriellen Monitor",
                     "Rotary Encoder", "Display", "Mikrofon", "RFID/NFC", "Potentiometer/Analog", "Binär Digital",
                     "Website"],
    "Datenuebertragung": ["Kabel", "WLAN", "Bluetooth", "Satellitenkommunikation", "Optokoppler",
                          "Serial Periphal Interface", "LoRa", "Universal Asynchronous Receiver Transmitter", "I2C",
                          "Piezo Akustik", "CAN", "USB", "Binär Digital"],
    "Sensorik_Turm": ["Infrarot", "Kamera", "Näherungssensor", "Ultraschallsensor", "Drucksensor (Center of Gravity)",
                      "Motion Tracking/Neigungssensor/IMU", "Laser-Abstandssensor", "Mikrofon", "Vibrationssensor",
                      "LiDAR", "Farbsensor"],
    "Sensorik_Stein": ["Kraftsensor", "Kamera", "Infrarot", "Näherungssensor", "Ultraschallsensor", "Hall Sensor",
                       "Capacitive Touch", "Akustische Emission", "RFID/NFC", "Thermokamera", "Computer Vision"],
    "Sensorik_Aktor": ["Positionsgeber (Encoder oder Resolver, Inkremental oder Absolut)", "Punktsteuerung",
                       "Bahnsteuerung", "Kamera", "Infrarot", "Potentiometer", "Mikrotaster", "Inkrementalgeber",
                       "Time of Flight", "Reedschalter/Magnete", "Hallsensoren"],
    "Antriebssystem": ["E-motor(DC Motor,BLDC, Schrittmotor, Servomotor)", "Pneumatikmotor", "Hydraulikmotor",
                       "Piezo-Antrieb", "Hubmagnet", "Uhrwerkmotorik"],
    "Aktorik_Linear": ["Zugspindel", "Zahnstangenantrieb", "Seilzug", "Leitungsbahn", "Linear Motoren", "Zahnriemen",
                       "Federmechanismus", "Schubkurbel-Mechanismus", "Elastomere"],
    "Aktorik_Wirkprinzip": ["Schießen", "Schieben", "Adhäsion", "Greifen", "Klopfen", "Vibration"],
    "Aktorik_Element": ["Nadelstoß", "Pneumatikzylinder", "Luftdruck", "Hubmagnet", "Peitsche", "Hydraulikzylinder",
                        "Haftmittel", "Elektroadhäsion"],
    "Regelung": ["Mikrokontroller", "Programmable Logic Controllers (PLC)", "Field-Programmable Gate Array (FPGA)",
                 "System on Chip (SoC)", "Relais Logik", "PLC"],
    "Programmiersprache": ["Matlab", "C/C++", "Python", "MicroPython", "Node-Red", "Java", "Verilog", "VHDL"]
}


cost_db = {
    # Energieversorgung
    "Batterie": 10, "Netzteil": 15, "Solarzelle": 25, "Brennstoffzelle": 80, "Stromgenerator": 60,

    # Energieuebertragung
    "Sicherung/PTC": 1, "Entkopplungskondensatoren": 2, "Kurze Leitungen": 0, "Shottky Dioden": 1,
    "Verdrillung der Leitungen": 0, "Separate Strompfade": 3, "Koaxialkabel": 8,

    # Basisstruktur & Material
    "Aluminium": 30, "3D-Druck": 10, "Karton": 2, "Sperrholz": 8, "Acryl": 20, "Stahl": 35, "Glas": 25,
    # Geometry assumed free; material dominates cost

    # Dateneingabe
    "Keypad": 3, "Laptop": 0, "Bluetooth Steuerung": 10, "Controller/Joystick": 15,
    "Cloud": 0, "Seriellen Monitor": 0, "Rotary Encoder": 2, "Display": 8,
    "Mikrofon": 2, "RFID/NFC": 5, "Potentiometer/Analog": 1, "Binär Digital": 0, "Website": 0,

    # Datenuebertragung
    "Kabel": 2, "WLAN": 8, "Bluetooth": 10, "Satellitenkommunikation": 100,
    "Optokoppler": 1, "Serial Periphal Interface": 0, "LoRa": 12, "Universal Asynchronous Receiver Transmitter": 0,
    "I2C": 0, "Piezo Akustik": 5, "CAN": 15, "USB": 3, "Binär Digital": 0,

    # Sensorik Turm
    "Infrarot": 2, "Kamera": 15, "Näherungssensor": 3, "Ultraschallsensor": 4,
    "Drucksensor (Center of Gravity)": 10, "Motion Tracking/Neigungssensor/IMU": 8,
    "Laser-Abstandssensor": 25, "Mikrofon": 2, "Vibrationssensor": 5, "LiDAR": 80, "Farbsensor": 6,

    # Sensorik Stein
    "Kraftsensor": 12, "Kamera": 15, "Infrarot": 2, "Näherungssensor": 3, "Ultraschallsensor": 4,
    "Hall Sensor": 2, "Capacitive Touch": 8, "Akustische Emission": 10, "RFID/NFC": 5,
    "Thermokamera": 60, "Computer Vision": 0,  # assumes software

    # Sensorik Aktor
    "Positionsgeber (Encoder oder Resolver, Inkremental oder Absolut)": 10,
    "Punktsteuerung": 0, "Bahnsteuerung": 0, "Kamera": 15, "Infrarot": 2, "Potentiometer": 1,
    "Mikrotaster": 1, "Inkrementalgeber": 8, "Time of Flight": 12, "Reedschalter/Magnete": 2, "Hallsensoren": 2,

    # Antriebssystem
    "E-motor(DC Motor,BLDC, Schrittmotor, Servomotor)": 20,
    "Pneumatikmotor": 30, "Hydraulikmotor": 50, "Piezo-Antrieb": 15, "Hubmagnet": 8, "Uhrwerkmotorik": 5,

    # Aktorik_Linear
    "Zugspindel": 10, "Zahnstangenantrieb": 15, "Seilzug": 5, "Leitungsbahn": 8,
    "Linear Motoren": 60, "Zahnriemen": 12, "Federmechanismus": 2, "Schubkurbel-Mechanismus": 10, "Elastomere": 3,

    # Aktorik_Wirkprinzip (no direct cost)
    "Schießen": 0, "Schieben": 0, "Adhäsion": 0, "Greifen": 0, "Klopfen": 0, "Vibration": 0,

    # Aktorik_Element
    "Nadelstoß": 2, "Pneumatikzylinder": 20, "Luftdruck": 0, "Hubmagnet": 8,
    "Peitsche": 1, "Hydraulikzylinder": 40, "Haftmittel": 5, "Elektroadhäsion": 15,

    # Regelung
    "Mikrokontroller": 5, "Programmable Logic Controllers (PLC)": 40,
    "Field-Programmable Gate Array (FPGA)": 60, "System on Chip (SoC)": 30, "Relais Logik": 8, "PLC": 40,

    # Programmiersprache (assumed no extra cost)
    "Matlab": 0, "C/C++": 0, "Python": 0, "MicroPython": 0, "Node-Red": 0, "Java": 0, "Verilog": 0, "VHDL": 0,
}


size_db = {
    "Basisstruktur_Geometrie": {
        "Quadratisch": 35, "Rechteckig": 38, "Rund": 36, "Elliptisch": 37,
        "Parallelogram": 38, "Reifen": 42  # >40 → will be filtered
    },
    "Material_Basisstruktur": {
    },
    "Aktorik_Linear": {
        "Zugspindel": 30, "Zahnstangenantrieb": 35, "Seilzug": 25, "Leitungsbahn": 28,
        "Linear Motoren": 45, "Zahnriemen": 32, "Federmechanismus": 20,
        "Schubkurbel-Mechanismus": 33, "Elastomere": 22
    },
    "Antriebssystem": {
        "E-motor(DC Motor,BLDC, Schrittmotor, Servomotor)": 10,
        "Pneumatikmotor": 15, "Hydraulikmotor": 20, "Piezo-Antrieb": 5,
        "Hubmagnet": 6, "Uhrwerkmotorik": 8
    }
}

power_db = {
    "Energieversorgung": {"Batterie": 4, "Netzteil": 4, "Solarzelle": 2, "Brennstoffzelle": 3, "Stromgenerator": 4},
    "Antriebssystem": {
        "E-motor(DC Motor,BLDC, Schrittmotor, Servomotor)": 2.0,
        "Pneumatikmotor": 1.5,
        "Hydraulikmotor": 3.0,
        "Piezo-Antrieb": 0.1,
        "Hubmagnet": 0.8,
        "Uhrwerkmotorik": 0.05
    },
    "Sensorik_Turm": {
        "Kamera": 0.2, "LiDAR": 1.0, "Laser-Abstandssensor": 0.3,
        "IMU": 0.05, "Ultraschallsensor": 0.02, "Infrarot": 0.02
    },
    "Regelung": {
        "Mikrokontroller": 0.05, "FPGA": 0.8, "SoC": 1.2, "PLC": 1.5
    },
    "Datenuebertragung": {
        "WLAN": 0.1, "Bluetooth": 0.1, "LoRa": 0.08
    }
}


def check_compatibility(design: Dict[str, str]) -> bool:
    # Rule 1: If using Kamera for Turm or Stein, must use KI/Computer Vision or advanced control
    if design["Sensorik_Turm"] == "Kamera" or design["Sensorik_Stein"] == "Kamera":
        if design["Programmiersprache"] not in ["Python", "C/C++"] and "KI" not in str(
                design.get("Datenverarbeitung", "")):
            return False

    # Rule 2: Greifen requires Pneumatikzylinder, Haftmittel, or Elektroadhäsion
    if design["Aktorik_Wirkprinzip"] == "Greifen":
        if design["Aktorik_Element"] not in ["Pneumatikzylinder", "Haftmittel", "Elektroadhäsion"]:
            return False

    # Rule 3: Linear Motoren require high power & SoC/FPGA
    if design["Aktorik_Linear"] == "Linear Motoren":
        if design["Regelung"] not in ["Field-Programmable Gate Array (FPGA)", "System on Chip (SoC)"]:
            return False

    # Rule 4: Satellitenkommunikation is too expensive/powerful → always invalid
    if design["Datenuebertragung"] == "Satellitenkommunikation":
        return False

    # Add more rules as needed
    return True

def passes_ko(design: Dict[str, str]) -> bool:
    # 1. Budget ≤ €150
    total_cost = 0
    for key, value in design.items():
        if value in cost_db:
            total_cost += cost_db[value]
    if total_cost > 150:
        return False

    # 2. Size ≤ 40cm
    geom_size = size_db["Basisstruktur_Geometrie"].get(design["Basisstruktur_Geometrie"], 50)
    linear_size = size_db["Aktorik_Linear"].get(design["Aktorik_Linear"], 30)
    total_size = max(geom_size, linear_size)
    if total_size > 40:
        return False

    # 3. Power ≤ 4A
    total_current = 0.0
    total_current += power_db["Antriebssystem"].get(design["Antriebssystem"], 0.1)
    total_current += power_db["Sensorik_Turm"].get(design["Sensorik_Turm"], 0.02)
    total_current += power_db["Regelung"].get(design["Regelung"], 0.05)
    total_current += power_db["Datenuebertragung"].get(design["Datenuebertragung"], 0.0)

    total_current += 0.2

    if total_current > 4.0:
        return False

    # 4. Compatibility
    if not check_compatibility(design):
        return False

    return True


def generate_random_design() -> Dict[str, str]:
    return {dim: random.choice(opts) for dim, opts in morphological_box.items()}


def main():
    N_SAMPLES = 10**6
    feasible_designs = []

    for _ in range(N_SAMPLES):
        design = generate_random_design()
        if passes_ko(design):
            feasible_designs.append(design)

    print(f"Generated {N_SAMPLES} random designs.")
    print(f"Feasible after KO filtering: {len(feasible_designs)}")

    # Show one example
    if feasible_designs:
        print("\nExample feasible design:")
        for k, v in feasible_designs[0].items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()