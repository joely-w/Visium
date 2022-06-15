# Deploying a project
**1. Creating a PaaS project**
1. Navigate to https://webservices-portal.web.cern.ch/my-sites. 
2. Select "Create->PaaS Project" from the drop-down at the top and follow the form instructions to create a PaaS project.
3. Navigate to the OKD console using the link that will be displayed, or using this link https://paas.cern.ch/k8s/cluster/projects.

**2. Building a Git Repository**

1. Select "Add" from the sidebar
2. Select "Import from Git" in the following dashboard. We are using the sample Python Flask git repository: `https://github.com/devfile-samples/devfile-sample-python-basic.git`. 
3. Name your application and click create. 
4. You will be shown a topological view of your projects. You will need to wait for your project to finish building. 

**3. Making accessible** 
Your project should now be accessible from inside the CERN network (I believe, not being at CERN I'm not entirely sure.) If you want to make this project accessible outside of the CERN network: 

1. Select your Route in the project dialogue opened from Topology.
2. Click YAML 
3. Search for the field `haproxy.router.openshift.io/ip_whitelist`. To make the route accessible to anyone, replace this entries values with (including quotes) `""`.
4. Select Save. 


Your project should now be accessible to anyone. If you navigate back to the Topology view and select your project, the endpoint is the the location in the "Routes" section.




 


