import java.lang.reflect.Method;
import java.util.Scanner;

public class errorClass {

    public static void main(String[] args) throws Exception {

        Scanner scanner = new Scanner(System.in);

        System.out.println("=== Versión Vulnerable ===");
        System.out.print("Escribe el nombre de un método a ejecutar: ");

        String input = scanner.nextLine();

        // Vulnerabilidad: ejecuta cualquier método público sin validación
        // saludar (esperado)
        // mostrarNombrePrograma
        Method method = VulnerableApp.class.getMethod(input);
        method.invoke(null);
    }

    // Método legítimo
    public static void saludar() {
        System.out.println("Hola usuario");
    }

    // Método sensible
    public static void mostrarNombrePrograma() {
        System.out.println("Nombre del programa: VulnerableApp");
    }
}
