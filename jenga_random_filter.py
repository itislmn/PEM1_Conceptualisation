import random
from pprint import pprint

# Your morphological box
morphological_box = {
    "Energieversorgung": ["Batterie", "Netzteil", "Solarzelle"],
    "Basisstruktur": ["Kubisch", "Kreuzförmig", "H-Förmig", "Dreieckförmig",
                      "Portalbasis", "Roboterarm", "Radial", "Zylindrisch", "Schere"],
    "Material": ["Aluminium", "Polymere/3D Druck", "Acryl"],
    "Dateneingabe": ["Kabel", "WLAN", "Bluetooth", "LoRa"],
    "Datenaufnahme TURM": ["Infrarot", "Kamera", "Näherungssensor", "Ultrashallsensor",
                           "Drucksensor", "Neigungssensor", "DMS", "IMU/Bewegungssensor"],
    "Datenaufnahme STEIN": ["Kraftsensor", "Kamera", "Infrarot", "Näherungssensor", "Ultrashallsensor",
                            "Hall-Sensor", "Capacitative Touch", "Computer Vision"],
    "Datenaufnahme AKTORPOSITION": ["Positionsgeber", "Kamera", "Infrarot", "Potentiometer",
                                    "Mikrotaster", "Time of Flight", "Reedschalter", "Hallsensor"],
    "Signalverstärkung": ["Platine"],
    "Datenverarbeitung": ["Maschinelles Lernen", "FEM & Strukturdynamik", "Robot Operating System/CAD",
                          "Finite State Machines"],
    "Antrieb": ["E-Motor", "Hubmagnet", "Zahnradssystem/Uhrwerk"],
    "Positionierung Aktorik": ["Zugspindel", "Zahnstangenantrieb", "Seilzug", "Leitungsbahn",
                               "Linearmotoren", "Zahnriemen"],  # removed duplicate "Zahnriemen"
    "Wirkprinzip auf Stein": ["Schießen", "Schieben", "Adhäsion", "Klopfen", "Vibration"],
    "Interagierendes Element": ["Nadelstoß", "Hubmagnet", "Haftmittel", "Wrecking Ball", "Bogen", "Gummizug",
                                "Seilzug", "Bogen", "Gummizug", "Nockenmechanismus"],
    "Empfang Steins": ["Greifen und Legen", "Chute/Netz", "Eimer"],
    "Steuerung": ["SOC", "FPGA", "Mikrokontroller", "Raspberry Pi"],
    "Zustand Anzeige": ["LEDs", "Ton", "Display", "Anzeige auf Laptop", "Haptisch", "Serieller Monitor"],
    "Compiler/Programmiersprache": ["Matlab", "C/C++", "Python", "MicroPython", "NodeRed", "Java", "Verilog", "VHDL"]
}

import random
from pprint import pprint

# Your morphological box
morphological_box = {
    "Energieversorgung": ["Batterie", "Netzteil", "Solarzelle"],
    "Basisstruktur": ["Kubisch", "Kreuzförmig", "H-Förmig", "Dreieckförmig",
                      "Portalbasis", "Roboterarm", "Radial", "Zylindrisch", "Schere"],
    "Material": ["Aluminium", "Polymere/3D Druck", "Acryl"],
    "Dateneingabe": ["Kabel", "WLAN", "Bluetooth", "LoRa"],
    "Datenaufnahme TURM": ["Infrarot", "Kamera", "Näherungssensor", "Ultrashallsensor",
                           "Drucksensor", "Neigungssensor", "DMS", "IMU/Bewegungssensor"],
    "Datenaufnahme STEIN": ["Kraftsensor", "Kamera", "Infrarot", "Näherungssensor", "Ultrashallsensor",
                            "Hall-Sensor", "Capacitative Touch", "Computer Vision"],
    "Datenaufnahme AKTORPOSITION": ["Positionsgeber", "Kamera", "Infrarot", "Potentiometer",
                                    "Mikrotaster", "Time of Flight", "Reedschalter", "Hallsensor"],
    "Signalverstärkung": ["Platine"],
    "Datenverarbeitung": ["Maschinelles Lernen", "FEM & Strukturdynamik", "Robot Operating System/CAD",
                          "Finite State Machines"],
    "Antrieb": ["E-Motor", "Hubmagnet", "Zahnradssystem/Uhrwerk"],
    "Positionierung Aktorik": ["Zugspindel", "Zahnstangenantrieb", "Seilzug", "Leitungsbahn",
                               "Linearmotoren", "Zahnriemen"],
    "Wirkprinzip auf Stein": ["Schieben", "Schießen", "Adhäsion", "Klopfen", "Vibration"],
    "Interagierendes Element": ["Nadelstoß", "Hubmagnet", "Haftmittel", "Wrecking Ball", "Bogen", "Gummizug",
                                "Seilzug", "Nockenmechanismus"],
    "Empfang Steins": ["Greifen und Legen", "Chute/Netz", "Eimer"],
    "Steuerung": ["SOC", "FPGA", "Mikrokontroller", "Raspberry Pi"],
    "Zustand Anzeige": ["LEDs", "Ton", "Display", "Anzeige auf Laptop", "Haptisch", "Serieller Monitor"],
    "Compiler/Programmiersprache": ["Matlab", "C/C++", "Python", "MicroPython", "NodeRed", "Java", "Verilog", "VHDL"]
}

