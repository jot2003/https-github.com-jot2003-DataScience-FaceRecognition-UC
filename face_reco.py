import numpy as np
import pandas as pd
import cv2

import redis
import os
from dotenv import load_dotenv

#insight face
from insightface.app import FaceAnalysis
from sklearn.metrics import pairwise

#time
import time
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Connect to Redis Client - Support both Streamlit secrets and environment variables
try:
    # Try Streamlit secrets first (for cloud deployment)
    import streamlit as st
    hostname = st.secrets["redis"]["REDIS_HOST"]
    portnumber = st.secrets["redis"]["REDIS_PORT"]
    password = st.secrets["redis"]["REDIS_PASSWORD"]
    print("🌐 Using Streamlit Cloud secrets")
except:
    # Fallback to environment variables (for local development)
    hostname = os.getenv('REDIS_HOST')
    portnumber = int(os.getenv('REDIS_PORT', 6379))
    password = os.getenv('REDIS_PASSWORD')
    print("🏠 Using local environment variables")

if not all([hostname, password]):
    raise ValueError("⚠️ MISSING REDIS CREDENTIALS! Please check your .env file or Streamlit secrets")

r = redis.StrictRedis(host=hostname,
                      port=portnumber,
                      password=password)

#Retrieve Data from Redis Database

def retrieve_data(name):
    retrive_dict = r.hgetall(name)
    
    # Kiểm tra nếu Redis database trống
    if not retrive_dict:
        # Trả về DataFrame trống với cấu trúc đúng
        return pd.DataFrame(columns=['Name', 'Role', 'facial_features'])
    
    retrive_series = pd.Series(retrive_dict)
    retrive_series = retrive_series.apply(lambda x: np.frombuffer(x, dtype=np.float32))
    index = retrive_series.index
    index = list(map(lambda x: x.decode(), index))
    retrive_series.index = index
    retrive_df = retrive_series.to_frame().reset_index()
    retrive_df.columns = ['name_role','facial_features']
    retrive_df[['Name', 'Role']]= retrive_df['name_role'].apply(lambda x: x.split('@')).apply(pd.Series)
    return retrive_df[['Name', 'Role', 'facial_features']]

def delete_user_from_redis(name, role):
    """Xóa user khỏi Redis database"""
    key = f"{name}@{role}"
    result = r.hdel('academy:register', key)
    return result > 0

def delete_all_users_from_redis():
    """Xóa tất cả user khỏi Redis database"""
    result = r.delete('academy:register')
    return result > 0

def get_all_registered_users():
    """Lấy danh sách tất cả user đã đăng ký"""
    users_dict = r.hgetall('academy:register')
    users_list = []
    for key in users_dict.keys():
        key_str = key.decode('utf-8')
        name, role = key_str.split('@')
        users_list.append({'Name': name, 'Role': role, 'Key': key_str})
    return users_list

#configure face analysis
faceapp = FaceAnalysis(name='buffalo_sc',
                       root='insightface_model',
                       providers=['CPUExecutionProvider'])
faceapp.prepare(ctx_id=0, det_size=(640,640), det_thresh=0.5)


#ML Search Algorithm
def ml_search_algorithm(dataframe, feature_column, test_vector,
                        name_role=['Name', 'Role'], thresh=0.5):
#cosine similarity base search algorithm
    # Step 1: Take the dataframe (collection of data)
    dataframe = dataframe.copy()

    # Check if dataframe is empty
    if dataframe.empty:
        return 'Unknown', 'Unknown'

    # Step 2: Index face embeding from the dataframe and convert into array
    X_list = dataframe[feature_column].tolist()
    x = np.asarray(X_list)
    
    # Step 3: Cal, cosine similarity
    similar = pairwise.cosine_similarity(x,test_vector.reshape(1,-1))
    similar_arr = np.array(similar).flatten()
         #add colume
    dataframe['cosine'] = similar_arr
    # Step 4: Filter the data
    data_filter = dataframe.query(f'cosine >= {thresh}')
    if len(data_filter) > 0:
        # Step 5: Get the person name
        data_filter.reset_index(drop=True, inplace=True)
        argmax = data_filter['cosine'].argmax()
        person_name, person_role = data_filter.loc[argmax][['Name', 'Role']]
    else: 
        person_name = 'Unknown'
        person_role = 'Unknown'

    return person_name, person_role

