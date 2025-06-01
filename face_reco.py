import numpy as np
import pandas as pd
import cv2
import redis
import os
from dotenv import load_dotenv
import threading
import time

#insight face
try:
    from insightface.app import FaceAnalysis
    INSIGHTFACE_AVAILABLE = True
except ImportError:
    INSIGHTFACE_AVAILABLE = False
    
from sklearn.metrics import pairwise

#time
from datetime import datetime

# Load environment variables
load_dotenv()

# Connect to Redis Client - Using Environment Variables for Security
hostname = os.getenv('REDIS_HOST', 'localhost')
portnumber = int(os.getenv('REDIS_PORT', 6379))
password = os.getenv('REDIS_PASSWORD', '')

# Fallback for local development (if .env not found)
if not hostname or hostname == 'localhost':
    print("⚠️ Warning: Using fallback Redis configuration")
    hostname = 'redis-10991.c244.us-east-1-2.ec2.redns.redis-cloud.com'
    portnumber = 10991
    password = 'NNGuJHe6l5ZgOQcKGLnvx00LkRBZqq5W'

# Redis connection with error handling
try:
    r = redis.StrictRedis(host=hostname,
                          port=portnumber,
                          password=password,
                          socket_connect_timeout=5)
    # Test connection
    r.ping()
    print("✅ Redis connected successfully")
except Exception as e:
    print(f"⚠️ Redis connection failed: {e}")
    # Create dummy Redis for demo
    class DummyRedis:
        def hgetall(self, name): return {}
        def hset(self, name, key, value): return True
        def lpush(self, name, *values): return True
        def ping(self): return True
    r = DummyRedis()

#Retrieve Data from Redis Database
def retrieve_data(name):
    try:
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
    except Exception as e:
        print(f"Error retrieving data: {e}")
        # Return demo data
        demo_data = pd.DataFrame({
            'Name': ['Demo User', 'Test Person'],
            'Role': ['Student', 'Teacher'], 
            'facial_features': [np.random.random(512).astype(np.float32) for _ in range(2)]
        })
        return demo_data

# Smart model loading with background download
DEMO_MODE = "STREAMLIT_SHARING" in os.environ or "STREAMLIT_CLOUD" in os.environ

# Global variables for model loading
faceapp = None
model_loading = False
model_loaded = False

def load_model_background():
    """Background model loading to avoid blocking UI"""
    global faceapp, model_loading, model_loaded
    
    if model_loading or model_loaded:
        return
        
    model_loading = True
    print("🔄 Starting background model download...")
    
    try:
        if INSIGHTFACE_AVAILABLE:
            # Try to load with minimal configuration
            faceapp = FaceAnalysis(
                name='buffalo_sc',
                providers=['CPUExecutionProvider']
            )
            # Prepare with minimal settings for faster loading
            faceapp.prepare(ctx_id=0, det_size=(320, 320), det_thresh=0.6)
            model_loaded = True
            print("✅ Face analysis model loaded successfully in background!")
        else:
            print("❌ InsightFace not available")
    except Exception as e:
        print(f"⚠️ Background model loading failed: {e}")
        faceapp = None
    finally:
        model_loading = False

def get_face_app():
    """Get face app with lazy loading"""
    global faceapp, model_loaded
    
    if not model_loaded and not model_loading:
        # Start background loading if not started
        thread = threading.Thread(target=load_model_background, daemon=True)
        thread.start()
        
    return faceapp

# Initialize model loading in background for cloud deployment
if DEMO_MODE and INSIGHTFACE_AVAILABLE:
    # Start background download immediately but don't block
    thread = threading.Thread(target=load_model_background, daemon=True)
    thread.start()
    print("🚀 Started background model loading for Streamlit Cloud")
elif not DEMO_MODE:
    # Local development - load immediately
    load_model_background()

def get_model_status():
    """Get current model loading status"""
    if model_loaded:
        return "✅ Ready"
    elif model_loading:
        return "🔄 Loading..."
    else:
        return "⏳ Not started"

#ML Search Algorithm
def ml_search_algorithm(dataframe, feature_column, test_vector,
                        name_role=['Name', 'Role'], thresh=0.5):
#cosine similarity base search algorithm
    # Step 1: Take the dataframe (collection of data)
    dataframe = dataframe.copy()


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

