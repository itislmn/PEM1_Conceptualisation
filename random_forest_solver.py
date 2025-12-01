import random
import csv
import pandas as pd
from pprint import pprint
from sklearn.ensemble import RandomForestRegressor

# =====================================================
# === 1) YOUR ORIGINAL MORPHOLOGICAL BOX (UNCHANGED) ===
# =====================================================
morphological_box = {
    "Energieversorgung": ["Batterie", "Netzteil", "Solarzelle"],
    "Basisstruktur": ["Kubisch", "Kreuzförmig", "H-Förmig", "Trussförmig", "Roboterarm", "Zylindrisch", "Schere", "Portalbasis",
                      "Pendel"],
    "Material": ["Aluminium", "Polymere"],
    "Dateneingabe": ["Keypad", "Laptop", "Controller/Joystick", "Touchscreen", "Webseite", "App/GUI", "Handgesten"],
    "Datenübertragung": ["Kabel", "WLAN", "Bluetooth", "LoRa"],
    "Datenaufnahme TURM": ["Infrarot", "Kamera", "Näherungssensor", "Ultrashallsensor",
                           "Drucksensor", "Neigungssensor", "DMS", "IMU/Bewegungssensor"],
    "Datenaufnahme STEIN": ["Kraftsensor", "Kamera", "Infrarot", "Näherungssensor", "Ultrashallsensor"
                            , "Computer Vision"],
    "Datenaufnahme AKTORPOSITION": ["Positionsgeber", "Kamera", "Infrarot", "Potentiometer",
                                    "Mikrotaster", "Time of Flight", "Reedschalter", "Hallsensor"],
    "Signalverstärkung": ["Platine"],
    "Datenverarbeitung": ["Maschinelles Lernen", "FEM & Strukturdynamik", "Robot Operating System/CAD",
                          "Finite State Machines", "Computer Vision"],
    "Antrieb": ["E-Motor", "Hubmagnet", "Zahnradsystem"],
    "Positionierung Aktorik": ["Zugspindel", "Zahnstangenantrieb", "Seilzug", "Zahnriemen", "Vibrationsmotor"],
    "Wirkprinzip auf Stein": ["Schieben", "Schießen", "Adhäsion", "Klopfen", "Vibration"],
    "Interagierendes Element": ["Nadelstoß", "Hubmagnetelement", "Haftmittel", "Wrecking Ball", "Bogen", "Gummizug",
                                "Seilzug", "Nockenmechanismus", "Vibration"],
    "Empfang Steins": ["Greifen und Legen", "Chute/Netz", "Eimer"],
    "Steuerung": ["SOC", "FPGA", "Mikrokontroller", "Raspberry Pi"],
    "Zustand Anzeige": ["LEDs", "Ton", "Display", "Anzeige auf Laptop", "Haptisch", "Serieller Monitor"],
}

# =====================================================
# === 2) PRICE MAP (UNCHANGED) ===
# =====================================================