# 💰 PRICE MAP — YOU NEED TO FILL THIS IN!
# Format: price_map["Category"]["Option"] = price_in_euros
# Example:
price_map = {
    "Energieversorgung": {
        "Batterie": 10,
        "Netzteil": 15,
        "Solarzelle": 25
    },
    "Basisstruktur": {
        "Kubisch": 30,
        "Kreuzförmig": 35,
        "H-Förmig": 40,
        "Dreieckförmig": 25,
        "Portalbasis": 60,
        "Roboterarm": 200,
        "Radial": 50,
        "Zylindrisch": 45,
        "Schere": 30
    },
    "Material": {
        "Aluminium": 50,
        "Polymere/3D Druck": 20,
        "Acryl": 15
    },
    "Dateneingabe": {
        "Kabel": 2,
        "WLAN": 8,
        "Bluetooth": 6,
        "LoRa": 12
    },
    "Datenaufnahme TURM": {
        "Infrarot": 5,
        "Kamera": 25,
        "Näherungssensor": 4,
        "Ultrashallsensor": 8,
        "Drucksensor": 12,
        "Neigungssensor": 10,
        "DMS": 15,
        "IMU/Bewegungssensor": 20
    },
    "Datenaufnahme STEIN": {
        "Kraftsensor": 18,
        "Kamera": 25,
        "Infrarot": 5,
        "Näherungssensor": 4,
        "Ultrashallsensor": 8,
        "Hall-Sensor": 3,
        "Capacitative Touch": 10,
        "Computer Vision": 0  # Software; maybe no hardware cost
    },
    "Datenaufnahme AKTORPOSITION": {
        "Positionsgeber": 20,
        "Kamera": 25,
        "Infrarot": 5,
        "Potentiometer": 3,
        "Mikrotaster": 1,
        "Time of Flight": 15,
        "Reedschalter": 2,
        "Hallsensor": 3
    },
    "Signalverstärkung": {
        "Platine": 10  # generic
    },
    "Datenverarbeitung": {
        "Maschinelles Lernen": 0,      # software
        "FEM & Strukturdynamik": 0,
        "Robot Operating System/CAD": 0,
        "Finite State Machines": 0
    },
    "Antrieb": {
        "E-Motor": 20,
        "Hubmagnet": 12,
        "Zahnradssystem/Uhrwerk": 8
    },
    "Positionierung Aktorik": {
        "Zugspindel": 30,
        "Zahnstangenantrieb": 25,
        "Seilzug": 10,
        "Leitungsbahn": 15,
        "Linearmotoren": 50,
        "Zahnriemen": 20
    },
    "Wirkprinzip auf Stein": {
        "Schieben": 0,
        "Schießen": 0,
        "Adhäsion": 5,      # e.g., glue or tape
        "Klopfen": 0,
        "Vibration": 0
    },
    "Interagierendes Element": {
        "Nadelstoß": 5,
        "Hubmagnet": 12,
        "Haftmittel": 3,
        "Wrecking Ball": 20,
        "Bogen": 10,
        "Gummizug": 2,
        "Seilzug": 8,
        "Nockenmechanismus": 25
    },
    "Empfang Steins": {
        "Greifen und Legen": 30,   # includes gripper
        "Chute/Netz": 5,
        "Eimer": 8
    },
    "Steuerung": {
        "SOC": 40,
        "FPGA": 80,
        "Mikrokontroller": 5,
        "Raspberry Pi": 45
    },
    "Zustand Anzeige": {
        "LEDs": 2,
        "Ton": 1,
        "Display": 15,
        "Anzeige auf Laptop": 0,  # assumed available
        "Haptisch": 10,
        "Serieller Monitor": 0
    },
    "Compiler/Programmiersprache": {
        "Matlab": 0,   # assume license not counted
        "C/C++": 0,
        "Python": 0,
        "MicroPython": 0,
        "NodeRed": 0,
        "Java": 0,
        "Verilog": 0,
        "VHDL": 0
    }
}

def calculate_total_cost(solution, price_map):
    """Calculate total hardware/software cost of a solution."""
    total = 0
    for category, option in solution.items():
        if category not in price_map:
            raise KeyError(f"Category '{category}' missing in price_map!")
        if option not in price_map[category]:
            raise KeyError(f"Option '{option}' missing in price_map['{category}']!")
        total += price_map[category][option]
    return total