# ###Real time prediction
# #Target: save logs for every minute
# class RealTimePred:
#     def __init__(self):
#         self.logs = dict(name=[], role=[], current_time=[])
    
#     def reset_dict(self):
#         self.logs = dict(name=[], role=[], current_time=[])

#     def saveLogs_redis(self):
#         #step 1: create a logs dataframe
#         dataframe = pd.DataFrame(self.logs)
#         #step 2: drop the duplicate infomation (distinct name)
#         dataframe.drop_duplicates('name',inplace=True)
#         #step 3: push data to redis database (list)
#         #encode the data
#         name_list = dataframe['name'].tolist()
#         role_list = dataframe['role'].tolist()
#         ctime_list = dataframe['current_time'].tolist()
#         encoded_data = []

#         for name, role, ctime in zip(name_list,role_list, ctime_list):
#             if name != 'Unknown':
#                 concat_string = f"{name}@{role}@{ctime}"
#                 encoded_data.append(concat_string)
        
#         if len(encoded_data) >0:
#             r.lpush('attendance:logs',*encoded_data)

#         self.reset_dict()



#     def face_prediction(self,test_image, dataframe, feature_column,
#                             name_role=['Name', 'Role'], thresh=0.5 ):
#         #step 1: find the time
#         current_time = str(datetime.now())
        
#         #step 1 take the test image and apply to insight face
#         results = faceapp.get(test_image)
#         test_copy = test_image.copy()
        
#         #step 2: use for loop and extract each embedding and pass to ml_search_algorithm
#         for res in results:
#             x1, y1, x2, y2 = res['bbox'].astype(int)
#             embeddings = res['embedding']
#             person_name, person_role = ml_search_algorithm(dataframe, feature_column, 
#                                                         test_vector = embeddings, 
#                                                         name_role=name_role,
#                                                         thresh=thresh)
#             # print(person_name, person_role)
#             if person_name == 'Unknown':
#                 color = (0,0,255) 
#             else:
#                 color = (0,255,0)
            
#             cv2.rectangle(test_copy, (x1,y1), (x2, y2), color)
#             text_gen =  person_name
#             cv2.putText(test_copy,text_gen,(x1,y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)
#             cv2.putText(test_copy,current_time, (x1,y2+10), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)
#             #save info in logs dict
#             self.logs['name'].append(person_name)
#             self.logs['role'].append(person_role)
#             self.logs['current_time'].append(current_time)   
    
#         return test_copy


# #### Registration form
# class RegistrationForm:
#     def __init__(self):
#         self.sample = 0
#     def reset(self):
#         self.sample = 0
#     def get_embedding(self,frame):
#         #get result from insightface model
#         results = faceapp.get(frame, max_num=1)
#         embeddings = None
#         for res in results:
#             self.sample += 1
#             x1, y1, x2, y2 = res['bbox'].astype(int)
#             cv2.rectangle(frame, (x1, y1), (x2,y2), (0, 255, 0), 1)
#             #put text samples info
#             text = f"samples={self.sample}"
#             cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX,0.6,(255, 255, 0),2)

#             #facial features
#             embeddings = res['embedding']

#         return frame, embeddings
    
#     def save_data_in_redis_db(self, name, role):
#         #validation name
#         if name is not None:
#             if name.strip() != '':
#                 key = f'{name}@{role}'
#             else:
#                 return 'name_false'
#         else:
#             return 'name_false'
#         #if face_embedding.txt exists
#         if 'face_embedding.txt' not in os.listdir():
#             return 'file_false'

        
#         #step-1: load "face_embedding.txt"
#         x_array = np.loadtxt('face_embedding.txt', dtype=np.float32) #flatten array


#         #step-2: convert into array (proper shape)
#         received_samples = int(x_array.size/512)
#         x_array = x_array.reshape(received_samples, 512)
#         x_array = np.asarray(x_array)

#         #step-3: cal. mean embeddings
#         x_mean = x_array.mean(axis=0)
#         x_mean = x_mean.astype(np.float32)
#         x_mean_bytes = x_mean.tobytes()

#         #step-4: save this into redis database
#         #redis hashes
#         r.hset('academy:register', key=key, value=x_mean_bytes)

