import tkinter as tk
from tkinter import ttk  # Import ttk module
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, lambdify
from tkinter import messagebox
from sympy import diff, Matrix
from sympy import sympify


def create_window():
    window = tk.Tk()  # Create a new window
    window.title("My Window")  # Set the title of the window
    window.geometry("1000x800")  # Set the size of the window

    # Create a style
    style = ttk.Style()

    # Configure the style for the input fields
    style.configure("TEntry", foreground="black", background="white", padding=10)

    # Configure the style for the buttons
    style.configure("TButton", foreground="black", background="lightgray", padding=10)


    # Create labels for x, y, and z
    x_label = ttk.Label(window, text="Enter x:", style="TLabel")
    y_label = ttk.Label(window, text="Enter y:", style="TLabel")
    z_label = ttk.Label(window, text="Enter z:", style="TLabel")

    # Place the labels at custom positions
    x_label.place(x=400, y=20)
    y_label.place(x=400, y=60)
    z_label.place(x=400, y=100)

    # Create input fields for x, y, and z
    x_entry = ttk.Entry(window, style="TEntry")  # Use the style
    y_entry = ttk.Entry(window, style="TEntry")
    z_entry = ttk.Entry(window, style="TEntry")

    # Place the input fields at custom positions
    x_entry.place(x=445, y=10)
    y_entry.place(x=445, y=50)
    z_entry.place(x=445, y=90)

    # Create a button that will display instructions when clicked
    instruction_button = ttk.Button(window, text="Instructions", command=show_instructions, style="TButton")  # Use the style
    instruction_button.place(x=260, y=140)

    # Create a button that will generate the graph when clicked
    button = ttk.Button(window, text="Generate Graph", command=lambda: generate_graph(x_entry.get(), y_entry.get(), z_entry.get(), ax, canvas, result_text), style="TButton")  # Use the style
    button.place(x=460, y=140)

    # Create a new figure for the plot
    fig = Figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create a canvas and add the plot to it
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().place(x=100, y=200)

    # Create a text widget for displaying the normal vector and tangent plane
    result_text = tk.Text(window, height=5, width=80)
    result_text.place(x=175, y=690)

    # Add navigation toolbar (for zooming, moving the plot, etc.)
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().place(x=175, y=200)

    # Create a button to close the application
    close_button = ttk.Button(window, text="Close", command=window.destroy, style="TButton")  # Use the style
    close_button.place(x=660, y=140)

    return window

    #Create the instructions 
def show_instructions():
    instructions = """
    This application generates a 3D plot of a surface defined by parametric equations. 

    You need to provide three functions, one for each of x, y, and z. These functions should be in terms of 'u' and 'v', which are parameters that vary over a certain range.

    Here's how to use the application:

    1. Enter your functions in the input fields for x, y, and z. These functions should be valid mathematical expressions involving 'u' and 'v'. You can use standard mathematical operations and functions, such as addition (+), subtraction (-), multiplication (*), division (/), and trigonometric functions (sin, cos, tan, etc.).

    For example, you could enter the following:

    x: sin(u)
    y: cos(v)
    z: u*v

    2. Click the 'Generate Graph' button. The application will calculate the x, y, and z values for each combination of 'u' and 'v' within the range, and display a 3D plot of the resulting surface.

    3. You can interact with the plot using the toolbar at the bottom of the window. This allows you to zoom in and out, move the plot around, and save the plot as an image.

    4. To close the application, click the 'Close' button.

    Ensure the following:
    - Each function uses 'u' and 'v' as independent variables.
    - Utilize standard mathematical operators: + (addition), - (subtraction), * (multiplication), / (division), ** (exponentiation), and functions like sin(), cos(), tan(), exp(), log(), etc.
    - Avoid using constants directly; instead, express them as mathematical expressions involving 'u' and 'v'.
    - Verify that each function is valid and can be evaluated over the specified ranges.
    - Ensure your expressions are well-formed and free of syntax errors.
    """

    # Create a top-level window
    instruction_window = tk.Toplevel()
    instruction_window.geometry("600x600")  # Set the size of the window

    # Create a scrollbar
    scrollbar = tk.Scrollbar(instruction_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a text widget and add the instructions to it
    text_widget = tk.Text(instruction_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_widget.insert(tk.END, instructions)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH)

    # Connect the scrollbar to the text widget
    scrollbar.config(command=text_widget.yview)

def generate_graph(x_eq, y_eq, z_eq, ax, canvas, result_text):
    try:
        # Clear the axes for the new plot
        ax.clear()

        # Create symbols
        u, v = symbols('u v')

        # Parse the user input into sympy expressions
        x_expr = sympify(x_eq)
        y_expr = sympify(y_eq)
        z_expr = sympify(z_eq)

        # Evaluate the expressions for the range of u and v
        u_values = np.linspace(0, 2*np.pi, 100)
        v_values = np.linspace(0, 2*np.pi, 100)
        x = np.array([[float(x_expr.evalf(subs={u:u_val, v:v_val})) for u_val in u_values] for v_val in v_values])
        y = np.array([[float(y_expr.evalf(subs={u:u_val, v:v_val})) for u_val in u_values] for v_val in v_values])
        z = np.array([[float(z_expr.evalf(subs={u:u_val, v:v_val})) for u_val in u_values] for v_val in v_values])

        # Plot the surface
        ax.plot_surface(x, y, z, color='b')

        # Calculate the partial derivatives
        x_u = diff(x_expr, u)
        x_v = diff(x_expr, v)
        y_u = diff(y_expr, u)
        y_v = diff(y_expr, v)
        z_u = diff(z_expr, u)
        z_v = diff(z_expr, v)

        # Calculate the normal vector
        normal_vector = Matrix([x_u, y_u, z_u]).cross(Matrix([x_v, y_v, z_v]))

        # Calculate the equation of the tangent plane
        tangent_plane_eq = normal_vector.dot(Matrix([symbols('x') - x_expr, symbols('y') - y_expr, symbols('z') - z_expr]))
        
        # Update the text widget with the normal vector and tangent plane
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"Normal vector: {normal_vector}\n")
        result_text.insert(tk.END, f"Tangent plane equation at (x,y,z): {tangent_plane_eq}")

        # Redraw the canvas
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create a window and start the event loop
window = create_window()
window.mainloop()