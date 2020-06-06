***********
Quick start
***********

Before you can use the client, you need to create yourself an API token. Use
the web console to create one. Keep this API token safe and for your eyes only.
Save this token in a file which is readable for your user. Now, let's start.

You can create an instance of the client with::

   >>> from genesiscloud.client import Client
   >>> client = Client(os.getenv("GENESISCLOUD_API_KEY"))

The client has one public method, with it, you can verify that the API key is
working::

   >>> client.connect()
   <Response [200]>

If the API key is invalid, you will get an HTTP error code.
The client has property for each GenesisCloud resources which allows you to do
CRUD operations on these resources. Note that currently not all resources support
all CRUD operations via the API. Nevertheless, the methods exist for all resources.

Each resource has the following methods `get, find, list, create, delete`::
The `get` methods accept one parameter, the resource id::

   >>> client.Instances.get('ee7a8707-33ef-49ae-9930-a4fb10c1b16a')
   Instance({'id': '86d7b549-930e-44d1-8a42-a483292adf63', 'name': 'folding@home via API 2', 'hostname': 'folding-at-home-api-2', 'type': 'vcpu-4_memory-12g_disk-80g_nvidia1080ti-1', 'allowed_actions': ['start', 'shutoff', 'reset'], 'ssh_keys': [{'id': 'd57521aa-36fd-4cbf-a1a1-8344391a7893', 'name': 'cschmidbauer@gc'}], 'image': {'id': 'edba720a-ba6b-4552-81eb-16fb91460e31', 'name': 'folding@home 1 gpu image'}, 'security_groups': [{'id': '2472c0bb-1fa9-4dcc-a658-4268e78ad907', 'name': 'default'}, {'id': 'd3040f01-3b12-4712-9e8e-8ecb1ae7ba04', 'name': 'standard'}, {'id': '56370632-ceeb-4357-a5d3-f2c3acf9d69e', 'name': 'Folding@home'}], 'status': 'active', 'private_ip': '192.168.10.108', 'public_ip': '194.61.20.206', 'created_at': '2020-03-26T18:49:18.771Z', 'updated_at': '2020-03-26T18:50:12.957Z'})

The `get` method always returns an instance of `ItemView`, which is special
dictionary like class, which allows the user to convinietly to access attribute
via dot notation. Some Instance properties are themselves `ItemViews`::

   >>> instance = client.Instances.get('ee7a8707-33ef-49ae-9930-a4fb10c1b16a')
   >>> instance.ssh_keys
   [SSHKey({'id': 'd57521aa-36fd-4cbf-a1a1-8344391a7893', 'name': 'cschmidbauer@gc'})]
   >>> instance.security_groups
   [SecurityGroup({'id': '2472c0bb-1fa9-4dcc-a658-4268e78ad907', 'name': 'default'}), SecurityGroup({'id': 'd3040f01-3b12-4712-9e8e-8ecb1ae7ba04', 'name': 'standard'}), SecurityGroup({'id': '56370632-ceeb-4357-a5d3-f2c3acf9d69e', 'name': 'Folding@home'})]
   >>> instance.security_groups[0].name
   'default'

The `list` method returns a lazy generator to list all the resources or filter some::

   >>> client.SecurityGroups.list()
   <generator object GenesisResource.__list at 0x7f97f9405b48>
   >>> list(client.SecurityGroups.list())
   [SecurityGroup({'id': 'd3040f01-3b12-4712-9e8e-8ecb1ae7ba04', 'name': 'standard', 'description': 'The recommended security group default applied by Genesis Cloud', 'created_at': '2019-11-21T13:43:22.824Z'}), SecurityGroup({'id': '258afd7b-fb40-439b-b146-b1dcdbfead8c', 'name': 'iperf', 'description': 'iperf default port settings', 'created_at': '2020-01-12T22:15:35.871Z'}), SecurityGroup({'id': 'f26a9bec-c254-4804-843e-d3d179464ec2', 'name': 'outbound-fully-opened', 'description': '', 'created_at': '2020-01-14T10:00:02.371Z'}), SecurityGroup({'id': '56370632-ceeb-4357-a5d3-f2c3acf9d69e', 'name': 'Folding@home', 'description': '', 'created_at': '2020-03-04T14:04:28.004Z'}), SecurityGroup({'id': '2781a739-bdd2-44b7-ac3a-9d1d38999738', 'name': 'VNC', 'description': '', 'created_at': '2020-05-03T17:23:00.822Z'}), SecurityGroup({'id': '8a8472a3-9af8-4f7e-a0fc-d8f7b40fa56c', 'name': 'cao-test', 'description': '', 'created_at': '2020-05-08T01:43:41.109Z'})]

The `list` method accepts paremters for page number and number of items per page::

   >>> list(client.SecurityGroups.list(page=2, item=40))

The `find` method allows one to search for specific resources::

   >>> list(client.SecurityGroups.find({'name': 'standard'}))
   <generator object GenesisResource.find at 0x7f97f9405b48>
   >>> list(client.SecurityGroups.find({'name': 'standard'}))
   [SecurityGroup({'id': 'd3040f01-3b12-4712-9e8e-8ecb1ae7ba04', 'name': 'standard', 'description': 'The recommended security group default applied by Genesis Cloud', 'created_at': '2019-11-21T13:43:22.824Z'})]

The `delete` method allowed one to delete a specific resource using the
id of the resource (currently only Snapshots and Instances)::

   >>> client.Instances.delete('ee7a8707-33ef-49ae-9930-a4fb10c1b16a')

These are the basics of using the client. In the next chapter, you can see a fully working example.
