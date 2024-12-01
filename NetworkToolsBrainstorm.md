# Network Analysis Software

* Igraph (Python, C, R)
  * Good performance. Implemented in C.
  * Method for generating scale-free networks (Barbasi-Albert model)
* Networkx (Python)
  * Low performance. 
  * Networkx is implemented in python.
  * Barabasi-Albert model
* Graph-tool (Python)
  * Good performance. Implemented in C++. OpenMP.
  * Barabasi-Albert model (or Price model)
* NetworKit (Python)
  * Good performance. Performance aware algorithms implemented in C++. OpenMP
  * For analysis of large networks
  * Barabasi-Albert model
  * Implementation of newer algorithms from publications

Some benchmarks: https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages-v2

# Generating “Real-World” Networks

*  Barabasi-Albert model
   *  Fails to exhibit much clustering (not realistic)
   *  Inhomogeneous in degree. Preferential attachment model.
*  Watts-Strogatz model
   *  Good clustering
   *  Relatively homogeneous in degree (not realistic)

# Catalog of Real-World Networks

* http://konect.cc/
* https://networks.skewed.de/
