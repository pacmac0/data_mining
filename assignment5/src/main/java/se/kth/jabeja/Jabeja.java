package se.kth.jabeja;

import org.apache.log4j.Logger;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.NodeSelectionPolicy;
import se.kth.jabeja.io.FileIO;
import se.kth.jabeja.rand.RandNoGenerator;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class Jabeja {
  final static Logger logger = Logger.getLogger(Jabeja.class);
  private final Config config;
  private final HashMap<Integer/*id*/, Node/*neighbors*/> entireGraph;
  private final List<Integer> nodeIds;
  private int numberOfSwaps;
  private int round;
  private float T;
  private boolean resultFileCreated = false;
  // our params
  private String annealingPolicy = "LINEAR";
  private Random random = new Random();
  private boolean restartTemperature = false;
  private int edgeCut = 0; // make edgeCut from report() global to use in restartTemperature()
  private int roundsWithSameEdgeCut = 0; // used to determain temperature restart
  private int prevEdgeCut = 0; // used to determain temperature restart
  private int restartConvThreashold = 100;
  private int allowedRestarts = 1;
  private int restarts = 0;

  //-------------------------------------------------------------------
  public Jabeja(HashMap<Integer, Node> graph, Config config) {
    this.entireGraph = graph;
    this.nodeIds = new ArrayList(entireGraph.keySet());
    this.round = 0;
    this.numberOfSwaps = 0;
    this.config = config;
    this.T = config.getTemperature();
    // our params
    this.random.setSeed(config.getSeed());
    this.annealingPolicy = "EXPONENTIAL"; // change for part 2, optins: LINEAR, EXPONENTIAL, IMPROVED
    this.restartTemperature = true; // change for part 2.2, options true, false
    this.restartConvThreashold = 100;
    this.allowedRestarts = 1;
    this.restarts = 0;
  }


  //-------------------------------------------------------------------
  public void startJabeja() throws IOException {
    for (round = 0; round < config.getRounds(); round++) {
      for (int id : entireGraph.keySet()) {
        sampleAndSwap(id);
      }

      //one cycle for all nodes have completed.
      //reduce the temperature
      saCoolDown();
      report();
      if (restartTemperature && (restarts < allowedRestarts)) { // only do if configured
        boolean restarted = restartTemperature();
        if (restarted)
          restarts++;
      }
    }
  }

  /**
   * Simulated analealing cooling function
   */
  private void saCoolDown(){
    // TODO for second task (http://katrinaeg.com/simulated-annealing.html)
    // T = T
    // T_min = t_min = 0.00001 on website

    // set t_min val
    float t_min = annealingPolicy.equals("LINEAR") ? 1.0f : 0.00001f;

    // non linear annealing cases (exponential)
    if (T > t_min && !annealingPolicy.equals("LINEAR"))
      T *= config.getDelta(); // update T with multiplication for exponential case
    else if (T > t_min && annealingPolicy.equals("LINEAR")) // linear annealing
      T -= config.getDelta();
    else
      T = t_min;
  }

  /**
   * Sample and swap algorith at node p
   * @param nodeId
   */
  private void sampleAndSwap(int nodeId) {
    Node partner = null;
    Node nodep = entireGraph.get(nodeId);

    if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
            || config.getNodeSelectionPolicy() == NodeSelectionPolicy.LOCAL) {
      // swap with random neighbors
      // TODO
      partner = findPartner(nodeId, getNeighbors(nodep));
    }

    if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
            || config.getNodeSelectionPolicy() == NodeSelectionPolicy.RANDOM) {
      // if local policy fails then randomly sample the entire graph
      // TODO
      if (partner == null) { // check if node was selected in previous routine
        partner = findPartner(nodeId, getSample(nodeId));
      }
    }
    // swap the colors
    // TODO
    if (partner != null) {
      // color exchange handshake
      int partnerColor = partner.getColor(); // get color of partner
      partner.setColor(nodep.getColor()); // reset partner.color to p.color
      nodep.setColor(partnerColor); // reset color of p to partner.color
      numberOfSwaps++; // update number of swaps in algorithm
    }
    // Update temperature not necessary here since done during main loop by calling saCoolDown()
  }

  public Node findPartner(int nodeId, Integer[] nodes){ 
    // changed data type of nodes Integer[] => ArrayList<Integer> to fit ret-val. of node.getNeighbours()
    // UPDATE: not necessary thanks to function getNeighbors() below

    Node nodep = entireGraph.get(nodeId);

    Node bestPartner = null;
    double highestBenefit = 0;

    // TODO
    double alpha = config.getAlpha();
    for (int nodeID : nodes) {
      Node nodeq = entireGraph.get(nodeID);
      // get nodes degrees
      int dpp = getDegree(nodep, nodep.getColor());
      int dqq = getDegree(nodeq, nodeq.getColor());
      double old_val = Math.pow(dpp, alpha) + Math.pow(dqq, alpha);
      // compute degree if color changed
      int dpq = getDegree(nodep, nodeq.getColor());
      int dqp = getDegree(nodeq, nodep.getColor());
      double new_val = Math.pow(dpq, alpha) + Math.pow(dqp, alpha);
      
      // rounds values
      double round_benefit = 0;
      boolean update = false;
      // update depending on annealing policy
      if (annealingPolicy.equals("LINEAR")) {
        round_benefit = new_val;
        update = (new_val * T > old_val);
      } else {
        double round_acceptanceProb = 0;
        /* (http://katrinaeg.com/simulated-annealing.html)
        $$ a = e^{\frac{c_{new} - c_{old}}{T}} $$
        where $a$ is the acceptance probability, 
        $(c_{new}-c_{old})$ is the difference between the new cost and the old one, 
        $T$ is the temperature, 
        and $e$ is 2.71828, that mathematical constant that pops up in all sorts of unexpected places.
        */
        // go through non linear cases
        if(annealingPolicy.equals("EXPONENTIAL")) { // exponential annealing
          round_acceptanceProb = Math.exp((new_val - old_val) / T);
        } else if(annealingPolicy.equals("IMPROVED")) { // imporved annealing
          
          // TODO for bonus


        } // else: stay 0
        // set round values
        round_benefit = round_acceptanceProb;
        update = (round_acceptanceProb > random.nextDouble()) && (new_val != old_val); // catch case of (new - old = 0)
      }
      // update parameters if better option found
      if (update && (round_benefit > highestBenefit)) {
        bestPartner = nodeq;
        highestBenefit = round_benefit;
      }
    }
    return bestPartner;
  }

  /**
   * Restart temperature once edge-cut has converged, to possibly avoid local minimum
   */
  private boolean restartTemperature(){
    // check edge-cut convergence, last x values
    if (edgeCut == prevEdgeCut) {
      roundsWithSameEdgeCut++;
      if (roundsWithSameEdgeCut == restartConvThreashold) {
        T = config.getTemperature(); // reset temperature to init
        roundsWithSameEdgeCut = 0;
        return true;
      }
    } else {
      roundsWithSameEdgeCut = 0; // reset if edgeCut changes
    }
    // update prevEdgecut
    prevEdgeCut = edgeCut;
    return false;
  }

  /**
   * The the degree on the node based on color
   * @param node
   * @param colorId
   * @return how many neighbors of the node have color == colorId
   */
  private int getDegree(Node node, int colorId){
    int degree = 0;
    for(int neighborId : node.getNeighbours()){
      Node neighbor = entireGraph.get(neighborId);
      if(neighbor.getColor() == colorId){
        degree++;
      }
    }
    return degree;
  }

  /**
   * Returns a uniformly random sample of the graph
   * @param currentNodeId
   * @return Returns a uniformly random sample of the graph
   */
  private Integer[] getSample(int currentNodeId) {
    int count = config.getUniformRandomSampleSize();
    int rndId;
    int size = entireGraph.size();
    ArrayList<Integer> rndIds = new ArrayList<Integer>();

    while (true) {
      rndId = nodeIds.get(RandNoGenerator.nextInt(size));
      if (rndId != currentNodeId && !rndIds.contains(rndId)) {
        rndIds.add(rndId);
        count--;
      }

      if (count == 0)
        break;
    }

    Integer[] ids = new Integer[rndIds.size()];
    return rndIds.toArray(ids);
  }

  /**
   * Get random neighbors. The number of random neighbors is controlled using
   * -closeByNeighbors command line argument which can be obtained from the config
   * using {@link Config#getRandomNeighborSampleSize()}
   * @param node
   * @return
   */
  private Integer[] getNeighbors(Node node) {
    ArrayList<Integer> list = node.getNeighbours();
    int count = config.getRandomNeighborSampleSize();
    int rndId;
    int index;
    int size = list.size();
    ArrayList<Integer> rndIds = new ArrayList<Integer>();

    if (size <= count)
      rndIds.addAll(list);
    else {
      while (true) {
        index = RandNoGenerator.nextInt(size);
        rndId = list.get(index);
        if (!rndIds.contains(rndId)) {
          rndIds.add(rndId);
          count--;
        }

        if (count == 0)
          break;
      }
    }

    Integer[] arr = new Integer[rndIds.size()];
    return rndIds.toArray(arr);
  }


  /**
   * Generate a report which is stored in a file in the output dir.
   *
   * @throws IOException
   */
  private void report() throws IOException {
    int grayLinks = 0;
    int migrations = 0; // number of nodes that have changed the initial color
    int size = entireGraph.size();

    for (int i : entireGraph.keySet()) {
      Node node = entireGraph.get(i);
      int nodeColor = node.getColor();
      ArrayList<Integer> nodeNeighbours = node.getNeighbours();

      if (nodeColor != node.getInitColor()) {
        migrations++;
      }

      if (nodeNeighbours != null) {
        for (int n : nodeNeighbours) {
          Node p = entireGraph.get(n);
          int pColor = p.getColor();

          if (nodeColor != pColor)
            grayLinks++;
        }
      }
    }

    edgeCut = grayLinks / 2;

    logger.info("round: " + round +
            ", edge cut:" + edgeCut +
            ", swaps: " + numberOfSwaps +
            ", migrations: " + migrations);

    saveToFile(edgeCut, migrations);
  }

  private void saveToFile(int edgeCuts, int migrations) throws IOException {
    String delimiter = "\t\t";
    String outputFilePath;

    //output file name
    File inputFile = new File(config.getGraphFilePath());
    outputFilePath = config.getOutputDir() +
            File.separator +
            inputFile.getName() + "_" +
            "NS" + "_" + config.getNodeSelectionPolicy() + "_" +
            "GICP" + "_" + config.getGraphInitialColorPolicy() + "_" +
            "T" + "_" + config.getTemperature() + "_" +
            "D" + "_" + config.getDelta() + "_" +
            "RNSS" + "_" + config.getRandomNeighborSampleSize() + "_" +
            "URSS" + "_" + config.getUniformRandomSampleSize() + "_" +
            "A" + "_" + config.getAlpha() + "_" +
            "R" + "_" + config.getRounds() + ".txt";

    if (!resultFileCreated) {
      File outputDir = new File(config.getOutputDir());
      if (!outputDir.exists()) {
        if (!outputDir.mkdir()) {
          throw new IOException("Unable to create the output directory");
        }
      }
      // create folder and result file with header
      String header = "# Migration is number of nodes that have changed color.";
      header += "\n\nRound" + delimiter + "Edge-Cut" + delimiter + "Swaps" + delimiter + "Migrations" + delimiter + "Skipped" + "\n";
      FileIO.write(header, outputFilePath);
      resultFileCreated = true;
    }

    FileIO.append(round + delimiter + (edgeCuts) + delimiter + numberOfSwaps + delimiter + migrations + "\n", outputFilePath);
  }
}
