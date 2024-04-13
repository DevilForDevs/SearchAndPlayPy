import ast
import astor

def insert_print_statements(filename):
    with open(filename,  'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=filename)

    # Define a function visitor to insert print statements
    class PrintStatementVisitor(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            print_args = ', '.join([f'{arg.arg}={{repr({arg.arg})}}' for arg in node.args.args])
            print_statement = f'print("Function {node.name}:", {", ".join([f"{arg.arg}" for arg in node.args.args])})'
            print_node = ast.parse(print_statement).body[0]
            node.body.insert(0, print_node)
            return node

    # Apply the visitor to the AST
    tree = PrintStatementVisitor().visit(tree)

    # Convert the modified AST back to Python code
    modified_code = astor.to_source(tree)

    # Save the modified code to a new file or overwrite the existing file
    output_filename = filename.replace('.py', '_modified.py')
    with open(output_filename,'w', encoding='utf-8') as output_file:
        output_file.write(modified_code)

    print(f"Modified code has been saved to {output_filename}")

# Replace 'your_target_file.py' with the path to the file you want to modify
insert_print_statements('_utils.py')
