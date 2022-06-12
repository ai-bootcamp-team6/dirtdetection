from preprocess import Pipeline
import YOLOMODEL.detect as infer
import os

# Preprocess the image and return the directory in which the processed images are saved
# pipeline = Pipeline()
# # takes a image list
# imgs_to_detect = pipeline.process("PASS IN A LIST OF IMAGES")

# Refer to detect.py for info on the args
# result_dir = infer.run(weights="YOLOMODEL/weights/full_10epoch.pt",project="YOLOMODEL/runs/detect",imgsz=[1280,900],source="0")
# print(f"Result dir is {result_dir}")

# detected_images = []
# for root,dirs,files in os.walk(result_dir):
#     for file in files:
#         detected_images.append(file)

class Inference():
    def _run(self,weights,source,project,name="exp",imgsz=[1280,800],conf_thres=0.25,max_det=1000,device="",line_thickness=3,hide_labels=False,hide_conf=False) -> str:
        """
        Wrapper for YOLOv3's detect.py
        Args:
            Refer to detect.py for info on the args

        Returns:
            str: directory in which the results of the inference are stored
        """
        result_dir= infer.run(weights=weights,source=source,project=project,name=name,imgsz=imgsz,conf_thres=conf_thres,max_det=max_det,device=device,line_thickness=line_thickness,hide_labels=hide_labels,hide_conf=hide_conf)
        return result_dir

    def get_results(self,result_dir:str)->list:
        """
        Returns a list of images that were ran through the inference

        Args:
            result_dir (str): Directory storing the inference results
        Returns:
            list: _description_
        """
        for path, subdirs, files in os.walk(result_dir):
            for name in files:
                return (os.path.join(path, name))

    def infer(self,weights,source,project,name="exp",imgsz=[640,640],conf_thres=0.25,max_det=1000,device="",line_thickness=3,hide_labels=False,hide_conf=False) -> str:
        result_dir = self._run(weights=weights,source=source,project=project,name=name,imgsz=imgsz,conf_thres=conf_thres,max_det=max_det,device=device,line_thickness=line_thickness,hide_labels=hide_labels,hide_conf=hide_conf)
        return result_dir