price_map = {
    "Energieversorgung": {"Batterie": 25, "Netzteil": 0, "Solarzelle": 50},
    "Basisstruktur": {
        "Kubisch": 0, "Kreuzförmig": 0, "H-Förmig": 0, "Trussförmig": 0, "Roboterarm": 0, "Zylindrisch": 0, "Schere": 0
        , "Portalbasis": 0, "Pendel": 0
    },
    "Material": {"Aluminium": 0, "Polymere": 0},
    "Dateneingabe": {"Keypad": 5, "Laptop": 0, "Controller/Joystick": 2.49, "Touchscreen": 10.99, "Website": 0, "App/GUI": 0, "Handgesten": 0},
    "Datenübertragung": {"Kabel": 2, "WLAN": 3, "Bluetooth": 3, "LoRa": 40},
    "Datenaufnahme TURM": {
        "Infrarot": 6, "Kamera": 3.99, "Näherungssensor": 5.3, "Ultrashallsensor": 4.4,
        "Drucksensor": 6.99, "Neigungssensor": 1.59, "DMS": 8.25, "IMU/Bewegungssensor": 9.49
    },
    "Datenaufnahme STEIN": {
        "Kraftsensor": 18, "Kamera": 3.99, "Infrarot": 5, "Näherungssensor": 4, "Ultrashallsensor": 4.4
        , "Computer Vision": 0
    },
    "Datenaufnahme AKTORPOSITION": {
        "Positionsgeber": 1.79, "Kamera": 3.99, "Infrarot": 5, "Potentiometer": 2.59,
        "Mikrotaster": 1, "Time of Flight": 4.33, "Reedschalter": 6, "Hallsensor": 2.19
    },
    "Signalverstärkung": {"Platine": 8},
    "Datenverarbeitung": {
        "Maschinelles Lernen": 0, "FEM & Strukturdynamik": 0,
        "Robot Operating System/CAD": 0, "Finite State Machines": 0, "Camera Vision": 0
    },
    "Antrieb": {"E-Motor": 5, "Hubmagnet": 15, "Zahnradsystem": 8},
    "Positionierung Aktorik": {
        "Zugspindel": 5.13, "Zahnstangenantrieb": 10, "Seilzug": 6, "Zahnriemen": 20, "Vibrationsmotor": 4
    },
    "Wirkprinzip auf Stein": {"Schieben": 0, "Schießen": 0, "Adhäsion": 0, "Klopfen": 0, "Vibration": 0},
    "Interagierendes Element": {
        "Nadelstoß": 5, "Hubmagnetelement": 15, "Haftmittel": 5, "Wrecking Ball": 0,
        "Bogen": 7, "Gummizug": 4, "Seilzug": 7, "Nockenmechanismus": 5, "Vibration": 4, "Saugnäpfe": 4
    },
    "Empfang Steins": {"Greifen und Legen": 25, "Chute/Netz": 3, "Eimer": 3},
    "Steuerung": {"SOC": 15, "Mikrokontroller": 20, "Raspberry Pi": 45},
    "Zustand Anzeige": {"LEDs": 1, "Ton": 3, "Display": 15, "Anzeige auf Laptop": 0, "Haptisch": 0.85,
                        "Serieller Monitor": 0},
}

structure_mass_map = {
    "Kubisch": 8,
    "Kreuzförmig": 6,
    "H-Förmig": 4,
    "Trussförmig": 5,
    "Roboterarm": 35,
    "Zylindrisch": 2,
    "Schere": 5,
    "Portalbasis": 6,
    "Pendel": 2
}
material_price_per_stange = {
    "Aluminium": 3,
    "Polymere": 0,
}


# =====================================================
# === 3) COMPATIBILITY CHECKS
# =====================================================
def is_compatible(solution):
    # R1 Computer Vision → camera required
    if solution["Datenaufnahme STEIN"] == "Computer Vision":
        if "Kamera" not in [
            solution["Datenaufnahme TURM"],
            solution["Datenaufnahme AKTORPOSITION"]
        ]:
            return False

    if solution["Datenverarbeitung"] == "Computer Vision":
        if "Kamera" not in [
            solution["Datenaufnahme TURM"],
            solution["Datenaufnahme AKTORPOSITION"]
        ]:
            return False

    if solution["Basisstruktur"] == "Roboterarm" and solution["Material"] != "Polymere/ 3D Druck":
        return False

    # R4
    if solution["Wirkprinzip auf Stein"] == "Schieben" and solution["Interagierendes Element"] != "Haftmittel":
        return False

    # R5 Gummizug → Schießen
    if solution["Interagierendes Element"] == "Gummizug" and solution["Wirkprinzip auf Stein"] != "Schießen":
        return False

    # R6 Wrecking Ball → Schießen or Klopfen
    if solution["Interagierendes Element"] == "Wrecking Ball":
        if solution["Wirkprinzip auf Stein"] not in ["Schießen", "Klopfen"]:
            return False

    # R7 Bogen → Schießen
    if solution["Interagierendes Element"] == "Bogen" and solution["Wirkprinzip auf Stein"] != "Schießen":
        return False

    if solution["Dateneingabe"] == "Handgesten" and solution["Datenaufnahme STEIN"] != "Computer Vision":
        return False

    if solution["Dateneingabe"] == "Handgesten" and solution["Datenaufnahme STEIN"] != "Kamera":
        return False

    if solution["Dateneingabe"] == "Handgesten" and solution["Datenaufnahme TURM"] != "Kamera":
        return False

    if solution["Dateneingabe"] == "Handgesten" and solution["Datenaufnahme AKTORPOSITION"] != "Kamera":
        return False

    return True


# =====================================================
# === 4) GENERATE VALID SOLUTIONS =====================
# =====================================================
def generate_valid_solution(max_attempts=10 ** 6):
    for _ in range(max_attempts):
        candidate = {cat: random.choice(opts) for cat, opts in morphological_box.items()}
        if is_compatible(candidate):
            return candidate
    raise RuntimeError("No compatible solution found.")


