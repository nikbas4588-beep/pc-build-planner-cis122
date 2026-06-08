# ==========================================
# CIS 122 - Mini Project: PC Build Planner
# Name: Nikolas Bass
# Description: A terminal-based application to select high-performance
#              PC components, check basic compatibility, and simulate
#              hardware stability testing.
# ==========================================

import random
import time

# --- DATA COLLECTIONS (Dictionaries and Lists) ---

# Dictionary storing available processors, their sockets, and wattage
CPUS = {
    "1: Intel i7-12700K": {"socket": "LGA1700", "power": 125, "cost": 280},
    "2: Intel i9-13900K": {"socket": "LGA1700", "power": 150, "cost": 450},
    "3: AMD Ryzen 7 7800X3D": {"socket": "AM5", "power": 120, "cost": 370}
}

# Dictionary storing available motherboards and their matching sockets
MOTHERBOARDS = {
    "1: ASUS Prime B760": {"socket": "LGA1700", "cost": 140},
    "2: ROG Strix Z790": {"socket": "LGA1700", "cost": 290},
    "3: MSI Pro X670-P": {"socket": "AM5", "cost": 200}
}

# Dictionary storing graphics cards and their power requirements
GPUS = {
    "1: NVIDIA GTX Titan X": {"power": 250, "cost": 150},
    "2: NVIDIA RTX 4070 Ti": {"power": 285, "cost": 750},
    "3: NVIDIA RTX 4090": {"power": 450, "cost": 1600}
}

# --- USER-DEFINED FUNCTIONS ---

def display_menu(title, options_dict):
    """
    Prints a formatted menu from a dictionary and gets valid user input.
    """
    print(f"\n--- Select Your {title} ---")
    for key, details in options_dict.items():
        # Clean up the key string for cleaner display
        display_name = key.split(": ")[1]
        print(f"[{key.split(':')[0]}] {display_name} (${details['cost']})")
        
    while True:
        choice = input("Enter the number of your selection: ").strip()
        # Find the matching full dictionary key based on the shortcut number
        for full_key in options_dict:
            if full_key.startswith(choice + ":"):
                return full_key
        print("Invalid selection. Please try again.")

def check_compatibility(cpu_name, mobo_name):
    """
    Compares the CPU socket type with the Motherboard socket type.
    """
    cpu_socket = CPUS[cpu_name]["socket"]
    mobo_socket = MOTHERBOARDS[mobo_name]["socket"]
    
    print("\n--- Running Compatibility Check ---")
    print(f"Checking: {cpu_name.split(': ')[1]} ({cpu_socket})")
    print(f"With: {mobo_name.split(': ')[1]} ({mobo_socket})")
    
    if cpu_socket == mobo_socket:
        print("[SUCCESS] Sockets match! Component interface is compatible.")
        return True
    else:
        print("[WARNING] Socket mismatch! The CPU physically will not fit this board.")
        return False

def run_stability_test(cpu_name, gpu_name):
    """
    Simulates a hardware stress test using a random number generator.
    Calculates power draw and checks the "silicon lottery" stability score.
    """
    print("\n--- Initializing Silicon Stability Test ---")
    print("Simulating BIOS configurations and fan curves...")
    time.sleep(1) # Small delay for immersion
    
    # Calculate estimated combined power consumption
    total_watts = CPUS[cpu_name]["power"] + GPUS[gpu_name]["power"]
    print(f"Estimated Peak Core Power Draw: {total_watts}W")
    
    # Generate a random hardware stability percentage (Silicon Lottery)
    stability_score = random.randint(65, 100)
    print(f"Calculated Hardware Stability Margin: {stability_score}%")
    
    if stability_score >= 80:
        print("Result: System STABLE. Voltages and temperatures are within safety boundaries.")
        return "Stable", total_watts
    else:
        print("Result: System UNSTABLE. Thermal throttling or BSOD crash detected under load.")
        return "Unstable (Requires Voltage Tuning)", total_watts

def save_build_to_file(cpu, mobo, gpu, compat, stability, power):
    """
    Writes the finalized build specifications out to a permanent log text file.
    """
    try:
        with open("pc_build_log.txt", "w") as file:
            file.write("=========================================\n")
            file.write("        CUSTOM PC BUILD SPEC SHEET       \n")
            file.write("=========================================\n")
            file.write(f"Processor:    {cpu.split(': ')[1]}\n")
            file.write(f"Motherboard:  {mobo.split(': ')[1]}\n")
            file.write(f"Graphics:     {gpu.split(': ')[1]}\n")
            file.write("-----------------------------------------\n")
            file.write(f"Socket Check: {'PASSED' if compat else 'FAILED (Mismatch)'}\n")
            file.write(f"Core Power:   {power} Watts peak\n")
            file.write(f"Stress Test:  {stability}\n")
            file.write("=========================================\n")
        print("\n[FILE I/O] Build configurations successfully saved to 'pc_build_log.txt'.")
    except IOError:
        print("\n[ERROR] Could not write system configurations to file.")

# --- MAIN PROGRAM LOOP ---

def main():
    print("=================================================")
    print("   WELCOME TO THE HIGH-PERFORMANCE PC PLANNER    ")
    print("=================================================")
    
    running = True
    while running:
        # 1. Gather components through selections
        selected_cpu = display_menu("Processor (CPU)", CPUS)
        selected_mobo = display_menu("Motherboard", MOTHERBOARDS)
        selected_gpu = display_menu("Graphics Card (GPU)", GPUS)
        
        # 2. Run validations and simulations
        is_compatible = check_compatibility(selected_cpu, selected_mobo)
        test_result, peak_power = run_stability_test(selected_cpu, selected_gpu)
        
        # 3. Output results to permanent file storage
        save_build_to_file(selected_cpu, selected_mobo, selected_gpu, is_compatible, test_result, peak_power)
        
        # 4. Check if the user wants to log another setup or exit
        print("\n-------------------------------------------------")
        retry = input("Would you like to plan another system configuration? (y/n): ").strip().lower()
        if retry != 'y' and retry != 'yes':
            print("\nExiting Planner. Thank you for utilizing the system framework.")
            running = False

# This line ensures the program runs when executed directly
if __name__ == "__main__":
    main()
