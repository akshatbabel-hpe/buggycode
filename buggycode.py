def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]

    return total / len(numbers)


def find_max_value(numbers):
    max_val = 0
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val


def divide_numbers(a, b):
    return a / b


data = [10, 5, 0, 8]

avg = calculate_average(data)
print("Average:", avg)

max_value = find_max_value(data)
print("Max:", max_value)

result = divide_numbers(10, 0)
print("Result:", result)