def generate_n_valid_solutions(n):
    return [generate_valid_solution() for _ in range(n)]


# =====================================================
# === 5) OPTION RATINGS (YOU FILL THESE IN) ============
# =====================================================
# Each option must get: Adaptivity / Stability / Precision / Speed
# Example: rating_map["Material"]["Aluminium"] = {"adapt":3,"stab":4,"prec":5,"speed":2}
rating_map = {cat: {opt: {"adapt": 3, "stab": 3, "prec": 3, "speed": 3}
                    for opt in opts}
              for cat, opts in morphological_box.items()}


# You can now manually edit rating_map before training.
rating_map["Basisstruktur"]["Kubisch"] = {"adapt": 3, "stab": 3, "prec": 4, "speed": 2}
rating_map["Basisstruktur"]["H-Förmig"] = {"adapt": 2, "stab": 3, "prec": 3, "speed": 3}
rating_map["Basisstruktur"]["Kreuzförmig"] = {"adapt": 2, "stab": 3, "prec": 3, "speed": 4}
rating_map["Basisstruktur"]["Trussförmig"] = {"adapt": 2, "stab": 3, "prec": 3, "speed": 4}
rating_map["Basisstruktur"]["Roboterarm"] = {"adapt": 5, "stab": 3, "prec": 5, "speed": 2}
rating_map["Basisstruktur"]["Zylindrisch"] = {"adapt": 4, "stab": 3, "prec": 3, "speed": 3}
rating_map["Basisstruktur"]["Schere"] = {"adapt": 2, "stab": 3, "prec": 3, "speed": 3}
rating_map["Basisstruktur"]["Portalbasis"] = {"adapt": 2, "stab": 3, "prec": 4, "speed": 2}
rating_map["Basisstruktur"]["Pendel"] = {"adapt": 1, "stab": 3, "prec": 3, "speed": 5}

rating_map["Material"]["Aluminium"] = {"adapt":3,"stab":5,"prec":3,"speed":4}
rating_map["Material"]["Polymere"] = {"adapt":3,"stab":2,"prec":3,"speed":3}

rating_map["Dateneingabe"]["Keypad"] = {"adapt":3,"stab":5,"prec":5,"speed":3}
rating_map["Dateneingabe"]["Laptop"] = {"adapt":3,"stab":5,"prec":5,"speed":3}
rating_map["Dateneingabe"]["Controller/Joystick"] = {"adapt":3,"stab":5,"prec":5,"speed":3}
rating_map["Dateneingabe"]["Touchscreen"] = {"adapt":3,"stab":5,"prec":4,"speed":3}
rating_map["Dateneingabe"]["Website"] = {"adapt":3,"stab":5,"prec":3,"speed":2}
rating_map["Dateneingabe"]["App/GUI"] = {"adapt":3,"stab":5,"prec":3,"speed":1}
rating_map["Dateneingabe"]["Handgesten"] = {"adapt":3,"stab":5,"prec":3,"speed":2}

rating_map["Datenübertragung"]["Kabel"] = {"adapt":5,"stab":4,"prec":3,"speed":5}
rating_map["Datenübertragung"]["WLAN"] = {"adapt":3,"stab":2,"prec":3,"speed":2}
rating_map["Datenübertragung"]["Bluetooth"] = {"adapt":3,"stab":3,"prec":3,"speed":3}
rating_map["Datenübertragung"]["LoRa"] = {"adapt":3,"stab":4,"prec":3,"speed":4}

rating_map["Datenaufnahme TURM"]["Infrarot"] = {"adapt":3,"stab":5,"prec":3,"speed":5}
rating_map["Datenaufnahme TURM"]["Kamera"] = {"adapt":4,"stab":5,"prec":5,"speed":2}
rating_map["Datenaufnahme TURM"]["Näherungssensor"] = {"adapt":2,"stab":5,"prec":3,"speed":5}
rating_map["Datenaufnahme TURM"]["Ultraschallsensor"] = {"adapt":3,"stab":5,"prec":3,"speed":3}
rating_map["Datenaufnahme TURM"]["Drucksensor"] = {"adapt":1,"stab":5,"prec":4,"speed":5}
rating_map["Datenaufnahme TURM"]["Neigungssensor"] = {"adapt":4,"stab":5,"prec":4,"speed":5}
rating_map["Datenaufnahme TURM"]["DMS"] = {"adapt":1,"stab":5,"prec":5,"speed":5}
rating_map["Datenaufnahme TURM"]["IMU/Bewegungssensor"] = {"adapt":3,"stab":5,"prec":3,"speed":5}

