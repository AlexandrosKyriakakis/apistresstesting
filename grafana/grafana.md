## Set Up Grafana with Prometheus
- Open Grafana in your web browser by navigating to http://localhost:3001.
- Log in to Grafana using the default username and password (both are admin).
- Add a new data source by clicking on the gear icon in the left sidebar and selecting "Data Sources". Click on "Add data source", select "Prometheus" from the list of data sources, and enter http://prometheus:9090 as the URL.
- Create a new dashboard by clicking on the plus icon in the left sidebar and selecting "Dashboard". Click on "Add panel", select "Graph", and enter the following query in the query editor:
- We can import dashboards from UI directly
