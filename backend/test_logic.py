from backend import engine

def test_matric_validation():
    print("Testing Matric Number Validation...")
    # Valid computer science matric numbers (BB=01, CC=03, DD=01)
    valid_matrics = [
        "23010301097",
        "22010301124",
        "24010301001",
        "23-01-03-01-097"
    ]
    # Invalid computer science matric numbers
    invalid_matrics = [
        "23020301097",  # Invalid college (02)
        "22010401124",  # Invalid department (04)
        "24010302001",  # Invalid programme (02)
        "abc10301097",  # Non-numeric
        "230103010",    # Too short (9 digits)
    ]
    
    for m in valid_matrics:
        assert engine.validate_matric_number(m) == True, f"Failed on valid matric: {m}"
    for m in invalid_matrics:
        assert engine.validate_matric_number(m) == False, f"Failed on invalid matric: {m}"
    print("✅ All Matric Validation tests passed!")

def test_level_calculation():
    print("Testing Level Calculation...")
    # Admission Year 23 (2023). Current date is June 2026.
    # Academic Year 2023/24 = 100L
    # Academic Year 2024/25 = 200L
    # Academic Year 2025/26 = 300L
    # Level calculated in June 2026 should be 300.
    level_23 = engine.calculate_level("23010301097")
    print(f"For entry suffix 23: calculated Level is {level_23}L")
    assert level_23 == 300, f"Expected 300 Level, got {level_23}"
    
    # Admission Year 24 (2024).
    # Academic Year 2024/25 = 100L
    # Academic Year 2025/26 = 200L
    level_24 = engine.calculate_level("24010301001")
    print(f"For entry suffix 24: calculated Level is {level_24}L")
    assert level_24 == 200, f"Expected 200 Level, got {level_24}"
    
    # Admission Year 25 (2025).
    # Academic Year 2025/26 = 100L
    level_25 = engine.calculate_level("25010301001")
    print(f"For entry suffix 25: calculated Level is {level_25}L")
    assert level_25 == 100, f"Expected 100 Level, got {level_25}"
    
    print("✅ All Level Calculation tests passed!")

if __name__ == "__main__":
    test_matric_validation()
    test_level_calculation()
    print("🎉 All backend unit tests passed successfully!")
