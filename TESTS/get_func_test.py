def get_functions(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    functions = []
    current_function = None

    for line in lines:
        if line.strip().startswith('def ') and line.strip().endswith(':') and '__init__' not in line:
            if current_function is not None:
                functions.append(current_function)

            current_function = {'name': line.strip()[4:-1], 'lines': []}
        elif current_function is not None:
            current_function['lines'].append(line.strip())

    if current_function is not None:
        functions.append(current_function)

    return functions

file_path = 'main.py'

functions = get_functions(file_path)

for function in functions:
    print(f"Function name: {function['name']}")
