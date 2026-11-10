using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Ingrese los coeficientes del polinomio separados por espacios:");
        string[] input = Console.ReadLine().Split(' ');
        double[] coeficientes = Array.ConvertAll(input, double.Parse);

        // Crear un polinomio con los coeficientes ingresados
        Polynomial polinomio = new Polynomial(coeficientes);

        // Calcular las raíces del polinomio
        double[] raices = polinomio.CalcularRaices();

        Console.WriteLine("Las raíces del polinomio son:");
        foreach (double raiz in raices)
        {
            Console.WriteLine(raiz);
        }
    }
}

class Polynomial
{
    private double[] coeficientes;

    public Polynomial(double[] coeficientes)
    {
        this.coeficientes = coeficientes;
    }

    public double[] CalcularRaices()
    {
        // Aquí iría la lógica para calcular las raíces del polinomio
        // Por ejemplo, se podría utilizar el método de Newton-Raphson o el método de la bisección

        // En este ejemplo, simplemente se devuelve un array vacío
        return new double[] { };
    }
}
