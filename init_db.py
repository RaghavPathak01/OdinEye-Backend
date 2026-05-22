from db_manager import add_medical_fact

# Adding Ground Truth to your 'veriguard_db'
add_medical_fact("med_01", "Maximum Paracetamol dose for adults is 4000mg (8 tablets of 500mg) in 24 hours. Exceeding this causes liver failure.", "WHO_Guidelines")
add_medical_fact("med_02", "Ideal Hemoglobin levels: 13.5-17.5 g/dL for men, 12.0-15.5 g/dL for women.", "Mayo_Clinic")
add_medical_fact("leg_01", "Section 302 of the IPC (now BNS) prescribes punishment for murder.", "Indian_Penal_Code")

print("Database Initialized with Truth!")