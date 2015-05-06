'''
Created on May 2015

@author: Shreekanth
File to validate the K nearest neighbors

References
http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.random.choice.html
'''
from sklearn.neighbors import NearestNeighbors
import numpy as np


feature_name_dict = {}
final_arr = []
feature_names_arr = []
count = 0
'''This is to run the validation on random review datas'''
file_line_num_arr = sorted(np.random.choice(range(0,589),400,replace = False)) 
print(file_line_num_arr) 

''' Function to return a array with all features with 0 if feature is not in user review or business and
    1 if feature is in user review or business. Also append the Lat Long etc to the Array returned'''

def return_array(arr):
    arr = [w.replace('u\'', '').replace('\'','').replace(' ','').replace('\n','').lower() for w in arr]
    temp_arr = [0 for i in range(feature_names_arr[0][1]+5)]
    for i in range(0,len(arr)-2):
        if arr[i] in feature_name_dict.keys():
            temp_arr[feature_name_dict[arr[i]]] = 1
    temp_arr[feature_names_arr[0][1]+1] = len(arr[len(arr)-4])
    temp_arr[feature_names_arr[0][1]+2] = float(arr[len(arr)-3])
    temp_arr[feature_names_arr[0][1]+3] = float(arr[len(arr)-2])
    temp_arr[feature_names_arr[0][1]+4] = float(arr[len(arr)-1])
    return temp_arr
'''Few variables to handle the file operations'''
file_path = 'C:\\Shree\\Study\\Data Mining\\Course_Project\\CSV_Files'
user_file = file_path+'\\user_reviews_att.csv'
business_file = file_path+'\\yelp_academic_dataset_business_clean.json'
file = open(business_file,encoding='utf8',mode='r')

'''read all the categories a restaurant can belong to and 
   add it to a dictionary with array a category array'''
for lines in file.readlines():  
    arr = lines.split('\t')
    cat_arr = eval(arr[len(arr)-1])
    cat_arr = [w.replace('u\'', '').replace('\'','').replace(' ','').replace('\n','').lower() for w in cat_arr]
    if 'restaurants' in cat_arr:
        for l in cat_arr:
            try:
                feature_name_dict[l]
            except KeyError:
                feature_name_dict[l] = count
                count += 1
file.close()
print (feature_name_dict)
feature_names_arr = sorted(feature_name_dict.items(), key = lambda x: x[1], reverse = True)
print(feature_names_arr)

'''Prepare a array with user review data got after querying the database
   This would be used to train the classifier'''

file = open(user_file,'r')
head = file.readline()
final_user_arr = []
training_data_ids = []
test_count = 1
file_num_count = 1
for lines in file:
    if file_num_count in file_line_num_arr:
        arr = lines.split('"')
        cat_arr = eval(arr[1])
        cat_arr.append(arr[len(arr)-1].split(',')[1])
        cat_arr.append(arr[len(arr)-1].split(',')[2])
        cat_arr.append(arr[len(arr)-1].split(',')[3])
        cat_arr.append(arr[len(arr)-1].split(',')[4])
        
        test = return_array(cat_arr)
        final_user_arr.append(test)
        if len(arr) > 5:            
            business_id = arr[4].split(',')[1]
        else:
            business_id = arr[2].split(',')[2]
        training_data_ids.append(business_id)
    file_num_count += 1
file.close()

'''Train the classifier with the user review data obtained in the array previously'''
training_data_ids = set(training_data_ids)
X = np.array(final_user_arr)
nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(X)
'''use K Nearest Neighbors classifier from library sklearn.neighbors library'''

final_dict = {}
business_name_dict = {}
file = open(business_file,encoding='utf8',mode='r')

'''this is to apply the classifier on business data for the columns 
    Give a score based on the distance of the business from the user
    review data and store in a dictionary'''

for lines in file.readlines():
    arr = lines.split('\t')
    cat_arr = eval(arr[len(arr)-1])
    cat_arr.append(arr[1])
    cat_arr.append(arr[10])
    cat_arr.append(arr[9])
    cat_arr.append(arr[11])
    business_id = arr[5]

    business_name_dict[business_id] = arr[2]
    if business_id in training_data_ids:
        continue
        #pass
    cat_arr = [w.replace('u\'', '').replace('\'','').replace(' ','').replace('\n','').lower() for w in cat_arr]
    '''This is to avoid the restaurants user has already visited'''
    if 'restaurants' not in cat_arr:
        continue
    test1_arr = return_array(cat_arr)
    numpy_array = np.array([test1_arr])
    distances, indices = nbrs.kneighbors(numpy_array)
    
    final_dict[business_id] = sum(distances[0])
final_result = sorted(final_dict.items(), key = lambda x: x[1])[:40]
print(final_result)
predicted_business_id = [X[0] for X in final_result]

for x in final_result:
    print(business_name_dict[x[0]],' ',x[1])
'''See the user review file and check how many values 
   obtained of the top 40 belong to actual user reviewed place'''    
file = open(user_file,'r')
file_num_count = 0
test_count = 0
for lines in file:
    if file_num_count not in file_line_num_arr:
        arr = lines.split('"')
        if len(arr) > 5:            
            business_id = arr[4].split(',')[1]
        else:
            business_id = arr[2].split(',')[2]
        if business_id in predicted_business_id:
            test_count += 1
    file_num_count += 1
print(test_count)
    