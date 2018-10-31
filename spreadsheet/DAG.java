import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DAG {
    private int m, n, capacity;
    private Map<String, DagNode> nodeMap;
    private Deque<String> topologicalList;

    public DAG(int m, int n) {
        this.m = m;
        this.n = n;
        capacity = (int) (m * n / 0.75) + 1;
        nodeMap = new HashMap<>(capacity);
    }

    public void addNode(String label, String expression) {

        nodeMap.put(label, new DagNode(label, expression));
    }

    public void buildLinks() {

        Pattern pattern = Pattern.compile("([A-Z])(\\d+)");

        for (int row = 1; row < m+1; row++) {
            for (int col = 1; col < n+1; col++) {

                String cLabel = (char)(64+row) + Integer.toString(col);
                DagNode cNode = nodeMap.get(cLabel);
                String expression = cNode.getExpr();

                Matcher matcher = pattern.matcher(expression);

                // has dependencies
                while(matcher.find()){
                    // add edges
                    String pLabel = matcher.group();
                    DagNode pNode = nodeMap.get(pLabel);
                    pNode.addOutgoing(cNode);
                    cNode.addIncoming(pNode);
                }

            }
        }

        topologicalList = new LinkedList<>();
        toplogicalSort(topologicalList);
    }


    private void dfs(String label, Map<String, Integer> state, Deque<String> topologicalList) {
        state.put(label, 0);

        DagNode node = nodeMap.get(label);

        for (DagNode child : node.getOutgoing()) {

            Integer sk = state.get(child.label);

            // reach a vertex that is already in the recursion stack
            if (sk != null && sk == 0)
                throw new RuntimeException("Cycle Detected !!");

            // done visited
            else if (sk != null && sk == 1)
                continue;

            dfs(child.label, state, topologicalList);
        }

        // end of recursion, mark node as done
        state.put(label, 1);

        topologicalList.addFirst(label);
    }

    private void toplogicalSort(Deque<String> topologicalList){
        // keep the state during recursion: being visited or done
        Map<String, Integer> state = new HashMap<>(capacity);

        for (String label : nodeMap.keySet()) {
            // already visited
            if(state.containsKey(label))
                continue;

            dfs(label, state, topologicalList);
        }
    }

    public void execute(){
        for (String label : topologicalList){
            DagNode node = nodeMap.get(label);
            node.eval();
        }
    }

    public void printResults(){

        System.out.println(String.format("%d %d", n, m));

        for (int row = 1; row < m+1; row++) {
            for (int col = 1; col < n+1; col++) {

                String clabel = (char)(64+row) + Integer.toString(col);
                DagNode node = nodeMap.get(clabel);
                System.out.println(String.format("%.5f", node.getValue()));
            }
        }
    }

    public class DagNode {
        private String label;
        private String expr;
        private double value;
        private boolean dirty;

        private Set<DagNode> incoming = new HashSet<>();
        private Set<DagNode> outgoing = new HashSet<>();

        public DagNode(String label, String expr) {
            this.label = label;
            this.expr = expr;
            this.dirty = true;

        }

        public void addIncoming(DagNode node) {
            incoming.add(node);
        }

        public void addOutgoing(DagNode node) {
            outgoing.add(node);
        }

        public String getExpr() {
            return expr;
        }

        public double getValue() {
            return value;
        }

        public Set<DagNode> getOutgoing() {
            return outgoing;
        }

        public void eval(){

            if(this.dirty) {
                String expr = this.expr;

                for (DagNode node : incoming) {
                    if (node.dirty) {
                        String msg = String.format("Evaluating %s but %s is not ready", this.label, node.label);
                        throw new RuntimeException(msg);
                    }

                    String regex = node.label;
                    Pattern p = Pattern.compile(regex);

                    Matcher m = p.matcher(expr);
                    expr = m.replaceAll(Double.toString(node.getValue()));
                }

                this.value = RpnParser.evaluate(expr);
                this.dirty = false;
            }
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            DagNode dagNode = (DagNode) o;
            return label.equals(dagNode.label);
        }

        @Override
        public int hashCode() {
            return label.hashCode();
        }
    }
}
