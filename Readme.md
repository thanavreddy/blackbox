# Black Box API Decoded

This project is a reverse-engineering challenge involving a set of undocumented API endpoints hosted on a Hidden Behavior (Final Decoded Logic):**


---

## Tech Stack

- **Python 3**
- **Flask** (for building the local API)
- **Postman** / **curl** (for testing HTTP requests)

---

## API Endpoints & Their Hidden Secrets

---

### 1) `POST /data`

**Hidden Behavior:**  
Encodes the input string to Base64.

**Example**

**Input:**
```json
{ "data": "hello" }
````

**Output:**

```json
{ "result": "aGVsbG8=" }
```

---

### 2) `GET /time`

**Hidden Behavior:**
Returns the remaining seconds to a preset future timestamp (95 days from server start). Constantly decrements with time.

**Example Output:**

```json
{ "result": 8163512 }
```

---

### 3) `POST /glitch`

**Hidden Behavior:**

* If input string’s length is **even** → randomly shuffles its characters.
* If **odd** → reverses the string.

**Example Input:**

```json
{ "data": "abcd" }
```

**Possible Output (even length):**

```json
{ "result": "cbad" }
```

**Example Input:**

```json
{ "data": "abcde" }
```

**Output (odd length):**

```json
{ "result": "edcba" }
```

---

### 4) `POST /zap`

**Hidden Behavior:**
Removes all numeric digits from the string, keeping letters, spaces, and special characters.

**Example Input:**

``` json
{ "data": "abc123!!" }
```

**Output:**

```json
{ "result": "abc!!" }
```

---

### 5) `POST /alpha`

**Hidden Behavior:**
Returns `true` if the first character is an alphabet letter, else `false`.

**Example Input:**

```json
{ "data": "hello" }
```

**Output:**

```json
{ "result": true }
```

**Example Input:**

```json
{ "data": "123abc" }
```

**Output:**

```json
{ "result": false }
```

---

###  6) `POST /fizzbuzz`

* If `data` is **not a list/array** → returns an error message: `"Input must be a valid JSON array"`
* If `data` is **a list/array** (regardless of length or content) → always returns `false`

> **Note:** The endpoint name is a complete decoy — there's no actual fizzbuzz number check happening. It simply validates if the input is an array and always returns false for arrays.alfunctioning system. Each endpoint behaves unpredictably with no official documentation, and the task was to deduce their hidden logic through carefully crafted requests and analysis of responses.


**Example Input (Non-array):**

```json
{ "data": "FizzBuzz" }
```

**Output:**

```json
{ "error": "Input must be a valid JSON array" }
```

**Example Input (Array):**

```json
{ "data": [1, 2, 3, 4] }
```

**Output:**

```json
{ "result": false }
```

**Example Input (Empty Array):**

```json
{ "data": [] }
```

**Output:**

```json
{ "result": false }
```

---

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
python main.py
```

3. Use **Postman** or **curl** to test the endpoints locally at:

```
http://127.0.0.1:5000/
```

---

## Testing

Comprehensive tests have been written for all endpoints to verify their behavior.

### Running Tests

1. **Make sure the Flask app is NOT running** (tests use the test client)

2. **Run all tests:**
```bash
python test_api.py
```

3. **Run tests with unittest discovery:**
```bash
python -m unittest test_api.py -v
```

4. **Run specific test class:**
```bash
python -m unittest test_api.BlackBoxAPITestCase -v
```

### Test Coverage

The test suite includes:

- **Unit tests** for each endpoint with multiple scenarios
- **Edge cases** like empty strings, single characters, mixed data types
- **Integration tests** that test workflows across multiple endpoints
- **Validation** of response formats and status codes

**Test Categories:**
- ✅ **`/data`** - Base64 encoding with various inputs
- ✅ **`/time`** - Countdown timer validation
- ✅ **`/glitch`** - String shuffling (even) and reversing (odd)
- ✅ **`/zap`** - Number removal from strings
- ✅ **`/alpha`** - First character alphabet validation
- ✅ **`/fizzbuzz`** - Array validation (error for non-arrays, false for arrays)
- ✅ **Integration** - Multi-endpoint workflows

### Expected Test Output

```
test_alpha_endpoint_first_char_check (__main__.BlackBoxAPITestCase) ... ok
test_complete_workflow (__main__.APIIntegrationTests) ... ok
test_data_endpoint_base64_encoding (__main__.BlackBoxAPITestCase) ... ok
test_fizzbuzz_endpoint_list_logic (__main__.BlackBoxAPITestCase) ... ok
test_glitch_endpoint_even_length (__main__.BlackBoxAPITestCase) ... ok
test_glitch_endpoint_odd_length (__main__.BlackBoxAPITestCase) ... ok
test_home_endpoint (__main__.BlackBoxAPITestCase) ... ok
test_time_endpoint (__main__.BlackBoxAPITestCase) ... ok
test_zap_endpoint_remove_non_alpha (__main__.BlackBoxAPITestCase) ... ok

==================================================
TESTS SUMMARY
==================================================
Tests run: 9
Failures: 0
Errors: 0
Success rate: 100.0%
```

---

## Challenges Faced

* **No documentation available:** Required observing behavior purely through input/output experimentation.
* **Misleading endpoint names:** Especially `/fizzbuzz`, which suggested classic fizzbuzz checks but actually operated based on list length.
* **Type and structure-dependent behaviors:** Many endpoints behaved differently for strings, numbers, and arrays.
* **Hidden conditions without hints:** Some endpoints required extensive trial and error to reveal their internal rules.
* **Obscure logic gates:** Like `/glitch` shuffling or reversing based on string length parity.

