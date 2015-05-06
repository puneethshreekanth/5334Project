'''
Created on May 2015

@author: Shreekanth
File to predict top 10 closest restaurants to user using KNN

References
http://stackoverflow.com/questions/14505716/implement-k-neighbors-classifier-in-scikit-learn-with-3-feature-per-object
http://scikit-learn.org/stable/modules/neighbors.html
http://blog.yhathq.com/posts/classification-using-knn-and-python.html
'''
from sklearn.neighbors import NearestNeighbors
import numpy as np

feature_names_dict = {}
final_arr = []
feature_names_arr = []
count = 0


''' Function to return a array with all features with 0 if feature is not in user review or business and
    1 if feature is in user review or business. Also append the Lat Long etc to the Array returned'''
def return_array(arr):
    arr = [w.replace('u\'', '').replace('\'','').replace(' ','').replace('\n','').lower() for w in arr]
    return_arr = [0 for i in range(feature_names_arr[0][1]+5)]
    for i in range(0,len(arr)-2):
        if arr[i] in feature_names_dict.keys():
            return_arr[feature_names_dict[arr[i]]] = 1
    return_arr[feature_names_arr[0][1]+1] = len(arr[len(arr)-4])
    return_arr[feature_names_arr[0][1]+2] = float(arr[len(arr)-3])
    return_arr[feature_names_arr[0][1]+3] = float(arr[len(arr)-2])
    return_arr[feature_names_arr[0][1]+4] = float(arr[len(arr)-1])
    return return_arr

'''Few variables to handle the file operations'''
file_path = 'C:\\Shree\\Study\\Data Mining\\Course_Project\\CSV_Files'
user_review_file = file_path+'\\input\\user_reviews_att.csv'
out_file = file_path+"\\output\\prediction_output.txt"
business_data_file = file_path+'\\yelp_academic_dataset_business_clean.json'
file = open(business_data_file,encoding='utf8',mode='r')


'''read all the categories a restaurant can belong to and 
   add it to a dictionary with array a category array'''
for lines in file.readlines():
    arr = lines.split('\t')
    category_arr = eval(arr[len(arr)-1])
    category_arr = [w.replace('u\'', '').replace('\'','').replace(' ','').replace('\n','').lower() for w in category_arr]
    if 'restaurants' in category_arr:
        for l in category_arr:
            try:
                feature_names_dict[l]
            except KeyError:
                feature_names_dict[l] = count
                count += 1
file.close()
print (feature_names_dict)
feature_names_arr = sorted(feature_names_dict.items(), key = lambda x: x[1], reverse = True)
print(feature_names_arr)

file = open(user_review_file,'r')
head_line = file.readline()
final_user_arr = []
training_data_ids = []
'''Prepare a array with user review data got after querying the database
   This would be used to train the classifier'''
for lines in file:
    arr = lines.split('"')
    category_arr = eval(arr[1])
    category_arr.append(arr[len(arr)-1].split(',')[1])
    category_arr.append(arr[len(arr)-1].split(',')[2])
    category_arr.append(arr[len(arr)-1].split(',')[3])
    category_arr.append(arr[len(arr)-1].split(',')[4])
    
    return_arr = return_array(category_arr)
    final_user_arr.append(return_arr)
    if len(arr) > 5:            
            business_id = arr[4].split(',')[1]
    else:
        business_id = arr[2].split(',')[2]
    training_data_ids.append(business_id)
file.close()

'''Train the classifier with the user review data obtained in the array previously'''
training_data_ids = set(training_data_ids)
X = np.array(final_user_arr)
nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X) 
'''use K Nearest Neighbors classifier from library sklearn.neighbors library'''


final_result_dict = {}
business_attributes_dict = {}
file = open(business_data_file,encoding='utf8',mode='r')

'''this is to apply the classifier on business data for the columns 
    Give a score based on the distance of the business from the user
    review data and store in a dictionary'''
for lines in file.readlines():
    arr = lines.split('\t')
    category_arr = eval(arr[len(arr)-1])
    category_arr.append(arr[1])
    category_arr.append(arr[10])
    category_arr.append(arr[9])
    category_arr.append(arr[11])
    business_id = arr[5]
    business_name = arr[2]
    longitude = arr[9]
    latitude = arr[11]
    business_attributes_dict[business_id] = [business_name,longitude,latitude]
    '''This is to avoid the restaurants user has already visited'''
    if business_id in training_data_ids:
        continue
        #pass
    category_arr = [w.replace('u\'', '').replace('\'','').replace(' ','').replace('\n','').lower() for w in category_arr]
    if 'restaurants' not in category_arr:
        continue
    return_arr = return_array(category_arr)
    numpy_array = np.array([return_arr])
    distances, indices = nbrs.kneighbors(numpy_array)    
    final_result_dict[business_id] = sum(distances[0])
file.close()
final_result_arr = sorted(final_result_dict.items(), key = lambda x: x[1])
print(final_result_arr)

'''Write the top 10 restaurants obtained to a file to be displayed on web page'''
file = open(out_file,encoding='utf8',mode='w')
for i in range(20):
    print(business_attributes_dict[final_result_arr[i][0]],' ',final_result_arr[i][1])
    result_str = ''
    for j in range(len(business_attributes_dict[final_result_arr[i][0]])):
        if j == len(business_attributes_dict[final_result_arr[i][0]])-1:
            result_str += business_attributes_dict[final_result_arr[i][0]][j] + '\n'
        else:
            result_str += business_attributes_dict[final_result_arr[i][0]][j] + ','
    file.write(result_str)
file.close()