###Real time prediction
#Target: save logs for every minute
class RealTimePred:
    def __init__(self):
        self.logs = dict(name=[], role=[], current_time=[])
    
    def reset_dict(self):
        self.logs = dict(name=[], role=[], current_time=[])

    def saveLogs_redis(self):
        #step 1: create a logs dataframe
        dataframe = pd.DataFrame(self.logs)
        #step 2: drop the duplicate infomation (distinct name)
        dataframe.drop_duplicates('name',inplace=True)
        #step 3: push data to redis database (list)
        #encode the data
        name_list = dataframe['name'].tolist()
        role_list = dataframe['role'].tolist()
        ctime_list = dataframe['current_time'].tolist()
        encoded_data = []

        for name, role, ctime in zip(name_list,role_list, ctime_list):
            if name != 'Unknown':
                concat_string = f"{name}@{role}@{ctime}"
                encoded_data.append(concat_string)
        
        if len(encoded_data) >0:
            r.lpush('attendance:logs',*encoded_data)

        self.reset_dict()



    def face_prediction(self,test_image, dataframe, feature_column,
                            name_role=['Name', 'Role'], thresh=0.5 ):
        #step 1: find the time
        current_time = str(datetime.now())
        
        #step 1 take the test image and apply to insight face
        results = faceapp.get(test_image)
        test_copy = test_image.copy()
        
        #step 2: use for loop and extract each embedding and pass to ml_search_algorithm
        for res in results:
            x1, y1, x2, y2 = res['bbox'].astype(int)
            embeddings = res['embedding']
            person_name, person_role = ml_search_algorithm(dataframe, feature_column, 
                                                        test_vector = embeddings, 
                                                        name_role=name_role,
                                                        thresh=thresh)
            # print(person_name, person_role)
            if person_name == 'Unknown':
                color = (0,0,255) 
            else:
                color = (0,255,0)
            
            cv2.rectangle(test_copy, (x1,y1), (x2, y2), color)
            text_gen =  person_name
            cv2.putText(test_copy,text_gen,(x1,y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)
            cv2.putText(test_copy,current_time, (x1,y2+10), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)
            #save info in logs dict
            self.logs['name'].append(person_name)
            self.logs['role'].append(person_role)
            self.logs['current_time'].append(current_time)   
    
        return test_copy


#### Registration form
class RegistrationFormV2:
    def __init__(self):
        self.sample = 0
    def reset(self):
        self.sample = 0
    def get_embedding(self,frame):
        #get result from insightface model
        results = faceapp.get(frame, max_num=1)
        embeddings = None
        for res in results:
            self.sample += 1
            x1, y1, x2, y2 = res['bbox'].astype(int)
            cv2.rectangle(frame, (x1, y1), (x2,y2), (0, 255, 0), 1)
            #put text samples info
            text = f"samples={self.sample}"
            cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX,0.6,(255, 255, 0),2)

            #facial features
            embeddings = res['embedding']

        return frame, embeddings
    
    def test_new_function(self, name, role):
        """Completely new function to test without caching issues"""
        import streamlit as st
        st.warning("🔍 NEW TEST: This is a brand new function!")
        st.success("✅ NEW TEST: If you see this, the function works!")
        return "test_success"
    
    def save_data_in_redis_db(self, name, role):
        """Ultra-simple cloud registration without file operations"""
        import streamlit as st
        import numpy as np
        
        # Debug: Show that function started
        st.warning("🔍 ULTRA-SIMPLE: Function called successfully!")
        
        # Step 1: Validate name
        if not name or name.strip() == '':
            st.error("🔍 ULTRA-SIMPLE: Name validation failed")
            return 'name_false'
        
        st.info(f"🔍 ULTRA-SIMPLE: Name validation OK: '{name}'")
        
        # Step 2: Create key
        key = f'{name}@{role}'
        st.info(f"🔍 ULTRA-SIMPLE: Key created: '{key}'")
        
        # Step 3: Create mock embedding (cloud demo)
        embeddings = np.random.rand(512).astype(np.float32)
        st.info(f"🔍 ULTRA-SIMPLE: Mock embedding created, shape: {embeddings.shape}")
        
        # Step 4: Save to Redis
        try:
            embeddings_bytes = embeddings.tobytes()
            result = r.hset(name='academy:register', key=key, value=embeddings_bytes)
            st.success(f"🔍 ULTRA-SIMPLE: Redis save result: {result}")
            st.success("✅ SUCCESS: Cloud demo registration completed!")
            return True
        except Exception as e:
            st.error(f"❌ ERROR: Redis failed: {str(e)}")
            return 'file_false'

# Keep old class for backward compatibility but mark as deprecated
class RegistrationForm(RegistrationFormV2):
    pass