import java.util.*;

public class RpnParser {

    @FunctionalInterface
    interface Operator{
        double calc(double a, double b);
    }

    private static Map<String, Operator> operatorMap = new HashMap<>();

    static{
        operatorMap.put("+", (double a, double b) -> a + b);
        operatorMap.put("-", (double a, double b) -> a - b);
        operatorMap.put("*", (double a, double b) -> a * b);
        operatorMap.put("/", (double a, double b) -> a / b);
        operatorMap.put("++", (double a, double b) -> a + b);
        operatorMap.put("--", (double a, double b) -> a - b);
    }

    public static double evaluate(String expression){

        Stack<Double> stack = new Stack<>();

        String[] tokens = expression.split("\\s+");
        for (String token : tokens){
            if(isNumeric(token)){
                stack.add(Double.parseDouble(token));
            }
            else if(isBiOperator(token)){
                if(stack.size() < 2)
                    throw new RuntimeException("Must have at least 2 parameters to perform op");

                double b = stack.pop();
                double a = stack.pop();

                stack.add(operatorMap.get(token).calc(a, b));

            }
            else if(isUniOperator(token)){
                if(stack.size() < 1)
                    throw new RuntimeException("Must have at least 1 parameters to perform op");

                double a = stack.pop();

                stack.add(operatorMap.get(token).calc(a, 1));

            }
            else{
                throw new RuntimeException("Invalid token %s".format(token));
            }
        }

        return stack.pop();
    }

    private static boolean isNumeric(String strNum) {
        try {
            float d = Float.parseFloat(strNum);
        } catch (NumberFormatException | NullPointerException nfe) {
            return false;
        }
        return true;
    }

    private static boolean isBiOperator(String s) {
        return s.equals("+") || s.equals("-") || s.equals("/") || s.equals("*");
    }

    private static boolean isUniOperator(String s) {
        return s.equals("++") || s.equals("--");
    }
}
