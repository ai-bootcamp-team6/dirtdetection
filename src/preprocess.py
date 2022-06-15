import string
import pandas as pd
import numpy as np
from PIL import Image

class Pipeline():
    def __init__(self) -> None:
        pass
    def resize(self,image:str)->Image:
        """
        Resizes to 1024 x 832(HxW) and saves the image
        Args:
            image_list: List of image filepaths in the format "root/folder/img.format"
        Returns:
            resized: resized image
        """
        # Get image size
        DESIRED_SIZE = (1024,832)
        img = Image.open(image)
        resolution = img.size
        if resolution != DESIRED_SIZE:
            resized = img.resize(DESIRED_SIZE)
            resized.save(image)
            return resized
        else:
            return img
        # for each in image_list:
        #     img = Image.open(each)
        #     resolution = img.size
        #     if resolution != DESIRED_SIZE:
        #         resized = img.resize(DESIRED_SIZE)
        #         resized.save(each)
        #         return resized
            

    def convert_color_space(self,image:Image,mode="RGB")->Image:
        """
        Checks color space of the image passed as the argument and converts it to the desired space
        Args:
            image: Pillow Image
            mode: Desired color space. Defaults to RGB
        Returns:
            image: Unchanged image
            converted_image: image with color space converted
        """
        color_space = image.mode
        if not color_space == mode:
            converted_image = image.convert(mode)
            return converted_image
        return image

    def convert_format(self,image:Image,format=".png") -> bool:
        """
        Checks color space of the image passed as the argument and converts it to the desired space
        Args:
            image: Pillow image

            format: Desired image format, defaults to png
        Returns:
            Bool: True if image converted and saved successfully, False if an error occured
        """
        print(image.filename.endswith(format))
        if not image.filename.endswith(format):
        # if not image.endswith(format):
            filename = image.filename[:-4]
            filename = filename + format
            # img = Image.open(image)
            img = self.convert_color_space(image)
            try:
                img.save(filename)
                return True
            except Exception as e:
                print(e)
                return False
        # for each in image_list:
        #     if not each.endswith(format):
        #         print("Converting format")
        #         filename = each[:-4]
        #         print(filename)
        #         filename = filename + "."+format
        #         print(filename)
        #         img = Image.open(each)
        #         img = self.convert_color_space(img)
        #         try:
        #             img.save(filename)
        #             return True
        #         except Exception as e:
        #             print(e)
        #             return False



    def create_labels(self,xmin:int, ymin:int, xmax:int, ymax:int,img_width:int,img_height:int) -> list:
        """
        Generates annotations for image labels

        Args:
            xmin (int): X Coords of top left of bounding box
            ymin (int): Y Coords of top left of bounding box
            xmax (int): X Coords of bottom right of bounding box
            ymax (int): Y Coords of bottom right of bounding box

        Returns:
            list: list of annotated labels for the bounding box
        """
        center_x, center_y = (xmax-xmin)/2, (ymax-ymin)/2
        bbox_width = xmax - xmin
        bbox_height = ymax - ymin
        return [(xmin+center_x)/img_width, (ymin+center_y)/img_height, bbox_width/img_width, bbox_height/img_height]

    def normalize_bbox(self,df:pd.DataFrame,output_dir:string) -> None:
        """
        Creates and saves normalized bounding box coordinates in a txt file

        Args:
            df (pd.DataFrame): DataFrame containing the filename,X1,Y1,X2,Y2 coordinates of the bounding box and the clas label
            output_dir (string): Desired output directory to save the txt label file in
        Returns:
            None 
        """     
        df["labels_new"]= df.apply(lambda x: self.create_labels(x.X1, x.Y1, x.X2, x.Y2), axis = 1)
        df[['center_x', 'center_y', 'width', 'height']] = pd.DataFrame(df["labels_new"].tolist(), index = df.index)

        df["label"] = df["label"].map({"dirt":1}).fillna(0)

        df_cleaned = df[["filename", "label", 'center_x', 'center_y', 'width', 'height']]

        for i in set(df_cleaned["filename"]):
            df_cleaned_sub = df_cleaned[df_cleaned['filename'] == i]
            df_cleaned_sub = df_cleaned_sub.drop(columns = ["filename"])
            df_cleaned_sub.to_csv(r"{0}/{1}.txt".format(output_dir,i), header=None, index=None, sep=' ', mode='a')

    def process(self,image_list:list) -> None:
        """
        Processes a list of images by performing the following actions:
        1. Resizing
        2. Converting color space
        3. Converting to desired format(default png)

        Args:
            image_list (list): List of image filepaths in the format "root/folder/img.format"
        """
        processed_images = []
        err_images = []
        for each in image_list:
            resized_img = self.resize(each)
            colored_img = self.convert_color_space(resized_img)
            converted_img = self.convert_format(colored_img)
            if converted_img:
                processed_images.append(each)
            else:
                err_images.append(each)
        print(f"{len(processed_images)} images proccesed successfully\n{len(err_images)} images could not be processed")
        return



if __name__ == "__main__":
    pipeline = Pipeline()
    img_list = []
    # img_list.append("images/processed/00/floor_000000_img_000000_r0_f0.png")
    img_list.append("resized_img.jpg")
    pipeline.process(img_list)
    # resized_img = pipeline.resize(img_list)
    # resized_img.save("resized_img.jpg",format="jpeg")
    # print(resized_img.size)