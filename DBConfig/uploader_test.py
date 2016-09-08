import uploader

path_to_data1 = "/home/jovyan/work/_core/projects/datasets/analytix-flights/test"
path_to_data2 = "/home/jovyan/work/_core/projects/datasets/analytix-flights/test"


if __name__ == '__main__':
    print("Commencing test...")
    #create an upload object containing the path to the target data
    upload1 = uploader.csv_upload(path_to_data1)
    #Test one: append all files to a single table
    print("Test one: "+upload1.append_upload())

	#Test two: load all files into separate tables
    upload2 = uploader.csv_upload(path_to_data2)
    print("Test two: "+upload2.multi_upload())