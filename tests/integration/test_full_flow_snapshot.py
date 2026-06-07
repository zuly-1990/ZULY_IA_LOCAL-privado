# Placeholder integration test for ZULY full flow snapshot.
# This test uses the mocked bpy module to simulate a Blender scene.
# It verifies that the state_snapshot, v0_validator, state_guard and
# intention_boundary modules can be imported and run without raising
# errors, while respecting the NOÉ principles.

import sys
import os
import unittest

# Add project root to sys.path to allow importing 'core'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# Import ZULY components (core) – using global mock from conftest.py
from core.validation.state_snapshot import StateSnapshot
from core.validation.v0_validator import V0Validator
from core.state.state_guard import StateGuard
from core.intention.intention_boundary import IntentionBoundary

import bpy 


class TestFullFlowSnapshot(unittest.TestCase):
    def setUp(self):
        # Populate the global mock scene with objects.
        # Since we use the global mock, we access bpy.data.objects directly.
        # We need to clear it first to ensure test isolation if running in non-isolated manner (though execution is sequential)
        if isinstance(bpy.data.objects, list):
            bpy.data.objects.clear()
            
            # Add simple mock objects directly as MagicMocks behaving like objects
            cube = unittest.mock.MagicMock()
            cube.name = "Cube"
            cube.type = "MESH"
            cube.location = (1, 2, 3)
            cube.rotation_euler = (0.1, 0.2, 0.3)
            cube.scale = (1, 1, 1)
            cube.users_collection = [unittest.mock.MagicMock()]
            cube.users_collection[0].name = "Scene Collection"
            cube.hide_viewport = False
            
            bpy.data.objects.append(cube)



    def test_snapshot_and_validation(self):
        # 1. Start Validation (Capture Pre-State)
        validator = V0Validator()
        validator.start_validation()
        self.assertTrue(validator.pre_snapshot, "Pre-snapshot should be captured")

        # 2. Simulate passive command (no changes expected)
        # In a real flow, a command execution would happen here.
        # Here we just ensure the mock state remains same.
        
        # 3. Validate (Capture Post-State and Compare)
        # Passing a result that implies success but no structural effect
        command_result = {
            'success': True,
            'result': {'data': 'some info'},
            'effect': None  # Passive effect
        }
        
        result = validator.validate(command_result)
        
        # Should be verified because nothing changed and nothing was expected to change
        self.assertTrue(result.get('verified', False), f"Validation failed: {result.get('details')}")
        self.assertIn('pasiva', result.get('details', '').lower())

        # 4. Check Guard
        guard = StateGuard()
        self.assertTrue(guard.is_allowed('logging'))
        self.assertFalse(guard.is_allowed('decision_making'), "Decision making should be blocked by Guard")

        # 5. Check Intention Boundary (Verify limits)
        intention = IntentionBoundary()
        self.assertTrue(intention.is_forbidden('state_snapshot'), "State snapshot should be forbidden source")
        self.assertTrue(intention.is_forbidden('pattern_memory'), "Pattern memory should be forbidden source")
        self.assertFalse(intention.is_allowed('self_reflection'), "Self reflection should not be allowed")


if __name__ == "__main__":
    unittest.main()
