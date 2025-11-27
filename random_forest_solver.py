import random
import pandas as pd

morphological_box = {
    "Energieversorgung": ["Batterie", "Netzteil", "Solarzelle"],
    "Basisstruktur": ["Kubisch", "Kreuzförmig", "H-Förmig", "Dreieckförmig", "Portalbasis", "Roboterarm", "Radial",
                      "Zylindrisch", "Schere"],
    "Material": ["Aluminium", "Polymere/3D Druck", "Acryl"],
    "Dateneingabe": ["Kabel", "WLAN", "Bluetooth", "LoRa"],
    "Datenaufnahme TURM": ["Infrarot", "Kamera", "Näherungssensor", "Ultrashallsensor", "Drucksensor", "Neigungssensor",
                           "DMS", "IMU/Bewegungssensor"],
    "Datenaufnahme STEIN": ["Kraftsensor", "Kamera", "Infrarot", "Näherungssensor", "Ultrashallsensor", "Hall-Sensor",
                            "Capacitative Touch", "Computer Vision"],
    "Datenaufnahme AKTORPOSITION": ["Positionsgeber", "Kamera", "Infrarot", "Potentiometer", "Mikrotaster",
                                    "Time of Flight", "Reedschalter", "Hallsensor"],
    "Signalverstärkung": ["Platine"],
    "Datenverarbeitung": ["Maschinelles Lernen", "FEM & Strukturdynamik", "Robot Operating System/CAD",
                          "Finite State Machines"],
    "Antrieb": ["E-Motor", "Hubmagnet", "Zahnradssystem/Uhrwerk"],
    "Positionierung Aktorik": ["Zugspindel", "Zahnstangenantrieb", "Seilzug", "Leitungsbahn", "Linearmotoren",
                               "Zahnriemen"],
    "Wirkprinzip auf Stein": ["Schießen", "Schieben", "Adhäsion", "Greifen", "Klopfen", "Vibration"],
    "Interagierendes Element": ["Nadelstoß", "Hubmagnet", "Haftmittel", "Wrecking Ball", "Bogen", "Gummizug",
                                "Seilzug"],
    "Steuerung": ["SOC", "FPGA", "Mikrocontroller"],
    "Zustand Anzeige": ["LEDs", "Ton", "Display", "Anzeige auf Laptop", "Haptisch", "Serieller Monitor"],
    "Compiler/Programmiersprache": ["Matlab", "C/C++", "Python", "MicroPython", "NodeRed", "Java", "Verilog", "VHDL"]
}

def is_compatible(solution):
    if solution["Datenaufnahme STEIN"] == "Computer Vision":
        if "Kamera" not in [solution["Datenaufnahme TURM"],
                            solution["Datenaufnahme STEIN"],
                            solution["Datenaufnahme AKTORPOSITION"]]:
            return False
    lang = solution["Compiler/Programmiersprache"]
    steuerung = solution["Steuerung"]
    if lang in ["Verilog", "VHDL"] and steuerung != "FPGA":
        return False
    if lang in ["MicroPython", "NodeRed"] and steuerung != "Mikrocontroller":
        return False
    if solution["Wirkprinzip auf Stein"] == "Schieben" and solution["Interagierendes Element"] != "Haftmittel":
        return False
    if solution["Interagierendes Element"] == "Gummizug" and solution["Wirkprinzip auf Stein"] != "Schießen":
        return False
    if solution["Interagierendes Element"] == "Wrecking Ball":
        if solution["Wirkprinzip auf Stein"] not in ["Schießen", "Klopfen"]:
            return False
    if solution["Interagierendes Element"] == "Bogen" and solution["Wirkprinzip auf Stein"] != "Schießen":
        return False
    return True


def generate_valid_solution(max_attempts=1000):
    for _ in range(max_attempts):
        candidate = {cat: random.choice(opts) for cat, opts in morphological_box.items()}
        if is_compatible(candidate):
            return candidate
    raise RuntimeError("Kein gültiges Design gefunden!")

component_costs = {
    "Batterie": 10, "Netzteil": 15, "Solarzelle": 25,
    "Kubisch": 20, "Kreuzförmig": 22, "H-Förmig": 25, "Dreieckförmig": 18, "Portalbasis": 40,
    "Roboterarm": 60, "Radial": 30, "Zylindrisch": 28, "Schere": 35,
    "Aluminium": 30, "Polymere/3D Druck": 10, "Acryl": 15,
    "Kabel": 5, "WLAN": 12, "Bluetooth": 8, "LoRa": 20,
    "Kamera": 40, "Infrarot": 8, "Näherungssensor": 6, "Ultrashallsensor": 10,
    "Drucksensor": 12, "Neigungssensor": 9, "DMS": 15, "IMU/Bewegungssensor": 25,
    "Kraftsensor": 18, "Hall-Sensor": 7, "Capacitative Touch": 22,
    "Computer Vision": 0,  # software, cost via processing
    "Positionsgeber": 14, "Potentiometer": 5, "Mikrotaster": 2,
    "Time of Flight": 30, "Reedschalter": 3, "Hallsensor": 7,
    "Platine": 25,
    "Maschinelles Lernen": 0, "FEM & Strukturdynamik": 0,
    "Robot Operating System/CAD": 0, "Finite State Machines": 0,
    "E-Motor": 35, "Hubmagnet": 20, "Zahnradssystem/Uhrwerk": 15,
    "Zugspindel": 28, "Zahnstangenantrieb": 32, "Seilzug": 10,
    "Leitungsbahn": 20, "Linearmotoren": 50, "Zahnriemen": 18,
    "Schießen": 0, "Schieben": 0, "Adhäsion": 0, "Greifen": 0, "Klopfen": 0, "Vibration": 0,
    "Nadelstoß": 12, "Haftmittel": 5, "Wrecking Ball": 25, "Bogen": 20, "Gummizug": 8, "Seilzug": 10,
    "SOC": 45, "FPGA": 80, "Mikrocontroller": 25,
    "LEDs": 2, "Ton": 3, "Display": 15, "Anzeige auf Laptop": 0,
    "Haptisch": 20, "Serieller Monitor": 0,
    "Matlab": 0, "C/C++": 0, "Python": 0, "MicroPython": 0,
    "NodeRed": 0, "Java": 0, "Verilog": 0, "VHDL": 0
}

