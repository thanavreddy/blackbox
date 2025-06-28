import unittest
import sys
import os
import json
import base64
import random

# Add the parent directory to sys.path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

class BlackBoxAPITestCase(unittest.TestCase):
    """Test cases for the Black Box API endpoints"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """Test the home endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Black Box Testing', response.data)
    
    def test_data_endpoint_base64_encoding(self):
        """Test /data endpoint - Base64 encoding"""
        test_cases = [
            ("hello", "aGVsbG8="),
            ("world", "d29ybGQ="),
            ("123", "MTIz"),
            ("", ""),  # Empty string
            ("a", "YQ=="),  # Single character
            ("Hello World!", "SGVsbG8gV29ybGQh"),  # With spaces and punctuation
        ]
        
        for input_str, expected_b64 in test_cases:
            with self.subTest(input_str=input_str):
                response = self.app.post('/data',
                                       data=json.dumps({"data": input_str}),
                                       content_type='application/json')
                self.assertEqual(response.status_code, 200)
                result = json.loads(response.data)
                self.assertEqual(result["result"], expected_b64)
                
                # Verify it's actually valid base64
                if input_str:  # Skip empty string
                    decoded = base64.b64decode(result["result"]).decode('utf-8')
                    self.assertEqual(decoded, input_str)
    
    def test_time_endpoint(self):
        """Test /time endpoint - Countdown timer"""
        response = self.app.get('/time')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        
        # Should return a positive integer (seconds remaining)
        self.assertIn("result", result)
        self.assertIsInstance(result["result"], int)
        self.assertGreater(result["result"], 0)  # Should be positive countdown
        
        # Make another request immediately - should be same or slightly less
        response2 = self.app.get('/time')
        result2 = json.loads(response2.data)
        self.assertLessEqual(result2["result"], result["result"])
    
    def test_glitch_endpoint_even_length(self):
        """Test /glitch endpoint with even length strings (shuffle)"""
        even_strings = ["ab", "abcd", "abcdef", "xy"]
        
        for test_str in even_strings:
            with self.subTest(test_str=test_str):
                # Test multiple times due to randomness
                results = []
                for _ in range(5):
                    response = self.app.post('/glitch',
                                           data=json.dumps({"data": test_str}),
                                           content_type='application/json')
                    self.assertEqual(response.status_code, 200)
                    result = json.loads(response.data)
                    results.append(result["result"])
                    
                    # Should contain same characters
                    self.assertEqual(sorted(result["result"]), sorted(test_str))
                    # Should be same length
                    self.assertEqual(len(result["result"]), len(test_str))
    
    def test_glitch_endpoint_odd_length(self):
        """Test /glitch endpoint with odd length strings (reverse)"""
        test_cases = [
            ("a", "a"),
            ("abc", "cba"),
            ("abcde", "edcba"),
            ("hello", "olleh"),
            ("x", "x"),
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                response = self.app.post('/glitch',
                                       data=json.dumps({"data": input_str}),
                                       content_type='application/json')
                self.assertEqual(response.status_code, 200)
                result = json.loads(response.data)
                self.assertEqual(result["result"], expected)
    
    def test_zap_endpoint_remove_non_alpha(self):
        """Test /zap endpoint - Remove non-alphabetic characters"""
        test_cases = [
            ("abc123!!", "abc"),
            ("Hello123World!", "HelloWorld"),
            ("123456", ""),  # Only numbers
            ("!@#$%", ""),   # Only special chars
            ("abcDEF", "abcDEF"),  # Only letters
            ("", ""),        # Empty string
            ("a1b2c3", "abc"),
            ("Test_String-123", "TestString"),
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                response = self.app.post('/zap',
                                       data=json.dumps({"data": input_str}),
                                       content_type='application/json')
                self.assertEqual(response.status_code, 200)
                result = json.loads(response.data)
                self.assertEqual(result["result"], expected)
    
    def test_alpha_endpoint_first_char_check(self):
        """Test /alpha endpoint - Check if first character is alphabetic"""
        test_cases = [
            ("hello", True),
            ("Hello", True),
            ("123abc", False),
            ("!hello", False),
            ("", False),  # Empty string
            ("a", True),
            ("Z", True),
            ("9abc", False),
            (" hello", False),  # Space first
            ("_test", False),   # Underscore first
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                response = self.app.post('/alpha',
                                       data=json.dumps({"data": input_str}),
                                       content_type='application/json')
                self.assertEqual(response.status_code, 200)
                result = json.loads(response.data)
                self.assertEqual(result["result"], expected)
    
    def test_fizzbuzz_endpoint_list_logic(self):
        """Test /fizzbuzz endpoint - List length parity check"""
        test_cases = [
            # Even length lists - should return the list itself
            ([1, 2], [1, 2]),
            ([1, 2, 3, 4], [1, 2, 3, 4]),
            (["a", "b"], ["a", "b"]),
            ([1, "mixed", 3, True], [1, "mixed", 3, True]),
            ([], []),  # Empty list (even length: 0)
            
            # Odd length lists - should return false
            ([1], False),
            ([1, 2, 3], False),
            (["a", "b", "c"], False),
            ([1, 2, 3, 4, 5], False),
            
            # Non-lists - should return false
            ("FizzBuzz", False),
            ("hello", False),
            (123, False),
            (True, False),
            (None, False),
        ]
        
        for input_data, expected in test_cases:
            with self.subTest(input_data=input_data):
                response = self.app.post('/fizzbuzz',
                                       data=json.dumps({"data": input_data}),
                                       content_type='application/json')
                self.assertEqual(response.status_code, 200)
                result = json.loads(response.data)
                self.assertEqual(result["result"], expected)


class APIIntegrationTests(unittest.TestCase):
    """Integration tests that test workflows across multiple endpoints"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_complete_workflow(self):
        """Test a complete workflow using multiple endpoints"""
        # Step 1: Use /zap to clean a string
        dirty_string = "test123!@#"
        response1 = self.app.post('/zap',
                                data=json.dumps({"data": dirty_string}),
                                content_type='application/json')
        clean_result = json.loads(response1.data)["result"]
        self.assertEqual(clean_result, "test")
        
        # Step 2: Use /glitch on the cleaned string (even length - should shuffle)
        response2 = self.app.post('/glitch',
                                data=json.dumps({"data": clean_result}),
                                content_type='application/json')
        glitch_result = json.loads(response2.data)["result"]
        self.assertEqual(sorted(glitch_result), sorted("test"))
        
        # Step 3: Encode the result with /data
        response3 = self.app.post('/data',
                                data=json.dumps({"data": glitch_result}),
                                content_type='application/json')
        encoded_result = json.loads(response3.data)["result"]
        
        # Verify the base64 encoding
        decoded_back = base64.b64decode(encoded_result).decode('utf-8')
        self.assertEqual(sorted(decoded_back), sorted("test"))
        
        # Step 4: Check if original clean string starts with alphabet
        response4 = self.app.post('/alpha',
                                data=json.dumps({"data": clean_result}),
                                content_type='application/json')
        alpha_result = json.loads(response4.data)["result"]
        self.assertTrue(alpha_result)  # "test" starts with 't'
        
        # Step 5: Test fizzbuzz with a list
        test_list = [1, 2, 3, 4]  # Even length
        response5 = self.app.post('/fizzbuzz',
                                data=json.dumps({"data": test_list}),
                                content_type='application/json')
        fizzbuzz_result = json.loads(response5.data)["result"]
        self.assertEqual(fizzbuzz_result, test_list)


def run_tests():
    """Run all tests and provide a summary"""
    # Create test loader
    loader = unittest.TestLoader()
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases using the modern approach
    suite.addTests(loader.loadTestsFromTestCase(BlackBoxAPITestCase))
    suite.addTests(loader.loadTestsFromTestCase(APIIntegrationTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print("TESTS SUMMARY")
    print("="*50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"Success rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    run_tests()