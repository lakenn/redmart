import java.util.*;

public class Spreadsheet {

    public static void main(String[] args) {
        Scanner inputScanner = new Scanner(System.in);
        int n = inputScanner.nextInt();
        int m = inputScanner.nextInt();
        inputScanner.nextLine();

        DAG dag = new DAG(m,n);

        for (int row = 1; row < m+1; row++) {
            for (int col = 1; col < n+1; col++) {

                String label = (char)(64+row) + Integer.toString(col);
                String expression = inputScanner.nextLine().trim().toUpperCase();
                dag.addNode(label, expression);
            }
        }

        inputScanner.close();

        try {
            dag.buildLinks();
        }
        catch (RuntimeException e) {
            System.out.println(e);
            System.exit(-1);
        }
        dag.execute();
        dag.printResults();

    }
}