rating_map["Datenaufnahme STEIN"]["Kraftsensor"] = {"adapt":4,"stab":5,"prec":5,"speed":2}
rating_map["Datenaufnahme STEIN"]["Kamera"] = {"adapt":4,"stab":5,"prec":5,"speed":2}
rating_map["Datenaufnahme STEIN"]["Infrarot"] = {"adapt":3,"stab":5,"prec":3,"speed":5}
rating_map["Datenaufnahme STEIN"]["Näherungssensor"] = {"adapt":2,"stab":5,"prec":3,"speed":5}
rating_map["Datenaufnahme STEIN"]["Ultraschallsensor"] = {"adapt":3,"stab":5,"prec":3,"speed":3}
rating_map["Datenaufnahme STEIN"]["Computer Vision"] = {"adapt":4,"stab":5,"prec":5,"speed":2}

rating_map["Datenaufnahme AKTORPOSITION"]["Positionsgeber"] = {"adapt":4,"stab":5,"prec":4,"speed":5}
rating_map["Datenaufnahme AKTORPOSITION"]["Kamera"] = {"adapt":4,"stab":5,"prec":5,"speed":2}
rating_map["Datenaufnahme AKTORPOSITION"]["Infrarot"] = {"adapt":3,"stab":5,"prec":3,"speed":5}
rating_map["Datenaufnahme AKTORPOSITION"]["Potentiometer"] = {"adapt":3,"stab":5,"prec":4,"speed":5}
rating_map["Datenaufnahme AKTORPOSITION"]["Mikrotaster"] = {"adapt":3,"stab":5,"prec":5,"speed":4}
rating_map["Datenaufnahme AKTORPOSITION"]["Time of Flight"] = {"adapt":4,"stab":5,"prec":4,"speed":3}
rating_map["Datenaufnahme AKTORPOSITION"]["Reedschalter"] = {"adapt":3,"stab":5,"prec":3,"speed":4}
rating_map["Datenaufnahme AKTORPOSITION"]["Hallsensor"] = {"adapt":4,"stab":5,"prec":5,"speed":4}

rating_map["Signalverstärkung"]["Platine"] = {"adapt":5,"stab":5,"prec":5,"speed":5}

rating_map["Datenverarbeitung"]["Maschinelles Lernen"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Datenverarbeitung"]["FEM & Strukturdynamik"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Datenverarbeitung"]["Robot Operating System/CAD"] = {"adapt":3,"stab":5,"prec":5,"speed":5}
rating_map["Datenverarbeitung"]["Finite State Machines"] = {"adapt":2,"stab":5,"prec":5,"speed":2}
rating_map["Datenverarbeitung"]["Computer Vision"] = {"adapt":5,"stab":5,"prec":5,"speed":5}

rating_map["Antrieb"]["E-Motor"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Antrieb"]["Hubmagnet"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Antrieb"]["Zahnradsystem"] = {"adapt":5,"stab":5,"prec":4,"speed":3}

