import yaml
import sys, os, time
import datetime
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
from utils.loggerutil.loggerutil import loggerfunc
from pprint import pprint

class kuberinteraction(object):

    def __init__(self,run_date="",configpath="/mnt/consumerhub/config/kubernetes/config.ini"):
        """
        Initiates the K8s object
        :param configpath: path for the k8s config
        """

        config.load_kube_config(configpath)
        self.api_instance = client.BatchV1Api()
        self.batch_instance= client.BatchV1beta1Api()
        if run_date:
            self.run_date=run_date
        else:
            self.run_date=datetime.date.today().isoformat()
        self.logger=loggerfunc(servicename="kubernetes",run_date=run_date)
        self.api_pods = client.CoreV1Api()



    def kube_delete_pods(self, namespace='default', podname=''):
        """
        Deletes the pod from K8s cluster
        :param namespace: K8s namespace
        :param podname: name of the pod
        :return:
        """

        api_response_pod = self.api_pods.delete_namespaced_pod(podname, namespace,pretty=True)
        self.logger.info("Pod: {} deleted!".format(podname))
        self.logger.debug(api_response_pod)

    def kube_cleanup_jobs(self, name="", namespace='default'):
        """
        Deletes Job Type Object from K8s cluster
        :param name: Name of the Job
        :param namespace: Namespace in the K8s cluster
        :return:
        """

        self.logger.info("deleting the job %s" % name)

        api_response_del = self.api_instance.delete_namespaced_job(name,namespace,
                                                                   grace_period_seconds=0,
                                                                   propagation_policy='Background')
        self.logger.debug(api_response_del)
        self.logger.info("%s deleted successfully" % name)




    def kube_wait_for_job(self, name="", namespace='default'):

        """
        Waits for the K8s Job to complete by polling the status of
        from K8s
        :param name: name of the job
        :param namespace: namespace
        :return:
        """

        try:
          api_response_wait = self.api_instance.read_namespaced_job_status(name, namespace)
          self.logger.info("api_response_wait %s" % api_response_wait.status)
        except Exception as e:
            self.logger.exception("Unable to find the Job,exiting ")
            sys.exit()
        jobstatus = api_response_wait.status.succeeded
        self.logger.info("job status is %s" % jobstatus)
        while (jobstatus != 1):

                self.logger.info("slept for 30 seconds")
                self.logger.info("checking job status")
                api_response_wait = self.api_instance.read_namespaced_job_status(name, namespace)
                self.logger.info("api_response_wait %s" % api_response_wait.status)
                jobstatus = api_response_wait.status.succeeded
                self.logger.info("job status is %s" % jobstatus)

        self.logger.info("Job %s completed" % name)


    def kube_launch_job(self, yamlpath="",namespace="default"):
        """
        Launch the Job object is K8s cluster
        :param yamlpath: absolute yaml path for the job
        :param namespace: namespace name
        :return:
        """
        self.logger.info("Reading the yaml for launching the job")
        f = open(yamlpath)
        dep = yaml.safe_load(f)
        self.logger.info("Lauching the Job")
        api_response = self.api_instance.create_namespaced_job(namespace, body=dep, pretty=True)
        self.logger.debug(api_response)


    def kube_launch_cron_job(self,yamlpath="",namespace="default"):
        """
        Launches the Cronjob on K8s cluster
        :param yamlpath: absolute yaml path for the cronjob
        :param namespace: namespace name
        :return:
        """
        self.logger.info("Reading the yaml for launching the Cron job")
        f = open(yamlpath)
        dep = yaml.safe_load(f)
        self.logger.info("Setting up the Cron Job")
        api_response =self.batch_instance.create_namespaced_cron_job(namespace, body=dep, pretty=True)
        self.logger.debug(api_response)

    def delete_cronjob(self,namespace="default",jobname=""):
        """
        Deletes the CronJob from the K8s cluster
        :param namespace: namespace name
        :param jobname: cronjob name
        :return:
        """
        self.logger.info("Deleting the cronjob")
        api_response = self.batch_instance.delete_namespaced_cron_job(jobname,namespace,pretty=True)
        self.logger.debug(api_response)


    def configmap_values(self,namespace='default',configmap_name=""):
        """
        Returns the config map(environment variables)
        :param namespace: namespace name
        :param configmap_name: name of the config map on K8s cluster
        :return:
        """
        self.logger.info("Trying to read the config map")
        api_response = api_instance.list_namespaced_config_map(namespace, pretty=True)
        self.logger.info(api_response.items)
        for i in api_response.items:
                if i.metadata.name==configmap_name:
                    metadata=i.data
                    break
        return(metadata)


if __name__ == "__main__":
    pass
