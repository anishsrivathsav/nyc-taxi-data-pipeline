import requests
import logging
import os
import json

# =============================
#  LOGGING CONFIGURATION 
# =============================
logging.basicConfig(
    filename = 'logs/download.log',
    filemode='a',                  
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# ==============================
# LOGGING TO COMNSOLE 
# ==============================
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

#=======================
# DATA DOWNLOADER FROM WEB 
# ========================
class DataDownloader():
    """
     Handles downloading  for a single file from a URL and saving it into the data folder in the respective year and month folders
     Attributes :
      url(str) : The Url of the file to be downloaded 
      save_path (str): The base folder path to save the downloaded file under year/month structure

    """
    def __init__(self,url,save_path):
        self.url = url
        self.save_path = save_path
    def download_data_from_web(self):
        try :
            response = requests.get(url=self.url,stream=True,timeout=30)
            response.raise_for_status()
            filename = self.url.split('/')[-1]
            year, month = filename.replace(".parquet", "").split("_")[-1].split("-")
            os.makedirs(os.path.join(self.save_path,year,month), exist_ok=True)
            file_save_path =os.path.join(self.save_path,year,month,filename)
            with open(file_save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logging.info(f"File downloaded successfully: {file_save_path}")
            return True
        except requests.exceptions.Timeout:
            logging.error("Timeout occurred while downloading the file.")
        except requests.exceptions.ConnectionError:
            logging.error("Network error: Failed to connect to the URL.")
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
        except PermissionError:
            logging.error("Permission denied: Cannot write to the specified directory.")
        except Exception as e:
            logging.exception(f"Unexpected error occurred: {e}")

        return False
class DownloadRun():
    """
    Handles  downloading a list of urls by utilizing the  Datadownloader class 
    Attributes :
    jobs_list(list) :  List of urls that neeeds ro be downloaded to local directory
    rootpath(str) :  Rootpath of the  file that needs to be stored in the local machine 

    """
    
    def __init__(self, jobs_list,rootpath):
         self.jobs_list = jobs_list 
         self.rootpath = rootpath
    def __iter__(self):
        for url in self.jobs_list:
            yield DataDownloader(url,self.rootpath)
    def run(self):
        [downloader.download_data_from_web() for downloader in self]


if __name__ == "__main__":
   try : 
    config_file_path = os.path.join(os.getcwd(),'config','download_urls.json')
    with open(config_file_path,"r") as file :
        url_info = json.load(file)
        url_list = url_info['url']
   except  Exception as e :
       logging.error("Unable to locate the file or  Issue Parsing the File with Error")
   
   rootpath = os.path.join(os.getcwd(),'data')
   runner = DownloadRun(url_list,rootpath)
   runner.run()
