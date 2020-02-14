from azure.storage.blob.blockblobservice import BlockBlobService
import os
import json
import pickle

class FileLayer(object):

    def __init__(self, **kwargs):
        self.storage_account_name = kwargs.get('storage_account_name', '<storage account name>')
        self.storage_account_access_key = kwargs.get('storage_account_access_key',
                                                     '<storage account acess key>')
        self.file_service = BlockBlobService(account_name=self.storage_account_name,
                                             account_key=self.storage_account_access_key)

    def download_blob(self,blobpath="",local_file_path="", container="testing-environment"):
        
        """
        Downloads file in the Azure Blob to current local directory
        Args:
            path_on_blob: path to the file on blob
            container: Azure Blob Container name

        Returns: Downloaded local file path

        """

        if len(local_file_path) == 0:
            local_path = "/"+ blobpath
        else:
            local_path=local_file_path
   
        os.makedirs("/".join(local_path.split("/")[:-1]), exist_ok=True)
        self.file_service.get_blob_to_path(container_name=container, blob_name=blobpath, file_path=local_path)
        print("downloaded to = {}".format(local_path))
        return local_path

    def upload_to_blob(self, local_file_path="",bloppath="", container="testing-environment"):
        
        """
        Uploads local file to the blob
        Args:
            local_file_path:
            container: Azure Blob Container name

        Returns:

        """
        if len(bloppath)==0:
              blob_file = "/".join(local_file_path.split("/")[1:])
        else:
            blob_file=bloppath
        self.file_service.create_blob_from_path(container_name=container, blob_name=blob_file,
                                                file_path=local_file_path)
        return blob_file

    def read_pickle(self, path_on_blob, container="testing-environment"):
        """

        Args:
            path_on_blob: pickle file Path on the blob
            container: Azure Blob Container name

        Returns:

        """
        model_obj = pickle.loads(self.file_service.get_blob_to_bytes(container_name="testing-environment",
                                                                     blob_name=path_on_blob).content)
        return model_obj

    def read_config(self, path_on_blob, container="testing-environment"):
        """
        Reads the json config file present on the blob
        Args:
            path_on_blob: Json file Path on the blob
            container: Azure Blob Container name

        Returns:

        """
        config_file = self.file_service.get_blob_to_text(container_name=container, blob_name=path_on_blob)
        return json.loads(config_file.content)

    def list_folders_in_blob_path(self, blob_path, container="testing-environment"):
        """
        Lists the Azure blob folder contents
        Args:
            blob_path: Folder path pn the blob
            container: Azure Blob Container name

        Returns:

        """
        list_generator = self.file_service.list_blobs(container_name=container, prefix=blob_path)
        folders_under_blob = list(set([pth.name for pth in list_generator]))
        return folders_under_blob

    def upload_folder(self, local_folder_path, container="testing-environment"):
        pass


    def copy_blob_same_storage(self,sourceblobpath="",destinationblobpath="",sourcecontainer="",destinationcontainer=""):

            if len(destinationblobpath)==0:
                destinationblobpath=sourceblobpath

            source_blob_url = self.file_service.make_blob_url(sourcecontainer,sourceblobpath)


            self.file_service.copy_blob(destinationcontainer,destinationblobpath,source_blob_url)

    def copy_blob_across_storage(self, sourceblobpath="", destinationblobpath="",
                                                                  sourcecontainer="", destinationcontainer="",
                                                                 destination_source_account_name="",
                                                                 destination_source_account_key=""):

        destinationfileservice=BlockBlobService(account_name=destination_source_account_name,
                                                account_key=destination_source_account_key)
        local_path=self.download_blob(blobpath=sourceblobpath,container=sourcecontainer)

        if len(destinationblobpath) == 0:
            destinationblobpath = "/".join(local_path.split("/")[1:])



        destinationfileservice.create_blob_from_path(container_name=destinationcontainer, blob_name=destinationblobpath,file_path=local_path)
        os.remove(local_path)



if __name__=="__main__":
    pass