component_scores = {
    # Beispiel – ERSETZE MIT DEINEN WERTEN!
    "Batterie": {"Adaptivity": 3, "Precision": 3, "Stability": 4, "Speed": 3},
    "Netzteil": {"Adaptivity": 2, "Precision": 5, "Stability": 5, "Speed": 4},
    "Solarzelle": {"Adaptivity": 4, "Precision": 2, "Stability": 3, "Speed": 2},

    "E-Motor": {"Adaptivity": 4, "Precision": 4, "Stability": 4, "Speed": 5},
    "Hubmagnet": {"Adaptivity": 2, "Precision": 3, "Stability": 3, "Speed": 4},
    "Zahnradssystem/Uhrwerk": {"Adaptivity": 1, "Precision": 4, "Stability": 5, "Speed": 2},

    "Kamera": {"Adaptivity": 5, "Precision": 5, "Stability": 3, "Speed": 4},
    "Infrarot": {"Adaptivity": 3, "Precision": 3, "Stability": 4, "Speed": 4},
    "Ultrashallsensor": {"Adaptivity": 4, "Precision": 3, "Stability": 3, "Speed": 3},

    "FPGA": {"Adaptivity": 3, "Precision": 5, "Stability": 5, "Speed": 5},
    "Mikrocontroller": {"Adaptivity": 5, "Precision": 4, "Stability": 4, "Speed": 4},
    "SOC": {"Adaptivity": 4, "Precision": 4, "Stability": 4, "Speed": 4},

    "Schießen": {"Adaptivity": 3, "Precision": 4, "Stability": 3, "Speed": 5},
    "Schieben": {"Adaptivity": 4, "Precision": 3, "Stability": 4, "Speed": 3},
    "Greifen": {"Adaptivity": 5, "Precision": 5, "Stability": 4, "Speed": 2},

    "Bogen": {"Adaptivity": 2, "Precision": 4, "Stability": 4, "Speed": 4},
    "Gummizug": {"Adaptivity": 3, "Precision": 3, "Stability": 2, "Speed": 5},
    "Wrecking Ball": {"Adaptivity": 1, "Precision": 2, "Stability": 3, "Speed": 3},

}

# Fallback
DEFAULT_SCORE = {"Adaptivity": 3, "Precision": 3, "Stability": 3, "Speed": 3}

def rate_cost(total_cost):
    if total_cost < 30:
        return 5
    elif total_cost < 60:
        return 4
    elif total_cost < 90:
        return 3
    elif total_cost < 120:
        return 2
    else:
        return 1

    return int(input(f"Rate total cost €{total_cost} (1-5): "))


def evaluate_solution(solution):
    total_cost = 0
    crit_sums = {"Adaptivity": 0, "Precision": 0, "Stability": 0, "Speed": 0}

    for category, component in solution.items():

        cost = component_costs.get(component, 0)
        total_cost += cost

        scores = component_scores.get(component, DEFAULT_SCORE)
        for crit in crit_sums:
            crit_sums[crit] += scores[crit]

    n = len(solution)
    adaptivity = crit_sums["Adaptivity"] / n
    precision = crit_sums["Precision"] / n
    stability = crit_sums["Stability"] / n
    speed = crit_sums["Speed"] / n

    cost_rating = rate_cost(total_cost)

    final_score = (
            adaptivity * 0.30 +
            precision * 0.20 +
            stability * 0.40 +
            speed * 0.05 +
            cost_rating * 0.05
    )

    return {
        "Solution": solution,
        "Total Cost (€)": round(total_cost, 2),
        "Cost Rating (1-5)": cost_rating,
        "Adaptivity": round(adaptivity, 2),
        "Precision": round(precision, 2),
        "Stability": round(stability, 2),
        "Speed": round(speed, 2),
        "Final Score (0-5)": round(final_score, 2)
    }


N = 100  # Number of valid solutions to evaluate

print(f"🔍 Generating and evaluating {N} valid solutions...\n")
results = []

for i in range(N):
    sol = generate_valid_solution()
    res = evaluate_solution(sol)
    results.append(res)

df = pd.DataFrame(results)
df = df.sort_values("Final Score (0-5)", ascending=False).reset_index(drop=True)

print("=" * 100)
print("🏆 TOP 10 SOLUTIONS (Ranked by Final Score)")
print("=" * 100)

for idx in range(min(10, len(df))):
    row = df.iloc[idx]
    print(f"\n🥇 Rank {idx + 1} | Final Score: {row['Final Score (0-5)']}/5 | Cost: €{row['Total Cost (€)']}")
    print("-" * 80)
    for cat, comp in row["Solution"].items():
        print(f"{cat:<25}: {comp}")


df.to_excel("excel_list/ranked_solutions.xlsx", index=False)