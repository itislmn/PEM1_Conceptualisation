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
    "Wirkprinzip auf Stein": ["Schießen", "Schieben", "Adhäsion", "Greifen", "Klopfen", "Vibration"],
    "Interagierendes Element": ["Nadelstoß", "Hubmagnet", "Haftmittel", "Wrecking Ball", "Bogen", "Gummizug",
                                "Seilzug"],
    "Steuerung": ["SOC", "FPGA", "Mikrokontroller"],
    "Zustand Anzeige": ["LEDs", "Ton", "Display", "Anzeige auf Laptop", "Haptisch", "Serieller Monitor"],
    "Compiler/Programmiersprache": ["Matlab", "C/C++", "Python", "MicroPython", "NodeRed", "Java", "Verilog", "VHDL"]
}

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