def is_compatible(solution):
    """Check if a solution satisfies all compatibility rules."""
    # Rule R1: Computer Vision requires Kamera in Datenaufnahme STEIN
    if solution["Datenaufnahme STEIN"] == "Computer Vision":
        if "Kamera" not in [solution["Datenaufnahme TURM"],
                            solution["Datenaufnahme STEIN"],
                            solution["Datenaufnahme AKTORPOSITION"]]:
            return False

    # Rule R2 & R3: Language → Steuerung
    lang = solution["Compiler/Programmiersprache"]
    steuerung = solution["Steuerung"]
    if lang in ["Verilog", "VHDL"] and steuerung != "FPGA":
        return False
    if lang in ["MicroPython", "NodeRed"] and steuerung != "Mikrokontroller":
        return False

    # Rule R4: Schieben → Haftmittel
    if solution["Wirkprinzip auf Stein"] == "Schieben" and solution["Interagierendes Element"] != "Haftmittel":
        return False

    # Rule R5: Gummizug → Schießen
    if solution["Interagierendes Element"] == "Gummizug" and solution["Wirkprinzip auf Stein"] != "Schießen":
        return False

    # Rule R6: Wrecking Ball → Schießen or Klopfen
    if solution["Interagierendes Element"] == "Wrecking Ball":
        if solution["Wirkprinzip auf Stein"] not in ["Schießen", "Klopfen"]:
            return False

    # Rule R7: Bogen → Schießen
    if solution["Interagierendes Element"] == "Bogen" and solution["Wirkprinzip auf Stein"] != "Schießen":
        return False

    # Note: Removed invalid rule about "Greifen" (not in Wirkprinzip options)

    return True

def generate_valid_solution(max_attempts=10**6):
    for _ in range(max_attempts):
        candidate = {cat: random.choice(opts) for cat, opts in morphological_box.items()}
        if is_compatible(candidate):
            return candidate
    raise RuntimeError("Failed to generate a valid solution after many attempts. Check constraints!")

def generate_n_valid_solutions(n):
    return [generate_valid_solution() for _ in range(n)]

# Example usage
if __name__ == "__main__":
    solutions = generate_n_valid_solutions(130)
    for i, sol in enumerate(solutions, 1):
        cost = calculate_total_cost(sol, price_map)
        print(f"\nSolution {i} — Estimated Cost: €{cost:.2f}")
        print("-" * 50)
        for k, v in sol.items():
            print(f"{k:<25}: {v}")

def is_compatible(solution):
    """Check if a solution satisfies all compatibility rules."""
    # Rule R1: Computer Vision requires Kamera in Datenaufnahme STEIN
    if solution["Datenaufnahme STEIN"] == "Computer Vision":
        if "Kamera" not in [solution["Datenaufnahme TURM"],
                            solution["Datenaufnahme STEIN"],
                            solution["Datenaufnahme AKTORPOSITION"]]:
            return False

    # Rule R2 & R3: Language → Steuerung
    lang = solution["Compiler/Programmiersprache"]
    steuerung = solution["Steuerung"]
    if lang in ["Verilog", "VHDL"] and steuerung != "FPGA":
        return False
    if lang in ["MicroPython", "NodeRed"] and steuerung != "Mikrocontroller":
        return False

    # Rule R4: Schieben → Haftmittel
    if solution["Wirkprinzip auf Stein"] == "Schieben" and solution["Interagierendes Element"] != "Haftmittel":
        return False

    # Rule R5: Gummizug → Schießen
    if solution["Interagierendes Element"] == "Gummizug" and solution["Wirkprinzip auf Stein"] != "Schießen":
        return False

    # Rule R6: Wrecking Ball → Schießen or Klopfen
    if solution["Interagierendes Element"] == "Wrecking Ball":
        if solution["Wirkprinzip auf Stein"] not in ["Schießen", "Klopfen"]:
            return False

    # Rule R7: Bogen → Schießen
    if solution["Interagierendes Element"] == "Bogen" and solution["Wirkprinzip auf Stein"] != "Schießen":
        return False
    if solution["Wirkprinzip auf Stein"] == "Greifen" and solution["Interagierendes Element"] not in  [""]:
        return False

    return True

def generate_valid_solution(max_attempts=10**6):
    """Generate one valid solution using rejection sampling."""
    for _ in range(max_attempts):
        candidate = {cat: random.choice(opts) for cat, opts in morphological_box.items()}
        if is_compatible(candidate):
            return candidate
    raise RuntimeError("Failed to generate a valid solution after many attempts. Check constraints!")

def generate_n_valid_solutions(n):
    """Generate n valid solutions."""
    return [generate_valid_solution() for _ in range(n)]

# Example usage
if __name__ == "__main__":
    solutions = generate_n_valid_solutions(130)
    for i, sol in enumerate(solutions, 1):
        print(f"\nSolution {i}")
        print("-" * 40)
        for k, v in sol.items():
            print(f"{k:<25}: {v}")
