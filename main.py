import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def display_polynomial_3d(coefficients):
    # Convert coefficients to a numpy array
    coefficients = np.array (coefficients)

    # Generate a polynomial object from coefficients
    polynomial = np.poly1d (coefficients)
    print(polynomial)
    # Generate points in the complex plane
    x_real = np.linspace (-5, 5, 1000)
    x_imaginary = np.linspace (-5, 5, 1000)
    X_real, X_imaginary = np.meshgrid (x_real, x_imaginary)
    X = X_real + 1j * X_imaginary
    # print(X)
    # Evaluate polynomial at these points
    Y = polynomial (X)

    fig = plt.figure ()
    ax = fig.add_subplot (111, projection='3d')

    # Plot
    # ax.plot_surface (X_real, X_imaginary, np.sqrt(np.real(Y)**2+np.imag(Y)**2), cmap='viridis')
    ax.plot_surface (X_real, X_imaginary, Y, cmap='viridis')
    # print(Y)
    # print("all")
    # print (abs(Y))

    # Set labels
    ax.set_xlabel ('Real(z)')
    ax.set_ylabel ('Imaginary(z)')
    ax.set_zlabel ('f(z)')

    plt.title ("Polynomial Plot")
    plt.show ()


# Example usage
if __name__ == "__main__":
   coefficients = [1, 0, 0, 0, 0, 0, 1, 2]
   # coefficients = [1, 1, 1]

   display_polynomial_3d(coefficients)
