from connectors import NetControllerConnector
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect


class VCenterConnector(NetControllerConnector):
    def __init__(self):
        self._service_instance = None
        self._properties = {
            "address": "127.0.0.1",
            "port": 0,
            "username": "",
            "password": "",
            "monkey_template_name": "",
            "monkey_vm_info": {
                "name":   "Monkey Test",
                "datacenter_name":   "",
                "vm_folder":   "",
                "datastore_name":   "",
                "cluster_name":   "",
                "resource_pool":   ""
            }
        }

    def connect(self):
        self._service_instance = SmartConnect(host=self._properties["address"],
                                              port=self._properties["port"],
                                              user=self._properties["username"],
                                              pwd=self._properties["password"])

    def is_connected(self):
        return not self._service_instance == None

    def get_vlans_list(self):
        return []

    def get_entities_on_vlan(self, vlanid):
        return []

    def deploy_monkey(self, vlanid):
        if not self._properties["monkey_template_name"]:
            raise Exception("Monkey template not configured")

        vcontent = self._service_instance.RetrieveContent()  # get updated vsphare state
        monkey_template = self._get_obj(vcontent, [vim.VirtualMachine], self._properties["monkey_template_name"])
        if not monkey_template:
            raise Exception("Monkey template not found")

        task = self._clone_vm(vcontent, monkey_template)
        if not task:
            raise Exception("Error deploying monkey VM")

        monkey_vm = task.entity

    def disconnect(self):
        Disconnect(self._service_instance)
        self._service_instance = None

    def __del__(self):
        if self._service_instance:
            self.disconnect()

    def _clone_vm(self, vcontent, vm):

        # get vm target folder
        if self._properties["monkey_vm_info"]["vm_folder"]:
            destfolder = self._get_obj(vcontent, [vim.Folder], self._properties["monkey_vm_info"]["vm_folder"])
        else:
            datacenter = self._get_obj(vcontent, [vim.Datacenter], self._properties["monkey_vm_info"]["datacenter_name"])
            destfolder = datacenter.vmFolder

        # get vm target datastore
        if self._properties["monkey_vm_info"]["datacenter_name"]:
            datastore = self._get_obj(vcontent, [vim.Datastore], self._properties["monkey_vm_info"]["datacenter_name"])
        else:
            datastore = self._get_obj(vcontent, [vim.Datastore], vm.datastore[0].info.name)

        # get vm target resoucepool
        if self._properties["monkey_vm_info"]["resource_pool"]:
            resource_pool = self._get_obj(vcontent, [vim.ResourcePool], self._properties["monkey_vm_info"]["resource_pool"])
        else:
            cluster = self._get_obj(vcontent, [vim.ClusterComputeResource], self._properties["monkey_vm_info"]["cluster_name"])
            resource_pool = cluster.resourcePool

        # set relospec
        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec

        task = vm.Clone(folder=destfolder, name=self._properties["monkey_vm_info"]["name"], spec=clonespec)
        return self._wait_for_task(task)


    @staticmethod
    def _wait_for_task(task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result

            if task.info.state == 'error':
                return None

    @staticmethod
    def _get_obj(content, vimtype, name):
        """
        Return an object by name, if name is None the
        first found object is returned
        """
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)
        for c in container.view:
            if name:
                if c.name == name:
                    obj = c
                    break
            else:
                obj = c
                break

        return obj