rating_map["Positionierung Aktorik"]["Zugspindel"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Positionierung Aktorik"]["Zahnstangenantrieb"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Positionierung Aktorik"]["Seilzug"] = {"adapt":5,"stab":3,"prec":5,"speed":5}
rating_map["Positionierung Aktorik"]["Zahnriemen"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Positionierung Aktorik"]["Vibrationsmotor"] = {"adapt":5,"stab":1,"prec":5,"speed":5}

rating_map["Wirkprinzip auf Stein"]["Schieben"] = {"adapt":4,"stab":5,"prec":3,"speed":3}
rating_map["Wirkprinzip auf Stein"]["Schießen"] = {"adapt":2,"stab":3,"prec":4,"speed":5}
rating_map["Wirkprinzip auf Stein"]["Adhäsion"] = {"adapt":1,"stab":3,"prec":2,"speed":3}
rating_map["Wirkprinzip auf Stein"]["Klopfen"] = {"adapt":5,"stab":4,"prec":5,"speed":4}
rating_map["Wirkprinzip auf Stein"]["Vibration"] = {"adapt":1,"stab":1,"prec":1,"speed":1}

rating_map["Interagierendes Element"]["Nadelstoß"] = {"adapt":5,"stab":5,"prec":5,"speed":4}
rating_map["Interagierendes Element"]["Hubmagnetelement"] = {"adapt":2,"stab":3,"prec":5,"speed":5}
rating_map["Interagierendes Element"]["Haftmittel"] = {"adapt":1,"stab":3,"prec":2,"speed":4}
rating_map["Interagierendes Element"]["Wrecking Ball"] = {"adapt":4,"stab":2,"prec":2,"speed":5}
rating_map["Interagierendes Element"]["Bogen"] = {"adapt":4,"stab":5,"prec":3,"speed":3}
rating_map["Interagierendes Element"]["Gummizug"] = {"adapt":4,"stab":5,"prec":4,"speed":4}
rating_map["Interagierendes Element"]["Seilzug"] = {"adapt":4,"stab":5,"prec":4,"speed":4}
rating_map["Interagierendes Element"]["Nockenmechanismus"] = {"adapt":3,"stab":5,"prec":5,"speed":4}
rating_map["Interagierendes Element"]["Vibration"] = {"adapt":1,"stab":1,"prec":1,"speed":1}
rating_map["Interagierendes Element"]["Saugnäpfe"] = {"adapt":4,"stab":5,"prec":3,"speed":5}

rating_map["Empfang Steins"]["Greifen und Legen"] = {"adapt":5,"stab":3,"prec":5,"speed":1}
rating_map["Empfang Steins"]["Chute/Netz"] = {"adapt":1,"stab":5,"prec":2,"speed":5}
rating_map["Empfang Steins"]["Eimer"] = {"adapt":1,"stab":5,"prec":3,"speed":5}

rating_map["Steuerung"]["SOC"] = {"adapt":4,"stab":3,"prec":5,"speed":5}
rating_map["Steuerung"]["Mikrocontroller"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Steuerung"]["Raspberry Pi"] = {"adapt":3,"stab":4,"prec":4,"speed":1}

rating_map["Zustand Anzeige"]["LEDs"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Zustand Anzeige"]["Ton"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Zustand Anzeige"]["Display"] = {"adapt":5,"stab":5,"prec":5,"speed":4}
rating_map["Zustand Anzeige"]["Anzeige auf Laptop"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
rating_map["Zustand Anzeige"]["Haptisch"] = {"adapt":3,"stab":5,"prec":5,"speed":1}
rating_map["Zustand Anzeige"]["Serieller Monitor"] = {"adapt":5,"stab":5,"prec":5,"speed":5}
# =====================================================
# === 6) SCORING LOGIC FOR DATASET A ==================
# =====================================================
def calculate_total_cost(solution, price_map, structure_mass_map, material_price_per_stange):
    """
    Computes cost of a solution with the following rules:
    1. Each partial function contributes its option's cost.
    2. If the same device appears in multiple categories, cost is counted only once.
    3. Material cost = price_per_stange[material] * stangen_needed[basis_structure] and counted once.
    4. All other prices from price_map, but each option only once.
    """

    total_cost = 0.0
    charged_devices = set()  # prevent double charging
    breakdown = []           # optional, for debugging

    # --- 1) MATERIAL + STRUCTURE SPECIAL CASE ---
    material = solution.get("Material", None)
    structure = solution.get("Basisstruktur", None)

    if material is not None and structure is not None:
        if structure in structure_mass_map and material in material_price_per_stange:
            stangen_needed = structure_mass_map[structure]
            price_per_stange = material_price_per_stange[material]
            mat_cost = stangen_needed * price_per_stange

            total_cost += mat_cost
            charged_devices.add("MATERIAL_COST")  # avoid recalculating
            breakdown.append(("Material × Structure", mat_cost))
        else:
            breakdown.append(("MATERIAL_MISSING", 0))

    # --- 2) ALL OTHER PARTIAL FUNCTIONS ---
    for category, device in solution.items():
        # skip special keys
        if category in ("Material", "Basisstruktur"):
            continue

        # already charged? skip
        if device in charged_devices:
            continue

        # get its cost
        if category in price_map and device in price_map[category]:
            device_cost = price_map[category][device]
            total_cost += device_cost
            charged_devices.add(device)
            breakdown.append((device, device_cost))
        else:
            breakdown.append((f"{category}:{device}_NO_PRICE", 0))

    return total_cost

    # Final weighted score


def score_solution_option_based(solution):
    """
    Computes the weighted score of a solution using rating_map and cost.
    """

    adapt = stability = precision = speed = 0

    # Sum ratings from each category
    for cat, opt in solution.items():
        r = rating_map.get(cat, {}).get(opt, {"adapt": 0, "stab": 0, "prec": 0, "speed": 0})
        adapt += r.get("adapt", 0)
        stability += r.get("stab", 0)
        precision += r.get("prec", 0)
        speed += r.get("speed", 0)

    # Compute cost and convert to points
    total_cost = calculate_total_cost(solution, price_map, structure_mass_map, material_price_per_stange)

    def cost_to_points(cost, max_cost=150):
        percentage = cost / max_cost
        if percentage <= 0.2: return 5
        if percentage <= 0.4: return 4
        if percentage <= 0.6: return 3
        if percentage <= 0.8: return 2
        return 1

    cost_pts = cost_to_points(total_cost)

    # Final weighted score
    final_score = (
            0.30 * adapt +
            0.40 * stability +
            0.20 * precision +
            0.05 * speed +
            0.05 * cost_pts
    )

    return final_score
# =====================================================
# === 7) DATASET A GENERATION =========================
# =====================================================
def build_dataset_a(n):
    solutions = generate_n_valid_solutions(n)
    rows = []
    for sol in solutions:
        cost = calculate_total_cost(sol, price_map, structure_mass_map, material_price_per_stange)
        final_score = score_solution_option_based(sol)

        row = sol.copy()
        row["Cost"] = cost
        row["Score"] = final_score

        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv("excel_list/dataset_a.csv", index=False)
    return df

# =====================================================
# === 8) DATASET B: HUMAN-RATED =======================
# =====================================================
def build_dataset_b(num_to_generate=50):
    solutions = generate_n_valid_solutions(num_to_generate)
    rows = []

    print("\n=== MANUALLY RATE THE FOLLOWING SOLUTIONS (1-5 float) ===\n")

    for i, sol in enumerate(solutions, 1):
        print(f"\nSolution #{i}")
        pprint(sol)

        # show full cost
        cost = calculate_total_cost(sol, price_map, structure_mass_map, material_price_per_stange)
        print(f"Calculated Total Cost: {cost} EUR")

        rating = float(input("Your rating (1-5): "))

        row = sol.copy()
        row["Cost"] = cost
        row["Score"] = rating
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv("excel_list/dataset_b.csv", index=False)
    return df

# =====================================================
# === 9) TRAIN RANDOM FOREST ON BOTH DATASETS =========
# =====================================================
def train_random_forest():
    df_a = pd.read_csv("excel_list/dataset_a.csv")
    df_b = pd.read_csv("excel_list/dataset_b.csv")

    df = pd.concat([df_a, df_b], ignore_index=True)

    # One-hot encoding
    df_enc = pd.get_dummies(df.drop(columns=["Score"]))
    y = df["Score"]

    model = RandomForestRegressor(n_estimators=500)
    model.fit(df_enc, y)

    return model, df_enc.columns


# =====================================================
# === 10) USE MODEL TO FIND BEST SOLUTIONS =============
# =====================================================
def generate_best_solutions(model, columns, k=10):
    candidates = generate_n_valid_solutions(2000)
    scored = []

    for sol in candidates:
        df_temp = pd.DataFrame([sol])
        df_temp = pd.get_dummies(df_temp)
        df_temp = df_temp.reindex(columns=columns, fill_value=0)

        pred = model.predict(df_temp)[0]
        cost = calculate_total_cost(sol)

        scored.append((pred, cost, sol))

    best = generate_best_solutions(model, cols, k=10)

# =====================================================
# === 11) MAIN EXECUTION =====================
# =====================================================
if __name__ == "__main__":

    print("Generating Dataset A...")
    build_dataset_a(10**12)

    print("Generate Dataset B now...")
    build_dataset_b(100)  # Uncomment to rate manually

    print("Training model...")
    model, cols = train_random_forest()

    print("\nTop 5 predicted optimal solutions:")
    best = generate_best_solutions(model, cols, k=10)
    for rank, (score, cost, sol) in enumerate(best, 1):
        print(f"\nRank {rank} — Predicted Score {score:.2f} — Cost: {cost} EUR")
        pprint(sol)
