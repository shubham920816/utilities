'''
Created on 06-Jun-2019

@author: shubham mishra
'''
import yaml
import sys, os, time
import datetime
from kubernetes import client, config, utils
import kubernetes.client
from kubernetes.client.rest import ApiException
from commonutils.logger.loggerutil import loggerfunc
from commonutils.storage.azure.files import FileLayer
from pprint import pprint
#try:
# container=os.environ["azurecontainer"]
#except Exception as e:
#    container="testing-environment"


class kuberinteraction(object):

    def __init__(self,req_id="",run_id="",run_date="",configpath="/mnt/consumerhub/config/kubernetes/config.ini",container="",storage_account_name="consumerhubstorage",storage_account_access_key="eu6nLBATI0sSav+IA+2+KlchYUpZTEof8WOujXNfAxjMstmIYf9Lx/9ibmQQyt/+UiED14oESEw4UL4rlLtx6g=="):
        '''
        This function performs authentication with kuberentes cluster
        and creates kubernetes_yamls reference object
        Args:
            req_id:Request id for the run
            run_id:Run_id for a particular run
            run_date:Running date for particular instance
            configpath:Config path containing the acces keys for a a particular cluster
        '''
        #self.filelayer = FileLayer(storage_account_access_key=storage_account_access_key,storage_account_name=storage_account_name)
        #configpath=self.filelayer.download_blob(configpath.lstrip("/"),container=container)

        #configpath = configpath

        config.load_kube_config(configpath)
        configuration = kubernetes.client.Configuration()
        #self.api_instance = kubernetes_yamls.client.BatchV1Api(kubernetes_yamls.client.ApiClient(configuration))
        #t1 = loggerfunc(req_id=req_id, run_id=run_id, run_date=run_date, servicename="kubernetesinteraction")
        #self.logger = t1.logger()
        self.api_instance = kubernetes.client.BatchV1Api(kubernetes.client.ApiClient(configuration))
        t1 = loggerfunc(req_id=req_id, run_id=run_id, run_date=run_date, servicename="kubernetesinteraction")
        self.logger = t1.logger()



    def kube_delete_empty_pods(self, namespace='default', phase='Succeded'):
        '''
        This function deletes the pods according to the status of  pods inside kuberenetes cluster
        Args:
            namespace:K8s namespace
            phase: State of the pod

        Returns:

        '''

        deleteoptions = client.V1DeleteOptions()

        api_pods = client.CoreV1Api()

        try:
            pods = api_pods.list_namespaced_pod(namespace,
                                                include_uninitialized=False,
                                                pretty=True,
                                                timeout_seconds=60)
        except ApiException as e:

            self.logger.error("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)

        for pod in pods.items:
            print("#########################################################################")
            self.logger.debug(pod)
            podname = pod.metadata.name
            #        print("pdname",podname)
            try:
                if pod.status.reason == "NodeLost":
                    api_response_pod = api_pods.delete_namespaced_pod(podname, namespace, body=deleteoptions)
                    self.logger.info("Pod: {} deleted!".format(podname))
                    pprint(api_response_pod)
                    self.logger.debug(api_response_pod)
                else:

                   self.logger.info("Pod: {} still not done... Phase: {}".format(podname, pod.status.phase))
            except ApiException as e:
                self.logger.error("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

        return

    def kube_cleanup_finished_jobs(self, name="", namespace='default'):
        '''
        This functions deletes the jobs from K8s cluster
        Args:
            name: name of the job to be deleted
            namespace: namespace in k8s

        Returns:

        '''
        self.logger.info("deleting the job %s" % name)
        time.sleep(2)


        try:

                    api_response_del = self.api_instance.delete_namespaced_job(name,
                                                                               namespace,
                                                                               grace_period_seconds=0,
                                                                               propagation_policy='Background')
                    self.logger.debug(api_response_del)
                    self.logger.info("%s deleted successfully" % name)
        except ApiException as e:
                    self.logger.exception("error ocurred while deleting the job")



    def kube_wait_for_job(self, name="", namespace='default'):
        '''
        This function pools the status of the job
        Args:
            name: name of the job
            namespace: namespace in k8s

        Returns:

        '''
        time.sleep(2)
        try:
            api_response_wait = self.api_instance.read_namespaced_job_status(name, namespace)
            self.logger.info("api_response_wait %s" % api_response_wait.status)
            jobstatus = api_response_wait.status.succeeded
            self.logger.info("job status is %s" % jobstatus)
            while (jobstatus != 1):

                time.sleep(2)
                self.logger.info("slept for 30 seconds")
                self.logger.info("checking job status")
                try:
                    api_response_wait = self.api_instance.read_namespaced_job_status(name, namespace)
                    self.logger.info("api_response_wait %s" % api_response_wait.status)
                except ApiException as e:
                    # pass
                    self.logger.exception("Exception when calling BatchV1Api->list_namespaced_job: %s\n" % str(e))
                jobstatus = api_response_wait.status.succeeded
                self.logger.info("job status is %s" % jobstatus)

            self.logger.info("Job %s completed" % name)
        except ApiException as e:
            self.logger.exception("Exception when calling BatchV1Api->list_namespaced_job: %s\n" % str(e))

    def kube_launch_job(self, yamlpath="",namespace="default"):
        '''
        This function launches the job inside K8s cluster
        Args:
            yamlpath: Yaml path for the job

        Returns:

        '''
        #  config.load_kube_config(self.configpath)
        # configuration = kubernetes_yamls.client.Configuration()
        # api_instance = kubernetes_yamls.client.BatchV1Api(kubernetes_yamls.client.ApiClient(configuration))
        f = open(yamlpath)
        dep = yaml.safe_load(f)
        time.sleep(2)
        try:
            api_response = self.api_instance.create_namespaced_job(namespace, body=dep, pretty=True)
        except ApiException as e:
            #pass
            self.logger.exception("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % str(e))

    def kube_launch_cron_job(self,yamlpath="",namespace="default"):
        '''
                This function launches the cron job inside K8s cluster
                Args:
                    yamlpath: Yaml path for the job

                Returns:

        '''

        f = open(yamlpath)
        dep = yaml.safe_load(f)
        time.sleep(2)
        api_instance=client.BatchV1beta1Api()
        try:
            api_response =api_instance.create_namespaced_cron_job(namespace, body=dep, pretty=True)
        except ApiException as e:
            # pass
            self.logger.exception("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % str(e))
            raise Exception("Error occured while launching the cron job")

    def delete_cronjob(self,namespace="default",jobname=""):

        api_instance = client.BatchV1beta1Api()
        try:
            api_response = api_instance.delete_namespaced_cron_job(jobname,namespace,pretty=True)
        except ApiException as e:
            # pass
            self.logger.exception("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % str(e))
            raise Exception("Error occured while launching the cron job")




    def configmap_values(self,namespace='default',configmap_name=""):

        api_instance=client.CoreV1Api()

        try:
            api_response = api_instance.list_namespaced_config_map(namespace, pretty=True)
            for i in api_response.items:
                if i.metadata.name==configmap_name:
                    metadata=i.data
                    break
            return(metadata)

        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_config_map: %s\n" % e)



    def kube_secret_auth(self, registery="", server="", username="", password="", email="", name="",
                         namespace="default"):
        kind = "Secret"
        data = {'docker.registry': registery,
                'docker.server': server,
                'docker.username': username,
                'docker.password': password,
                'docker.email': email}
        metadata = {"name": name}

        body = kubernetes.client.V1Secret(data=data, metadata=metadata)

        try:
            api_response = self.api_instance.create_namespaced_secret(namespace, body)
            self.logger.info("response for secret key creation: %s" % api_response)
        except ApiException as e:
            #pass
            self.logger.exception("Exception when calling CoreV1Api->create_namespaced_secret: %s\n" % str(e))


if __name__ == "__main__":
    pass
    # t1=kuberinteraction("/data/shubham.mishra2/AKSLaunch/data-enginerring/PODLAUNCH/configdata/kubernetesconfig.ini")
    # t1.kube_launch_job("synthesio.yaml")
    # t1.kube_wait_for_job("synthesio",namespace='default')
    # t1.kube_cleanup_finished_jobs("synthesio")
# t1.kube_delete_empty_pods()
