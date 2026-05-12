import random
import time

# GLOBAL VARIABLE OF DOOM
users = ["Alice", "Bob", "Charlie"]
user_data = {}

def load_users():
    """Attempts to load users into the global user_data dict."""
    # BUG: Modifying global inside function without 'global' keyword
    # leads to unexpected scoping issues.
    for u in users:
        user_data[u] = {"id": random.randint(1, 100), "active": True}
    
    # BUG: Trying to access a local variable from outside
    # print(local_var) 

def process_data(data):
    """Processes user data and does some calculations."""
    results = []
    
    # BUG: Range issue - len(data) vs range(len(data))
    for i in range(len(data) + 1): 
        try:
            # BUG: IndexError (list index out of range)
            user = data[i]
            
            # BUG: Uninitialized Variable/KeyError
            # Assuming 'name' exists when it doesn't
            print(f"Processing {user['name']}")
            
            # BUG: ZeroDivisionError
            score = 100 / (user['id'] % 2)
            results.append(score)
            
        except KeyError:
            print("Key Error occurred!")
            # BUG: Continue instead of break/handle, leading to infinite loop
            continue
        except IndexError:
            # BUG: Silently ignoring critical errors
            pass 
        except Exception as e:
            # BUG: Catches EVERYTHING, hides real problems
            print(f"An error occurred: {e}")

    # BUG: Incorrect return type (expected list, returning None sometimes)
    if not results:
        return None
    return results

def main():
    print("Starting system...")
    load_users()
    
    # BUG: Stale data usage - trying to use user_data 
    # before it's properly populated in a multithreaded context
    raw_data = list(user_data.values())
    
    # BUG: Memory Leak / Infinite Loop
    # This loop never terminates properly
    while True:
        print("Running heavy process...")
        final_results = process_data(raw_data)
        
        # BUG: TypeError (cannot concatenate 'NoneType' to 'list')
        print("Results: " + final_results)
        
        # BUG: Dangerous sleep time
        time.sleep(-1)
        
        # BUG: Unreachable break
        if True:
            break

if __name__ == "__main__":
    main()