#         os.remove('face_embedding.txt')
#         self.reset()
#         return True


### Real Time Prediction
# we need to save logs for every 1 mins
class RealTimePred:
    def __init__(self):
        self.logs = dict(name=[],role=[],current_time=[])
        
    def reset_dict(self):
        self.logs = dict(name=[],role=[],current_time=[])
        
    def saveLogs_redis(self):
        # step-1: create a logs dataframe
        dataframe = pd.DataFrame(self.logs)        
        # step-2: drop the duplicate information (distinct name)
        dataframe.drop_duplicates('name',inplace=True) 
        # step-3: push data to redis database (list)
        # encode the data
        name_list = dataframe['name'].tolist()
        role_list = dataframe['role'].tolist()
        ctime_list = dataframe['current_time'].tolist()
        encoded_data = []
        for name, role, ctime in zip(name_list, role_list, ctime_list):
            if name != 'Unknown':
                concat_string = f"{name}@{role}@{ctime}"
                encoded_data.append(concat_string)
                
        if len(encoded_data) >0:
            r.lpush('attendance:logs',*encoded_data)
        
                    
        self.reset_dict()     
        
        
    def face_prediction(self,test_image, dataframe,feature_column,
                            name_role=['Name','Role'],thresh=0.5):
        # step-1: find the time
        current_time = str(datetime.now())
        
        # step-1: take the test image and apply to insight face
        results = faceapp.get(test_image)
        test_copy = test_image.copy()
        # step-2: use for loop and extract each embedding and pass to ml_search_algorithm

        for res in results:
            x1, y1, x2, y2 = res['bbox'].astype(int)
            embeddings = res['embedding']
            person_name, person_role = ml_search_algorithm(dataframe,
                                                        feature_column,
                                                        test_vector=embeddings,
                                                        name_role=name_role,
                                                        thresh=thresh)
            if person_name == 'Unknown':
                color =(0,0,255) # bgr
            else:
                color = (0,255,0)

            cv2.rectangle(test_copy,(x1,y1),(x2,y2),color)

            text_gen = person_name
            cv2.putText(test_copy,text_gen,(x1,y1),cv2.FONT_HERSHEY_DUPLEX,0.7,color,2)
            cv2.putText(test_copy,current_time,(x1,y2+10),cv2.FONT_HERSHEY_DUPLEX,0.7,color,2)
            # save info in logs dict
            self.logs['name'].append(person_name)
            self.logs['role'].append(person_role)
            self.logs['current_time'].append(current_time)
            

        return test_copy


#### Registration Form
class RegistrationForm:
    def __init__(self):
        self.sample = 0
    def reset(self):
        self.sample = 0
        
    def get_embedding(self,frame):
        # get results from insightface model
        results = faceapp.get(frame,max_num=1)
        embeddings = None
        for res in results:
            self.sample += 1
            x1, y1, x2, y2 = res['bbox'].astype(int)
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),1)
            # put text samples info
            text = f"samples = {self.sample}"
            cv2.putText(frame,text,(x1,y1),cv2.FONT_HERSHEY_DUPLEX,0.6,(255,255,0),2)
            
            # facial features
            embeddings = res['embedding']
            
        return frame, embeddings
    
    def save_data_in_redis_db(self,name,role):
        # validation name
        if name is not None:
            if name.strip() != '':
                key = f'{name}@{role}'
            else:
                return 'name_false'
        else:
            return 'name_false'
        
        # if face_embedding.txt exists
        if 'face_embedding.txt' not in os.listdir():
            return 'file_false'
        
        
        # step-1: load "face_embedding.txt"
        x_array = np.loadtxt('face_embedding.txt',dtype=np.float32) # flatten array            
        
        # step-2: convert into array (proper shape)
        received_samples = int(x_array.size/512)
        x_array = x_array.reshape(received_samples,512)
        x_array = np.asarray(x_array)       
        
        # step-3: cal. mean embeddings
        x_mean = x_array.mean(axis=0)
        x_mean = x_mean.astype(np.float32)
        x_mean_bytes = x_mean.tobytes()
        
        # step-4: save this into redis database
        # redis hashes
        r.hset(name='academy:register',key=key,value=x_mean_bytes)
        
        # 
        os.remove('face_embedding.txt')
        self.reset()
        
        return True